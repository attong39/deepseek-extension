"""Domain events cho Outbox pattern.

Định nghĩa các domain events và base classes để hỗ trợ event-driven architecture
với Outbox pattern để đảm bảo consistency.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
import EVENT_TYPE_REGISTRY
import ValueError
import bool
import dict
import event_type
import float
import int
import list
import str
import type


def _now() -> datetime:
    """Trả về timestamp UTC hiện tại."""
    return datetime.now(UTC)


class DomainEvent(BaseModel):
    """Base class cho tất cả domain events."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: str = Field(description="Unique event ID")
    event_type: str = Field(description="Loại event")
    occurred_at: datetime = Field(
        default_factory=_now, description="Thời điểm event xảy ra"
    )
    aggregate_id: str = Field(description="ID của aggregate gây ra event")
    aggregate_type: str = Field(description="Loại aggregate")
    version: int = Field(default=1, description="Event schema version")
    correlation_id: str | None = Field(default=None, description="Correlation ID")
    causation_id: str | None = Field(
        default=None, description="ID của event/command gây ra"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata bổ sung"
    )


# Agent Events
class AgentStatusChanged(DomainEvent):
    """Event khi trạng thái agent thay đổi."""

    event_type: str = Field(default="agent.status_changed", frozen=True)
    old_status: str = Field(description="Trạng thái cũ")
    new_status: str = Field(description="Trạng thái mới")
    reason: str | None = Field(default=None, description="Lý do thay đổi")


class AgentCreated(DomainEvent):
    """Event khi agent được tạo."""

    event_type: str = Field(default="agent.created", frozen=True)
    agent_name: str = Field(description="Tên agent")
    capabilities: list[str] = Field(description="Danh sách capabilities")
    owner_id: str = Field(description="ID người tạo")


class AgentDeleted(DomainEvent):
    """Event khi agent bị xóa."""

    event_type: str = Field(default="agent.deleted", frozen=True)
    deletion_reason: str = Field(description="Lý do xóa")
    soft_delete: bool = Field(default=True, description="Có phải soft delete không")


# Training Job Events
class TrainingJobProgressed(DomainEvent):
    """Event khi training job tiến triển."""

    event_type: str = Field(default="training.progressed", frozen=True)
    progress_percent: float = Field(ge=0.0, le=100.0, description="Tiến độ %")
    current_epoch: int = Field(ge=0, description="Epoch hiện tại")
    total_epochs: int = Field(ge=1, description="Tổng số epochs")
    metrics: dict[str, float] = Field(
        default_factory=dict, description="Training metrics"
    )


class TrainingJobCompleted(DomainEvent):
    """Event khi training job hoàn thành."""

    event_type: str = Field(default="training.completed", frozen=True)
    final_metrics: dict[str, float] = Field(description="Metrics cuối cùng")
    model_artifacts: dict[str, str] = Field(description="Paths của model artifacts")
    duration_seconds: float = Field(ge=0, description="Thời gian training (giây)")


class TrainingJobFailed(DomainEvent):
    """Event khi training job thất bại."""

    event_type: str = Field(default="training.failed", frozen=True)
    error_message: str = Field(description="Thông báo lỗi")
    error_type: str = Field(description="Loại lỗi")
    stacktrace: str | None = Field(default=None, description="Stack trace chi tiết")


# Memory Events
class MemoryCreated(DomainEvent):
    """Event khi memory record được tạo."""

    event_type: str = Field(default="memory.created", frozen=True)
    memory_type: str = Field(description="Loại memory")
    content_length: int = Field(ge=0, description="Độ dài content")
    has_embedding: bool = Field(description="Có embedding không")


class MemoryExpired(DomainEvent):
    """Event khi memory record hết hạn."""

    event_type: str = Field(default="memory.expired", frozen=True)
    expiration_reason: str = Field(description="Lý do hết hạn")
    ttl_seconds: int = Field(ge=0, description="TTL ban đầu (giây)")


# Plan Events
class PlanExecutionStarted(DomainEvent):
    """Event khi bắt đầu thực hiện plan."""

    event_type: str = Field(default="plan.execution_started", frozen=True)
    total_steps: int = Field(ge=1, description="Tổng số steps")
    estimated_duration: int | None = Field(
        default=None, description="Thời gian ước tính (giây)"
    )


class PlanStepCompleted(DomainEvent):
    """Event khi một step của plan hoàn thành."""

    event_type: str = Field(default="plan.step_completed", frozen=True)
    step_index: int = Field(ge=0, description="Index của step")
    step_name: str = Field(description="Tên step")
    execution_time_ms: int = Field(ge=0, description="Thời gian thực hiện (ms)")
    output: dict[str, Any] = Field(default_factory=dict, description="Kết quả output")


class PlanExecutionCompleted(DomainEvent):
    """Event khi plan hoàn thành."""

    event_type: str = Field(default="plan.execution_completed", frozen=True)
    total_duration_ms: int = Field(ge=0, description="Tổng thời gian (ms)")
    success_rate: float = Field(ge=0.0, le=1.0, description="Tỷ lệ thành công")
    final_result: dict[str, Any] = Field(
        default_factory=dict, description="Kết quả cuối cùng"
    )


# User Events
class UserRegistered(DomainEvent):
    """Event khi user đăng ký."""

    event_type: str = Field(default="user.registered", frozen=True)
    email: str = Field(description="Email user")
    role: str = Field(description="Role user")
    registration_source: str = Field(description="Nguồn đăng ký")


class UserPermissionChanged(DomainEvent):
    """Event khi quyền user thay đổi."""

    event_type: str = Field(default="user.permission_changed", frozen=True)
    old_permissions: list[str] = Field(description="Quyền cũ")
    new_permissions: list[str] = Field(description="Quyền mới")
    changed_by: str = Field(description="ID người thay đổi")
    reason: str = Field(description="Lý do thay đổi")


# System Events
class SystemHealthChanged(DomainEvent):
    """Event khi health status của hệ thống thay đổi."""

    event_type: str = Field(default="system.health_changed", frozen=True)
    component: str = Field(description="Component bị ảnh hưởng")
    old_status: str = Field(description="Trạng thái cũ")
    new_status: str = Field(description="Trạng thái mới")
    metrics: dict[str, Any] = Field(default_factory=dict, description="Health metrics")


# Event Registry để mapping event types
EVENT_TYPE_REGISTRY: dict[str, type[DomainEvent]] = {
    "agent.status_changed": AgentStatusChanged,
    "agent.created": AgentCreated,
    "agent.deleted": AgentDeleted,
    "training.progressed": TrainingJobProgressed,
    "training.completed": TrainingJobCompleted,
    "training.failed": TrainingJobFailed,
    "memory.created": MemoryCreated,
    "memory.expired": MemoryExpired,
    "plan.execution_started": PlanExecutionStarted,
    "plan.step_completed": PlanStepCompleted,
    "plan.execution_completed": PlanExecutionCompleted,
    "user.registered": UserRegistered,
    "user.permission_changed": UserPermissionChanged,
    "system.health_changed": SystemHealthChanged,
}


def get_event_class(event_type: str) -> type[DomainEvent]:
    """Lấy event class từ event type string."""
    if event_type not in EVENT_TYPE_REGISTRY:
        raise ValueError(f"Unknown event type: {event_type}")
    return EVENT_TYPE_REGISTRY[event_type]
