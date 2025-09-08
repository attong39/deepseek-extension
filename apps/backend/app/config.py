"""
App Configuration Module.

This module provides centralized configuration management for the Zeta VN application.
It loads settings from environment variables, config files, and provides defaults.
"""

from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings
import bool
import dict
import int
import list
import str


class AppSettings(BaseSettings):
    """Application settings using Pydantic for validation."""

    # Basic app info
    app_name: str = Field(default="Zeta VN", description="Application name")
    version: str = Field(default="2.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    env: str = Field(default="development", description="Environment (development/production)")

    # API settings
    api_prefix: str = Field(default="/api", description="API prefix")
    api_version: str = Field(default="v1", description="API version")
    docs_url: str = Field(default="/docs", description="API documentation URL")
    redoc_url: str = Field(default="/redoc", description="ReDoc URL")

    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(default=True, description="Auto reload in development")

    # Database settings
    database_url: str = Field(
        default="sqlite:///./zeta.db",
        description="Database connection URL"
    )

    # Security settings
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT and other security features"
    )
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str | None = Field(default=None, description="Log file path")

    # Service settings
    redis_url: str = Field(default="redis://localhost:6379", description="Redis URL")
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")

    # Performance settings
    max_concurrency: int = Field(default=10, description="Maximum concurrent requests")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from environment variables


# Global settings instance
_settings: AppSettings | None = None


def get_settings() -> AppSettings:
    """
    Get application settings.

    Returns a singleton instance of AppSettings, loading from environment
    variables and config files.

    Returns:
        AppSettings: Application settings instance
    """
    global _settings

    if _settings is None:
        _settings = AppSettings()

    return _settings


def get_settings_dict() -> dict[str, Any]:
    """
    Get settings as a dictionary.

    Returns:
        Dict[str, Any]: Settings as dictionary
    """
    settings = get_settings()
    return settings.dict()


def reload_settings() -> AppSettings:
    """
    Reload settings from environment.

    This is useful for testing or when environment variables change.

    Returns:
        AppSettings: Fresh settings instance
    """
    global _settings
    _settings = AppSettings()
    return _settings


# Convenience functions for common settings
def is_debug() -> bool:
    """Check if debug mode is enabled."""
    return get_settings().debug


def is_production() -> bool:
    """Check if running in production environment."""
    return get_settings().env.lower() == "production"


def get_database_url() -> str:
    """Get database URL."""
    return get_settings().database_url


def get_secret_key() -> str:
    """Get secret key."""
    return get_settings().secret_key


def get_log_level() -> str:
    """Get log level."""
    return get_settings().log_level


def get_log_file() -> str | None:
    """Get log file path."""
    return get_settings().log_file


# Constants for backward compatibility
PROJECT_NAME = "Zeta VN"
API_PREFIX = "/api"
API_VERSION = "v1"
DEBUG = False
ENV = "development"
DATABASE_URL = "sqlite:///./zeta.db"
SERVICE_NAME = "zeta-vn"
DESCRIPTION = "AI-powered backend service"
BUILD_TIME_UTC = "2025-09-09T00:00:00Z"
METRICS_PORT = 9090
DOCS_URL = "/docs"
REDOC_URL = "/redoc"
ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]
TRUSTED_HOSTS = ["localhost", "127.0.0.1"]

# Permissions constants
ADMIN_FULL = "admin:full"
AGENT_CREATE = "agent:create"
AGENT_READ = "agent:read"
AGENT_UPDATE = "agent:update"
AGENT_DELETE = "agent:delete"
CHAT_CREATE = "chat:create"
CHAT_READ = "chat:read"
CHAT_HISTORY = "chat:history"

# Tags metadata for API documentation
TAGS_METADATA = [
    {"name": "agents", "description": "Agent management operations"},
    {"name": "chat", "description": "Chat and conversation operations"},
    {"name": "auth", "description": "Authentication operations"},
    {"name": "admin", "description": "Administrative operations"},
    {"name": "health", "description": "Health check operations"},
]


__all__ = [
    "get_settings",
    "get_settings_dict",
    "reload_settings",
    "is_debug",
    "is_production",
    "get_database_url",
    "get_secret_key",
    "get_log_level",
    "get_log_file",
    # Constants
    "PROJECT_NAME",
    "API_PREFIX",
    "API_VERSION",
    "DEBUG",
    "ENV",
    "DATABASE_URL",
    "SERVICE_NAME",
    "DESCRIPTION",
    "BUILD_TIME_UTC",
    "METRICS_PORT",
    "DOCS_URL",
    "REDOC_URL",
    "ALLOWED_ORIGINS",
    "TRUSTED_HOSTS",
    # Permissions
    "ADMIN_FULL",
    "AGENT_CREATE",
    "AGENT_READ",
    "AGENT_UPDATE",
    "AGENT_DELETE",
    "CHAT_CREATE",
    "CHAT_READ",
    "CHAT_HISTORY",
    # Metadata
    "TAGS_METADATA",
]
