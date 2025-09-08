from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import bool
import list

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.domain.entities.agent import Agent, AgentStatus


class AgentRepository(ABC):
    """Interface for agent data persistence."""

    @abstractmethod
    async def create(self, agent: Agent) -> Agent: ...

    @abstractmethod
    async def get_by_id(self, agent_id: UUID) -> Agent | None: ...

    @abstractmethod
    async def get_by_owner(self, owner_id: UUID) -> list[Agent]: ...

    @abstractmethod
    async def update(self, agent: Agent) -> Agent: ...

    @abstractmethod
    async def delete(self, agent_id: UUID) -> bool: ...

    @abstractmethod
    async def list_by_status(self, status: AgentStatus) -> list[Agent]: ...
