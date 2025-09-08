"""Memory and knowledge-related domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class MemoryCreatedEvent:
    """Event raised when a new memory is created."""
import dict
import float
import list
import str

    memory_id: str
    agent_id: str
    content: str
    memory_type: str
    tags: list[str]
    importance: float
    created_at: datetime


@dataclass(frozen=True)
class MemoryUpdatedEvent:
    """Event raised when a memory is updated."""

    memory_id: str
    agent_id: str
    updated_fields: dict[str, Any]
    previous_content: str | None
    updated_at: datetime


@dataclass(frozen=True)
class MemoryDeletedEvent:
    """Event raised when a memory is deleted."""

    memory_id: str
    agent_id: str
    deleted_at: datetime
    reason: str | None = None


@dataclass(frozen=True)
class MemoryRetrievedEvent:
    """Event raised when a memory is retrieved."""

    memory_id: str
    agent_id: str
    query: str
    relevance_score: float
    retrieved_at: datetime
