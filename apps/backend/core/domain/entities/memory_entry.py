"""
Memory Entry Entity - Standard Domain Model
===========================================

Đại diện cho một entry cụ thể trong memory system
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from app._base_model import DomainModel
from pydantic import Field, field_validator
import ValueError
import classmethod
import dict
import isinstance
import list
import new_content
import new_tags
import self
import set
import str
import tag
import v


class MemoryEntryType(str, Enum):
    """Loại memory entry"""

    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    WORKING = "working"


class MemoryEntryStatus(str, Enum):
    """Trạng thái memory entry"""

    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class MemoryEntry(DomainModel):
    """
    Memory Entry Entity

    Represents a specific memory entry with content, metadata and relationships
    """

    # === Core Identity ===
    id: UUID = Field(default_factory=uuid4, description="Unique memory entry ID")
    memory_id: UUID = Field(description="Parent memory ID")

    # === Core Content ===
    content: str = Field(
        min_length=1, max_length=10000, description="Memory entry content"
    )
    entry_type: MemoryEntryType = Field(
        default=MemoryEntryType.EPISODIC, description="Type of memory entry"
    )

    # === Status & Lifecycle ===
    status: MemoryEntryStatus = Field(
        default=MemoryEntryStatus.ACTIVE, description="Entry status"
    )

    # === Metadata ===
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    tags: list[str] = Field(default_factory=list, description="Search tags")

    # === Timestamps ===
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate memory entry content"""
        if not v or not v.strip():
            raise ValueError("Memory entry content cannot be empty")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Validate and normalize tags"""
        if not isinstance(v, list):
            raise ValueError("Tags must be a list")
        return [tag.lower().strip() for tag in v if tag and tag.strip()]

    def update_content(self, new_content: str) -> MemoryEntry:
        """Update memory entry content"""
        return self.model_copy(
            update={"content": new_content, "updated_at": datetime.now(UTC)}
        )

    def add_tags(self, new_tags: list[str]) -> MemoryEntry:
        """Add new tags to memory entry"""
        current_tags = set(self.tags)
        for tag in new_tags:
            if tag and tag.strip():
                current_tags.add(tag.lower().strip())

        return self.model_copy(
            update={"tags": list(current_tags), "updated_at": datetime.now(UTC)}
        )

    def archive(self) -> MemoryEntry:
        """Archive memory entry"""
        return self.model_copy(
            update={
                "status": MemoryEntryStatus.ARCHIVED,
                "updated_at": datetime.now(UTC),
            }
        )

    def delete(self) -> MemoryEntry:
        """Soft delete memory entry"""
        return self.model_copy(
            update={
                "status": MemoryEntryStatus.DELETED,
                "updated_at": datetime.now(UTC),
            }
        )
