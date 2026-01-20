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
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "kcl-student-bot-api"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("KCL Student Bot API starting up...")
    logger.info("API documentation available at /docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("KCL Student Bot API shutting down...")


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
