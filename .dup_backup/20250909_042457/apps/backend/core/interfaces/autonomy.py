#!/usr/bin/env python3
"""
🤖 Autonomous AI Interfaces/Ports

Abstract interfaces cho Autonomous system theo clean architecture:
- IPlanner: lập kế hoạch từ goal → plan
- ISkillRegistry: quản lý và thực thi skills
- ISafetyPolicy: đánh giá an toàn actions
- IPerceptionService: thu thập context từ môi trường
- ILearningPipeline: học từ feedback và cải thiện

Tuân thủ: Protocol pattern, dependency inversion, type-safe
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable

from apps.backend.core.domain.autonomy import (
import Exception
import dict
import int
import list
import str
    Action,
    AutonomySession,
    Goal,
    Observation,
    Plan,
    SafetyDecision,
)


@runtime_checkable
class IPlanner(Protocol):
    """Interface cho planner - tạo plan từ goal và observation."""

    async def create_plan(
        self,
        goal: Goal,
        observation: Observation | None = None,
        context: dict[str, Any] | None = None,
    ) -> Plan:
        """
        Tạo plan từ goal.

        Args:
            goal: Mục tiêu cần đạt
            observation: Context hiện tại từ perception
            context: Thêm context từ RAG/memory

        Returns:
            Plan với chuỗi actions

        Raises:
            PlannerError: Nếu không tạo được plan hợp lệ
        """
        ...

    async def refine_plan(
        self,
        plan: Plan,
        feedback: list[dict[str, Any]],
    ) -> Plan:
        """
        Tinh chỉnh plan dựa trên feedback từ execution.

        Args:
            plan: Plan hiện tại
            feedback: Feedback từ actions đã thực thi

        Returns:
            Plan đã được tinh chỉnh
        """
        ...


@runtime_checkable
class ISkillRegistry(Protocol):
    """Interface cho skill registry - quản lý kỹ năng AI."""

    def list_available_skills(self) -> list[str]:
        """Liệt kê tất cả skills khả dụng."""
        ...

    def get_skill_info(self, skill_name: str) -> dict[str, Any]:
        """Lấy thông tin chi tiết về skill."""
        ...

    async def execute_skill(
        self,
        action: Action,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Thực thi skill.

        Args:
            action: Action chứa skill name và params
            context: Context thêm cho execution

        Returns:
            Result dict với status và output

        Raises:
            SkillExecutionError: Nếu thực thi thất bại
        """
        ...

    def register_skill(
        self,
        name: str,
        handler: Any,  # Callable hoặc class
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Đăng ký skill mới."""
        ...


@runtime_checkable
class ISafetyPolicy(Protocol):
    """Interface cho safety policy engine."""

    async def evaluate_action(
        self,
        action: Action,
        context: dict[str, Any] | None = None,
    ) -> SafetyDecision:
        """
        Đánh giá tính an toàn của action.

        Args:
            action: Action cần đánh giá
            context: Context thêm (user, session, etc.)

        Returns:
            SafetyDecision với allow/deny và lý do
        """
        ...

    async def evaluate_goal(
        self,
        goal: Goal,
        user_context: dict[str, Any] | None = None,
    ) -> SafetyDecision:
        """Đánh giá tính an toàn của goal ban đầu."""
        ...

    def get_policy_rules(self) -> list[dict[str, Any]]:
        """Lấy danh sách rules đang áp dụng."""
        ...


@runtime_checkable
class IPerceptionService(Protocol):
    """Interface cho perception - thu thập context từ môi trường."""

    async def capture_screen_context(self) -> str | None:
        """Chụp và phân tích màn hình hiện tại."""
        ...

    async def listen_audio(self, duration_seconds: int = 5) -> str | None:
        """Ghi âm và chuyển thành text."""
        ...

    async def read_clipboard(self) -> str | None:
        """Đọc nội dung clipboard."""
        ...

    async def get_current_observation(self) -> Observation:
        """Tạo observation tổng hợp từ các nguồn."""
        ...


@runtime_checkable
class ILearningPipeline(Protocol):
    """Interface cho learning pipeline - học từ feedback."""

    async def ingest_feedback(
        self,
        session: AutonomySession,
        action_results: list[dict[str, Any]],
    ) -> None:
        """
        Nhập feedback từ session để học.

        Args:
            session: Session vừa hoàn thành
            action_results: Kết quả chi tiết từng action
        """
        ...

    async def extract_patterns(self) -> list[dict[str, Any]]:
        """Trích xuất patterns từ historical data."""
        ...

    async def improve_planning(self, planner: IPlanner) -> None:
        """Cải thiện planner dựa trên patterns học được."""
        ...

    async def get_learning_stats(self) -> dict[str, Any]:
        """Lấy thống kê quá trình học."""
        ...


# Repository interfaces cho persistence
class IAutonomySessionRepository(ABC):
    """Repository cho AutonomySession persistence."""

    @abstractmethod
    async def save_session(self, session: AutonomySession) -> None:
        """Lưu session."""
        ...

    @abstractmethod
    async def get_session(self, session_id: str) -> AutonomySession | None:
        """Lấy session theo ID."""
        ...

    @abstractmethod
    async def list_active_sessions(self, user_id: str) -> list[AutonomySession]:
        """Liệt kê sessions đang active của user."""
        ...

    @abstractmethod
    async def get_user_history(
        self,
        user_id: str,
        limit: int = 50,
    ) -> list[AutonomySession]:
        """Lấy lịch sử sessions của user."""
        ...


class IGoalRepository(ABC):
    """Repository cho Goal persistence."""

    @abstractmethod
    async def save_goal(self, goal: Goal) -> None:
        """Lưu goal."""
        ...

    @abstractmethod
    async def get_goal(self, goal_id: str) -> Goal | None:
        """Lấy goal theo ID."""
        ...

    @abstractmethod
    async def list_user_goals(
        self,
        user_id: str,
        status: str | None = None,
    ) -> list[Goal]:
        """Liệt kê goals của user, có thể filter theo status."""
        ...


# Event streaming interface
@runtime_checkable
class IAutonomyEventStreamer(Protocol):
    """Interface cho event streaming qua WebSocket."""

    async def subscribe_to_session(
        self,
        session_id: str,
        callback: Any,  # Callable[[AutonomyEvent], Awaitable[None]]
    ) -> None:
        """Subscribe để nhận events của session."""
        ...

    async def publish_event(self, event: Any) -> None:  # AutonomyEvent
        """Publish event cho subscribers."""
        ...

    async def unsubscribe(self, session_id: str) -> None:
        """Unsubscribe khỏi session."""
        ...


# Exceptions
class PlannerError(Exception):
    """Lỗi từ planner."""


class SkillExecutionError(Exception):
    """Lỗi khi thực thi skill."""


class SafetyPolicyError(Exception):
    """Lỗi từ safety policy."""


class PerceptionError(Exception):
    """Lỗi từ perception service."""


class LearningPipelineError(Exception):
    """Lỗi từ learning pipeline."""
