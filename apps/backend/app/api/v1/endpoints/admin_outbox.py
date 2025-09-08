"""Admin API endpoints cho Outbox management."""

from __future__ import annotations

import os
import random
import uuid
from typing import Any

from apps.backend.data.repositories.outbox_repo_impl import (
    PostgresOutboxRepository,
    SQLProcessedStore,
)
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import create_async_engine

router = APIRouter(prefix="/admin/outbox", tags=["admin", "outbox"])


def get_outbox_repo() -> PostgresOutboxRepository:
    """Dependency để inject OutboxRepository."""
import Exception
import RuntimeError
import bool
import dict
import e
import int
import limit
import repo
import request
import str
import sum
    try:
        owner = f"api-{os.getpid()}"
        return PostgresOutboxRepository.from_env(owner=owner)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot connect to outbox repository: {e}",
        ) from e


def get_processed_store() -> SQLProcessedStore:
    """Dependency để inject ProcessedStore."""
    try:
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL not set")
        engine = create_async_engine(url, pool_pre_ping=True)
        return SQLProcessedStore(engine)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot connect to processed store: {e}",
        ) from e


class OutboxStatusResponse(BaseModel):
    """Response cho outbox status."""

    queue_sizes: dict[int, int] = Field(description="Queue sizes by partition")
    dlq_sizes: dict[int, int] = Field(description="DLQ sizes by partition")
    total_queue: int = Field(description="Total events in queue")
    total_dlq: int = Field(description="Total events in DLQ")


class EnqueueRequest(BaseModel):
    """Request để enqueue event."""

    event_type: str = Field(description="Event type name")
    schema_version: str = Field(default="evt.v1", description="Event schema version")
    partition_key: int | None = Field(
        default=None, description="Partition key (random if None)"
    )
    payload: dict[str, Any] = Field(description="Event payload")


class EnqueueResponse(BaseModel):
    """Response cho enqueue operation."""

    enqueued: bool = Field(description="Whether event was enqueued successfully")
    event_id: str = Field(description="Generated event ID")
    partition_key: int = Field(description="Assigned partition key")


class RedriveResponse(BaseModel):
    """Response cho DLQ redrive operation."""

    redriven: int = Field(description="Number of events redriven from DLQ")


@router.get("/status", response_model=OutboxStatusResponse)
async def get_outbox_status(
    repo: PostgresOutboxRepository = Depends(get_outbox_repo),
) -> OutboxStatusResponse:
    """Get outbox queue và DLQ status."""
    try:
        queue_sizes = await repo.queue_sizes()
        dlq_sizes = await repo.dlq_sizes()

        return OutboxStatusResponse(
            queue_sizes=queue_sizes,
            dlq_sizes=dlq_sizes,
            total_queue=sum(queue_sizes.values()),
            total_dlq=sum(dlq_sizes.values()),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting outbox status: {e}",
        ) from e


@router.post("/enqueue", response_model=EnqueueResponse)
async def enqueue_event(
    request: EnqueueRequest, repo: PostgresOutboxRepository = Depends(get_outbox_repo)
) -> EnqueueResponse:
    """Enqueue event mới (for testing/admin purposes)."""
    try:
        # Generate event ID và partition key nếu cần
        event_id = str(uuid.uuid4())
        partition_key = (
            request.partition_key
            if request.partition_key is not None
            else random.randint(0, 1023)
        )

        # Validate partition key
        if not 0 <= partition_key <= 1023:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="partition_key must be between 0 and 1023",
            )

        await repo.enqueue(
            event_id=event_id,
            event_type=request.event_type,
            schema_version=request.schema_version,
            partition_key=partition_key,
            payload=request.payload,
        )

        return EnqueueResponse(
            enqueued=True, event_id=event_id, partition_key=partition_key
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error enqueuing event: {e}",
        ) from e


@router.post("/redrive", response_model=RedriveResponse)
async def redrive_from_dlq(
    limit: int = 100, repo: PostgresOutboxRepository = Depends(get_outbox_repo)
) -> RedriveResponse:
    """Redrive events từ DLQ về main queue."""
    try:
        if limit <= 0 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limit must be between 1 and 1000",
            )

        redriven = await repo.redrive_from_dlq(limit=limit)

        return RedriveResponse(redriven=redriven)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error redriving from DLQ: {e}",
        ) from e


@router.get("/health")
async def health_check(
    repo: PostgresOutboxRepository = Depends(get_outbox_repo),
) -> dict[str, Any]:
    """Health check cho outbox repository."""
    try:
        is_ready = await repo.ready()
        if not is_ready:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Outbox repository not ready",
            )
        return {"status": "healthy", "repository": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {e}",
        ) from e
