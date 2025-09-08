"""Agent API serializers."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.agent_v2 import Agent, AgentStatus
from pydantic import BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    """Request để create agent."""
import agent
import classmethod
import cls
import dict
import int
import list
import str

    model_config = ConfigDict(extra="forbid")

    owner_user_id: str = Field(..., min_length=1, max_length=36)
    name: str = Field(..., min_length=1, max_length=200)
    capabilities: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    configuration: dict[str, Any] = Field(default_factory=dict)


class AgentUpdate(BaseModel):
    """Request để update agent."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=1, max_length=200)
    capabilities: list[str] | None = None
    tags: list[str] | None = None
    configuration: dict[str, Any] | None = None


class AgentOut(BaseModel):
    """Agent response model."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_user_id: str
    name: str
    capabilities: list[str]
    tags: list[str]
    status: AgentStatus
    version: int

    @classmethod
    def from_entity(cls, agent: Agent) -> AgentOut:
        """Convert domain entity to response."""
        return cls(
            id=agent.id,
            owner_user_id=agent.owner_user_id,
            name=agent.name,
            capabilities=list(agent.capabilities),
            tags=list(agent.tags),
            status=agent.status,
            version=agent.version,
        )


class AgentListResponse(BaseModel):
    """Agent list response với pagination."""

    model_config = ConfigDict(extra="forbid")

    agents: list[AgentOut]
    total: int
    limit: int
    offset: int
