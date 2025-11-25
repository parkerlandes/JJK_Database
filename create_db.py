# create_db.py
from database import engine, Base
import models  # noqa: F401  (import to register models)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database schema created.")
