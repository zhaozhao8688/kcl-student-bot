"""
KCL Student Bot - FastAPI Backend

Main FastAPI application entry point for the KCL Student Bot.
Provides REST API for chat, timetable, and session management.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat, timetable, session
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="KCL Student Bot API",
    description="REST API for the KCL Student Bot - AI assistant for King's College London students",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server (alternative)
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://kcl-bot-frontend.onrender.com",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    chat.router,
    prefix="/api/chat",
    tags=["chat"]
)

app.include_router(
    timetable.router,
    prefix="/api/timetable",
    tags=["timetable"]
)

app.include_router(
    session.router,
    prefix="/api/session",
    tags=["session"]
)


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "name": "KCL Student Bot API",
        "version": "2.0.0",
        "status": "online",
        "message": "Welcome to the KCL Student Bot API"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with API key validation."""
    from config.settings import settings

    health_status = {
        "status": "healthy",
        "service": "kcl-student-bot-api",
        "checks": {
            "api": "ok"
        }
    }

    # Check if OpenRouter API key is configured
    if not settings.openrouter_api_key:
        health_status["status"] = "degraded"
        health_status["checks"]["openrouter_api_key"] = "missing"
        health_status["warning"] = "OpenRouter API key not configured"
    else:
        health_status["checks"]["openrouter_api_key"] = "configured"

    # Check if other required keys are configured
    if not settings.supabase_url or not settings.supabase_key:
        health_status["status"] = "degraded"
        health_status["checks"]["supabase"] = "missing"
        if "warning" in health_status:
            health_status["warning"] += ", Supabase credentials missing"
        else:
            health_status["warning"] = "Supabase credentials not configured"
    else:
        health_status["checks"]["supabase"] = "configured"

    return health_status


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("KCL Student Bot API starting up...")
    logger.info("API documentation available at /docs")

    # Verify OpenRouter API key
    try:
        from services.llm_service import llm_service
        logger.info("Verifying OpenRouter API credentials...")

        # Test with a minimal request
        test_response = llm_service.generate(
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        logger.info("✅ OpenRouter API key verified successfully")
        logger.info(f"Test response received: {len(test_response)} characters")
    except Exception as e:
        logger.error(f"❌ OpenRouter API key verification failed: {str(e)}")
        logger.error("Please check your OPENROUTER_API_KEY in .env file")
        logger.error("The API will start but chat functionality may not work")
        # Don't fail startup - let the app run for other endpoints


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("KCL Student Bot API shutting down...")


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    env = os.environ.get("APP_ENV", "development")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=(env == "development"),  # Only reload in development
        log_level="info"
    )
