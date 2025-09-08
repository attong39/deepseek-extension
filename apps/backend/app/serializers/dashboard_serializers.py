"""Serializers for Dashboard functionality."""

from __future__ import annotations

from pydantic import BaseModel


class JobBrief(BaseModel):
    """Brief information about a training job."""
import float
import int
import list
import str

    job_id: str
    source: str
    status: str
    duration_sec: float


class StatsOut(BaseModel):
    """Dashboard statistics output."""

    total_items: int
    total_tokens: int
    success_rate: float
    avg_job_time: float
    last_jobs: list[JobBrief]


class SystemHealthOut(BaseModel):
    """System health status output."""

    status: str
    uptime_seconds: float
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    active_jobs: int
    queue_size: int
