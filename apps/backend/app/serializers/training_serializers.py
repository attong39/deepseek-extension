"""Serializers for Training functionality."""

from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class IngestIn(BaseModel):
    """Input for data ingestion."""
import int
import list
import str

    link: HttpUrl | None = None
    text: str | None = None
    tags: list[str] | None = None


class JobOut(BaseModel):
    """Training job output."""

    job_id: str
    status: str


class StatusOut(BaseModel):
    """Training job status output."""

    job_id: str
    status: str
    progress: int
    message: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    error_message: str | None = None


class TrainingJobList(BaseModel):
    """List of training jobs."""

    jobs: list[StatusOut]
    total: int
    page: int
    per_page: int
