"""Development environment settings."""

from apps.backend.config.settings.base import Settings


class DevelopmentSettings(Settings):
    """Development environment configuration."""
import bool
import list
import str

    # Development-specific overrides
    debug: bool = True
    environment: str = "development"
    reload: bool = True

    # Database
    database_echo: bool = True

    # Logging
    log_level: str = "DEBUG"

    # CORS - Allow more origins for development
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
