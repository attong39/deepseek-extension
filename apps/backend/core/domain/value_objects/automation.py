"""Automation Value Objects for UI automation and control.

This module contains the core value objects for the automation system,
including action types, coordinates, plans, and execution results.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
import ValueError
import action
import all
import bbox_hint
import bool
import classmethod
import cls
import confidence
import confidence_threshold
import context
import coords
import created_at
import description
import dict
import error_details
import estimated_duration
import estimated_duration_seconds
import execution_time_ms
import float
import globals
import goal
import id
import int
import len
import list
import max
import message
import object
import parameters
import plan
import plan_id
import point
import property
import r
import recommended_action
import result
import safety_level
import safety_mode
import self
import session_id
import sleep_ms
import staticmethod
import step
import step_id
import steps
import str
import sum
import target
import target_image
import target_text
import text
import tuple
import violations
import warnings


class ActionType(str, Enum):
    """Types of automation actions that can be performed."""

    MOVE = "move"
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    RIGHT_CLICK = "right_click"
    TYPE = "type"
    HOTKEY = "hotkey"
    WAIT = "wait"
    SCREENSHOT = "screenshot"
    DRAG = "drag"
    SCROLL = "scroll"


class ExecutionStatus(str, Enum):
    """Overall execution status for a plan run."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SafetyLevel(str, Enum):
    """Coarse-grained safety level indicator."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Point:
    """Represents a point on the screen with x, y coordinates."""

    x: int
    y: int

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"


@dataclass(frozen=True)
class BBox:
    """Represents a bounding box with position and dimensions."""

    x: int
    y: int
    w: int
    h: int

    def center(self) -> Point:
        """Get the center point of the bounding box."""
        return Point(self.x + self.w // 2, self.y + self.h // 2)

    def contains(self, point: Point) -> bool:
        """Check if a point is within this bounding box."""
        return (
            self.x <= point.x <= self.x + self.w
            and self.y <= point.y <= self.y + self.h
        )

    def __str__(self) -> str:
        return f"BBox({self.x}, {self.y}, {self.w}, {self.h})"


@dataclass
class AutomationStep:
    """Represents a single step in an automation plan."""

    def __init__(
        self,
        action: ActionType,
        target_text: str | None = None,
        target_image: str | None = None,
        coords: Point | None = None,
        bbox_hint: BBox | None = None,
        keys: tuple[str, ...] | None = None,
        text: str | None = None,
        sleep_ms: int = 0,
        confidence_threshold: float = 0.85,
        description: str = "",
        # legacy aliases
        step_id: str | None = None,
        target: str | None = None,
        parameters: dict | None = None,
        **kwargs,
    ):
        self.action = action
        self.target_text = target_text or target
        self.target_image = target_image
        self.coords = coords
        self.bbox_hint = bbox_hint
        self.keys = keys
        self.text = text
        self.sleep_ms = sleep_ms
        self.confidence_threshold = confidence_threshold
        self.description = description
        # legacy
        self.step_id = step_id
        # legacy parameters: map x/y to coords
        if parameters and ("x" in parameters and "y" in parameters):
            self.coords = Point(parameters["x"], parameters["y"])

        if not self.description:
            self.description = self._generate_description()

    def _generate_description(self) -> str:
        if self.action == ActionType.CLICK:
            if self.target_text:
                return f"Click on '{self.target_text}'"
            elif self.target_image:
                return f"Click on image '{self.target_image}'"
            elif self.coords:
                return f"Click at {self.coords}"
            else:
                return "Click"
        elif self.action == ActionType.TYPE:
            return f"Type '{self.text}'"
        elif self.action == ActionType.HOTKEY:
            return f"Press {'+'.join(self.keys or [])}"
        elif self.action == ActionType.WAIT:
            return f"Wait {self.sleep_ms}ms"
        else:
            return f"{self.action.value}"


class AutomationPlan:
    """Represents a complete automation plan with multiple steps.

    Compatible with legacy constructor used in tests:
    - plan_id: str
    - description: str
    - estimated_duration: float | int
    - safety_level: Any
    """

    def __init__(
        self,
        *,
        id: UUID | str | None = None,
        goal: str | None = None,
        context: str = "",
        steps: list[AutomationStep] | None = None,
        created_at: datetime | None = None,
        safety_mode: str = "strict",
        estimated_duration_seconds: int | None = None,
        # legacy aliases
        plan_id: str | None = None,
        description: str | None = None,
        estimated_duration: float | int | None = None,
        safety_level: object | None = None,
        **_kwargs: object,
    ) -> None:
        self.id: UUID | str = id or plan_id or uuid4()
        self.goal: str = goal or description or ""
        self.context: str = context
        self.steps: list[AutomationStep] = steps or []
        self.created_at: datetime = created_at or datetime.now()
        self.safety_mode: str = safety_mode
        # Keep both new and legacy duration fields
        if estimated_duration_seconds is not None:
            self.estimated_duration_seconds: int = int(estimated_duration_seconds)
        elif estimated_duration is not None:
            # tests may pass float seconds
            self.estimated_duration_seconds = int(float(estimated_duration))
        else:
            self.estimated_duration_seconds = self._estimate_duration(self.steps)

        # Legacy attributes to satisfy tests
        self.plan_id: str = str(plan_id) if plan_id is not None else str(self.id)
        self.description: str = description or self.goal
        self.safety_level = (
            safety_level
            if safety_level is not None
            else SafetyLevel.MEDIUM
            if "SafetyLevel" in globals()
            else "medium"
        )  # type: ignore[truthy-bool]

    @classmethod
    def create(
        cls,
        goal: str,
        context: str = "",
        steps: list[AutomationStep] | None = None,
        safety_mode: str = "strict",
    ) -> AutomationPlan:
        """Create a new automation plan."""
        return cls(
            id=uuid4(),
            goal=goal,
            context=context,
            steps=steps or [],
            safety_mode=safety_mode,
            created_at=datetime.now(),
            estimated_duration_seconds=cls._estimate_duration(steps or []),
        )

    @staticmethod
    def _estimate_duration(steps: list[AutomationStep]) -> int:
        """Estimate the duration of the plan in seconds."""
        total_ms = sum(
            step.sleep_ms + 500  # 500ms average per action
            for step in steps
        )
        return max(1, total_ms // 1000)

    def add_step(self, step: AutomationStep) -> None:
        """Add a step to the plan."""
        self.steps.append(step)
        self.estimated_duration_seconds = self._estimate_duration(self.steps)


@dataclass
class StepResult:
    """Result of executing a single automation step."""

    step_id: int
    success: bool
    message: str
    screenshot_path: str | None = None
    execution_time_ms: int = 0
    confidence: float = 0.0
    error_details: str | None = None

    @classmethod
    def success_result(
        cls,
        step_id: int,
        message: str = "Success",
        execution_time_ms: int = 0,
        confidence: float = 1.0,
    ) -> StepResult:
        """Create a successful step result."""
        return cls(
            step_id=step_id,
            success=True,
            message=message,
            execution_time_ms=execution_time_ms,
            confidence=confidence,
        )

    @classmethod
    def failure_result(
        cls,
        step_id: int,
        message: str,
        error_details: str | None = None,
        execution_time_ms: int = 0,
    ) -> StepResult:
        """Create a failed step result."""
        return cls(
            step_id=step_id,
            success=False,
            message=message,
            error_details=error_details,
            execution_time_ms=execution_time_ms,
            confidence=0.0,
        )


@dataclass
class ExecutionReport:
    """Complete report of automation plan execution."""

    plan_id: UUID
    session_id: UUID
    plan: AutomationPlan
    results: list[StepResult]
    all_success: bool
    total_time_ms: int
    safety_violations: list[str]
    started_at: datetime
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        plan: AutomationPlan,
        session_id: UUID,
        results: list[StepResult] | None = None,
        safety_violations: list[str] | None = None,
    ) -> ExecutionReport:
        """Create a new execution report."""
        results = results or []
        safety_violations = safety_violations or []

        return cls(
            plan_id=plan.id,
            session_id=session_id,
            plan=plan,
            results=results,
            all_success=all(r.success for r in results),
            total_time_ms=sum(r.execution_time_ms for r in results),
            safety_violations=safety_violations,
            started_at=datetime.now(),
        )

    def add_result(self, result: StepResult) -> None:
        """Add a step result to the report."""
        self.results.append(result)
        self.all_success = all(r.success for r in self.results)
        self.total_time_ms = sum(r.execution_time_ms for r in self.results)

    def complete(self) -> None:
        """Mark the execution as completed."""
        self.completed_at = datetime.now()

    @property
    def success_rate(self) -> float:
        """Calculate the success rate of executed steps."""
        if not self.results:
            return 0.0
        return sum(1 for r in self.results if r.success) / len(self.results)

    @property
    def duration_seconds(self) -> float:
        """Get the total duration in seconds."""
        return self.total_time_ms / 1000.0


@dataclass(frozen=True)
class SafetyConfig:
    """Configuration for automation safety constraints."""

    allowed_apps: list[str]
    danger_zones: list[BBox]
    max_actions_per_minute: int = 30
    require_confirmation_for: list[ActionType] | None = None
    emergency_stop_hotkey: tuple[str, ...] = ("ctrl", "alt", "shift", "esc")

    def __post_init__(self) -> None:
        """Validate safety configuration."""
        if self.max_actions_per_minute <= 0:
            raise ValueError("max_actions_per_minute must be positive")


@dataclass
class SafetyResult:
    """Result of a safety validation check."""

    is_safe: bool
    violations: list[str]
    warnings: list[str]
    recommended_action: str = ""

    @classmethod
    def safe(cls, warnings: list[str] | None = None) -> SafetyResult:
        """Create a safe result."""
        return cls(
            is_safe=True,
            violations=[],
            warnings=warnings or [],
            recommended_action="proceed",
        )

    @classmethod
    def unsafe(
        cls, violations: list[str], recommended_action: str = "abort"
    ) -> SafetyResult:
        """Create an unsafe result."""
        return cls(
            is_safe=False,
            violations=violations,
            warnings=[],
            recommended_action=recommended_action,
        )
