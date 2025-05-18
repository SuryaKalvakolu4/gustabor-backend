from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback/submit")
def submit_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(
        patient_id=feedback.patient_id.strip(),
        recipe_name=feedback.recipe_name.strip(),
        feedback_text=feedback.feedback_text.strip()
    )
    db.add(new_feedback)
    db.commit()
    return {"message": "Feedback submitted successfully."}
