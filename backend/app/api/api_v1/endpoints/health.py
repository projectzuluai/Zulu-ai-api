from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/status", response_model=dict)
def status():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "ai_mode": settings.ai_mode,
        "gemini_configured": settings.gemini_configured,
        "live_mode": settings.is_live_mode,
    }