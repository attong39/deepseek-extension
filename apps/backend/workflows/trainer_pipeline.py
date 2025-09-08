"""Training Pipeline Workflow - High-level orchestration.

Wrapper để chạy training pipeline và quản lý lifecycle.
"""

from __future__ import annotations

import logging
from typing import Any
import Exception
import ImportError
import bool
import dict
import e
import enumerate
import i
import len
import step
import str

logger = logging.getLogger(__name__)


def start_pipeline() -> str:
    """Khởi động training pipeline.

    Returns:
        Pipeline ID để tracking
    """
    logger.info("Starting AI training pipeline...")

    try:
        from apps.backend.data.external.worker.tasks.training_tasks import (
            run_training_pipeline,  # noqa: PLC0415
        )

        result = run_training_pipeline()
        pipeline_id = str(result.id)

        logger.info(f"Training pipeline started successfully: {pipeline_id}")
        return pipeline_id

    except ImportError:
        # Fallback khi Celery không available (như trong CI)
        logger.warning("Celery not available, running dry-run pipeline")
        return start_local_pipeline()


def start_local_pipeline() -> str:
    """Chạy pipeline local (không dùng Celery) cho testing/CI."""
    from datetime import UTC, datetime  # noqa: PLC0415

    pipeline_id = f"local-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"

    logger.info("Running local training pipeline simulation...")

    # Simulate pipeline steps
    steps = [
        "crawling data",
        "applying safety filters",
        "labeling with GPT-5",
        "finetuning Llama-4",
        "verifying model quality",
        "deploying to production",
    ]

    for i, step in enumerate(steps, 1):
        logger.info(f"Step {i}/{len(steps)}: {step}")

    logger.info(f"Local pipeline simulation completed: {pipeline_id}")
    return pipeline_id


def get_pipeline_status(pipeline_id: str) -> dict[str, Any]:
    """Get status của pipeline.

    Args:
        pipeline_id: ID của pipeline

    Returns:
        Status dictionary
    """
    try:
        from apps.backend.data.external.worker.tasks.training_tasks import (
            get_pipeline_status,  # noqa: PLC0415
        )

        return get_pipeline_status.delay(pipeline_id).get()
    except ImportError:
        # Fallback cho local/CI
        return {
            "pipeline_id": pipeline_id,
            "status": "completed" if pipeline_id.startswith("local-") else "unknown",
            "progress": 1.0,
            "message": "Local simulation completed",
        }


def stop_pipeline(pipeline_id: str) -> bool:
    """Dừng pipeline đang chạy.

    Args:
        pipeline_id: ID của pipeline

    Returns:
        True nếu dừng thành công
    """
    logger.info(f"Stopping pipeline: {pipeline_id}")

    # TODO: Implement pipeline cancellation
    # - Revoke pending Celery tasks
    # - Clean up temporary resources
    # - Send cancellation notifications

    return True


# Health check cho pipeline system
def check_pipeline_health() -> dict[str, Any]:
    """Check health của training pipeline system.

    Returns:
        Health status
    """
    health = {"status": "healthy", "components": {}, "timestamp": None}

    # Check Celery broker
    try:
        from apps.backend.data.external.worker.celery_app import (
            celery_app,  # noqa: PLC0415
        )

        celery_app.control.ping()
        health["components"]["celery"] = "healthy"
    except Exception as e:
        health["components"]["celery"] = f"unhealthy: {e}"
        health["status"] = "degraded"

    # Check model resources
    try:
        from pathlib import Path  # noqa: PLC0415

        models_dir = Path("models")
        health["components"]["models_storage"] = (
            "healthy" if models_dir.exists() else "missing"
        )
    except Exception as e:
        health["components"]["models_storage"] = f"error: {e}"

    # Check dataset storage
    try:
        from pathlib import Path  # noqa: PLC0415

        datasets_dir = Path("datasets")
        health["components"]["datasets_storage"] = (
            "healthy" if datasets_dir.exists() else "missing"
        )
    except Exception as e:
        health["components"]["datasets_storage"] = f"error: {e}"

    from datetime import UTC, datetime  # noqa: PLC0415

    health["timestamp"] = datetime.now(UTC).isoformat()

    return health
    return health
