"""Training-related SQLAlchemy models (SQLAlchemy 2.0 style).

This module defines training job and dataset item entities using the
canonical DeclarativeBase located at ``zeta_vn.data.models.base.Base``.

Notes:
- Keep JSON columns portable by using SQLAlchemy's generic JSON type at the
  ORM layer; migrations will use PostgreSQL JSONB where available.
- Timestamps use the project's Base timestamps (utc-naive) for consistency
  with existing tables. Per-database server defaults are applied via migrations.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from apps.backend.data.models.base import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON
import dict
import getattr
import int
import kwargs
import list
import self
import str
import super


class TrainingJob(Base):
    """Represents a model training job.

    Attributes:
        id: UUID string primary key (inherited from Base).
        name: Human-friendly job name.
        status: Lifecycle status (pending, running, completed, failed, canceled).
        model_name: Target model/recipe identifier.
        params: Training parameters (hyperparameters, options).
        metrics: Result metrics (loss, accuracy, etc.).
        error_message: Optional error details if failed.
        started_at: When the job started (if started).
        completed_at: When the job completed (if finished).
        items: Relationship to dataset items processed by this job.
    """

    __tablename__: str = "training_jobs"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, default="pending"
    )
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)

    params: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    items: Mapped[list[DatasetItem]] = relationship(
        back_populates="training_job",
        cascade="all, delete-orphan",
    )

    # Avoid duplicate Table errors if this module is imported via multiple aliases
    __table_args__ = ({"extend_existing": True},)

    # Ensure Python-side defaults are available immediately after instantiation
    def __init__(
        self, **kwargs: Any
    ) -> None:  # pragma: no cover - simple field defaults
        super().__init__(**kwargs)
        if getattr(self, "params", None) is None:
            self.params = {}
        if getattr(self, "metrics", None) is None:
            self.metrics = {}


class DatasetItem(Base):
    """Represents an individual dataset item used for training.

    Attributes:
        id: UUID string primary key (inherited from Base).
        training_job_id: FK to the training job (optional when item exists before job).
        dataset_name: Logical dataset grouping/name.
        external_id: Optional upstream identifier for traceability.
        content: Raw textual content (or serialized representation).
        metadata: Arbitrary metadata (source, labels, etc.).
        status: Ingestion/validation status.
        order_index: Optional ordering hint for deterministic batching.
        training_job: Relationship back to the job.
    """

    __tablename__: str = "dataset_items"

    training_job_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("training_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    dataset_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    external_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )

    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 'metadata' is reserved in SQLAlchemy Declarative; map using a different attribute name
    meta: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSON, nullable=False, default=dict
    )

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="ready", index=True
    )
    order_index: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    training_job: Mapped[TrainingJob | None] = relationship(
        back_populates="items",
        primaryjoin="DatasetItem.training_job_id==TrainingJob.id",
    )

    # Avoid duplicate Table errors if this module is imported via multiple aliases
    __table_args__ = ({"extend_existing": True},)
