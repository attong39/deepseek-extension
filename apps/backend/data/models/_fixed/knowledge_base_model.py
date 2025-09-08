"""
Knowledge Base Database Model - Fixed SQLAlchemy 2.x Version.

Represents knowledge bases and documents for AI agents.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from apps.backend.data.models.base_model import BaseModel, SoftDeleteMixin, TaggedMixin
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
import TypeError
import bool
import dict
import exclude_fields
import float
import int
import len
import list
import max_length
import self
import str
import super
import value
import vector


class KnowledgeBase(BaseModel, SoftDeleteMixin, TaggedMixin):
    """Knowledge base model for storing structured knowledge."""

    # Basic Information
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, doc="Knowledge base name"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="Knowledge base description"
    )

    # Status tracking - using proper mapped_column for SQLAlchemy 2.x
    _processing_status: Mapped[str] = mapped_column(
        "processing_status", String(50), default="pending", nullable=False
    )
    _embedding_status: Mapped[str] = mapped_column(
        "embedding_status", String(50), default="pending", nullable=False
    )

    # Timestamps
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    embedded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Metrics
    _word_count: Mapped[int] = mapped_column(
        "word_count", Integer, default=0, nullable=False
    )

    @hybrid_property
    def processing_status(self) -> str:
        """Get processing status."""
        return self._processing_status

    @processing_status.setter
    def processing_status(self, value: str) -> None:
        """Set processing status."""
        self._processing_status = value

    @hybrid_property
    def embedding_status(self) -> str:
        """Get embedding status."""
        return self._embedding_status

    @embedding_status.setter
    def embedding_status(self, value: str) -> None:
        """Set embedding status."""
        self._embedding_status = value

    @hybrid_property
    def word_count(self) -> int:
        """Get word count."""
        return self._word_count

    @word_count.setter
    def word_count(self, value: int) -> None:
        """Set word count."""
        self._word_count = value

    def mark_processing_started(self) -> None:
        """Mark processing as started."""
        self._processing_status = "processing"

    def mark_processing_completed(self) -> None:
        """Mark processing as completed."""
        self._processing_status = "completed"
        self.processed_at = datetime.now(UTC)

    def mark_processing_failed(self) -> None:
        """Mark processing as failed."""
        self._processing_status = "failed"

    def mark_embedding_started(self) -> None:
        """Mark embedding as started."""
        self._embedding_status = "processing"

    def mark_embedding_completed(self) -> None:
        """Mark embedding as completed."""
        self._embedding_status = "completed"
        self.embedded_at = datetime.now(UTC)

    def mark_embedding_failed(self) -> None:
        """Mark embedding as failed."""
        self._embedding_status = "failed"

    def is_ready_for_embedding(self) -> bool:
        """Check if document is ready for embedding."""
        return self._processing_status == "completed" and self._embedding_status in (
            "pending",
            "failed",
        )

    def to_dict(self, exclude_fields: list[str] | None = None) -> dict[str, Any]:
        """Convert to dictionary - compatible with BaseModel signature."""
        base_dict = super().to_dict(exclude_fields or [])
        base_dict.update(
            {
                "processing_status": self._processing_status,
                "embedding_status": self._embedding_status,
                "word_count": self._word_count,
            }
        )
        return base_dict


class Document(BaseModel, SoftDeleteMixin):
    """Document model for knowledge base content."""

    # Basic Information
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    _content: Mapped[str] = mapped_column("content", Text, nullable=False)

    # Metadata
    content_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default="text/plain"
    )
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Processing Status
    _processing_status: Mapped[str] = mapped_column(
        "processing_status", String(50), default="pending", nullable=False
    )
    _embedding_status: Mapped[str] = mapped_column(
        "embedding_status", String(50), default="pending", nullable=False
    )

    # Embeddings
    _embedding_vector: Mapped[str | None] = mapped_column(
        "embedding_vector", Text, nullable=True
    )
    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    embedding_created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Metrics
    _word_count: Mapped[int] = mapped_column(
        "word_count", Integer, default=0, nullable=False
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    embedded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    @hybrid_property
    def content(self) -> str:
        """Get content."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        """Set content and update word count."""
        self._content = value
        if value:
            words = value.split()
            self._word_count = len(words)

    @hybrid_property
    def processing_status(self) -> str:
        """Get processing status."""
        return self._processing_status

    @processing_status.setter
    def processing_status(self, value: str) -> None:
        """Set processing status."""
        self._processing_status = value

    @hybrid_property
    def embedding_status(self) -> str:
        """Get embedding status."""
        return self._embedding_status

    @embedding_status.setter
    def embedding_status(self, value: str) -> None:
        """Set embedding status."""
        self._embedding_status = value

    @hybrid_property
    def word_count(self) -> int:
        """Get word count."""
        return self._word_count

    @hybrid_property
    def embedding_vector(self) -> list[float] | None:
        """Get embedding vector."""
        if not self._embedding_vector:
            return None
        try:
            return json.loads(self._embedding_vector)
        except (json.JSONDecodeError, TypeError):
            return None

    @embedding_vector.setter
    def embedding_vector(self, vector: list[float] | None) -> None:
        """Set embedding vector."""
        if vector is None:
            self._embedding_vector = None
        else:
            self._embedding_vector = json.dumps(vector)
            self.embedding_created_at = datetime.now(UTC)

    def mark_processing_started(self) -> None:
        """Mark processing as started."""
        self._processing_status = "processing"

    def mark_processing_completed(self) -> None:
        """Mark processing as completed."""
        self._processing_status = "completed"
        self.processed_at = datetime.now(UTC)

    def mark_processing_failed(self) -> None:
        """Mark processing as failed."""
        self._processing_status = "failed"

    def mark_embedding_started(self) -> None:
        """Mark embedding as started."""
        self._embedding_status = "processing"

    def mark_embedding_completed(self) -> None:
        """Mark embedding as completed."""
        self._embedding_status = "completed"
        self.embedded_at = datetime.now(UTC)

    def mark_embedding_failed(self) -> None:
        """Mark embedding as failed."""
        self._embedding_status = "failed"

    def update_word_count(self) -> None:
        """Update word count from content."""
        if self._content:
            words = self._content.split()
            self._word_count = len(words)

    def get_preview(self, max_length: int = 200) -> str:
        """Get content preview."""
        if not self._content:
            return ""
        if len(self._content) <= max_length:
            return self._content
        return self._content[:max_length] + "..."

    def to_dict(self, exclude_fields: list[str] | None = None) -> dict[str, Any]:
        """Convert to dictionary - compatible with BaseModel signature."""
        base_dict = super().to_dict(exclude_fields or [])
        base_dict.update(
            {
                "content": self._content,
                "processing_status": self._processing_status,
                "embedding_status": self._embedding_status,
                "word_count": self._word_count,
                "embedding_vector": self.embedding_vector,
            }
        )
        return base_dict


__all__ = ["KnowledgeBase", "Document"]
