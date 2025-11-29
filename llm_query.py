import os
from dotenv import load_dotenv
import google.generativeai as genai
from database import SessionLocal
import models
from sqlalchemy import text
import sqlalchemy
import re

load_dotenv()

# Load Gemini key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-pro-latest"


# ============================
# SCHEMA DISCOVERY
# ============================
def get_schema():
    inspector = sqlalchemy.inspect(SessionLocal().bind)
    tables = inspector.get_table_names()

    columns = {}
    for t in tables:
        cols = inspector.get_columns(t)
        columns[t] = [c["name"] for c in cols]

    return tables, columns


# ============================
# SAFE IDENTIFIER WRAPPING
# ============================
def wrap_identifiers(sql):
    tables, columns = get_schema()

    # wrap table names ONLY when they appear after FROM / JOIN
    for t in tables:
        # match: FROM character → FROM `character`
        sql = re.sub(rf'(\bFROM\s+){t}(\b)', rf'\1`{t}`\2', sql, flags=re.IGNORECASE)

        # match: JOIN character → JOIN `character`
        sql = re.sub(rf'(\bJOIN\s+){t}(\b)', rf'\1`{t}`\2', sql, flags=re.IGNORECASE)

        # match: INNER JOIN character
        sql = re.sub(rf'(\bINNER\s+JOIN\s+){t}(\b)', rf'\1`{t}`\2', sql, flags=re.IGNORECASE)

    # Now wrap table.column references
    for t in tables:
        for c in columns[t]:
            sql = re.sub(rf'\b{t}\.{c}\b', f'`{t}`.`{c}`', sql)

    return sql.strip()


# ============================
# SQL CLEANER
# ============================
def clean_sql(sql):
    # uppercase keywords
    keywords = ["select", "from", "where", "join", "inner", "left", "right", "on", "as", "and", "or"]
    for kw in keywords:
        sql = re.sub(rf'\b{kw}\b', kw.upper(), sql)

    # ensure spacing
    sql = re.sub(r'([a-zA-Z0-9_])FROM', r'\1 FROM', sql)
    sql = re.sub(r'([a-zA-Z0-9_])WHERE', r'\1 WHERE', sql)
    sql = re.sub(r'\s+', ' ', sql)
    sql = re.sub(r"=\s*'([^']+)'", r"LIKE '%\1%'", sql)

    return sql.strip()


# ============================
# MAIN QUERY FUNCTION
# ============================
def answer_query(user_query: str) -> str:
    """
    Converts natural language into SQL using Gemini,
    runs it against the database, and returns results.
    """

    schema = """
Tables:
series(series_id, name, description, author, media_type)
arc(arc_id, series_id, arc_name, description, start_episode_id, end_episode_id)
episode(episode_id, arc_id, season_number, episode_number, title, synopsis)
character(character_id, clan_id, name, grade, description, first_appearance_episode_id, technique_id, is_curse)
clan(clan_id, name)
cursed_technique(technique_id, name, description)
character_technique(technique_id, character_id, is_innate)
domain(domain_id, character_id, name, description)
inherited_technique(inherited_technique_id, character_id, name, description)
location(location_id, name, type, city, country)
fight(fight_id, name, arc_id, location_id, start_episode_id, end_episode_id, summary)
fight_participant(fight_id, character_id, outcome)
"""

    prompt = f"""
You are an expert MySQL query generator.

User question:
"{user_query}"

Database schema:
{schema}

RULES:
- Return ONLY a SQL SELECT statement.
- Use MySQL syntax.
- Do NOT include comments.
- Do NOT include markdown.
- DO NOT invent fields that do not exist.
- ALWAYS include spaces between tokens.
- Always compare names using LIKE '%text%' instead of '='
- You MAY use JOINs.
- You MAY check fight locations using `location.location_id`.
- You MAY check fight participants using `fight_participant`.
- You MAY check location names, cities, and countries.
"""

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    print("\nRAW SQL FROM MODEL:\n", sql)

    if not sql.lower().startswith("select"):
        return f"Invalid SQL generated: {sql}"

    # ——————————————
    # SQL post-processing
    # ——————————————
    sql = clean_sql(sql)
    sql = wrap_identifiers(sql)

    print("\nFINAL SQL TO EXECUTE:\n", sql)

    # ——————————————
    # Execute SQL safely
    # ——————————————
    session = SessionLocal()
    try:
        result = session.execute(text(sql)).fetchall()
    except Exception as e:
        return f"SQL Execution Error: {e}"
    finally:
        session.close()

    if not result:
        return "No results found."

    # ================
    # NATURAL LANGUAGE RESPONSE
    # ================
    pretty_prompt = f"""
    You are summarizing database results.

    User question:
    {user_query}

    Raw answer:
    {result}

    Respond with a short, human-readable answer.
    """

    try:
        pretty_model = genai.GenerativeModel(MODEL_NAME)
        pretty_response = pretty_model.generate_content(pretty_prompt)
        return pretty_response.text.strip()
    except Exception:
        # fallback: plain return values
        return "\n".join([str(row) for row in result])