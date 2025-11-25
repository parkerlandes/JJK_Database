import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def get_session():
    return SessionLocal()

st.title("Jujutsu Kaisen Database GUI")

menu = st.sidebar.selectbox("Select Operation", ["Create Character", "View Characters", "Delete Character"])

session = get_session()

if menu == "Create Character":
    name = st.text_input("Name")
    grade = st.text_input("Grade")
    desc = st.text_area("Description")

    if st.button("Add Character"):
        new_char = models.Character(name=name, grade=grade, description=desc, is_curse=False)
        session.add(new_char)
        session.commit()
        st.success("Character added!")

elif menu == "View Characters":
    chars = session.query(models.Character).all()
    for c in chars:
        st.write(f"{c.character_id} — {c.name} — {c.grade}")

elif menu == "Delete Character":
    chars = session.query(models.Character).all()
    selected = st.selectbox("Select character", [c.name for c in chars])
    if st.button("Delete"):
        obj = session.query(models.Character).filter_by(name=selected).first()
        session.delete(obj)
        session.commit()
        st.success("Character deleted!")

st.subheader("Ask the Database")

query = st.text_input("Ask a question (e.g., Who uses Limitless?)")

if st.button("Ask"):
    from llm_query import answer_query
    res = answer_query(query)
    st.write(res)


