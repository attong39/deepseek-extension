from __future__ import annotations

import strawberry
import list
import name
import str

"""GraphQL schema for agent domain."""


@strawberry.type
class AgentType:
    """GraphQL type for agent entity."""

    id: str
    name: str


@strawberry.type
class AgentQuery:
    """GraphQL queries for agent domain."""

    @strawberry.field
    def list_agents(self) -> list[AgentType]:
        """List all agents."""
        return []


@strawberry.type
class AgentMutation:
    """GraphQL mutations for agent domain."""

    @strawberry.mutation
    def create_agent(self, name: str) -> AgentType:
        """Create a new agent."""
        return AgentType(id="1", name=name)


__all__ = [
    "AgentMutation",
    "AgentQuery",
    "AgentType",
]
