from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.app.core.config import settings
from backend.app.routes.generate import router as generate_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="An AI-powered app generator service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate_router, prefix="/api/v1", tags=["generation"])


@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": "1.0.0",
        "ai_mode": settings.ai_mode
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "ai_mode": settings.ai_mode,
        "gemini_configured": settings.gemini_api_key is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )