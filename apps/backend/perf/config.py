"""
Performance settings và runtime state management.

Features:
- Environment-driven configuration với validation
- Runtime toggles cho performance features
- SLO thresholds cho P95/P99 latency
- Secure admin authentication
- OpenTelemetry endpoint configuration
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import bool
import float
import int
import str


class PerfSettings(BaseSettings):
    """Performance configuration từ environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="PERF_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra environment variables
    )

    PERF_ENABLED: bool = Field(
        default=True, description="Enable performance monitoring"
    )
    PERF_TRACING_ENABLED: bool = Field(
        default=False, description="Enable OpenTelemetry tracing"
    )
    PERF_SAMPLING: float = Field(
        default=0.1, ge=0.0, le=1.0, description="Sampling rate for tracing (0.0-1.0)"
    )
    PERF_ADMIN_TOKEN: str = Field(
        default="dev-token", description="Admin API authentication token"
    )
    PERF_SLO_P95_MS: int = Field(
        default=500, ge=1, description="SLO threshold for P95 latency (ms)"
    )
    PERF_SLO_P99_MS: int = Field(
        default=1200, ge=1, description="SLO threshold for P99 latency (ms)"
    )
    PERF_OTLP_ENDPOINT: str = Field(
        default="http://localhost:4318", description="OpenTelemetry OTLP/HTTP endpoint"
    )


@dataclass
class PerfRuntimeState:
    """Runtime state cho performance features (có thể toggle qua admin API)."""

    enabled: bool = True
    tracing_enabled: bool = False


# Global singletons
_settings: PerfSettings | None = None
_runtime = PerfRuntimeState()


def get_settings() -> PerfSettings:
    """Get performance settings singleton (reads from env once)."""
    global _settings
    if _settings is None:
        _settings = PerfSettings()
    return _settings


def get_runtime() -> PerfRuntimeState:
    """Get runtime state (mutable via admin API)."""
    return _runtime


def initialize_runtime_from_env() -> None:
    """Initialize runtime state from environment settings."""
    settings = get_settings()
    runtime = get_runtime()
    runtime.enabled = settings.PERF_ENABLED
    runtime.tracing_enabled = settings.PERF_TRACING_ENABLED
