"""
Plan Step Value Object - ZETA AI Server
Domain-Driven Design (DDD) Compliant
======================================

Immutable value object representing một step trong execution plan.
Chứa action, parameters, state, và execution metadata.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4
import ValueError
import all
import bool
import classmethod
import cls
import completed_step_ids
import data
import dep_id
import dict
import error
import float
import int
import kwargs
import list
import object
import reason
import result
import self
import set
import str


class StepStatus(Enum):
    """Status của một plan step."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class PlanStepVO:
    """
    Plan Step Value Object.

    Immutable representation của một execution step trong plan.
    Chứa tất cả thông tin cần thiết để execute và track step.
    """

    # Core identification
    id: str | None
    action: str  # e.g., "create_file", "call_api", "process_data"
    description: str

    # Execution parameters
    parameters: dict[str, Any] | None = None  # normalized in __post_init__
    order: int = 0
    dependencies: list[str] | None = None  # normalized in __post_init__

    # State tracking
    status: StepStatus = StepStatus.PENDING
    is_completed: bool = False
    is_failed: bool = False

    # Results
    result: str | None = None
    error_message: str | None = None

    # Timing
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # Metadata
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 300

    def __post_init__(self) -> None:
        """Validate invariants after initialization."""
        if not self.id:
            object.__setattr__(self, "id", str(uuid4()))

        # Normalize default containers
        if self.parameters is None:
            object.__setattr__(self, "parameters", {})
        if self.dependencies is None:
            object.__setattr__(self, "dependencies", [])

        if not self.action.strip():
            raise ValueError("Step action không thể rỗng")

        if not self.description.strip():
            raise ValueError("Step description không thể rỗng")

        if self.order < 0:
            raise ValueError("Step order phải >= 0")

        if self.retry_count < 0:
            raise ValueError("retry_count phải >= 0")

        if self.max_retries < 0:
            raise ValueError("max_retries phải >= 0")

        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds phải > 0")

    def complete(self, result: str) -> "PlanStepVO":
        """
        Tạo step mới với trạng thái completed.

        Args:
            result: Kết quả thực hiện step

        Returns:
            PlanStepVO: Step mới với status completed
        """
        if self.is_completed:
            raise ValueError(f"Step {self.id} đã completed")

        if self.is_failed:
            raise ValueError(f"Step {self.id} đã failed, không thể complete")

        return self._replace(
            status=StepStatus.COMPLETED,
            is_completed=True,
            result=result,
            completed_at=datetime.now(),
        )

    def fail(self, error: str) -> "PlanStepVO":
        """
        Tạo step mới với trạng thái failed.

        Args:
            error: Error message

        Returns:
            PlanStepVO: Step mới với status failed
        """
        if self.is_completed:
            raise ValueError(f"Step {self.id} đã completed, không thể fail")

        return self._replace(
            status=StepStatus.FAILED,
            is_failed=True,
            error_message=error,
            retry_count=self.retry_count + 1,
            completed_at=datetime.now(),
        )

    def start(self) -> "PlanStepVO":
        """
        Tạo step mới với trạng thái in_progress.

        Returns:
            PlanStepVO: Step mới với status in_progress
        """
        if self.is_completed:
            raise ValueError(f"Step {self.id} đã completed")

        if self.is_failed:
            raise ValueError(f"Step {self.id} đã failed")

        return self._replace(status=StepStatus.IN_PROGRESS, started_at=datetime.now())

    def skip(self, reason: str = "") -> "PlanStepVO":
        """
        Tạo step mới với trạng thái skipped.

        Args:
            reason: Lý do skip step

        Returns:
            PlanStepVO: Step mới với status skipped
        """
        if self.is_completed:
            raise ValueError(f"Step {self.id} đã completed")

        return self._replace(
            status=StepStatus.SKIPPED,
            result=f"Skipped: {reason}",
            completed_at=datetime.now(),
        )

    def retry(self) -> "PlanStepVO":
        """
        Tạo step mới để retry (reset về pending).

        Returns:
            PlanStepVO: Step mới reset về pending

        Raises:
            ValueError: Nếu đã vượt quá max_retries
        """
        if self.retry_count >= self.max_retries:
            raise ValueError(
                f"Step {self.id} đã vượt quá max_retries ({self.max_retries})"
            )

        return self._replace(
            status=StepStatus.PENDING,
            is_failed=False,
            error_message="",
            started_at=None,
            completed_at=None,
        )

    def can_execute(self, completed_step_ids: set[str]) -> bool:
        """
        Kiểm tra xem step có thể execute không (dependencies đã hoàn thành).

        Args:
            completed_step_ids: Set các step IDs đã completed

        Returns:
            bool: True nếu có thể execute
        """
        if self.is_completed or self.is_failed:
            return False

        if self.status == StepStatus.SKIPPED:
            return False

        # Check dependencies
        deps = self.dependencies or []
        return all(dep_id in completed_step_ids for dep_id in deps)

    def get_duration_seconds(self) -> float:
        """
        Tính duration thực hiện step (seconds).

        Returns:
            float: Duration in seconds, 0 if chưa start hoặc chưa complete
        """
        if not self.started_at or not self.completed_at:
            return 0.0

        return (self.completed_at - self.started_at).total_seconds()

    def is_overdue(self) -> bool:
        """
        Kiểm tra xem step có overdue timeout không.

        Returns:
            bool: True nếu đã vượt quá timeout
        """
        if not self.started_at or self.is_completed or self.is_failed:
            return False

        elapsed = (datetime.now() - self.started_at).total_seconds()
        return elapsed > self.timeout_seconds

    def to_dict(self) -> dict[str, Any]:
        """
        Convert step to dictionary representation.

        Returns:
            dict: Step data as dictionary
        """
        return {
            "id": self.id,
            "action": self.action,
            "description": self.description,
            "parameters": self.parameters,
            "order": self.order,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "is_completed": self.is_completed,
            "is_failed": self.is_failed,
            "result": self.result,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
            "duration_seconds": self.get_duration_seconds(),
            "is_overdue": self.is_overdue(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlanStepVO":
        """
        Create step from dictionary.

        Args:
            data: Step data dictionary

        Returns:
            PlanStepVO: New step instance
        """
        started_at = None
        if data.get("started_at"):
            started_at = datetime.fromisoformat(data["started_at"])

        completed_at = None
        if data.get("completed_at"):
            completed_at = datetime.fromisoformat(data["completed_at"])

        return cls(
            id=data.get("id"),
            action=data["action"],
            description=data["description"],
            parameters=data.get("parameters", {}),
            order=data.get("order", 0),
            dependencies=data.get("dependencies", []),
            status=StepStatus(data.get("status", "pending")),
            is_completed=data.get("is_completed", False),
            is_failed=data.get("is_failed", False),
            result=data.get("result"),
            error_message=data.get("error_message"),
            started_at=started_at,
            completed_at=completed_at,
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            timeout_seconds=data.get("timeout_seconds", 300),
        )

    def _replace(self, **kwargs: Any) -> "PlanStepVO":
        """
        Create new instance with replaced fields.
        Workaround for dataclass replace with frozen=True.
        """
        current_data = {
            "id": self.id,
            "action": self.action,
            "description": self.description,
            "parameters": self.parameters,
            "order": self.order,
            "dependencies": self.dependencies,
            "status": self.status,
            "is_completed": self.is_completed,
            "is_failed": self.is_failed,
            "result": self.result,
            "error_message": self.error_message,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
        }
        current_data.update(kwargs)
        return PlanStepVO(**current_data)
