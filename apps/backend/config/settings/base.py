"""Base settings configuration.





This module contains the base settings class that all environment-specific


settings inherit from. It includes all common configuration options.


"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import AttributeError
import ValueError
import bool
import classmethod
import cls
import dict
import getattr
import int
import list
import name
import self
import str
import v


class Settings(BaseSettings):
    """Base settings class for ZETA AI Server configuration."""

    # Application info

    app_name: str = Field(default="ZETA AI Server", description="Application name")

    app_version: str = Field(default="1.0.0", description="Application version")

    debug: bool = Field(default=False, description="Debug mode")

    environment: str = Field(default="development", description="Environment name")

    # Server configuration

    host: str = Field(default="0.0.0.0", description="Server host")

    port: int = Field(default=8000, description="Server port")

    reload: bool = Field(default=True, description="Auto-reload server")

    workers: int = Field(default=1, description="Number of worker processes")

    # Database configuration

    database_url: str = Field(
        default="sqlite+aiosqlite:///./zeta.db",
        description="Database connection URL",
    )

    database_echo: bool = Field(default=False, description="Database echo SQL")

    database_pool_size: int = Field(default=5, description="Database pool size")

    # Redis configuration

    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )

    redis_max_connections: int = Field(default=20, description="Redis max connections")

    # Security

    secret_key: str = Field(
        default="your-secret-key-change-in-production", description="Secret key for JWT"
    )

    algorithm: str = Field(default="HS256", description="JWT algorithm")

    access_token_expire_minutes: int = Field(
        default=30, description="Access token expiration"
    )

    # Added: Refresh token expiration days

    refresh_token_expire_days: int = Field(
        default=7, description="Refresh token expiration in days"
    )

    # CORS settings

    cors_origins: list[str] = Field(
        default=["http://localhost:3000"], description="CORS allowed origins"
    )

    cors_allow_credentials: bool = Field(default=True, description="CORS credentials")

    # Logging

    log_level: str = Field(default="INFO", description="Logging level")

    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format",
    )

    # AI Service configuration

    openai_api_key: str = Field(default="", description="OpenAI API key")

    anthropic_api_key: str = Field(default="", description="Anthropic API key")

    huggingface_api_key: str = Field(default="", description="HuggingFace API key")

    # Dashboard Training Settings (compat with legacy flat settings)
    use_gpt_tutor: bool = Field(
        default=True,
        description="Enable GPT Tutor guidance in dashboard training",
    )
    training_chunk_size: int = Field(
        default=1000,
        description="Chunk size for training document splitting",
    )
    training_overlap: int = Field(
        default=200,
        description="Overlap between chunks for training",
    )
    max_concurrent_jobs: int = Field(
        default=5,
        description="Maximum number of concurrent training jobs",
    )

    # File storage

    upload_max_size: int = Field(default=10485760, description="Max upload size (10MB)")

    upload_allowed_types: list[str] = Field(
        default=[".txt", ".pdf", ".docx", ".md"], description="Allowed file types"
    )

    # Celery configuration (defaults suitable for local dev)
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1", description="Celery broker URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2", description="Celery result backend"
    )
    celery_task_track_started: bool = Field(
        default=True, description="Track task start events"
    )
    celery_result_expires: int = Field(
        default=3600, description="Result expiration in seconds"
    )
    celery_worker_pool: str | None = Field(
        default=None, description="Worker pool implementation (prefork/gevent/solo)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        extra="ignore",
    )

    @field_validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""

        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of: {valid_levels}")

        return v.upper()

    @field_validator("port")
    def validate_port(cls, v: int) -> int:
        """Validate port number."""

        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")

        return v

    def configure_logging(self) -> None:
        """Configure logging for the application."""

        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format=self.log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("logs/app.log"),
            ],
        )

    def get_cors_config(self) -> dict[str, Any]:
        """Return CORS configuration compatible with FastAPI CORSMiddleware.





        Returns:


            Dict containing allow_origins, allow_credentials, allow_methods, allow_headers.


        """

        return {
            "allow_origins": self.cors_origins,
            "allow_credentials": self.cors_allow_credentials,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }

    # --- Backward-compatibility attribute aliases (UPPERCASE) ---
    # Some legacy modules/tests refer to UPPERCASE settings attributes.
    # Provide dynamic aliases via __getattr__ to avoid naming clashes/lint issues.
    def __getattr__(self, name: str):  # pragma: no cover - dynamic alias
        mapping = {
            "SECRET_KEY": "secret_key",
            "ALGORITHM": "algorithm",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "access_token_expire_minutes",
            "REFRESH_TOKEN_EXPIRE_DAYS": "refresh_token_expire_days",
            "DATABASE_URL": "database_url",
            "REDIS_URL": "redis_url",
        }
        if name in mapping:
            return getattr(self, mapping[name])
        raise AttributeError(name)


# Singleton settings instance


class SettingsManager:
    """Manages the singleton instance of Settings."""

    _instance: Settings | None = None

    @classmethod
    def get_settings(cls) -> Settings:
        """Get settings instance (singleton pattern)."""
        if cls._instance is None:
            cls._instance = Settings()
        return cls._instance


# Back-compat convenience functions expected by package barrels and tests
def get_settings() -> Settings:
    """Return the singleton Settings instance.

    Returns:
        Settings: The shared settings object.
    """

    return SettingsManager.get_settings()


def reload_settings() -> Settings:
    """Reload settings by resetting the singleton.

    This is primarily useful in tests to pick up environment changes.

    Returns:
        Settings: A fresh Settings instance.
    """

    SettingsManager._instance = None
    return SettingsManager.get_settings()
