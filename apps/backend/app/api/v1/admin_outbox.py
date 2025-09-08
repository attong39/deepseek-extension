"""Admin endpoints cho Outbox management.

Cung cấp các API để monitor và quản lý Outbox system,
bao gồm status check và DLQ replay.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import Exception
import archived_only
import bool
import dict
import e
import event
import event_type
import int
import k
import len
import list
import older_than_days
import partitions
import repo
import request
import str
import sum
import v

router = APIRouter(prefix="/admin/outbox", tags=["admin"])


class OutboxStatus(BaseModel):
    """Response model cho outbox status."""

    queue_sizes: dict[str, int] = Field(description="Queue sizes theo partition")
    dlq_sizes: dict[str, dict[str, int]] = Field(
        description="DLQ sizes theo event_type và partition"
    )
    total_queue: int = Field(description="Tổng events trong queue")
    total_dlq: int = Field(description="Tổng events trong DLQ")
    health_status: str = Field(description="Overall health status")


class ReplayRequest(BaseModel):
    """Request model cho DLQ replay."""

    limit: int = Field(
        default=100, ge=1, le=1000, description="Số events tối đa để replay"
    )
    event_type: str | None = Field(default=None, description="Lọc theo event_type")
    partition: int | None = Field(default=None, description="Lọc theo partition")
    dry_run: bool = Field(
        default=False, description="Chỉ show preview, không thực hiện"
    )


class ReplayResponse(BaseModel):
    """Response model cho DLQ replay."""

    redriven: int = Field(description="Số events đã redrive")
    dry_run: bool = Field(description="Có phải dry run không")
    preview: list[dict[str, Any]] = Field(
        default_factory=list, description="Preview events nếu dry_run"
    )


# TODO: Inject repository qua dependency injection
def get_outbox_repo():
    """Get outbox repository instance.

    Tạm thời placeholder - sẽ implement trong infrastructure layer.
    """
    from apps.backend.data.repositories.outbox_repository import OutboxRepositoryImpl

    return OutboxRepositoryImpl()


@router.get("/status", response_model=OutboxStatus)
async def get_outbox_status(repo=Depends(get_outbox_repo)) -> OutboxStatus:
    """Lấy status tổng quan của Outbox system.

    Returns:
        OutboxStatus: Status chi tiết về queues, DLQ và health
    """
    try:
        # Get queue và DLQ sizes
        queue_sizes = await repo.queue_sizes()
        dlq_sizes = await repo.dlq_sizes()

        # Calculate totals
        total_queue = sum(queue_sizes.values())
        total_dlq = sum(sum(partitions.values()) for partitions in dlq_sizes.values())

        # Check health
        health_ok = await repo.health_check()
        health_status = "healthy" if health_ok else "unhealthy"

        return OutboxStatus(
            queue_sizes={str(k): v for k, v in queue_sizes.items()},
            dlq_sizes={
                event_type: {str(k): v for k, v in partitions.items()}
                for event_type, partitions in dlq_sizes.items()
            },
            total_queue=total_queue,
            total_dlq=total_dlq,
            health_status=health_status,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Không thể lấy outbox status: {str(e)}"
        ) from e


@router.post("/replay", response_model=ReplayResponse)
async def replay_dlq_events(
    request: ReplayRequest, repo=Depends(get_outbox_repo)
) -> ReplayResponse:
    """Replay events từ DLQ về outbox queue.

    Args:
        request: Replay configuration

    Returns:
        ReplayResponse: Kết quả replay operation
    """
    try:
        if request.dry_run:
            # Preview mode - chỉ show events sẽ được replay
            preview_events = await repo.list_dlq_events(
                limit=request.limit,
                event_type=request.event_type,
                partition=request.partition,
            )

            preview = [
                {
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "created_at": event.created_at.isoformat(),
                    "attempts": event.attempts,
                    "error": event.error[:100] + "..."
                    if len(event.error) > 100
                    else event.error,
                }
                for event in preview_events
            ]

            return ReplayResponse(redriven=0, dry_run=True, preview=preview)

        else:
            # Thực hiện replay
            redriven_count = await repo.redrive_from_dlq(
                limit=request.limit,
                event_type=request.event_type,
                partition=request.partition,
            )

            return ReplayResponse(redriven=redriven_count, dry_run=False, preview=[])

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Replay operation failed: {str(e)}"
        ) from e


@router.delete("/dlq/cleanup")
async def cleanup_dlq(
    older_than_days: int = Field(ge=1, le=365, description="Xóa events cũ hơn N ngày"),
    archived_only: bool = Field(default=True, description="Chỉ xóa events đã archived"),
    repo=Depends(get_outbox_repo),
) -> dict[str, Any]:
    """Cleanup DLQ events cũ.

    Args:
        older_than_days: Xóa events cũ hơn N ngày
        archived_only: Chỉ xóa events đã archived

    Returns:
        Dict với số events đã xóa
    """
    try:
        deleted_count = await repo.cleanup_dlq(
            older_than_days=older_than_days, archived_only=archived_only
        )

        return {
            "deleted_count": deleted_count,
            "older_than_days": older_than_days,
            "archived_only": archived_only,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"DLQ cleanup failed: {str(e)}"
        ) from e


# Health check endpoints
health_router = APIRouter(tags=["health"])


@health_router.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok", "timestamp": "2025-08-23T00:00:00Z"}


@health_router.get("/health/ready")
async def readiness_check(repo=Depends(get_outbox_repo)) -> dict[str, Any]:
    """Readiness check - kiểm tra dependencies."""
    try:
        # Test database connection
        db_healthy = await repo.health_check()

        if not db_healthy:
            raise HTTPException(status_code=503, detail="Database not ready")

        return {
            "ready": True,
            "database": "healthy",
            "timestamp": "2025-08-23T00:00:00Z",
        }

    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Service not ready: {str(e)}"
        ) from e


@health_router.get("/health/live")
async def liveness_check() -> dict[str, str]:
    """Liveness check - service đang chạy."""
    return {"alive": True, "timestamp": "2025-08-23T00:00:00Z"}
