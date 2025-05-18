from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.api import feedback

from . import models, database
from .api import patient, query

# Load environment variables from .env (for OpenAI API key)
load_dotenv()

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Gustabor Recommendation Engine",
    description="API backend for patient form handling and AI-based recipe recommendation.",
    version="1.0.0",
)

# CORS settings for local frontend (adjust origin in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gustabor-recommendation-project.onrender.com"],  # Use ["http://localhost:8080"] for stricter config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(patient.router)
app.include_router(query.router)
app.include_router(feedback.router)
