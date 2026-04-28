# JJK Database

A full-stack Python application for browsing and querying a relational database modeled on the *Jujutsu Kaisen* universe — characters, clans, cursed techniques, domains, arcs, episodes, locations, and fights. The app exposes traditional CRUD pages through a Streamlit GUI and adds a natural-language query interface that uses Google Gemini to translate plain-English questions into SQL.

> *"List every character who fought in Shibuya Station."*
> *"Which Special Grade sorcerers belong to the Gojo Clan?"*

The LLM converts the question to SQL, the app post-processes it, executes it against MySQL, and Gemini summarizes the result back into a readable answer.

---

## Features

- **Relational schema with 12 tables** — series, arcs, episodes, characters, clans, cursed techniques, domains, inherited techniques, locations, fights, and association tables for character–technique and fight–participant many-to-many relationships
- **SQLAlchemy ORM layer** with foreign keys, cascade rules, unique constraints, and a `CheckConstraint` validating character grade values
- **Streamlit GUI** with one page per entity (Characters, Arcs, Episodes, Fights, Domains, Techniques, Clans, Locations) — each supporting browse, filter, and add operations
- **Natural-language query page** — ask a question in plain English, get a generated SQL statement, executed result, and a Gemini-written summary
- **LLM output guardrails** — generated SQL is validated to be a `SELECT` only, identifiers are auto-quoted, keywords are normalized, and equality comparisons on string columns are rewritten to `LIKE '%...%'` for friendlier matching
- **Seed data script** that populates the database with a starter set of arcs, episodes, characters, and fights

---

## Tech stack

| Layer       | Tool                              |
|-------------|-----------------------------------|
| Language    | Python 3.8+                       |
| ORM         | SQLAlchemy                        |
| Database    | MySQL (via `pymysql`)             |
| GUI         | Streamlit                         |
| LLM         | Google Gemini (`google-generativeai`) |
| Config      | `python-dotenv`                   |

---

## Project layout

```
JJK_Database/
├── database.py          # SQLAlchemy engine + session factory, reads .env
├── models.py            # All ORM models and table relationships
├── create_db.py         # Creates all tables from the model definitions
├── seed_data.py         # Populates the database with sample data
├── crud_demo.py         # Tiny script demonstrating create / read / update / delete
├── llm_query.py         # Gemini integration: NL → SQL → result → summary
├── gui.py               # Streamlit application
└── jujutsu_kaisen.drawio  # ER diagram source
```

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/parkerlandes/JJK_Database.git
cd JJK_Database
python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install sqlalchemy pymysql streamlit python-dotenv google-generativeai
```

### 2. Set up MySQL

Create an empty database (any name, e.g. `jjk_db`) on a local or remote MySQL server.

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DB_USER=your_mysql_user
DB_PASS=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=jjk_db
GEMINI_API_KEY=your_google_gemini_api_key
```

### 4. Build and seed the database

```bash
python3 create_db.py        # creates all tables
python3 seed_data.py        # populates with starter data
```

### 5. Run the app

```bash
streamlit run gui.py
```

Streamlit will open the app in your browser (default `http://localhost:8501`).

---

## How the natural-language query works

The "AI Query" page in the GUI is wired to `llm_query.answer_query()`. The flow:

1. **Schema injection.** The full table/column schema is included in the prompt to Gemini, along with rules constraining the output (must be a `SELECT`, no markdown, prefer `LIKE` over `=` for string matches).
2. **Generation.** Gemini returns a SQL string, which is stripped of markdown fences and validated to start with `SELECT`. Any other prefix is rejected before execution.
3. **Post-processing.**
   - `clean_sql()` uppercases keywords, repairs missing whitespace around `FROM` / `WHERE`, and rewrites `= 'value'` into `LIKE '%value%'`.
   - `wrap_identifiers()` introspects the live database schema and adds backtick quoting around table and `table.column` references — necessary because some table names (e.g. `character`) collide with reserved-ish words.
4. **Execution.** The cleaned SQL runs through SQLAlchemy with a fresh session.
5. **Summarization.** Raw rows are sent back to Gemini with the original question, and the model returns a short human-readable answer.

This pipeline is deliberately conservative: the model is never trusted to issue arbitrary SQL, only to draft a SELECT that the application then sanitizes and runs.

---

## Schema overview

```
series ──< arc ──< episode
                    │
                    └── (start/end episodes referenced by arc and fight)

clan ──< character ──< character_technique >── cursed_technique
            │
            ├── domain (1:1)
            ├── inherited_technique (1:N)
            └── fight_participant >── fight ──> location
                                       │
                                       └── arc
```

Highlights:
- `character_technique` is a join table with an `is_innate` flag distinguishing inborn from learned techniques
- `fight_participant` records each character's outcome in a fight (e.g. *won*, *lost*, *escaped*)
- Episode references in `arc` and `fight` use distinct `start_episode_id` / `end_episode_id` foreign keys
- Character grade is constrained to a fixed set of valid values via `CheckConstraint`

The full ER diagram source is in `jujutsu_kaisen.drawio`.

---

## Sample queries to try

- *Who are the Special Grade sorcerers?*
- *List every fight that happened in Shibuya.*
- *Which characters are from the Zenin Clan?*
- *Show me all techniques owned by Satoru Gojo.*
- *Which arcs include Sukuna as a fight participant?*

---

## Limitations and known issues

- The SELECT-only check is a syntactic safeguard; for stronger isolation the database connection should use a read-only MySQL user with no DDL or DML privileges.
- The regex-based identifier wrapper assumes column names are unique substrings; ambiguous names could be mishandled.
- The Streamlit GUI opens a single SQLAlchemy session at module scope. This is fine for local single-user use but should be refactored to per-request sessions for any multi-user deployment.
- No automated tests — the `crud_demo.py` script is a manual smoke test only.

---

## Course context

Built for CMSC 4513 / database coursework at Oklahoma Christian University. The project exercises relational schema design, ORM modeling, GUI development, and LLM integration end-to-end.
