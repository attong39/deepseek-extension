"""Plan serializers for API contracts.

Defines DTOs for plan creation, updates, and responses including
plan steps and execution status.
"""

from __future__ import annotations

from typing import Any

from app.serializers.common import BaseSerializer
from apps.backend.core.domain.entities.plan import Plan, PlanPriority, PlanStatus
from pydantic import BaseModel, Field, field_validator
import ValueError
import bool
import classmethod
import cls
import data
import dict
import entity
import float
import getattr
import goal
import int
import len
import list
import self
import step
import str
import tag
import v


class PlanStepIn(BaseModel):
    """Plan step input DTO."""

    name: str = Field(..., min_length=1, max_length=200, description="Step name")
    description: str | None = Field(
        None, max_length=1000, description="Step description"
    )
    action: str = Field(..., min_length=1, max_length=100, description="Action type")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Step parameters"
    )
    dependencies: list[str] = Field(
        default_factory=list, description="Dependent step names"
    )
    estimated_duration: int | None = Field(
        None, ge=0, description="Estimated duration in seconds"
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate step name."""
        if not v.strip():
            raise ValueError("Step name cannot be empty")
        return v.strip()

    def to_entity_dict(self) -> dict[str, Any]:
        """Convert to dictionary for entity creation."""
        return {
            "name": self.name,
            "description": self.description,
            "action": self.action,
            "parameters": self.parameters,
            "dependencies": self.dependencies,
            "estimated_duration": self.estimated_duration,
        }


class PlanCreate(BaseModel):
    """Plan creation request DTO."""

    name: str = Field(..., min_length=1, max_length=200, description="Plan name")
    description: str | None = Field(
        None, max_length=1000, description="Plan description"
    )
    # pydantic v2 prefers validators for length checks; keep Field simple here
    goals: list[str] = Field(..., description="Plan objectives")
    steps: list[PlanStepIn] = Field(..., description="Plan execution steps")
    tags: list[str] = Field(
        default_factory=list, description="Plan tags for categorization"
    )
    priority: int = Field(
        default=5, ge=1, le=10, description="Plan priority (1=highest, 10=lowest)"
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate plan name."""
        if not v.strip():
            raise ValueError("Plan name cannot be empty")
        return v.strip()

    @field_validator("goals")
    def validate_goals(cls, v: list[str]) -> list[str]:
        """Validate plan goals."""
        goals = [goal.strip() for goal in v if goal.strip()]
        if not goals:
            raise ValueError("At least one goal is required")
        return goals

    @field_validator("tags")
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Validate and normalize tags."""
        return [tag.strip().lower() for tag in v if tag.strip()]

    def to_entity_dict(self) -> dict[str, Any]:
        """Convert to dictionary for entity creation."""
        return {
            "name": self.name,
            "description": self.description,
            "goals": self.goals,
            "steps": [step.to_entity_dict() for step in self.steps],
            "tags": self.tags,
            "priority": self.priority,
            "status": PlanStatus.DRAFT,  # Default status
        }


class PlanUpdate(BaseModel):
    """Plan update request DTO."""

    name: str | None = Field(
        None, min_length=1, max_length=200, description="Plan name"
    )
    description: str | None = Field(
        None, max_length=1000, description="Plan description"
    )
    goals: list[str] | None = Field(None, description="Plan objectives")
    tags: list[str] | None = Field(None, description="Plan tags")
    priority: int | None = Field(None, ge=1, le=10, description="Plan priority")
    status: PlanStatus | None = Field(None, description="Plan status")

    @field_validator("name")
    def validate_name(cls, v: str | None) -> str | None:
        """Validate plan name if provided."""
        if v is not None and not v.strip():
            raise ValueError("Plan name cannot be empty")
        return v.strip() if v else None

    @field_validator("goals")
    def validate_goals(cls, v: list[str] | None) -> list[str] | None:
        """Validate plan goals if provided."""
        if v is None:
            return None
        goals = [goal.strip() for goal in v if goal.strip()]
        if not goals:
            raise ValueError("At least one goal is required")
        return goals

    @field_validator("tags")
    def validate_tags(cls, v: list[str] | None) -> list[str] | None:
        """Validate and normalize tags if provided."""
        if v is None:
            return None
        return [tag.strip().lower() for tag in v if tag.strip()]

    def to_update_dict(self) -> dict[str, Any]:
        """Convert to dictionary for entity updates (excluding None values)."""
        data: dict[str, Any] = {}

        if self.name is not None:
            data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        if self.goals is not None:
            data["goals"] = self.goals
        if self.tags is not None:
            data["tags"] = self.tags
        if self.priority is not None:
            data["priority"] = self.priority
        if self.status is not None:
            data["status"] = self.status

        return data


class PlanStepOut(BaseModel):
    """Plan step output DTO."""

    name: str = Field(..., description="Step name")
    description: str | None = Field(None, description="Step description")
    action: str = Field(..., description="Action type")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Step parameters"
    )
    dependencies: list[str] = Field(
        default_factory=list, description="Dependent step names"
    )
    estimated_duration: int | None = Field(
        None, description="Estimated duration in seconds"
    )
    actual_duration: int | None = Field(None, description="Actual execution duration")
    status: str = Field(default="pending", description="Step execution status")
    error_message: str | None = Field(None, description="Error message if step failed")
    result: dict[str, Any] | None = Field(None, description="Step execution result")


class PlanOut(BaseSerializer[Plan]):
    """Plan response DTO."""

    id: str = Field(..., description="Plan unique identifier")
    name: str = Field(..., description="Plan name")
    description: str | None = Field(None, description="Plan description")
    goals: list[str] = Field(..., description="Plan objectives")
    status: PlanStatus = Field(..., description="Plan execution status")
    owner_id: str = Field(..., description="Plan owner user ID")
    steps: list[PlanStepOut] = Field(default_factory=list, description="Plan steps")
    tags: list[str] = Field(default_factory=list, description="Plan tags")
    # Domain uses PlanPriority enum; keep typed to domain type
    priority: PlanPriority = Field(..., description="Plan priority")
    # Timestamps present on entity
    created_at: str | None = Field(None, description="Creation timestamp")
    updated_at: str | None = Field(None, description="Last update timestamp")

    # Execution metadata
    started_at: str | None = Field(None, description="Execution start timestamp")
    completed_at: str | None = Field(None, description="Execution completion timestamp")
    progress_percent: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Execution progress"
    )

    @classmethod
    def from_entity(cls, entity: Plan) -> PlanOut:
        """Convert Plan entity to output DTO."""

        def _map_step(step: Any) -> PlanStepOut:
            status_val = "pending"
            s = getattr(step, "status", None)
            if s is not None:
                # StepStatus enum -> use its value
                status_val = getattr(s, "value", str(s))

            return PlanStepOut(
                # Map domain PlanStepVO fields to serializer fields
                name=getattr(step, "action", ""),
                description=getattr(step, "description", None),
                action=getattr(step, "action", ""),
                parameters=getattr(step, "parameters", {}) or {},
                dependencies=getattr(step, "dependencies", []) or [],
                estimated_duration=(
                    getattr(step, "estimated_duration", None)
                    or getattr(step, "timeout_seconds", None)
                ),
                actual_duration=getattr(step, "actual_duration", None),
                status=status_val,
                error_message=getattr(step, "error_message", None),
                result=getattr(step, "result", None),
            )

        steps_out = [_map_step(s) for s in (entity.steps or [])]

        started_at_val = getattr(entity, "started_at", None)
        started_at_str: str | None = None
        if started_at_val is not None:
            started_at_str = started_at_val.isoformat()

        completed_at_val = getattr(entity, "completed_at", None)
        completed_at_str: str | None = None
        if completed_at_val is not None:
            completed_at_str = completed_at_val.isoformat()

        # Ensure required string fields are typed correctly for Pydantic model
        name_val = getattr(entity, "title", None) or getattr(entity, "name", "")
        name_str = str(name_val) if name_val is not None else ""
        owner_id_val = getattr(entity, "user_id", None) or getattr(
            entity, "owner_id", ""
        )
        owner_id_str = str(owner_id_val) if owner_id_val is not None else ""

        return cls(
            id=entity.id,
            name=name_str,
            description=entity.description,
            goals=getattr(entity, "goals", []) or [],
            status=entity.status,
            owner_id=owner_id_str,
            steps=steps_out,
            tags=getattr(entity, "tags", []) or [],
            priority=entity.priority,
            started_at=started_at_str,
            completed_at=completed_at_str,
            progress_percent=getattr(entity, "progress_percent", 0.0),
            created_at=entity.created_at.isoformat()
            if getattr(entity, "created_at", None)
            else None,
            updated_at=entity.updated_at.isoformat()
            if getattr(entity, "updated_at", None)
            else None,
        )

    def to_entity_dict(self) -> dict[str, Any]:
        """Convert to entity dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "goals": self.goals,
            "tags": self.tags,
            "priority": self.priority,
            "status": self.status,
        }


class PlanSummary(BaseModel):
    """Lightweight plan summary for lists."""

    id: str = Field(..., description="Plan unique identifier")
    name: str = Field(..., description="Plan name")
    description: str | None = Field(None, description="Plan description")
    status: PlanStatus = Field(..., description="Plan execution status")
    owner_id: str = Field(..., description="Plan owner user ID")
    step_count: int = Field(..., description="Number of steps")
    priority: PlanPriority = Field(..., description="Plan priority")
    progress_percent: float = Field(default=0.0, description="Execution progress")
    created_at: str | None = Field(None, description="Creation timestamp")

    @classmethod
    def from_entity(cls, entity: Plan) -> PlanSummary:
        """Convert Plan entity to summary DTO."""
        name_val = getattr(entity, "title", None) or getattr(entity, "name", "")
        name_str = str(name_val) if name_val is not None else ""
        owner_id_val = getattr(entity, "user_id", None) or getattr(
            entity, "owner_id", ""
        )
        owner_id_str = str(owner_id_val) if owner_id_val is not None else ""

        return cls(
            id=entity.id,
            name=name_str,
            description=entity.description,
            status=entity.status,
            owner_id=owner_id_str,
            step_count=len(entity.steps) if entity.steps else 0,
            priority=entity.priority,
            progress_percent=getattr(entity, "progress_percent", 0.0),
            created_at=entity.created_at.isoformat()
            if getattr(entity, "created_at", None)
            else None,
        )


class PlanExecutionRequest(BaseModel):
    """Plan execution request DTO."""

    mode: str = Field(
        default="sequential", description="Execution mode (sequential, parallel)"
    )
    dry_run: bool = Field(default=False, description="Whether to perform a dry run")
    timeout_seconds: int | None = Field(None, ge=1, description="Execution timeout")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Runtime parameters"
    )

    @field_validator("mode")
    def validate_mode(cls, v: str) -> str:
        """Validate execution mode."""
        allowed_modes = ["sequential", "parallel"]
        if v not in allowed_modes:
            raise ValueError(f"Mode must be one of: {allowed_modes}")
        return v
