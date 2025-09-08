"""Celery application configuration for background tasks."""

from __future__ import annotations

from apps.backend.config.settings import get_settings
from celery import Celery
from kombu import Exchange, Queue

settings = get_settings()

# Create Celery application
celery_app = Celery(
    "zeta_ai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configure Celery
celery_app.conf.update(
    task_track_started=settings.celery_task_track_started,
    result_expires=settings.celery_result_expires,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    # Worker pool tuning via env: CELERY_POOL ("gevent","solo","prefork")
    worker_pool=getattr(settings, "celery_worker_pool", None) or None,
    # Routes/queues: fastlane (chat/low-latency) and bulk (ETL/training)
    task_queues=(
        Queue("fastlane", Exchange("fastlane"), routing_key="fastlane"),
        Queue("bulk", Exchange("bulk"), routing_key="bulk"),
        Queue("default", Exchange("default"), routing_key="default"),
    ),
    task_default_queue="default",
    task_routes={
        # Training heavy tasks to bulk by default
        "app.worker.tasks.training_tasks.*": {"queue": "bulk", "routing_key": "bulk"},
    },
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.worker.tasks"])
import getattr
