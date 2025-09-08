"""
Plan Entity - Pattern example cho GitHub Copilot.

Entity cho execution plans với steps, immutable design.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from app._base_model import DomainModel, Timestamped, Traceable, Versioned
from pydantic import Field, field_validator, model_validator
import ValueError
import bool
import classmethod
import dict
import enumerate
import float
import i
import index
import int
import len
import list
import range
import reason
import s
import self
import set
import sorted
import step
import str
import sum
import tuple
import v


class PlanStatus(str, Enum):
    """Status của execution plan."""

    DRAFT = "DRAFT"
    READY = "READY"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PlanStep(DomainModel):
    """
    Single step trong execution plan.

    Immutable value object đại diện cho một bước thực thi.
    """

    order: int = Field(ge=0, description="Thứ tự thực hiện step")
    action: str = Field(..., min_length=1, description="Action/command cần thực hiện")
    params: dict[str, Any] = Field(
        default_factory=dict, description="Parameters cho action"
    )
    description: str = Field(default="", description="Mô tả step")
    estimated_duration_seconds: int = Field(
        default=30, ge=1, description="Ước tính thời gian thực hiện"
    )

    @field_validator("action")
    @classmethod
    def _validate_action(cls, v: str) -> str:
        """Validate action không rỗng và format hợp lệ."""
        action = v.strip()
        if not action:
            raise ValueError("Action must not be empty")
        if len(action) > 200:
            raise ValueError("Action too long")
        return action


class Plan(DomainModel, Timestamped, Versioned, Traceable):
    """
    Execution Plan entity.

    Quản lý sequence of steps để đạt được goal.
    Immutable với business logic validation.

    Business Rules:
    - goal không được rỗng
    - steps phải có order unique và consecutive
    - plan EXECUTING phải có ít nhất 1 step
    - không thể modify plan đang EXECUTING

    Examples:
        # Tạo plan mới
        plan = Plan(
            owner_agent_id=agent_id,
            goal="Analyze user requirements and create specification"
        )

        # Thêm steps
        plan = plan.add_step(PlanStep(
            order=0,
            action="parse_requirements",
            params={"input": "user_text"}
        ))

        # Start execution
        plan = plan.start_execution()
    """

    # Identity
    id: UUID = Field(default_factory=uuid4, description="Unique identifier cho Plan")

    owner_agent_id: UUID = Field(..., description="ID của agent sở hữu plan này")

    # Core attributes
    goal: str = Field(
        ..., min_length=1, max_length=1000, description="Mục tiêu của plan"
    )

    status: PlanStatus = Field(
        default=PlanStatus.DRAFT, description="Trạng thái hiện tại của plan"
    )

    # Steps
    steps: tuple[PlanStep, ...] = Field(
        default=(), description="Danh sách steps theo thứ tự"
    )

    # Execution tracking
    current_step_index: int = Field(
        default=0, ge=0, description="Index của step đang thực hiện"
    )

    started_at: datetime | None = Field(
        default=None, description="Thời điểm bắt đầu execution"
    )

    completed_at: datetime | None = Field(
        default=None, description="Thời điểm hoàn thành"
    )

    # Metadata
    priority: int = Field(
        default=5, ge=1, le=10, description="Độ ưu tiên [1=low, 10=high]"
    )

    tags: tuple[str, ...] = Field(default=(), description="Tags để phân loại")

    metadata: dict[str, str] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @field_validator("goal")
    @classmethod
    def _validate_goal(cls, v: str) -> str:
        """Validate goal không rỗng."""
        goal = v.strip()
        if not goal:
            raise ValueError("Plan goal must not be empty")
        return goal

    @field_validator("steps")
    @classmethod
    def _validate_steps(cls, v: tuple[PlanStep, ...]) -> tuple[PlanStep, ...]:
        """
        Validate steps có order hợp lệ và consecutive.

        Returns:
            Valid steps tuple

        Raises:
            ValueError: Nếu order không consecutive hoặc duplicate
        """
        if not v:
            return v

        # Kiểm tra order consecutive và unique
        orders = [step.order for step in v]
        if len(set(orders)) != len(orders):
            raise ValueError("Step orders must be unique")

        sorted_orders = sorted(orders)
        expected_orders = list(range(len(orders)))
        if sorted_orders != expected_orders:
            raise ValueError(
                f"Step orders must be consecutive starting from 0. Got: {sorted_orders}"
            )

        # Sort by order
        return tuple(sorted(v, key=lambda s: s.order))

    @model_validator(mode="after")
    def _validate_business_rules(self) -> Plan:
        """Validate business rules."""
        # Plan EXECUTING phải có steps
        if self.status == PlanStatus.EXECUTING and not self.steps:
            raise ValueError("Executing plan must have at least one step")

        # current_step_index phải valid
        if self.steps and self.current_step_index >= len(self.steps):
            raise ValueError("Current step index out of range")

        # Completed plan phải có completed_at
        if (
            self.status in {PlanStatus.COMPLETED, PlanStatus.FAILED}
            and not self.completed_at
        ):
            raise ValueError("Completed/failed plan must have completed_at timestamp")

        # Started plan phải có started_at
        if (
            self.status
            in {PlanStatus.EXECUTING, PlanStatus.COMPLETED, PlanStatus.FAILED}
            and not self.started_at
        ):
            raise ValueError("Started plan must have started_at timestamp")

        return self

    # === Business Methods ===

    def add_step(self, step: PlanStep) -> Plan:
        """
        Thêm step mới vào cuối plan.

        Args:
            step: Step cần thêm

        Returns:
            Plan mới với step đã thêm

        Raises:
            ValueError: Nếu plan đang executing hoặc step order không hợp lệ
        """
        if self.status == PlanStatus.EXECUTING:
            raise ValueError("Cannot modify executing plan")

        # Auto-assign order
        new_order = len(self.steps)
        new_step = step.model_copy(update={"order": new_order})

        new_steps = (*self.steps, new_step)

        return self.model_copy(
            update={
                "steps": new_steps,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def insert_step(self, index: int, step: PlanStep) -> Plan:
        """
        Chèn step tại vị trí chỉ định.

        Args:
            index: Vị trí chèn
            step: Step cần chèn

        Returns:
            Plan mới với step đã chèn
        """
        if self.status == PlanStatus.EXECUTING:
            raise ValueError("Cannot modify executing plan")

        if not 0 <= index <= len(self.steps):
            raise ValueError("Insert index out of range")

        # Rebuild steps với order mới
        new_steps = list(self.steps)
        new_steps.insert(index, step)

        # Re-assign orders
        reordered_steps = []
        for i, s in enumerate(new_steps):
            reordered_steps.append(s.model_copy(update={"order": i}))

        return self.model_copy(
            update={
                "steps": tuple(reordered_steps),
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def remove_step(self, index: int) -> Plan:
        """
        Xóa step tại vị trí chỉ định.

        Args:
            index: Index của step cần xóa

        Returns:
            Plan mới với step đã xóa
        """
        if self.status == PlanStatus.EXECUTING:
            raise ValueError("Cannot modify executing plan")

        if not 0 <= index < len(self.steps):
            raise ValueError("Remove index out of range")

        # Remove step và re-order
        new_steps = list(self.steps)
        new_steps.pop(index)

        # Re-assign orders
        reordered_steps = []
        for i, s in enumerate(new_steps):
            reordered_steps.append(s.model_copy(update={"order": i}))

        return self.model_copy(
            update={
                "steps": tuple(reordered_steps),
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def start_execution(self) -> Plan:
        """
        Bắt đầu execution.

        Returns:
            Plan mới với status EXECUTING

        Raises:
            ValueError: Nếu plan không thể start
        """
        if self.status != PlanStatus.READY:
            raise ValueError(f"Cannot start execution from status {self.status.value}")

        if not self.steps:
            raise ValueError("Cannot start execution without steps")

        now = datetime.now(UTC)
        return self.model_copy(
            update={
                "status": PlanStatus.EXECUTING,
                "started_at": now,
                "current_step_index": 0,
                "updated_at": now,
                "version": self.version + 1,
            }
        )

    def advance_step(self) -> Plan:
        """
        Chuyển sang step tiếp theo.

        Returns:
            Plan mới với current_step_index tăng
        """
        if self.status != PlanStatus.EXECUTING:
            raise ValueError("Plan must be executing to advance step")

        if self.current_step_index >= len(self.steps) - 1:
            # Last step -> complete
            return self.complete()

        return self.model_copy(
            update={
                "current_step_index": self.current_step_index + 1,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def complete(self) -> Plan:
        """
        Hoàn thành plan.

        Returns:
            Plan mới với status COMPLETED
        """
        if self.status != PlanStatus.EXECUTING:
            raise ValueError("Only executing plan can be completed")

        now = datetime.now(UTC)
        return self.model_copy(
            update={
                "status": PlanStatus.COMPLETED,
                "completed_at": now,
                "updated_at": now,
                "version": self.version + 1,
            }
        )

    def fail(self, reason: str = "") -> Plan:
        """
        Đánh dấu plan failed.

        Args:
            reason: Lý do fail (optional)

        Returns:
            Plan mới với status FAILED
        """
        if self.status not in {PlanStatus.EXECUTING, PlanStatus.READY}:
            raise ValueError("Only ready/executing plan can fail")

        now = datetime.now(UTC)
        update_data = {
            "status": PlanStatus.FAILED,
            "completed_at": now,
            "updated_at": now,
            "version": self.version + 1,
        }

        if reason:
            new_metadata = dict(self.metadata)
            new_metadata["failure_reason"] = reason
            update_data["metadata"] = new_metadata

        return self.model_copy(update=update_data)

    def cancel(self) -> Plan:
        """
        Hủy plan.

        Returns:
            Plan mới với status CANCELLED
        """
        if self.status in {PlanStatus.COMPLETED, PlanStatus.FAILED}:
            raise ValueError("Cannot cancel completed/failed plan")

        now = datetime.now(UTC)
        return self.model_copy(
            update={
                "status": PlanStatus.CANCELLED,
                "completed_at": now,
                "updated_at": now,
                "version": self.version + 1,
            }
        )

    def mark_ready(self) -> Plan:
        """
        Đánh dấu plan sẵn sàng thực hiện.

        Returns:
            Plan mới với status READY
        """
        if self.status != PlanStatus.DRAFT:
            raise ValueError("Only draft plan can be marked ready")

        if not self.steps:
            raise ValueError("Plan must have steps to be ready")

        return self.model_copy(
            update={
                "status": PlanStatus.READY,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    # === Query Methods ===

    def current_step(self) -> PlanStep | None:
        """Lấy step hiện tại."""
        if not self.steps or self.current_step_index >= len(self.steps):
            return None
        return self.steps[self.current_step_index]

    def remaining_steps(self) -> tuple[PlanStep, ...]:
        """Lấy các steps còn lại."""
        if not self.steps:
            return ()
        return self.steps[self.current_step_index :]

    def completed_steps(self) -> tuple[PlanStep, ...]:
        """Lấy các steps đã hoàn thành."""
        if not self.steps:
            return ()
        return self.steps[: self.current_step_index]

    def progress_percentage(self) -> float:
        """Tính phần trăm hoàn thành."""
        if not self.steps:
            return 0.0
        return (self.current_step_index / len(self.steps)) * 100.0

    def estimated_duration_seconds(self) -> int:
        """Tính tổng thời gian ước tính."""
        return sum(step.estimated_duration_seconds for step in self.steps)

    def is_finished(self) -> bool:
        """Kiểm tra plan đã kết thúc chưa."""
        return self.status in {
            PlanStatus.COMPLETED,
            PlanStatus.FAILED,
            PlanStatus.CANCELLED,
        }

    def can_start(self) -> bool:
        """Kiểm tra có thể start execution không."""
        return self.status == PlanStatus.READY and len(self.steps) > 0


__all__ = ["Plan", "PlanStep", "PlanStatus"]
