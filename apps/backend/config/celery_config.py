"""Celery configuration for ZETA AI system.

This module provides Celery configuration for distributed task processing,
including broker settings, result backend, and task routing.
"""

from __future__ import annotations

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import Exception
import bool
import content
import dict
import int
import isinstance
import list
import str
import v


class CelerySettings(BaseSettings):
    """Celery configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Broker Configuration
    broker_url: str = Field(default="redis://localhost:6379/5")
    broker_connection_retry_on_startup: bool = Field(default=True)
    broker_connection_retry: bool = Field(default=True)
    broker_connection_max_retries: int = Field(default=3)

    # Result Backend
    result_backend: str = Field(default="redis://localhost:6379/6")
    result_backend_transport_options: dict = Field(default={})
    result_expires: int = Field(default=3600)  # 1 hour
    result_persistent: bool = Field(default=True)

    # Task Configuration
    task_serializer: str = Field(default="json")
    result_serializer: str = Field(default="json")
    accept_content: list[str] = Field(default=["json"])
    task_compression: str = Field(default="gzip")
    result_compression: str = Field(default="gzip")

    # Task Execution
    task_always_eager: bool = Field(default=False)  # Set to True for testing
    task_eager_propagates: bool = Field(default=True)
    task_ignore_result: bool = Field(default=False)
    task_store_eager_result: bool = Field(default=True)

    # Task Routing
    task_routes: dict = Field(
        default={
            "app.worker.tasks.ai_tasks.*": {"queue": "ai_processing"},
            "app.worker.tasks.file_tasks.*": {"queue": "file_processing"},
            "app.worker.tasks.email_tasks.*": {"queue": "notifications"},
            "app.worker.tasks.analytics_tasks.*": {"queue": "analytics"},
            "app.worker.tasks.maintenance_tasks.*": {"queue": "maintenance"},
        }
    )

    # Queue Configuration
    task_default_queue: str = Field(default="default")
    task_queues: dict = Field(
        default={
            "default": {
                "exchange": "default",
                "exchange_type": "direct",
                "routing_key": "default",
            },
            "ai_processing": {
                "exchange": "ai_processing",
                "exchange_type": "direct",
                "routing_key": "ai_processing",
            },
            "file_processing": {
                "exchange": "file_processing",
                "exchange_type": "direct",
                "routing_key": "file_processing",
            },
            "notifications": {
                "exchange": "notifications",
                "exchange_type": "direct",
                "routing_key": "notifications",
            },
            "analytics": {
                "exchange": "analytics",
                "exchange_type": "direct",
                "routing_key": "analytics",
            },
            "maintenance": {
                "exchange": "maintenance",
                "exchange_type": "direct",
                "routing_key": "maintenance",
            },
        }
    )

    # Worker Configuration
    worker_prefetch_multiplier: int = Field(default=4)
    worker_max_tasks_per_child: int = Field(default=1000)
    worker_max_memory_per_child: int = Field(default=200000)  # 200MB in KB
    worker_concurrency: int = Field(default=4)
    worker_pool: str = Field(default="prefork")  # prefork, eventlet, gevent, solo

    # Task Time Limits
    task_soft_time_limit: int = Field(default=300)  # 5 minutes
    task_time_limit: int = Field(default=600)  # 10 minutes
    task_acks_late: bool = Field(default=True)
    task_reject_on_worker_lost: bool = Field(default=True)

    # Monitoring and Logging
    worker_send_task_events: bool = Field(default=True)
    task_send_sent_event: bool = Field(default=True)
    worker_log_level: str = Field(default="INFO")
    worker_hijack_root_logger: bool = Field(default=False)

    # Beat Scheduler (Periodic Tasks)
    beat_schedule: dict = Field(
        default={
            "cleanup-expired-sessions": {
                "task": "app.worker.tasks.maintenance_tasks.cleanup_expired_sessions",
                "schedule": 3600.0,  # Every hour
            },
            "update-analytics": {
                "task": "app.worker.tasks.analytics_tasks.update_daily_analytics",
                "schedule": 86400.0,  # Every day
            },
            "health-check": {
                "task": "app.worker.tasks.maintenance_tasks.system_health_check",
                "schedule": 300.0,  # Every 5 minutes
            },
            "cleanup-old-files": {
                "task": "app.worker.tasks.file_tasks.cleanup_old_temp_files",
                "schedule": 7200.0,  # Every 2 hours
            },
        }
    )
    beat_scheduler: str = Field(
        default="django_celery_beat.schedulers:DatabaseScheduler"
    )

    # Security
    worker_enable_remote_control: bool = Field(default=False)
    worker_disable_rate_limits: bool = Field(default=False)

    # Error Handling
    task_reject_on_worker_lost: bool = Field(default=True)
    task_acks_on_failure_or_timeout: bool = Field(default=True)
    task_retry_jitter: bool = Field(default=True)

    # Performance
    worker_prefetch_multiplier: int = Field(default=4)
    worker_optimization: str = Field(default="fair")  # fair, speed

    # Development Settings
    task_always_eager: bool = Field(default=False)
    task_eager_propagates: bool = Field(default=True)

    @validator("accept_content", pre=True)
    def parse_accept_content(cls, v):
        """Parse accepted content types from string or list."""
        if isinstance(v, str):
            return [content.strip() for content in v.split(",") if content.strip()]
        return v


def get_celery_settings() -> CelerySettings:
    """Get Celery settings instance."""
    return CelerySettings()


# Task Priority Levels
class TaskPriority:
    """Task priority level constants."""

    LOW = 1
    NORMAL = 5
    HIGH = 7
    CRITICAL = 9


# Task Queues
class TaskQueues:
    """Task queue name constants."""

    DEFAULT = "default"
    AI_PROCESSING = "ai_processing"
    FILE_PROCESSING = "file_processing"
    NOTIFICATIONS = "notifications"
    ANALYTICS = "analytics"
    MAINTENANCE = "maintenance"
    HIGH_PRIORITY = "high_priority"
    LOW_PRIORITY = "low_priority"


# Task Categories
class TaskCategory:
    """Task category constants."""

    AI_INFERENCE = "ai_inference"
    AI_TRAINING = "ai_training"
    FILE_PROCESSING = "file_processing"
    EMAIL_SENDING = "email_sending"
    DATA_EXPORT = "data_export"
    DATA_IMPORT = "data_import"
    ANALYTICS = "analytics"
    MAINTENANCE = "maintenance"
    BACKUP = "backup"
    CLEANUP = "cleanup"


# Common Task Options
TASK_OPTIONS = {
    "ai_inference": {
        "queue": TaskQueues.AI_PROCESSING,
        "priority": TaskPriority.HIGH,
        "time_limit": 300,
        "soft_time_limit": 240,
    },
    "ai_training": {
        "queue": TaskQueues.AI_PROCESSING,
        "priority": TaskPriority.NORMAL,
        "time_limit": 3600,
        "soft_time_limit": 3300,
    },
    "file_processing": {
        "queue": TaskQueues.FILE_PROCESSING,
        "priority": TaskPriority.NORMAL,
        "time_limit": 600,
        "soft_time_limit": 540,
    },
    "email_sending": {
        "queue": TaskQueues.NOTIFICATIONS,
        "priority": TaskPriority.HIGH,
        "time_limit": 60,
        "soft_time_limit": 50,
    },
    "analytics": {
        "queue": TaskQueues.ANALYTICS,
        "priority": TaskPriority.LOW,
        "time_limit": 1800,
        "soft_time_limit": 1620,
    },
    "maintenance": {
        "queue": TaskQueues.MAINTENANCE,
        "priority": TaskPriority.LOW,
        "time_limit": 3600,
        "soft_time_limit": 3300,
    },
}

# Retry Policies
RETRY_POLICIES = {
    "default": {
        "autoretry_for": (Exception,),
        "retry_kwargs": {"max_retries": 3, "countdown": 60},
        "retry_backoff": True,
        "retry_backoff_max": 700,
        "retry_jitter": True,
    },
    "critical": {
        "autoretry_for": (Exception,),
        "retry_kwargs": {"max_retries": 5, "countdown": 30},
        "retry_backoff": True,
        "retry_backoff_max": 600,
        "retry_jitter": True,
    },
    "no_retry": {
        "autoretry_for": (),
        "retry_kwargs": {"max_retries": 0},
    },
}


# Worker Pool Types
class WorkerPool:
    """Worker pool type constants."""

    PREFORK = "prefork"
    EVENTLET = "eventlet"
    GEVENT = "gevent"
    SOLO = "solo"  # Single threaded for debugging
