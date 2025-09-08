"""Assistant serializers for API requests and responses.

Cung cấp các Pydantic models cho validation và serialization
của dữ liệu assistant trong API endpoints.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar

from app.serializers.base_serializers import OrjsonModel
from pydantic import ConfigDict, Field, field_validator
import ValueError
import bool
import dict
import float
import int
import len
import list
import str
import v

# Note: datetime is imported at runtime to avoid Pydantic forward-ref issues.


class AssistantTemplateIn(OrjsonModel):
    """Input schema for creating assistant from template."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=64,
        description="Assistant name",
        examples=["Finance Assistant"],
    )
    base_model: str = Field(
        ...,
        description="Base AI model to use",
        examples=["gpt-4o-mini", "gpt-3.5-turbo"],
    )
    instructions: str = Field(
        "",
        description="System instructions for the assistant",
        examples=["You are a helpful assistant specialized in financial analysis."],
    )
    tools: list[str] = Field(
        default_factory=list,
        description="List of tool IDs",
        examples=[["search", "calculator"]],
    )
    capabilities: list[str] = Field(
        default_factory=list,
        description="Assistant capabilities",
        examples=[["analytics", "reporting"]],
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
        examples=[{"team": "finance", "priority": "high"}],
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate assistant name."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class AssistantUpdateIn(OrjsonModel):
    """Input schema for updating assistant."""

    name: str | None = Field(None, min_length=2, max_length=64, examples=["New Name"])
    base_model: str | None = Field(default=None, examples=["gpt-4o-mini"])
    instructions: str | None = Field(default=None, examples=["Updated system prompt"])
    tools: list[str] | None = Field(default=None, examples=[["search", "weather"]])
    capabilities: list[str] | None = Field(default=None, examples=[["analytics"]])
    metadata: dict[str, Any] | None = Field(
        default=None, examples=[{"priority": "low"}]
    )
    status: str | None = Field(default=None, examples=["active", "inactive"])


class AssistantOut(OrjsonModel):
    """Output schema for assistant data."""

    id: str
    name: str
    base_model: str
    instructions: str
    tools: list[str]
    capabilities: list[str]
    status: str = "inactive"
    owner_id: str
    created_at: datetime
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    performance_metrics: dict[str, Any] = Field(default_factory=dict)

    # Pydantic v2 configuration with OpenAPI example
    model_config: ClassVar[ConfigDict] = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "a7c8f7f2-1234-5678-9abc-def012345678",
                "name": "Finance Assistant",
                "base_model": "gpt-4o-mini",
                "instructions": "You are a helpful assistant specialized in financial analysis.",
                "tools": ["search", "calculator"],
                "capabilities": ["analytics", "reporting"],
                "status": "inactive",
                "owner_id": "user-123",
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:00:00Z",
                "metadata": {"team": "finance"},
                "performance_metrics": {"total_interactions": 0},
            }
        }
    )


class AssistantSearchParams(OrjsonModel):
    """Search parameters for assistant listing."""

    owner_id: str | None = None
    status: str | None = None
    base_model: str | None = None
    capability: str | None = None
    search: str | None = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    sort_by: str = "created_at"
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


class AssistantBatchCreateIn(OrjsonModel):
    """Input schema for batch assistant creation."""

    batch_id: str | None = None
    assistants: list[AssistantTemplateIn]
    continue_on_error: bool = False

    @field_validator("assistants")
    def validate_assistants(
        cls, v: list[AssistantTemplateIn]
    ) -> list[AssistantTemplateIn]:
        """Validate assistants list."""
        if not v:
            raise ValueError("At least one assistant is required")
        if len(v) > 50:
            raise ValueError("Maximum 50 assistants per batch")
        return v


class AssistantAnalyticsOut(OrjsonModel):
    """Output schema for assistant analytics."""

    assistant_id: str
    period_days: int
    total_interactions: int
    successful_interactions: int
    success_rate: float
    avg_response_time_ms: float
    total_tokens_used: int
    error_count: int
    performance_trend: list[dict[str, Any]]
    usage_patterns: dict[str, Any]
    top_tools_used: list[dict[str, Any]]


class AssistantConfigVersionOut(OrjsonModel):
    """Output schema for assistant configuration versions."""

    version_id: str
    assistant_id: str
    version_number: int
    config_data: dict[str, Any]
    created_at: datetime
    created_by: str
    is_active: bool
    change_summary: str | None = None
