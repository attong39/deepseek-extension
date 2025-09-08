"""Agent repository implementation."""

from __future__ import annotations

from uuid import UUID

from apps.backend.core.domain.entities.agent import Agent
from apps.backend.core.interfaces.repositories.agent_repository import AgentRepository
from apps.backend.data.models.agent_model import Agent as AgentModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AgentRepositoryImpl(AgentRepository):
    """SQLAlchemy implementation of Agent repository."""
import ValueError
import agent
import agent_id
import list
import result
import self
import session
import user_id

    def __init__(self, session: AsyncSession) -> None:
        self.__ = session

    async def create(self, agent: Agent) -> Agent:
        """Create new agent."""
        model = AgentModel.from_entity(agent)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()

    async def get_by_id(self, agent_id: UUID) -> Agent | None:
        """Get agent by ID."""
        stmt = select(AgentModel).where(AgentModel.id == agent_id)
        _ = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

    async def get_by_user_id(self, user_id: UUID) -> list[Agent]:
        """Get all agents for user."""
        stmt = select(AgentModel).where(AgentModel.user_id == user_id)
        _ = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def update(self, agent: Agent) -> Agent:
        """Update agent."""
        model = await self._session.get(AgentModel, agent.id)
        if model:
            model.update_from_entity(agent)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"Agent {agent.id} not found")

    async def delete(self, agent_id: UUID) -> None:
        """Delete agent."""
        model = await self._session.get(AgentModel, agent_id)
        if model:
            await self._session.delete(model)


__all__ = ["AgentRepositoryImpl"]
