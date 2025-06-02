from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

import os

load_dotenv()


# ✅ Load from .env or config
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Create engine (talks to the DB)
engine = create_engine(DATABASE_URL)

# ✅ Create session factory (used for making db sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for your models to inherit
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






