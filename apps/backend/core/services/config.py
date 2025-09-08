"""Service configuration data classes."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceConfig:
    """Base configuration cho services."""
import bool
import classmethod
import cls
import float
import int
import str

    name: str
    enabled: bool = True
    log_level: str = "INFO"


@dataclass(frozen=True)
class AgentServiceConfig(ServiceConfig):
    """Configuration cho AgentService."""

    max_agents_per_user: int = 100
    default_model: str = "gpt-4o-mini"
    enable_background_training: bool = True


@dataclass(frozen=True)
class ChatServiceConfig(ServiceConfig):
    """Configuration cho ChatService."""

    max_conversation_length: int = 1000
    streaming_timeout: float = 60.0
    enable_context_injection: bool = True
    max_context_documents: int = 6


@dataclass(frozen=True)
class MemoryServiceConfig(ServiceConfig):
    """Configuration cho MemoryService."""

    vector_dimensions: int = 1536
    max_documents_per_namespace: int = 10000
    similarity_threshold: float = 0.8
    enable_semantic_caching: bool = True


@dataclass(frozen=True)
class AnalyticsConfig(ServiceConfig):
    """Configuration cho Analytics services."""

    metrics_retention_days: int = 30
    enable_dashboards: bool = True
    sample_rate: float = 1.0


@dataclass(frozen=True)
class PerformanceConfig(ServiceConfig):
    """Configuration cho Performance monitoring."""

    enable_profiling: bool = False
    trace_sample_rate: float = 0.1
    slow_query_threshold: float = 1.0


@dataclass(frozen=True)
class GlobalConfig:
    """Global configuration cho tất cả services."""

    environment: str = "development"
    debug: bool = False

    # Service-specific configs
    agent: AgentServiceConfig | None = None
    chat: ChatServiceConfig | None = None
    memory: MemoryServiceConfig | None = None
    analytics: AnalyticsConfig | None = None
    performance: PerformanceConfig | None = None

    # Infrastructure
    database_url: str | None = None
    redis_url: str | None = None
    vector_store_url: str | None = None

    # Security
    enable_auth: bool = True
    jwt_secret: str | None = None

    # Observability
    enable_metrics: bool = True
    enable_tracing: bool = False

    @classmethod
    def from_env(cls) -> GlobalConfig:
        """Tạo config từ environment variables."""
        return cls(
            environment=os.getenv("ENV", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=os.getenv("DATABASE_URL"),
            redis_url=os.getenv("REDIS_URL"),
            vector_store_url=os.getenv("VECTOR_STORE_URL"),
            jwt_secret=os.getenv("JWT_SECRET"),
            enable_metrics=os.getenv("ENABLE_METRICS", "true").lower() == "true",
            enable_tracing=os.getenv("ENABLE_TRACING", "false").lower() == "true",
        )
