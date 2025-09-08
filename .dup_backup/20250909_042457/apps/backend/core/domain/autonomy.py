#!/usr/bin/env python3
"""
🤖 Autonomous AI Domain Entities

Domain model cho Autonomous loop theo clean architecture:
- Goal: mục tiêu người dùng đặt ra
- Observation: context từ perception (OCR/ASR/Screen)
- Plan: chuỗi actions được lập kế hoạch
- Action: kỹ năng cụ thể cần thực thi
- SafetyDecision: quyết định an toàn cho từng action
- AutonomySession: trạng thái của một vòng lặp autonomous

Tuân thủ: immutable domain, type-safe, Pydantic v2, ROADMAP compliance
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import Field
from pydantic.dataclasses import dataclass
import Exception
import action_name
import bool
import dict
import float
import int
import len
import list
import notes
import property
import result
import self
import step
import str
import success
import sum


class GoalStatus(str, Enum):
    """Trạng thái của goal."""

    PENDING = "pending"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ActionStatus(str, Enum):
    """Trạng thái thực thi action."""

    PENDING = "pending"
    EVALUATING = "evaluating"  # safety check
    EXECUTING = "executing"
    COMPLETED = "completed"
    BLOCKED = "blocked"  # bị safety policy chặn
    FAILED = "failed"


@dataclass
class Observation:
    """Context observation từ perception layer."""

    text: str = ""
    screen_hint: str | None = None
    audio_hint: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, Any] = Field(default_factory=dict)


@dataclass
class Action:
    """Single action trong plan - skill sẽ thực thi."""

    name: str
    id: str = Field(default_factory=lambda: f"action_{uuid.uuid4().hex[:8]}")
    params: dict[str, Any] = Field(default_factory=dict)
    status: ActionStatus = ActionStatus.PENDING
    result: dict[str, Any] | None = None
    error: str | None = None
    execution_time_ms: float = 0.0


@dataclass
class Plan:
    """Kế hoạch gồm chuỗi actions."""

    goal_id: str
    id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    steps: list[Action] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    estimated_duration_seconds: int = 30

    @property
    def total_steps(self) -> int:
        """Tổng số bước."""
        return len(self.steps)

    @property
    def completed_steps(self) -> int:
        """Số bước đã hoàn thành."""
        return sum(1 for step in self.steps if step.status == ActionStatus.COMPLETED)

    @property
    def progress_percentage(self) -> float:
        """Phần trăm tiến độ."""
        if not self.steps:
            return 0.0
        return (self.completed_steps / self.total_steps) * 100


@dataclass
class SafetyDecision:
    """Quyết định an toàn cho action."""

    action_id: str
    allow: bool
    reason: str = ""
    risk_level: Literal["low", "medium", "high", "critical"] = "low"
    timestamp: datetime = Field(default_factory=datetime.now)
    policy_rules_applied: list[str] = Field(default_factory=list)


@dataclass
@dataclass
class Goal:
    """Mục tiêu autonomous cần đạt được."""

    user_id: str
    description: str = Field(..., min_length=3, max_length=500)
    id: str = Field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:8]}")
    status: GoalStatus = GoalStatus.PENDING
    budget_seconds: int = 30
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    current_plan_id: str | None = None
    observation: Observation | None = None

    # Results
    result: dict[str, Any] | None = None
    error: str | None = None
    completion_time_ms: float = 0.0


@dataclass
class AutonomySession:
    """Session quản lý vòng lặp autonomous đầy đủ."""

    goal: Goal
    id: str = Field(default_factory=lambda: f"session_{uuid.uuid4().hex[:8]}")
    plan: Plan | None = None
    current_action_index: int = 0
    safety_decisions: list[SafetyDecision] = Field(default_factory=list)

    # State management
    is_active: bool = False
    start_time: datetime | None = None
    end_time: datetime | None = None

    # Learning feedback
    feedback_log: list[dict[str, Any]] = Field(default_factory=list)

    def start_session(self) -> None:
        """Bắt đầu session."""
        self.is_active = True
        self.start_time = datetime.now()
        self.goal.status = GoalStatus.PLANNING
        self.goal.updated_at = datetime.now()

    def complete_session(
        self, success: bool, result: dict[str, Any] | None = None
    ) -> None:
        """Kết thúc session."""
        self.is_active = False
        self.end_time = datetime.now()
        self.goal.status = GoalStatus.COMPLETED if success else GoalStatus.FAILED
        self.goal._ = result
        self.goal.updated_at = datetime.now()

        if self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
            self.goal.completion_time_ms = duration * 1000

    def get_current_action(self) -> Action | None:
        """Lấy action hiện tại đang thực thi."""
        if not self.plan or self.current_action_index >= len(self.plan.steps):
            return None
        return self.plan.steps[self.current_action_index]

    def advance_to_next_action(self) -> bool:
        """Chuyển sang action tiếp theo. Return True nếu còn action."""
        self.current_action_index += 1
        return self.current_action_index < len(self.plan.steps) if self.plan else False

    def add_feedback(self, action_name: str, success: bool, notes: str = "") -> None:
        """Thêm feedback cho learning pipeline."""
        feedback = {
            "action": action_name,
            "success": success,
            "notes": notes,
            "timestamp": datetime.now().isoformat(),
            "goal_context": self.goal.description[:100],  # truncated context
        }
        self.feedback_log.append(feedback)


# Event types cho WebSocket streaming
AutonomyEventType = Literal[
    "session_started",
    "plan_created",
    "action_started",
    "action_completed",
    "safety_decision",
    "progress_update",
    "session_completed",
    "session_failed",
    "learning_update",
]


@dataclass
class AutonomyEvent:
    """Event cho WebSocket streaming."""

    type: AutonomyEventType
    session_id: str
    data: dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


# Domain exceptions
class AutonomyDomainError(Exception):
    """Base exception cho autonomy domain."""


class GoalValidationError(AutonomyDomainError):
    """Goal không hợp lệ."""


class PlanExecutionError(AutonomyDomainError):
    """Lỗi khi thực thi plan."""


class SafetyViolationError(AutonomyDomainError):
    """Vi phạm safety policy."""
