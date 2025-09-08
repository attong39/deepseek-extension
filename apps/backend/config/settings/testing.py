"""Testing environment settings."""

from apps.backend.config.settings.base import Settings


class TestingSettings(Settings):
    """Testing environment configuration."""
import bool
import int
import list
import str

    # Testing-specific overrides
    debug: bool = True
    environment: str = "testing"

    # Database - Use in-memory SQLite for tests
    database_url: str = "sqlite:///:memory:"
    database_echo: bool = False

    # Redis - Use fake Redis for tests
    redis_url: str = "redis://localhost:6379/15"  # Different DB for tests

    # Security - Use test keys
    secret_key: str = "test-secret-key-for-testing-only"

    # Logging - Minimal for tests
    log_level: str = "WARNING"

    # CORS - Allow all for testing
    cors_origins: list[str] = ["*"]

    # Performance - Fast for tests
    upload_max_size: int = 1048576  # 1MB for tests
