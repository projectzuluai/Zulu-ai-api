from pydantic_settings import BaseSettings
from pydantic import ValidationError
import os


class Settings(BaseSettings):
    app_name: str = "Zulu AI API"
    ai_mode: str = os.getenv("AI_MODE", "mock")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    @property
    def gemini_configured(self):
        return bool(self.gemini_api_key)

    @property
    def is_live_mode(self):
        return self.ai_mode == "live" and self.gemini_configured

    def validate(self):
        if self.ai_mode == "live" and not self.gemini_configured:
            raise ValueError("AI_MODE is 'live' but GEMINI_API_KEY is missing.")

settings = Settings()
try:
    settings.validate()
except Exception as e:
    print(f"[Zulu AI API] Configuration error: {e}")