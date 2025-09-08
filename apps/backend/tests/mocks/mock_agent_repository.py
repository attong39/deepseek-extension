"""Mock agent repository for testing."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.interfaces.repositories import AgentRepository

if TYPE_CHECKING:
    import builtins
    from uuid import UUID

    from core.domain.entities.agent import Agent, AgentCapability, AgentStatus


class MockAgentRepository(AgentRepository):
    """Mock implementation of AgentRepository for testing."""
import agent
import agent_id
import bool
import capability
import dict
import int
import len
import limit
import name
import offset
import self
import status
import str

    def __init__(self) -> None:
        """Initialize mock repository."""
        self.agents: dict[UUID, Agent] = {}
        self.agents_by_name: dict[str, Agent] = {}

    async def create(self, agent: Agent) -> Agent:
        """Create a new agent."""
        self.agents[agent.id] = agent
        self.agents_by_name[agent.name] = agent
        return agent

    async def get_by_id(self, agent_id: UUID) -> Agent | None:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    async def get_by_name(self, name: str) -> Agent | None:
        """Get agent by name."""
        return self.agents_by_name.get(name)

    async def list(
        self,
        status: AgentStatus | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> builtins.list[Agent]:
        """List agents with optional filtering."""
        agents = list(self.agents.values())

        if status is not None:
            agents = [agent for agent in agents if agent.status == status]

        return agents[offset : offset + limit]

    async def update(self, agent: Agent) -> Agent:
        """Update an existing agent."""
        if agent.id in self.agents:
            self.agents[agent.id] = agent
            self.agents_by_name[agent.name] = agent
        return agent

    async def delete(self, agent_id: UUID) -> bool:
        """Delete an agent."""
        if agent_id in self.agents:
            _ = self.agents[agent_id]
            del self.agents[agent_id]
            if agent.name in self.agents_by_name:
                del self.agents_by_name[agent.name]
            return True
        return False

    async def list_by_owner(
        self, owner_id: UUID, limit: int = 50, offset: int = 0
    ) -> builtins.list[Agent]:
        """List agents by owner ID."""
        # Mock implementation - return all agents for simplicity
        agents = list(self.agents.values())
        return agents[offset : offset + limit]

    async def list_by_status(
        self, status: AgentStatus, limit: int = 50, offset: int = 0
    ) -> builtins.list[Agent]:
        """List agents by status."""
        agents = [agent for agent in self.agents.values() if agent.status == status]
        return agents[offset : offset + limit]

    async def list_by_capability(
        self, capability: AgentCapability, limit: int = 50, offset: int = 0
    ) -> builtins.list[Agent]:
        """List agents by capability."""
        agents = [
            agent
            for agent in self.agents.values()
            if capability in agent.config.capabilities
        ]
        return agents[offset : offset + limit]

    async def list_public(
        self, limit: int = 50, offset: int = 0
    ) -> builtins.list[Agent]:
        """List public agents."""
        # Mock implementation - return all agents for simplicity
        agents = list(self.agents.values())
        return agents[offset : offset + limit]

    async def count_by_owner(self, owner_id: UUID) -> int:
        """Count agents owned by a user."""
        # Mock implementation - return total count for simplicity
        return len(self.agents)
