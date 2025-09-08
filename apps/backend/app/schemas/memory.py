"""Memory API schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.memory import Memory
from pydantic import BaseModel, Field


class MemoryCreate(BaseModel):
    """Schema for creating memory."""
import classmethod
import cls
import dict
import float
import int
import list
import memory
import str

    content: str = Field(min_length=1)
    content_type: str = Field(default="text")
    tags: list[str] = Field(default_factory=list)
    importance: float = Field(default=1.0, ge=0.0, le=10.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemorySearch(BaseModel):
    """Schema for searching memories."""

    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=100)


class MemoryResponse(BaseModel):
    """Schema for memory response."""

    id: UUID
    user_id: UUID
    content: str
    content_type: str
    tags: list[str]
    importance: float
    metadata: dict[str, Any]
    created_at: datetime
    accessed_at: datetime
    access_count: int

    @classmethod
    def from_entity(cls, memory: Memory) -> MemoryResponse:
        """Convert from domain entity."""
        return cls(
            id=memory.id,
            user_id=memory.user_id,
            content=memory.content,
            content_type=memory.content_type,
            tags=memory.tags,
            importance=memory.importance,
            metadata=memory.metadata,
            created_at=memory.created_at,
            accessed_at=memory.accessed_at,
            access_count=memory.access_count,
        )


__all__ = ["MemoryCreate", "MemorySearch", "MemoryResponse"]
