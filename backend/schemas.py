from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    patient_id: str
    name: str
    taste_preferences: str
    texture_likes: str
    dietary_restriction: str
    symptoms: str
    sensory_sweet: int
    sensory_salty: int
    sensory_bitter: int
    sensory_umami: int
    sensory_sour: int
    known_deficits: str

class QueryRequest(BaseModel):
    patient_id: str
    name: str
    query: str

class FeedbackCreate(BaseModel):
    patient_id: str
    recipe_name: str
    feedback_text: str