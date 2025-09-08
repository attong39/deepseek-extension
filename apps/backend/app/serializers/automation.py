"""Serializers for automation API endpoints.

This module provides Pydantic models for request/response serialization
in the UI automation API.

Features:
- Request models for plan creation and execution
- Response models for plans, execution status, and results
- Proper validation and type safety
- OpenAPI documentation support
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from apps.backend.core.domain.value_objects.automation import SafetyConfig
from pydantic import BaseModel, Field
import bool
import dict
import float
import int
import list
import str


class CreateAutomationPlanRequest(BaseModel):
    """Request model for creating automation plans."""

    description: str = Field(
        ...,
        description="Description of what should be automated",
        example="Click the login button and enter credentials",
    )
    context: dict[str, Any] | None = Field(
        None,
        description="Additional context for plan creation",
        example={"application": "web_browser", "url": "https://example.com"},
    )
    safety_config: SafetyConfig | None = Field(
        None, description="Safety configuration for the plan"
    )


class AutomationStepResponse(BaseModel):
    """Response model for automation steps."""

    step_id: str = Field(..., description="Unique step identifier")
    action: str = Field(..., description="Action type (click, type, etc.)")
    target: str = Field(..., description="Target element description")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Action parameters"
    )
    description: str = Field(..., description="Human-readable step description")


class AutomationPlanResponse(BaseModel):
    """Response model for automation plans."""

    plan_id: str = Field(..., description="Unique plan identifier")
    description: str = Field(..., description="Plan description")
    steps: list[AutomationStepResponse] = Field(
        default_factory=list, description="List of automation steps"
    )
    estimated_duration: float = Field(
        ..., description="Estimated execution duration in seconds"
    )
    safety_level: str = Field(..., description="Safety level (low/medium/high)")
    created_at: datetime = Field(..., description="Plan creation timestamp")


class AutomationExecutionResponse(BaseModel):
    """Response model for automation execution."""

    execution_id: str = Field(..., description="Unique execution identifier")
    plan_id: str = Field(..., description="Plan being executed")
    status: str = Field(..., description="Execution status")
    progress: float = Field(
        ..., ge=0.0, le=1.0, description="Execution progress (0.0 to 1.0)"
    )
    current_step: int | None = Field(None, description="Current step index")
    steps_completed: int = Field(..., description="Number of completed steps")
    total_steps: int = Field(..., description="Total number of steps")
    started_at: datetime = Field(..., description="Execution start timestamp")
    completed_at: datetime | None = Field(
        None, description="Execution completion timestamp"
    )
    error_message: str | None = Field(
        None, description="Error message if execution failed"
    )


class ExecutionStatusResponse(BaseModel):
    """Response model for execution status."""

    execution_id: str = Field(..., description="Unique execution identifier")
    status: str = Field(..., description="Current execution status")
    progress: float = Field(
        ..., ge=0.0, le=1.0, description="Execution progress (0.0 to 1.0)"
    )
    current_step: int | None = Field(None, description="Current step index")
    steps_completed: int = Field(..., description="Number of completed steps")
    total_steps: int = Field(..., description="Total number of steps")
    last_updated: str = Field(..., description="Last update timestamp")


class StepResultResponse(BaseModel):
    """Response model for individual step results."""

    step_id: str = Field(..., description="Step identifier")
    action: str = Field(..., description="Action that was performed")
    success: bool = Field(..., description="Whether step succeeded")
    duration: float = Field(..., description="Step execution duration in seconds")
    error_message: str | None = Field(None, description="Error message if step failed")


class AutomationResultResponse(BaseModel):
    """Response model for complete automation results."""

    execution_id: str = Field(..., description="Unique execution identifier")
    plan_id: str = Field(..., description="Plan that was executed")
    status: str = Field(..., description="Final execution status")
    success: bool = Field(..., description="Whether execution succeeded")
    steps_results: list[StepResultResponse] = Field(
        default_factory=list, description="Results for each step"
    )
    total_duration: float = Field(
        ..., description="Total execution duration in seconds"
    )
    screenshots: list[str] = Field(
        default_factory=list, description="List of screenshot filenames"
    )
    started_at: str = Field(..., description="Execution start timestamp")
    completed_at: str = Field(..., description="Execution completion timestamp")


class SafetyValidationResponse(BaseModel):
    """Response model for safety validation."""

    is_safe: bool = Field(..., description="Whether the plan is safe to execute")
    risk_level: str = Field(..., description="Risk level (low/medium/high)")
    warnings: list[str] = Field(
        default_factory=list, description="List of safety warnings"
    )
    blocked_actions: list[str] = Field(
        default_factory=list, description="List of blocked actions"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="List of safety recommendations"
    )


class AutomationErrorResponse(BaseModel):
    """Response model for automation errors."""

    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(None, description="Additional error details")
    timestamp: datetime = Field(..., description="Error occurrence timestamp")


class AutomationHealthResponse(BaseModel):
    """Response model for automation service health."""

    status: str = Field(..., description="Service status")
    services: dict[str, str] = Field(
        default_factory=dict, description="Status of individual services"
    )
    version: str = Field(..., description="Service version")
    uptime: float = Field(..., description="Service uptime in seconds")
    last_check: datetime = Field(..., description="Last health check timestamp")


class AutomationMetricsResponse(BaseModel):
    """Response model for automation metrics."""

    total_plans: int = Field(..., description="Total number of plans created")
    total_executions: int = Field(..., description="Total number of executions")
    success_rate: float = Field(..., ge=0.0, le=1.0, description="Overall success rate")
    average_duration: float = Field(
        ..., description="Average execution duration in seconds"
    )
    last_24h_executions: int = Field(
        ..., description="Number of executions in last 24 hours"
    )
    top_actions: list[dict[str, Any]] = Field(
        default_factory=list, description="Most commonly used actions"
    )
