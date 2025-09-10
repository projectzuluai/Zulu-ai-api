from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from dotenv import load_dotenv
import os
import uuid

from backend.app.core.config import settings
from backend.app.routes.generate import router as generate_router

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zulu-ai-api")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="An AI-powered app generator service",
    version="1.0.0",
    docs_url="/docs",       # Swagger
    redoc_url="/redoc"      # ReDoc
)

# ✅ CORS setup (allow frontend + local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",   # Allow all for now (change to specific domains in prod)
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://zulu-ai-frontend.onrender.com",
        "https://<your-lovable-preview-domain>"  # replace if you know it
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(generate_router, prefix="/api/v1", tags=["generation"])


@app.get("/", tags=["root"])
async def root():
    """Root welcome endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": "1.0.0",
        "ai_mode": settings.ai_mode
    }


@app.get("/health", tags=["system"])
async def health():
    """Health check endpoint for monitoring/deployment."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "ai_mode": settings.ai_mode,
        "gemini_configured": bool(settings.gemini_api_key),
        "live_mode": settings.ai_mode == "live" and bool(settings.gemini_api_key)
    }


@app.get("/status", tags=["system"])
async def status():
    """Detailed status endpoint for diagnostics."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "ai_mode": settings.ai_mode,
        "gemini_configured": bool(settings.gemini_api_key),
        "live_mode": settings.ai_mode == "live" and bool(settings.gemini_api_key),
        "docs_url": app.docs_url,
        "redoc_url": app.redoc_url
    }


@app.on_event("startup")
def validate_env():
    if not settings.gemini_api_key:
        logger.warning("Gemini API key is missing! Backend will run in mock mode.")
    if settings.ai_mode == "live" and not settings.gemini_api_key:
        logger.error("AI_MODE is 'live' but GEMINI_API_KEY is missing. Live mode will not work.")
    else:
        logger.info("Gemini API key loaded. Backend will run in live mode if AI_MODE=live.")


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response


# Request ID middleware for traceability
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Error handling middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(status_code=422, content={"error": "Validation error", "details": exc.errors()})


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal server error", "details": str(exc)})


@app.get("/version", tags=["system"])
async def version():
    return {
        "app_name": settings.app_name,
        "version": "1.0.0"
    }


api_call_count = 0

def increment_api_count():
    global api_call_count
    api_call_count += 1

@app.middleware("http")
async def count_api_calls(request: Request, call_next):
    increment_api_count()
    response = await call_next(request)
    return response

@app.get("/metrics", tags=["system"])
async def metrics():
    return {
        "api_call_count": api_call_count,
        "uptime_seconds": int((os.times().elapsed if hasattr(os.times(), 'elapsed') else 0))
    }

@app.get("/ping", tags=["system"])
async def ping():
    return {"ping": "pong"}

@app.get("/info", tags=["system"])
async def info():
    return {
        "app_name": settings.app_name,
        "ai_mode": settings.ai_mode,
        "gemini_configured": bool(settings.gemini_api_key),
        "env": dict(os.environ),
    }

@app.get("/docs-link", tags=["system"])
async def docs_link():
    return {"docs_url": app.docs_url, "redoc_url": app.redoc_url}

@app.get("/debug", tags=["system"])
async def debug(request: Request):
    if os.getenv("DEBUG", "false").lower() != "true":
        return JSONResponse(status_code=403, content={"error": "Debug mode not enabled"})
    return {
        "request_headers": dict(request.headers),
        "request_id": getattr(request.state, "request_id", None),
        "settings": {"ai_mode": settings.ai_mode, "gemini_api_key": bool(settings.gemini_api_key)},
        "env": dict(os.environ)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),  # Use Render's dynamic port
        reload=True
    )
