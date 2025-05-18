import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.models import Recipe, Base

# ✅ Use same SQLite path as FastAPI
DATABASE_URL = "sqlite:///C:/Users/surya/Desktop/gustabor_project/gustabor.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# Load data
df = pd.read_csv("C:/Users/surya/Downloads/healthy_cancer_recipes.csv")
db = SessionLocal()

for _, row in df.iterrows():
    recipe = Recipe(
        id=int(row["id"]),
        name=row["name"],
        description=row["description"],
        flavor_profile=row["flavor_profile"],
        suitable_for=row["suitable_for"]
    )
    db.merge(recipe)  # Insert or update
    db.commit()

db.close()
print("✅ Recipes loaded into database.")
