"""
Centralized configuration management using Pydantic Settings.
All environment variables are loaded and validated here.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenRouter Configuration
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    default_model: str = "anthropic/claude-3.5-sonnet"

    # Supabase Configuration
    supabase_url: str
    supabase_key: str

    # SerpAPI Configuration
    serpapi_api_key: str

    # Firecrawl Configuration
    firecrawl_api_key: str

    # Microsoft SSO Configuration
    microsoft_client_id: str
    microsoft_client_secret: str
    microsoft_tenant_id: str = "common"
    microsoft_redirect_uri: str = "http://localhost:8501"
    microsoft_authority: Optional[str] = None
    microsoft_scopes: list[str] = ["User.Read", "Calendars.Read"]

    # Application Configuration
    app_env: str = "development"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Construct Microsoft authority URL if not provided
        if not self.microsoft_authority:
            self.microsoft_authority = f"https://login.microsoftonline.com/{self.microsoft_tenant_id}"


# Singleton instance
settings = Settings()
