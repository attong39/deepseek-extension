from __future__ import annotations

from datetime import datetime
from enum import Enum

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable, Versioned
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field, model_validator
import ValueError
import float
import message
import new_progress
import self
import str


class TrainingJobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class TrainingJob(DomainModel, Versioned, Traceable):
    """
    Job huấn luyện (fine-tune/embedding/retrain).
    Invariants:
      - completed_at >= started_at
      - progress ∈ [0,1] và không giảm khi advance_progress()
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Job ID")
    agent_id: str = Field(..., description="Agent được train")
    dataset_id: str | None = None

    status: TrainingJobStatus = TrainingJobStatus.QUEUED
    progress: float = Field(default=0.0, ge=0.0, le=1.0)

    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None

    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    @model_validator(mode="after")
    def _time_order(self) -> TrainingJob:
        if (
            self.completed_at
            and self.started_at
            and self.completed_at < self.started_at
        ):
            raise ValueError("completed_at không thể trước started_at")
        return self

    # Convenience APIs (giúp Copilot gợi ý đúng luồng)
    def mark_started(self) -> TrainingJob:
        return self.model_copy(
            update={
                "status": TrainingJobStatus.RUNNING,
                "started_at": self.started_at or now_utc(),
                "updated_at": now_utc(),
                "version": self.version + 1,
            }
        )

    def advance_progress(self, new_progress: float) -> TrainingJob:
        if new_progress < self.progress:
            raise ValueError("progress không được giảm")
        if not (0.0 <= new_progress <= 1.0):
            raise ValueError("progress phải trong [0,1]")
        return self.model_copy(
            update={
                "progress": new_progress,
                "updated_at": now_utc(),
                "version": self.version + 1,
            }
        )

    def mark_succeeded(self) -> TrainingJob:
        return self.model_copy(
            update={
                "status": TrainingJobStatus.SUCCEEDED,
                "progress": 1.0,
                "completed_at": now_utc(),
                "updated_at": now_utc(),
                "version": self.version + 1,
                "error": None,
            }
        )

    def mark_failed(self, message: str) -> TrainingJob:
        return self.model_copy(
            update={
                "status": TrainingJobStatus.FAILED,
                "completed_at": now_utc(),
                "updated_at": now_utc(),
                "version": self.version + 1,
                "error": message.strip()[:5000],
            }
        )

    def cancel(self) -> TrainingJob:
        return self.model_copy(
            update={
                "status": TrainingJobStatus.CANCELED,
                "completed_at": now_utc(),
                "updated_at": now_utc(),
                "version": self.version + 1,
            }
        )
