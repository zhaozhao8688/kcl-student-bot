"""
Simple FastAPI test without agent dependencies.
This will help us diagnose if the issue is with the agent system or the basic app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="KCL Student Bot API - Simple Test")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "KCL Student Bot API",
        "version": "2.0.0",
        "status": "online",
        "message": "Simple test version - no agent system"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "kcl-student-bot-api",
        "port": os.environ.get("PORT", "not set"),
        "env_vars": {
            "OPENROUTER_API_KEY": "set" if os.environ.get("OPENROUTER_API_KEY") else "missing",
            "SUPABASE_URL": "set" if os.environ.get("SUPABASE_URL") else "missing",
            "SERPAPI_API_KEY": "set" if os.environ.get("SERPAPI_API_KEY") else "missing",
            "FIRECRAWL_API_KEY": "set" if os.environ.get("FIRECRAWL_API_KEY") else "missing",
        }
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    print(f"Starting simple test server on port {port}")

    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
