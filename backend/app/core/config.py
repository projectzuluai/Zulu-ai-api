from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Zulu AI API"
    ai_mode: str = "mock"
    gemini_api_key: Optional[str] = None

    class Config:
        env_file = ".env"


# Create settings instance
_settings = Settings()

# Override ai_mode to live if gemini_api_key is present (temporary fix)
if _settings.gemini_api_key and _settings.ai_mode == "mock":
    _settings.ai_mode = "live"
    print("🚀 AI_MODE automatically set to 'live' because Gemini API key is configured")

settings = _settings