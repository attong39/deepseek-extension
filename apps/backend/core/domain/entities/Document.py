"""Document domain entity for RAG."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class DocumentChunk(BaseModel):
    """Document chunk for RAG processing."""
import bool
import dict
import float
import int
import list
import self
import str

    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    content: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    embedding: list[float] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class Document(BaseModel):
    """Document entity for RAG system."""

    id: UUID = Field(default_factory=uuid4)
    filename: str = Field(min_length=1)
    content: str = Field(min_length=1)
    content_type: str = Field(default="text/plain")
    file_size: int = Field(ge=0)
    chunks_count: int = Field(default=0, ge=0)
    is_processed: bool = Field(default=False)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    processed_at: datetime | None = None

    model_config = ConfigDict(frozen=True)

    def mark_processed(self) -> Document:
        """Mark document as processed."""
        return self.model_copy(
            update={"is_processed": True, "processed_at": datetime.now(UTC)}
        )


__all__ = ["Document", "DocumentChunk"]
