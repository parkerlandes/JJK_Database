from database import SessionLocal
import models

session = SessionLocal()

# ---------------------------
# CREATE
# ---------------------------
new_character = models.Character(
    name="Toge Inumaki",
    grade="Semi Grade 1",
    description="Cursed Speech user",
    is_curse=False
)
session.add(new_character)
session.commit()
print("CREATED:", new_character.character_id)

# ---------------------------
# READ
# ---------------------------
char = session.query(models.Character).filter_by(name="Toge Inumaki").first()
print("READ:", char.name, char.grade)

# ---------------------------
# UPDATE
# ---------------------------
char.grade = "Grade 1"
session.commit()
print("UPDATED:", char.name, "->", char.grade)

# ---------------------------
# DELETE
# ---------------------------
session.delete(char)
session.commit()
print("DELETED: Toge Inumaki")

session.close()
