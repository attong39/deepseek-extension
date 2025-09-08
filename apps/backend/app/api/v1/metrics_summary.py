"""Metrics summary endpoints.

Cung cấp human-readable metrics summary ngoài Prometheus /metrics endpoint.
Dành cho debugging và monitoring dashboard.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
import dict
import float
import int
import str

router = APIRouter(prefix="/metrics-summary", tags=["metrics"])


class MetricsSummary(BaseModel):
    """Summary model cho key metrics."""

    outbox_queue_total: int = Field(description="Tổng events trong outbox queue")
    dlq_total: int = Field(description="Tổng events trong DLQ")
    events_processed_last_hour: int = Field(description="Events processed trong 1h qua")
    events_failed_last_hour: int = Field(description="Events failed trong 1h qua")
    avg_processing_time_ms: float = Field(description="Thời gian xử lý trung bình (ms)")
    active_workers: int = Field(description="Số workers đang active")
    health_status: str = Field(description="Overall system health")
    last_updated: str = Field(description="Timestamp metrics được update")


def get_outbox_repo():
    """Placeholder cho repository dependency."""
    # TODO: Implement proper DI


@router.get("", response_model=MetricsSummary)
async def get_metrics_summary(repo=Depends(get_outbox_repo)) -> MetricsSummary:
    """Lấy tóm tắt metrics chính.

    Returns:
        MetricsSummary: Key metrics của Outbox system
    """
    # Placeholder implementation
    # Trong thực tế sẽ query từ Prometheus hoặc database

    return MetricsSummary(
        outbox_queue_total=0,
        dlq_total=0,
        events_processed_last_hour=0,
        events_failed_last_hour=0,
        avg_processing_time_ms=0.0,
        active_workers=0,
        health_status="unknown",
        last_updated=datetime.now(UTC).isoformat(),
    )


@router.get("/prometheus-info")
async def get_prometheus_info() -> dict[str, Any]:
    """Thông tin về Prometheus metrics endpoint.

    Returns:
        Dict với thông tin về metrics endpoint
    """
    return {
        "prometheus_endpoint": "/metrics",
        "description": "Use /metrics endpoint for Prometheus scraping",
        "available_metrics": [
            "outbox_event_processed_total",
            "outbox_event_failed_total",
            "outbox_event_retried_total",
            "outbox_dlq_written_total",
            "outbox_processing_seconds",
            "outbox_queue_size",
            "outbox_dlq_size",
            "outbox_worker_active",
            "outbox_lock_contention_total",
            "outbox_health_status",
        ],
        "grafana_dashboard": "TODO: Link to Grafana dashboard",
    }


@router.get("/health-details")
async def get_health_details() -> dict[str, Any]:
    """Chi tiết health status của từng component.

    Returns:
        Dict với health status chi tiết
    """
    return {
        "components": {
            "database": {
                "status": "unknown",
                "last_check": datetime.now(UTC).isoformat(),
                "details": "Not implemented yet",
            },
            "workers": {"status": "unknown", "active_count": 0, "last_heartbeat": None},
            "queue": {"status": "unknown", "size": 0, "oldest_event_age_seconds": None},
            "dlq": {"status": "unknown", "size": 0, "alerts": []},
        },
        "overall_status": "unknown",
        "note": "Full implementation pending",
    }
