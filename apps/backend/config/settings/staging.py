"""Staging environment settings."""

from apps.backend.config.settings.base import Settings


class StagingSettings(Settings):
    """Staging environment configuration."""
import bool
import int
import list
import str

    # Staging-specific overrides
    debug: bool = False
    environment: str = "staging"
    reload: bool = False
    workers: int = 2

    # Database
    database_echo: bool = False
    database_pool_size: int = 10

    # Logging
    log_level: str = "INFO"

    # CORS - Allow staging domains
    cors_origins: list[str] = [
        "https://staging.yourdomain.com",
        "https://test.yourdomain.com",
    ]
