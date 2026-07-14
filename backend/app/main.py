import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from the backend directory's .env file
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from app.routes import extract, sync

app = FastAPI(
    title="Schedule to Calendar Backend",
    description="FastAPI gateway managing Gemini OCR extraction and Google Calendar synchronization.",
    version="1.0.0"
)

# Configure CORS Middleware
# Allows frontend development server to communicate with backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins in production as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(extract.router)
app.include_router(sync.router)

@app.get("/health", tags=["System"])
async def health_check():
    """Simple operational health check to verify backend server vitality."""
    return {
        "status": "healthy",
        "service": "quickcal_backend",
        "engine": "google-genai"
    }