from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import models, schemas, llm_recommender
from backend.database import SessionLocal, engine

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/query")
def handle_query(request: schemas.QueryRequest, db: Session = Depends(get_db)):
    print("🧠 QUERY endpoint using DB:", engine.url)

    try:
        # Normalize user input
        input_id = request.patient_id.strip()
        input_name = request.name.strip().lower()

        # Case-insensitive, whitespace-stripped lookup
        patient = db.query(models.Patient).filter(
            models.Patient.patient_id == input_id,
            models.Patient.name.ilike(input_name)
        ).first()

        if not patient:
            return {"error": "Patient not found"}

        feedbacks = db.query(models.Feedback).filter_by(patient_id=input_id).all()
        clinical = db.query(models.ClinicalResult).filter_by(patient_id=input_id).first()
        recipes = db.query(models.Recipe).all()

        response = llm_recommender.generate_recommendation(
            patient=patient,
            feedbacks=feedbacks,
            clinical_results=clinical,
            recipes=recipes
        )

        return {"recommendation": response}

    except Exception as e:
        print("❌ LLM ERROR:", str(e))
        return {"error": "Internal server error"}
