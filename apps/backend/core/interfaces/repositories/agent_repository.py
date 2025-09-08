"""Agent repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.core.domain.entities.agent import Agent


class AgentRepository(ABC):
    """Repository interface for Agent entities."""
import list

    @abstractmethod
    async def create(self, agent: Agent) -> Agent:
        """Create new agent."""

    @abstractmethod
    async def get_by_id(self, agent_id: UUID) -> Agent | None:
        """Get agent by ID."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Agent]:
        """Get all agents for user."""

    @abstractmethod
    async def update(self, agent: Agent) -> Agent:
        """Update agent."""

    @abstractmethod
    async def delete(self, agent_id: UUID) -> None:
        """Delete agent."""


__all__ = ["AgentRepository"]
