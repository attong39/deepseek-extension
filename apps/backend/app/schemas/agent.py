"""Agent API schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.agent import Agent
from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    """Schema for creating agent."""
import agent
import bool
import classmethod
import cls
import dict
import float
import int
import str

    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    system_prompt: str = Field(default="", max_length=2000)
    model_name: str = Field(default="gpt-3.5-turbo")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1)
    capabilities: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentUpdate(BaseModel):
    """Schema for updating agent."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    system_prompt: str | None = Field(None, max_length=2000)
    model_name: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, ge=1)
    capabilities: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None


class AgentResponse(BaseModel):
    """Schema for agent response."""

    id: UUID
    user_id: UUID
    name: str
    description: str
    system_prompt: str
    model_name: str
    temperature: float
    max_tokens: int | None
    is_active: bool
    capabilities: dict[str, Any]
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, agent: Agent) -> AgentResponse:
        """Convert from domain entity."""
        return cls(
            id=agent.id,
            user_id=agent.user_id,
            name=agent.name,
            description=agent.description,
            system_prompt=agent.system_prompt,
            model_name=agent.model_name,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
            is_active=agent.is_active,
            capabilities=agent.capabilities,
            metadata=agent.metadata,
            created_at=agent.created_at,
            updated_at=agent.updated_at,
        )


__all__ = ["AgentCreate", "AgentUpdate", "AgentResponse"]
