from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)
    name = Column(String)
    taste_preferences = Column(String)
    texture_likes = Column(String)
    dietary_restriction = Column(Text)
    symptoms = Column(String)
    sensory_sweet = Column(Integer)
    sensory_salty = Column(Integer)
    sensory_bitter = Column(Integer)
    sensory_umami = Column(Integer)
    sensory_sour = Column(Integer)
    known_deficits = Column(Text)

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    flavor_profile = Column(String)
    suitable_for = Column(String)  # symptoms the recipe is helpful for

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String)
    recipe_name = Column(String)
    feedback_text = Column(Text)

class ClinicalResult(Base):
    __tablename__ = "clinical_results"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String)
    result_summary = Column(Text)
