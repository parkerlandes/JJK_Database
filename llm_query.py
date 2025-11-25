import subprocess
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def ask_local_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3.2", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout

def answer_query(user_query: str):
    session = SessionLocal()

    # Extract character names from DB
    char_names = [c.name for c in session.query(models.Character).all()]
    clan_names = [c.name for c in session.query(models.Clan).all()]
    tech_names = [t.name for t in session.query(models.CursedTechnique).all()]
    fight_names = [f.name for f in session.query(models.Fight).all()]

    knowledge = f"""
You are answering questions about the Jujutsu Kaisen database.

Characters: {char_names}
Clans: {clan_names}
Techniques: {tech_names}
Fights: {fight_names}
"""

    prompt = knowledge + "\nQuestion: " + user_query

    return ask_local_llm(prompt)
