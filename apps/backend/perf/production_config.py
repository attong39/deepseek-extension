"""
Production-ready performance configuration với feature flags và environment profiles.

Features:
- Environment-specific settings (dev/staging/prod)
- Feature flags cho gradual rollout
- Dynamic configuration updates
- Performance budgets và SLO enforcement
- Monitoring configuration management
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import bool
import dict
import enabled
import feature_name
import float
import getattr
import hasattr
import int
import self
import setattr
import str


class Environment(str, Enum):
    """Deployment environment."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class PerformanceFeatureFlags(BaseModel):
    """Feature flags cho performance monitoring components."""

    # Core features
    basic_monitoring: bool = True
    enhanced_metrics: bool = False
    ml_optimization: bool = False
    predictive_analysis: bool = False

    # Advanced features
    anomaly_detection: bool = False
    intelligent_alerting: bool = False
    auto_optimization: bool = False
    chaos_engineering: bool = False

    # Experimental features
    advanced_profiling: bool = False
    distributed_tracing_correlation: bool = False
    real_time_optimization: bool = False


@dataclass
class PerformanceBudget:
    """Performance budget configuration cho SLO enforcement."""

    # Response time budgets (milliseconds)
    p50_response_time_ms: float = 150.0
    p95_response_time_ms: float = 500.0
    p99_response_time_ms: float = 1200.0

    # Error rate budgets (percentage)
    error_rate_threshold: float = 1.0
    critical_error_rate: float = 5.0

    # Resource utilization budgets (percentage)
    cpu_utilization_target: float = 70.0
    cpu_utilization_max: float = 85.0
    memory_utilization_target: float = 75.0
    memory_utilization_max: float = 90.0

    # Throughput budgets
    min_requests_per_second: float = 10.0
    target_requests_per_second: float = 100.0

    # Cache performance budgets
    cache_hit_rate_target: float = 0.85
    cache_hit_rate_min: float = 0.70


class EnhancedPerfSettings(BaseSettings):
    """Enhanced performance settings với environment profiles."""

    model_config = SettingsConfigDict(
        env_prefix="PERF_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Environment configuration
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # Core performance settings (inherited từ base config)
    ENABLED: bool = True
    TRACING_ENABLED: bool = False
    SAMPLING_RATE: float = Field(default=0.1, ge=0.0, le=1.0)
    ADMIN_TOKEN: str = "dev-token"
    OTLP_ENDPOINT: str = "http://localhost:4318"

    # Enhanced monitoring settings
    ENHANCED_METRICS_ENABLED: bool = False
    ML_OPTIMIZATION_ENABLED: bool = False
    PREDICTIVE_ANALYSIS_ENABLED: bool = False
    ANOMALY_DETECTION_ENABLED: bool = False
    INTELLIGENT_ALERTING_ENABLED: bool = False

    # Monitoring intervals (seconds)
    METRICS_COLLECTION_INTERVAL: int = 5
    ANOMALY_DETECTION_INTERVAL: int = 30
    PREDICTION_UPDATE_INTERVAL: int = 60

    # ML configuration
    ANOMALY_DETECTION_THRESHOLD: float = 2.0
    ANOMALY_DETECTION_WINDOW_SIZE: int = 50
    ANOMALY_DETECTION_MIN_DATA_POINTS: int = 10

    # Alert configuration
    ALERT_COOLDOWN_MINUTES: int = 15
    ALERT_WEBHOOK_URL: str = ""
    ALERT_EMAIL_ENABLED: bool = False

    # Storage configuration
    METRICS_RETENTION_DAYS: int = 30
    PERFORMANCE_DATA_PATH: str = "/tmp/perf_data"

    def get_performance_budget(self) -> PerformanceBudget:
        """Get performance budget based on environment."""
        if self.ENVIRONMENT == Environment.PRODUCTION:
            return PerformanceBudget(
                p95_response_time_ms=300.0,
                p99_response_time_ms=800.0,
                error_rate_threshold=0.5,
                cpu_utilization_max=80.0,
                memory_utilization_max=85.0,
                cache_hit_rate_target=0.90,
            )
        elif self.ENVIRONMENT == Environment.STAGING:
            return PerformanceBudget(
                p95_response_time_ms=500.0,
                p99_response_time_ms=1200.0,
                error_rate_threshold=1.0,
                cpu_utilization_max=85.0,
                memory_utilization_max=90.0,
                cache_hit_rate_target=0.85,
            )
        else:  # Development
            return PerformanceBudget()  # Default relaxed budgets

    def get_feature_flags(self) -> PerformanceFeatureFlags:
        """Get feature flags based on environment và explicit settings."""
        if self.ENVIRONMENT == Environment.PRODUCTION:
            return PerformanceFeatureFlags(
                basic_monitoring=True,
                enhanced_metrics=self.ENHANCED_METRICS_ENABLED,
                ml_optimization=self.ML_OPTIMIZATION_ENABLED,
                anomaly_detection=self.ANOMALY_DETECTION_ENABLED,
                intelligent_alerting=self.INTELLIGENT_ALERTING_ENABLED,
                # Production: conservative approach
                predictive_analysis=False,
                auto_optimization=False,
                advanced_profiling=False,
            )
        elif self.ENVIRONMENT == Environment.STAGING:
            return PerformanceFeatureFlags(
                basic_monitoring=True,
                enhanced_metrics=True,
                ml_optimization=self.ML_OPTIMIZATION_ENABLED,
                predictive_analysis=self.PREDICTIVE_ANALYSIS_ENABLED,
                anomaly_detection=self.ANOMALY_DETECTION_ENABLED,
                intelligent_alerting=self.INTELLIGENT_ALERTING_ENABLED,
                # Staging: test advanced features
                auto_optimization=False,
                advanced_profiling=True,
            )
        else:  # Development
            return PerformanceFeatureFlags(
                # Development: enable all features for testing
                basic_monitoring=True,
                enhanced_metrics=True,
                ml_optimization=True,
                predictive_analysis=True,
                anomaly_detection=True,
                intelligent_alerting=True,
                auto_optimization=True,
                advanced_profiling=True,
                distributed_tracing_correlation=True,
                real_time_optimization=True,
            )

    def get_monitoring_config(self) -> dict[str, Any]:
        """Get monitoring configuration."""
        return {
            "collection_interval": self.METRICS_COLLECTION_INTERVAL,
            "anomaly_detection": {
                "enabled": self.ANOMALY_DETECTION_ENABLED,
                "threshold": self.ANOMALY_DETECTION_THRESHOLD,
                "window_size": self.ANOMALY_DETECTION_WINDOW_SIZE,
                "min_data_points": self.ANOMALY_DETECTION_MIN_DATA_POINTS,
                "interval": self.ANOMALY_DETECTION_INTERVAL,
            },
            "predictions": {
                "enabled": self.PREDICTIVE_ANALYSIS_ENABLED,
                "update_interval": self.PREDICTION_UPDATE_INTERVAL,
            },
            "alerts": {
                "cooldown_minutes": self.ALERT_COOLDOWN_MINUTES,
                "webhook_url": self.ALERT_WEBHOOK_URL,
                "email_enabled": self.ALERT_EMAIL_ENABLED,
            },
            "storage": {
                "retention_days": self.METRICS_RETENTION_DAYS,
                "data_path": Path(self.PERFORMANCE_DATA_PATH),
            },
        }


@dataclass
class PerformanceRuntimeState:
    """Enhanced runtime state với feature toggles."""

    # Base runtime state
    enabled: bool = True
    tracing_enabled: bool = False

    # Enhanced features runtime state
    enhanced_metrics_active: bool = False
    ml_optimization_active: bool = False
    anomaly_detection_active: bool = False
    predictive_analysis_active: bool = False
    intelligent_alerting_active: bool = False

    # Performance state
    current_load_level: str = "normal"  # low, normal, high, critical
    auto_optimization_enabled: bool = False
    emergency_mode: bool = False

    def update_from_settings(self, settings: EnhancedPerfSettings) -> None:
        """Update runtime state from settings."""
        flags = settings.get_feature_flags()

        self.enhanced_metrics_active = flags.enhanced_metrics and self.enabled
        self.ml_optimization_active = flags.ml_optimization and self.enabled
        self.anomaly_detection_active = flags.anomaly_detection and self.enabled
        self.predictive_analysis_active = flags.predictive_analysis and self.enabled
        self.intelligent_alerting_active = flags.intelligent_alerting and self.enabled

    def enable_emergency_mode(self) -> None:
        """Enable emergency mode - disable non-essential features."""
        self.emergency_mode = True
        self.ml_optimization_active = False
        self.predictive_analysis_active = False
        self.auto_optimization_enabled = False
        self.current_load_level = "critical"

    def disable_emergency_mode(self, settings: EnhancedPerfSettings) -> None:
        """Disable emergency mode và restore normal operation."""
        self.emergency_mode = False
        self.current_load_level = "normal"
        self.update_from_settings(settings)


# Global instances
_enhanced_settings: EnhancedPerfSettings | None = None
_enhanced_runtime = PerformanceRuntimeState()


def get_enhanced_settings() -> EnhancedPerfSettings:
    """Get enhanced performance settings singleton."""
    global _enhanced_settings
    if _enhanced_settings is None:
        _enhanced_settings = EnhancedPerfSettings()
    return _enhanced_settings


def get_enhanced_runtime() -> PerformanceRuntimeState:
    """Get enhanced runtime state."""
    return _enhanced_runtime


def initialize_enhanced_runtime() -> None:
    """Initialize enhanced runtime state from settings."""
    settings = get_enhanced_settings()
    runtime = get_enhanced_runtime()
    runtime.update_from_settings(settings)


def is_feature_enabled(feature_name: str) -> bool:
    """Check if a specific feature is enabled."""
    settings = get_enhanced_settings()
    flags = settings.get_feature_flags()
    return getattr(flags, feature_name, False)


def get_current_performance_budget() -> PerformanceBudget:
    """Get current performance budget based on environment."""
    settings = get_enhanced_settings()
    return settings.get_performance_budget()


def update_runtime_feature(feature_name: str, enabled: bool) -> bool:
    """Update runtime feature state dynamically."""
    runtime = get_enhanced_runtime()

    if hasattr(runtime, f"{feature_name}_active"):
        setattr(runtime, f"{feature_name}_active", enabled and runtime.enabled)
        return True

    return False
