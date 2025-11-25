from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from sqlalchemy.orm import Session
from database import SessionLocal
import models

def answer_query(user_query: str):
    session = SessionLocal()

    char_names = [c.name for c in session.query(models.Character).all()]
    clan_names = [c.name for c in session.query(models.Clan).all()]
    tech_names = [t.name for t in session.query(models.CursedTechnique).all()]
    fight_names = [f.name for f in session.query(models.Fight).all()]

    context = f"""
Characters: {char_names}
Clans: {clan_names}
Techniques: {tech_names}
Fights: {fight_names}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You answer questions about the Jujutsu Kaisen database."},
            {"role": "system", "content": context},
            {"role": "user", "content": user_query}
        ]
    )

    answer = response.choices[0].message.content
    return answer
