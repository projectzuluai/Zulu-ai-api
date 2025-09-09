from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
import asyncio

from backend.app.core.config import settings
from backend.app.services.codegen import generate_mock_app, generate_live_app

router = APIRouter()


class GenerationRequest(BaseModel):
    idea: str


@router.post("/generate_app")
async def generate_app(request: GenerationRequest) -> Dict:
    """Generate an application based on the provided idea."""
    if not request.idea or not request.idea.strip():
        raise HTTPException(status_code=400, detail="Idea cannot be empty")
    
    try:
        if settings.ai_mode.lower() == "live":
            # Use Gemini AI to generate the app
            generated_files = await generate_live_app(request.idea.strip())
            return {
                "message": "App generated with Gemini AI!",
                "generated_files": generated_files,
                "mode": "live"
            }
        else:
            # Use mock generation
            generated_files = generate_mock_app(request.idea.strip())
            return {
                "message": "Mock app generated successfully!",
                "generated_files": generated_files,
                "mode": "mock"
            }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate app: {str(e)}")


@router.get("/modes")
async def get_modes():
    """Get available AI modes and current mode."""
    return {
        "available_modes": ["mock", "live"],
        "current_mode": settings.ai_mode,
        "gemini_configured": settings.gemini_api_key is not None
    }