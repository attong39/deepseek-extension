from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any
import ValueError
import bool
import classmethod
import cls
import config_key
import data
import dict
import env_var
import float
import int
import k
import prefix
import self
import str
import v

"""Configuration cho Outbox system với environment support và validation nâng cao."""


@dataclass
class OutboxConfig:
    """Configuration cho Outbox repository với environment support."""

    max_connections: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_MAX_CONNECTIONS", "20"))
    )
    connection_timeout: float = field(
        default_factory=lambda: float(os.getenv("OUTBOX_CONNECTION_TIMEOUT", "30.0"))
    )
    command_timeout: float = field(
        default_factory=lambda: float(os.getenv("OUTBOX_COMMAND_TIMEOUT", "10.0"))
    )
    max_attempts: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_MAX_ATTEMPTS", "10"))
    )
    base_backoff_sec: float = field(
        default_factory=lambda: float(os.getenv("OUTBOX_BASE_BACKOFF", "1.2"))
    )
    max_backoff_sec: float = field(
        default_factory=lambda: float(os.getenv("OUTBOX_MAX_BACKOFF", "300.0"))
    )
    jitter_factor: float = field(
        default_factory=lambda: float(os.getenv("OUTBOX_JITTER", "0.3"))
    )
    lock_timeout_minutes: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_LOCK_TIMEOUT", "15"))
    )
    stale_lock_cleanup_interval: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_STALE_CLEANUP", "60"))
    )
    default_batch_size: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_BATCH_SIZE", "50"))
    )
    max_batch_size: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_MAX_BATCH_SIZE", "200"))
    )
    enable_partitioning: bool = field(
        default_factory=lambda: os.getenv("OUTBOX_ENABLE_PARTITIONING", "true").lower()
        == "true"
    )
    partition_count: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_PARTITION_COUNT", "16"))
    )
    enable_metrics: bool = field(
        default_factory=lambda: os.getenv("OUTBOX_ENABLE_METRICS", "true").lower()
        == "true"
    )
    metrics_prefix: str = field(
        default_factory=lambda: os.getenv("OUTBOX_METRICS_PREFIX", "zeta_outbox")
    )
    dlq_max_age_days: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_DLQ_MAX_AGE", "30"))
    )
    dlq_cleanup_batch_size: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_DLQ_CLEANUP_BATCH", "1000"))
    )
    enable_connection_pooling: bool = field(
        default_factory=lambda: os.getenv("OUTBOX_CONNECTION_POOLING", "true").lower()
        == "true"
    )
    connection_pool_size: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_POOL_SIZE", "10"))
    )
    connection_pool_max_overflow: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_POOL_OVERFLOW", "20"))
    )
    enable_circuit_breaker: bool = field(
        default_factory=lambda: os.getenv("OUTBOX_CIRCUIT_BREAKER", "true").lower()
        == "true"
    )
    circuit_failure_threshold: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_CIRCUIT_THRESHOLD", "5"))
    )
    circuit_recovery_timeout: int = field(
        default_factory=lambda: int(os.getenv("OUTBOX_CIRCUIT_RECOVERY", "60"))
    )

    def __post_init__(self) -> None:
        """Validate configuration với detailed error messages."""
        self._validate_database_settings()
        self._validate_processing_settings()
        self._validate_performance_settings()

    def _validate_database_settings(self) -> None:
        """Validate database-related settings."""
        if self.max_connections <= 0:
            raise ValueError(f"max_connections phải > 0, got {self.max_connections}")
        if self.connection_timeout <= 0:
            raise ValueError(
                f"connection_timeout phải > 0, got {self.connection_timeout}"
            )
        if self.command_timeout <= 0:
            raise ValueError(f"command_timeout phải > 0, got {self.command_timeout}")

    def _validate_processing_settings(self) -> None:
        """Validate processing-related settings."""
        if self.max_attempts <= 0:
            raise ValueError(f"max_attempts phải > 0, got {self.max_attempts}")
        if self.base_backoff_sec <= 1.0:
            raise ValueError(
                f"base_backoff_sec phải > 1.0, got {self.base_backoff_sec}"
            )
        if not 0 <= self.jitter_factor <= 1.0:
            raise ValueError(
                f"jitter_factor phải trong khoảng [0, 1], got {self.jitter_factor}"
            )
        if self.lock_timeout_minutes <= 0:
            raise ValueError(
                f"lock_timeout_minutes phải > 0, got {self.lock_timeout_minutes}"
            )

    def _validate_performance_settings(self) -> None:
        """Validate performance-related settings."""
        if self.default_batch_size <= 0:
            raise ValueError(
                f"default_batch_size phải > 0, got {self.default_batch_size}"
            )
        if self.max_batch_size < self.default_batch_size:
            raise ValueError(
                f"max_batch_size phải >= default_batch_size, got {self.max_batch_size} < {self.default_batch_size}"
            )
        if self.partition_count <= 0:
            raise ValueError(f"partition_count phải > 0, got {self.partition_count}")

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary for serialization."""
        return {
            "max_connections": self.max_connections,
            "connection_timeout": self.connection_timeout,
            "command_timeout": self.command_timeout,
            "max_attempts": self.max_attempts,
            "base_backoff_sec": self.base_backoff_sec,
            "max_backoff_sec": self.max_backoff_sec,
            "jitter_factor": self.jitter_factor,
            "lock_timeout_minutes": self.lock_timeout_minutes,
            "stale_lock_cleanup_interval": self.stale_lock_cleanup_interval,
            "default_batch_size": self.default_batch_size,
            "max_batch_size": self.max_batch_size,
            "enable_partitioning": self.enable_partitioning,
            "partition_count": self.partition_count,
            "enable_metrics": self.enable_metrics,
            "metrics_prefix": self.metrics_prefix,
            "dlq_max_age_days": self.dlq_max_age_days,
            "dlq_cleanup_batch_size": self.dlq_cleanup_batch_size,
            "enable_connection_pooling": self.enable_connection_pooling,
            "connection_pool_size": self.connection_pool_size,
            "connection_pool_max_overflow": self.connection_pool_max_overflow,
            "enable_circuit_breaker": self.enable_circuit_breaker,
            "circuit_failure_threshold": self.circuit_failure_threshold,
            "circuit_recovery_timeout": self.circuit_recovery_timeout,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboxConfig:
        """Create config from dictionary."""
        return cls(**data)

    @classmethod
    def from_env(cls, prefix: str = "OUTBOX_") -> OutboxConfig:
        """Create config from environment variables với custom prefix."""
        env_vars = {k: v for k, v in os.environ.items() if k.startswith(prefix)}
        config_dict = {}
        env_mapping = {
            f"{prefix}MAX_CONNECTIONS": "max_connections",
            f"{prefix}CONNECTION_TIMEOUT": "connection_timeout",
            f"{prefix}COMMAND_TIMEOUT": "command_timeout",
            f"{prefix}MAX_ATTEMPTS": "max_attempts",
            f"{prefix}BASE_BACKOFF": "base_backoff_sec",
            f"{prefix}MAX_BACKOFF": "max_backoff_sec",
            f"{prefix}JITTER": "jitter_factor",
            f"{prefix}LOCK_TIMEOUT": "lock_timeout_minutes",
            f"{prefix}STALE_CLEANUP": "stale_lock_cleanup_interval",
            f"{prefix}BATCH_SIZE": "default_batch_size",
            f"{prefix}MAX_BATCH_SIZE": "max_batch_size",
            f"{prefix}ENABLE_PARTITIONING": "enable_partitioning",
            f"{prefix}PARTITION_COUNT": "partition_count",
            f"{prefix}ENABLE_METRICS": "enable_metrics",
            f"{prefix}METRICS_PREFIX": "metrics_prefix",
            f"{prefix}DLQ_MAX_AGE": "dlq_max_age_days",
            f"{prefix}DLQ_CLEANUP_BATCH": "dlq_cleanup_batch_size",
            f"{prefix}CONNECTION_POOLING": "enable_connection_pooling",
            f"{prefix}POOL_SIZE": "connection_pool_size",
            f"{prefix}POOL_OVERFLOW": "connection_pool_max_overflow",
            f"{prefix}CIRCUIT_BREAKER": "enable_circuit_breaker",
            f"{prefix}CIRCUIT_THRESHOLD": "circuit_failure_threshold",
            f"{prefix}CIRCUIT_RECOVERY": "circuit_recovery_timeout",
        }
        for env_var, config_key in env_mapping.items():
            if env_var in env_vars:
                value = env_vars[env_var]
                if config_key in [
                    "max_connections",
                    "max_attempts",
                    "lock_timeout_minutes",
                    "stale_lock_cleanup_interval",
                    "default_batch_size",
                    "max_batch_size",
                    "partition_count",
                    "dlq_max_age_days",
                    "dlq_cleanup_batch_size",
                    "connection_pool_size",
                    "connection_pool_max_overflow",
                    "circuit_failure_threshold",
                    "circuit_recovery_timeout",
                ]:
                    config_dict[config_key] = int(value)
                elif config_key in [
                    "connection_timeout",
                    "command_timeout",
                    "base_backoff_sec",
                    "max_backoff_sec",
                    "jitter_factor",
                ]:
                    config_dict[config_key] = float(value)  # type: ignore
                elif config_key in [
                    "enable_partitioning",
                    "enable_metrics",
                    "enable_connection_pooling",
                    "enable_circuit_breaker",
                ]:
                    config_dict[config_key] = value.lower() == "true"
                else:
                    config_dict[config_key] = value  # type: ignore
        if config_dict:
            return cls(**config_dict)  # type: ignore
        else:
            return cls()


@dataclass
class DispatcherConfig:
    """Configuration cho Outbox dispatcher."""

    worker_count: int = 4
    worker_id_prefix: str = "dispatcher"
    poll_interval_sec: float = 0.05
    batch_size: int = 50
    max_concurrent_batches: int = 16
    enable_prefetch: bool = True
    prefetch_multiplier: int = 3
    enable_health_checks: bool = True
    health_check_interval: int = 30
    enable_detailed_metrics: bool = True
    metrics_update_interval: int = 15
    enable_circuit_breaker: bool = True
    circuit_failure_threshold: int = 5
    circuit_recovery_timeout: int = 60

    def __post_init__(self) -> None:
        """Validate configuration."""
        if self.worker_count <= 0:
            raise ValueError("worker_count phải > 0")
        if self.batch_size <= 0:
            raise ValueError("batch_size phải > 0")
        if self.poll_interval_sec <= 0:
            raise ValueError("poll_interval_sec phải > 0")


@dataclass
class EventBusConfig:
    """Configuration cho Event Bus."""

    max_concurrent_handlers: int = 50
    handler_timeout_sec: float = 30.0
    enable_dead_letter: bool = True
    dlq_max_retries: int = 3
    enable_handler_metrics: bool = True

    def __post_init__(self) -> None:
        """Validate configuration."""
        if self.max_concurrent_handlers <= 0:
            raise ValueError("max_concurrent_handlers phải > 0")
        if self.handler_timeout_sec <= 0:
            raise ValueError("handler_timeout_sec phải > 0")


__all__ = [
    "DispatcherConfig",
    "EventBusConfig",
    "OutboxConfig",
]
