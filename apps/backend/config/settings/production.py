"""Production environment settings."""

from apps.backend.config.settings.base import Settings


class ProductionSettings(Settings):
    """Production environment configuration."""
import bool
import float
import int
import list
import str

    # Production-specific overrides
    debug: bool = False
    environment: str = "production"
    reload: bool = False
    workers: int = 4

    # Database - Production optimizations
    database_echo: bool = False
    database_pool_size: int = 20

    # Security
    secret_key: str = ""  # Must be set via environment variable

    # Logging
    log_level: str = "WARNING"

    # CORS - Restrictive for production
    cors_origins: list[str] = [
        "https://yourdomain.com",
        "https://app.yourdomain.com",
    ]

    # Performance
    upload_max_size: int = 52428800  # 50MB for production

    # Feature flags for AI behavior (mirrors ML config where applicable)
    FAST_STREAMING: bool = True
    HYBRID_RETRIEVAL: bool = True
    EMBEDDING_BATCH_SIZE: int = 100
    RERANK_MIN_SCORE: float = 0.2
    LONG_CONTEXT_MODEL: str = "gpt-4o"
    RAG_CACHE_TTL: int = 900
