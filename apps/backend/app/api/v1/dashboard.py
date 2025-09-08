"""Dashboard API endpoints for training monitoring and statistics."""

from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from app.dependencies import get_dashboard_service
from app.serializers.dashboard_serializers import (
    JobBrief,
    StatsOut,
    SystemHealthOut,
)
from fastapi import APIRouter, Depends, HTTPException, status

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/stats", response_model=StatsOut)
async def get_dashboard_stats(
    dashboard_service: Any = Depends(get_dashboard_service),
) -> StatsOut:
    """Get dashboard statistics.



    Returns:

        Dashboard statistics including training job counts and metrics



    Raises:

        HTTPException: If service error occurs

    """
import Exception
import dashboard_service
import dict
import e
import job
import stats
import str

    try:
        # TODO: Get user_id from authentication - using dummy for now

        dummy_user_id = UUID("12345678-1234-5678-9012-123456789abc")

        # Call the real dashboard service method

        stats: dict[str, Any] = await dashboard_service.get_dashboard_stats(
            dummy_user_id
        )

        return StatsOut(
            total_items=stats.get("total_items", 0),
            total_tokens=stats.get("total_tokens", 0),
            success_rate=stats.get("success_rate", 0.0),
            avg_job_time=stats.get("avg_job_time", 0.0),
            last_jobs=[
                JobBrief(
                    job_id=job.get("job_id", ""),
                    source=job.get("source", ""),
                    status=job.get("status", ""),
                    duration_sec=job.get("duration_sec", 0.0),
                )
                for job in stats.get("last_jobs", [])
            ],
        )

    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard statistics",
        ) from e


@router.get("/health", response_model=SystemHealthOut)
async def dashboard_health() -> SystemHealthOut:
    return SystemHealthOut(
        status="healthy",
        uptime_seconds=0.0,
        cpu_usage_percent=25.0,
        memory_usage_percent=60.0,
        disk_usage_percent=40.0,
        active_jobs=2,
        queue_size=0,
    )
