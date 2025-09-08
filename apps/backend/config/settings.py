"""Application settings."""

from __future__ import annotations

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
import bool
import int
import list
import str

    # Application
    app_name: str = "ZETA_VN"
    version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./zeta_vn.db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # AI Models
    openai_api_key: str | None = None
    default_model: str = "gpt-3.5-turbo"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = ConfigDict(env_file=".env", case_sensitive=False)


def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()


__all__ = ["Settings", "get_settings"]
