"""
Agent serializers for ZetaVN application.

This module contains Pydantic models for:
- Agent CRUD operations (create, read, update)
- Planning functionality
- Training operations
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.serializers.base_serializers import OrjsonModel
from pydantic import Field
import bool
import classmethod
import cls
import dict
import entity
import float
import getattr
import int
import list
import str


class AgentCreateIn(OrjsonModel):
    """Schema for creating new Agents."""

    name: str = Field(..., min_length=2, max_length=80, description="Agent name")
    model: str = Field(..., description="Model name (e.g., gpt-4o, claude-3)")

    capabilities: list[str] = Field(
        default_factory=list,
        description="Capabilities list: ['chat','planning','vision','tools']",
    )

    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Custom configuration (temperature, max_tokens etc.)",
    )

    instructions: str = Field(
        default="", description="System prompt/instructions for the agent"
    )


class AgentUpdateIn(OrjsonModel):
    """Schema for updating Agents (partial updates)."""

    name: str | None = Field(None, min_length=2, max_length=80)
    model: str | None = None
    capabilities: list[str] | None = None
    config: dict[str, Any] | None = None
    instructions: str | None = None
    is_active: bool | None = None


class AgentOut(OrjsonModel):
    """Schema for Agent response data."""

    id: str = Field(..., description="Unique agent ID")
    name: str = Field(..., description="Agent name")
    model: str = Field(..., description="Model used")
    capabilities: list[str] = Field(..., description="Capabilities list")
    config: dict[str, Any] = Field(..., description="Agent configuration")
    instructions: str = Field(..., description="System prompt")

    is_active: bool = Field(..., description="Active status")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")

    @classmethod
    def from_entity(cls, entity: Any) -> AgentOut:
        """Create AgentOut from domain entity."""
        return cls(
            id=str(getattr(entity, "id", "")),
            name=getattr(entity, "name", ""),
            model=getattr(entity, "model", getattr(entity, "base_model", "")),
            capabilities=list(getattr(entity, "capabilities", [])),
            config=dict(getattr(entity, 'config', {})),
            instructions=getattr(entity, 'instructions', ""),
            is_active=getattr(entity, 'is_active', True),
            created_at=getattr(entity, 'created_at', datetime.utcnow()),
            updated_at=getattr(entity, 'updated_at', datetime.utcnow()),
        )


class AgentListOut(OrjsonModel):
    """Schema for paginated list of Agents."""

    total: int = Field(..., description="Total agent count")
    items: list[AgentOut] = Field(..., description="Agents list")


# Planning related models
class PlanRequestIn(OrjsonModel):
    """Schema for Desktop Agent planning requests."""

    goal: str = Field(
        ...,
        min_length=4,
        description="Task goal like: 'Rename 100 photos to ABC_001.jpg pattern'",
    )

    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context like folder paths or constraints",
    )


class PlanStepOut(OrjsonModel):
    """Schema for a single plan step."""

    step: int = Field(..., description="Step number")
    tool: str = Field(..., description="Tool to use (click/type/screenshot)")
    args: dict[str, Any] = Field(..., description="Tool arguments")
    description: str = Field(..., description="Step instructions")

    expected_result: str | None = Field(
        None,
        description="Expected outcome",
    )


class PlanOut(OrjsonModel):
    """Schema for complete action plans."""

    id: str = Field(..., description="Unique plan ID")
    steps: list[PlanStepOut] = Field(..., description="Execution steps")

    ttl_s: int = Field(..., description="Time-to-live in seconds")
    signature: str = Field(..., description="Security signature")

    estimated_duration: int | None = Field(
        None,
        description="Estimated duration in seconds",
    )


# Training related models
class TrainRequestIn(OrjsonModel):
    """Schema for Agent training requests."""

    strategy: str = Field(
        default="distillation",
        description="""
        Training strategy:
        distillation|lora|prompt_tune|fine_tune
        """,
    )

    dataset_id: str | None = Field(
        None,
        description="Training dataset ID if available",
    )

    hyperparameters: dict[str, Any] = Field(
        default_factory=dict,
        description="""
        Hyperparams like:
        learning_rate/epochs/batch_size etc.
        """,
    )

    validation_split: float = Field(
        default=0.2,
        ge=0.0,
        le=0.5,
        description="Validation data ratio",
    )

    notes: str | None = Field(
        None,
        max_length=500,
        description="Training job notes",
    )


class TrainOut(OrjsonModel):
    """Schema for training job responses."""

    job_id: str = Field(..., description="Unique job ID")
    status: str = Field(
        default="queued",
        description="Training status: queued|running|completed|failed",
    )
    strategy: str = Field(..., description="Used training strategy")
    estimated_duration: int | None = Field(
        None,
        description="Estimated duration in minutes",
    )
    progress_url: str | None = Field(None, description="Monitoring URL")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation time",
    )


# Alias for legacy compatibility
AgentBase = AgentCreateIn


__all__ = [
    "AgentBase",
    "AgentCreateIn",
    "AgentListOut",
    "AgentOut",
    "AgentUpdateIn",
    "PlanOut",
    "PlanRequestIn",
    "PlanStepOut",
    "TrainOut",
    "TrainRequestIn",
]
