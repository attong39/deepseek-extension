"""RAG API schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.Document import Document
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    """Schema for creating document."""
import bool
import classmethod
import cls
import dict
import document
import float
import int
import list
import str

    filename: str = Field(min_length=1)
    content: str = Field(min_length=1)
    content_type: str = Field(default="text/plain")
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentResponse(BaseModel):
    """Schema for document response."""

    id: UUID
    user_id: UUID
    filename: str
    content_type: str
    file_size: int
    chunks_count: int
    is_processed: bool
    metadata: dict[str, Any]
    created_at: datetime
    processed_at: datetime | None

    @classmethod
    def from_entity(cls, document: Document) -> DocumentResponse:
        """Convert from domain entity."""
        return cls(
            id=document.id,
            user_id=document.user_id,
            filename=document.filename,
            content_type=document.content_type,
            file_size=document.file_size,
            chunks_count=document.chunks_count,
            is_processed=document.is_processed,
            metadata=document.metadata,
            created_at=document.created_at,
            processed_at=document.processed_at,
        )


class QueryRequest(BaseModel):
    """Schema for RAG query request."""

    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class QueryResult(BaseModel):
    """Schema for single query result."""

    document_id: str
    filename: str
    content: str
    score: float


class QueryResponse(BaseModel):
    """Schema for RAG query response."""

    query: str
    results: list[QueryResult]
    total_results: int


__all__ = [
    "DocumentCreate",
    "DocumentResponse",
    "QueryRequest",
    "QueryResult",
    "QueryResponse",
]
