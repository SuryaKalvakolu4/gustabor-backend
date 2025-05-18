import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use absolute DB path to avoid SQLite path issues

DATABASE_URL = "sqlite:///C:/Users/surya/Desktop/gustabor_project/gustabor.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

print("🧠 DB ENGINE using:", DATABASE_URL)
