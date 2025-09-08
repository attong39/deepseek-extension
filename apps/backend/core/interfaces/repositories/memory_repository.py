"""Memory repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.core.domain.entities.memory import Memory


class MemoryRepository(ABC):
    """Repository interface for Memory entities."""
import int
import list
import str

    @abstractmethod
    async def create(self, memory: Memory) -> Memory:
        """Create new memory."""

    @abstractmethod
    async def get_by_id(self, memory_id: UUID) -> Memory | None:
        """Get memory by ID."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Memory]:
        """Get all memories for user."""

    @abstractmethod
    async def search_by_content(
        self, user_id: UUID, query: str, limit: int = 10
    ) -> list[Memory]:
        """Search memories by content."""

    @abstractmethod
    async def update(self, memory: Memory) -> Memory:
        """Update memory."""

    @abstractmethod
    async def delete(self, memory_id: UUID) -> None:
        """Delete memory."""


__all__ = ["MemoryRepository"]
