"""
Knowledge Base Database Model - SQLAlchemy 2.x Fixed Version.

Represents knowledge bases and documents for AI agents with proper type safety.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from apps.backend.data.models.base_model import BaseModel
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
import TypeError
import all
import bool
import float
import int
import isinstance
import len
import list
import max_length
import self
import str
import value
import vector
import x


class KnowledgeBase(BaseModel):
    """Knowledge base model for storing structured knowledge."""

    # Basic Information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Status tracking
    processing_status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )
    embedding_status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )

    # Timestamps
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    embedded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Metrics
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def mark_processing_started(self) -> None:
        """Mark processing as started."""
        self.processing_status = "processing"

    def mark_processing_completed(self) -> None:
        """Mark processing as completed."""
        self.processing_status = "completed"
        self.processed_at = datetime.now(UTC)

    def mark_processing_failed(self) -> None:
        """Mark processing as failed."""
        self.processing_status = "failed"

    def mark_embedding_started(self) -> None:
        """Mark embedding as started."""
        self.embedding_status = "processing"

    def mark_embedding_completed(self) -> None:
        """Mark embedding as completed."""
        self.embedding_status = "completed"
        self.embedded_at = datetime.now(UTC)

    def mark_embedding_failed(self) -> None:
        """Mark embedding as failed."""
        self.embedding_status = "failed"

    def is_ready_for_embedding(self) -> bool:
        """Check if document is ready for embedding."""
        return self.processing_status == "completed" and self.embedding_status in (
            "pending",
            "failed",
        )


class Document(BaseModel):
    """Document model for knowledge base content."""

    # Basic Information
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Metadata
    content_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default="text/plain"
    )
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Processing Status
    processing_status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )
    embedding_status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )

    # Embeddings
    embedding_vector_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    embedding_created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Metrics
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    embedded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def set_content(self, value: str) -> None:
        """Set content and update word count."""
        self.content = value
        if value:
            words = value.split()
            self.word_count = len(words)

    def get_embedding_vector(self) -> list[float] | None:
        """Get embedding vector from JSON."""
        if not self.embedding_vector_json:
            return None
        try:
            parsed = json.loads(self.embedding_vector_json)
            if isinstance(parsed, list) and all(
                isinstance(x, int | float) for x in parsed
            ):
                return [float(x) for x in parsed]
            return None
        except (json.JSONDecodeError, TypeError):
            return None

    def set_embedding_vector(self, vector: list[float] | None) -> None:
        """Set embedding vector as JSON."""
        if vector is None:
            self.embedding_vector_json = None
        else:
            self.embedding_vector_json = json.dumps(vector)
            self.embedding_created_at = datetime.now(UTC)

    def mark_processing_started(self) -> None:
        """Mark processing as started."""
        self.processing_status = "processing"

    def mark_processing_completed(self) -> None:
        """Mark processing as completed."""
        self.processing_status = "completed"
        self.processed_at = datetime.now(UTC)

    def mark_processing_failed(self) -> None:
        """Mark processing as failed."""
        self.processing_status = "failed"

    def mark_embedding_started(self) -> None:
        """Mark embedding as started."""
        self.embedding_status = "processing"

    def mark_embedding_completed(self) -> None:
        """Mark embedding as completed."""
        self.embedding_status = "completed"
        self.embedded_at = datetime.now(UTC)

    def mark_embedding_failed(self) -> None:
        """Mark embedding as failed."""
        self.embedding_status = "failed"

    def update_word_count(self) -> None:
        """Update word count from content."""
        if self.content:
            words = self.content.split()
            self.word_count = len(words)

    def get_preview(self, max_length: int = 200) -> str:
        """Get content preview."""
        if not self.content:
            return ""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


__all__ = ["KnowledgeBase", "Document"]
