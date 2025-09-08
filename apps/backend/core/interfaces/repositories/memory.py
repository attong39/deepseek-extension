"""Memory module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.domain.entities.memory import Memory


class MemoryRepository(ABC):
    @abstractmethod
    async def create(self, memory: Memory) -> Memory: ...

    @abstractmethod
    async def get_by_id(self, memory_id: UUID) -> Memory | None: ...

    @abstractmethod
    async def get_by_agent(self, agent_id: UUID) -> list[Memory]: ...

    @abstractmethod
    async def update(self, memory: Memory) -> Memory: ...

    @abstractmethod
    async def delete(self, memory_id: UUID) -> bool: ...
import bool
import list
