#!/usr/bin/env python3
"""
🤖 Autonomous AI Use Cases

Application logic cho Autonomous system:
- CreateAutonomousSessionUseCase: tạo và bắt đầu session
- ExecuteAutonomousLoopUseCase: chạy vòng lặp perception→plan→act→learn
- ManageAutonomousSessionUseCase: quản lý session lifecycle
- AutonomousLearningUseCase: pipeline học từ feedback

Tuân thủ: Clean Architecture, dependency injection, error handling
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from apps.backend.core.domain.autonomy import (
import Exception
import ValueError
import a
import action
import action_results
import bool
import budget_seconds
import dict
import e
import enumerate
import event_streamer
import goal_description
import goal_repo
import i
import include_perception
import int
import learning_pipeline
import len
import list
import perception
import planner
import result
import s
import safety_policy
import self
import session
import session_id
import session_repo
import skill_registry
import str
import sum
import user_id
    ActionStatus,
    AutonomyEvent,
    AutonomySession,
    Goal,
    GoalStatus,
)
from apps.backend.core.interfaces.autonomy import (
    IAutonomyEventStreamer,
    IAutonomySessionRepository,
    IGoalRepository,
    ILearningPipeline,
    IPerceptionService,
    IPlanner,
    ISafetyPolicy,
    ISkillRegistry,
    PlannerError,
    SafetyPolicyError,
)

logger = logging.getLogger(__name__)


class CreateAutonomousSessionUseCase:
    """Use case tạo và khởi tạo autonomous session."""

    def __init__(
        self,
        goal_repo: IGoalRepository,
        session_repo: IAutonomySessionRepository,
        planner: IPlanner,
        safety_policy: ISafetyPolicy,
        perception: IPerceptionService,
        event_streamer: IAutonomyEventStreamer,
    ) -> None:
        self.goal_repo = goal_repo
        self.session_repo = session_repo
        self.planner = planner
        self.safety_policy = safety_policy
        self.perception = perception
        self.event_streamer = event_streamer

    async def execute(
        self,
        goal_description: str,
        user_id: str,
        budget_seconds: int = 30,
        include_perception: bool = True,
    ) -> AutonomySession:
        """
        Tạo autonomous session mới.

        Args:
            goal_description: Mô tả mục tiêu
            user_id: ID người dùng
            budget_seconds: Thời gian tối đa cho session
            include_perception: Có thu thập context không

        Returns:
            AutonomySession đã được khởi tạo

        Raises:
            SafetyPolicyError: Nếu goal bị chặn bởi safety policy
            PlannerError: Nếu không tạo được plan
        """
        # 1. Tạo goal
        goal = Goal(
            description=goal_description,
            user_id=user_id,
            budget_seconds=budget_seconds,
        )

        # 2. Safety check cho goal
        goal_safety = await self.safety_policy.evaluate_goal(goal, {"user_id": user_id})
        if not goal_safety.allow:
            raise SafetyPolicyError(f"Goal blocked: {goal_safety.reason}")

        # 3. Thu thập observation nếu cần
        observation = None
        if include_perception:
            try:
                observation = await self.perception.get_current_observation()
                goal.observation = observation
            except Exception as e:
                logger.warning(f"Failed to get observation: {e}")

        # 4. Tạo plan
        try:
            plan = await self.planner.create_plan(goal, observation)
            goal.current_plan_id = plan.id
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            raise PlannerError(f"Cannot create plan: {e}")

        # 5. Tạo session
        _ = AutonomySession(goal=goal, plan=plan)
        session.start_session()

        # 6. Persist
        await self.goal_repo.save_goal(goal)
        await self.session_repo.save_session(session)

        # 7. Notify
        event = AutonomyEvent(
            type="session_started",
            session_id=session.id,
            data={
                "goal": goal.description,
                "plan_steps": len(plan.steps),
                "budget_seconds": budget_seconds,
            },
        )
        await self.event_streamer.publish_event(event)

        logger.info(
            f"Created autonomous session {session.id} for goal: {goal_description[:50]}..."
        )

        return session


class ExecuteAutonomousLoopUseCase:
    """Use case thực thi vòng lặp autonomous chính."""

    def __init__(
        self,
        session_repo: IAutonomySessionRepository,
        skill_registry: ISkillRegistry,
        safety_policy: ISafetyPolicy,
        event_streamer: IAutonomyEventStreamer,
        learning_pipeline: ILearningPipeline,
    ) -> None:
        self.session_repo = session_repo
        self.skill_registry = skill_registry
        self.safety_policy = safety_policy
        self.event_streamer = event_streamer
        self.learning_pipeline = learning_pipeline

    async def execute(self, session: AutonomySession) -> AutonomySession:
        """
        Thực thi autonomous loop cho session.

        Args:
            session: Session cần thực thi

        Returns:
            Session đã hoàn thành

        Raises:
            SafetyPolicyError: Nếu action bị chặn
            SkillExecutionError: Nếu skill thất bại
        """
        if not session.plan:
            raise ValueError("Session không có plan")

        session.goal.status = GoalStatus.EXECUTING
        await self.session_repo.save_session(session)

        action_results: list[dict[str, Any]] = []

        try:
            # Thực thi từng action trong plan
            for i, action in enumerate(session.plan.steps):
                # Update current action index
                session.current_action_index = i

                # Publish action start event
                event = AutonomyEvent(
                    type="action_started",
                    session_id=session.id,
                    data={
                        "action": action.name,
                        "params": action.params,
                        "step": i + 1,
                        "total": len(session.plan.steps),
                    },
                )
                await self.event_streamer.publish_event(event)

                # Safety evaluation
                action.status = ActionStatus.EVALUATING
                safety_decision = await self.safety_policy.evaluate_action(
                    action, {"session_id": session.id, "user_id": session.goal.user_id}
                )
                session.safety_decisions.append(safety_decision)

                # Publish safety decision
                safety_event = AutonomyEvent(
                    type="safety_decision",
                    session_id=session.id,
                    data={
                        "action": action.name,
                        "allowed": safety_decision.allow,
                        "reason": safety_decision.reason,
                        "risk_level": safety_decision.risk_level,
                    },
                )
                await self.event_streamer.publish_event(safety_event)

                if not safety_decision.allow:
                    action.status = ActionStatus.BLOCKED
                    action.error = f"Blocked by safety: {safety_decision.reason}"
                    logger.warning(
                        f"Action {action.name} blocked: {safety_decision.reason}"
                    )

                    # Add negative feedback
                    session.add_feedback(
                        action.name, False, f"Safety blocked: {safety_decision.reason}"
                    )
                    continue

                # Execute action
                action.status = ActionStatus.EXECUTING
                start_time = time.perf_counter()

                try:
                    _ = await self.skill_registry.execute_skill(action)
                    execution_time = (time.perf_counter() - start_time) * 1000

                    action.status = ActionStatus.COMPLETED
                    action._ = result
                    action.execution_time_ms = execution_time

                    # Add positive feedback
                    session.add_feedback(action.name, True, "Completed successfully")

                    action_results.append(
                        {
                            "action": action.name,
                            "success": True,
                            "result": result,
                            "execution_time_ms": execution_time,
                        }
                    )

                    logger.info(
                        f"Action {action.name} completed in {execution_time:.1f}ms"
                    )

                except Exception as e:
                    execution_time = (time.perf_counter() - start_time) * 1000
                    action.status = ActionStatus.FAILED
                    action.error = str(e)
                    action.execution_time_ms = execution_time

                    # Add negative feedback
                    session.add_feedback(action.name, False, f"Execution failed: {e}")

                    action_results.append(
                        {
                            "action": action.name,
                            "success": False,
                            "error": str(e),
                            "execution_time_ms": execution_time,
                        }
                    )

                    logger.error(f"Action {action.name} failed: {e}")

                # Publish action completion
                completion_event = AutonomyEvent(
                    type="action_completed",
                    session_id=session.id,
                    data={
                        "action": action.name,
                        "status": action.status.value,
                        "result": action.result,
                        "error": action.error,
                        "execution_time_ms": action.execution_time_ms,
                    },
                )
                await self.event_streamer.publish_event(completion_event)

                # Publish progress
                progress_event = AutonomyEvent(
                    type="progress_update",
                    session_id=session.id,
                    data={
                        "completed": i + 1,
                        "total": len(session.plan.steps),
                        "percentage": ((i + 1) / len(session.plan.steps)) * 100,
                    },
                )
                await self.event_streamer.publish_event(progress_event)

                # Save intermediate state
                await self.session_repo.save_session(session)

                # Brief pause để không overwhelm system
                await asyncio.sleep(0.1)

            # Complete session
            completed_actions = sum(
                1 for a in session.plan.steps if a.status == ActionStatus.COMPLETED
            )
            success = completed_actions > 0  # Partial success acceptable

            session.complete_session(
                success=success,
                result={
                    "completed_actions": completed_actions,
                    "total_actions": len(session.plan.steps),
                    "action_results": action_results,
                },
            )

            # Persist final state
            await self.session_repo.save_session(session)

            # Publish completion
            completion_event = AutonomyEvent(
                type="session_completed" if success else "session_failed",
                session_id=session.id,
                data={
                    "success": success,
                    "completed_actions": completed_actions,
                    "total_actions": len(session.plan.steps),
                    "total_time_ms": session.goal.completion_time_ms,
                },
            )
            await self.event_streamer.publish_event(completion_event)

            # Feed to learning pipeline
            try:
                await self.learning_pipeline.ingest_feedback(session, action_results)

                learning_event = AutonomyEvent(
                    type="learning_update",
                    session_id=session.id,
                    data={"feedback_ingested": len(action_results)},
                )
                await self.event_streamer.publish_event(learning_event)

            except Exception as e:
                logger.warning(f"Learning pipeline failed: {e}")

            return session

        except Exception as e:
            # Emergency completion on error
            session.complete_session(success=False, result={"error": str(e)})
            await self.session_repo.save_session(session)

            error_event = AutonomyEvent(
                type="session_failed", session_id=session.id, data={"error": str(e)}
            )
            await self.event_streamer.publish_event(error_event)

            raise


class ManageAutonomousSessionUseCase:
    """Use case quản lý lifecycle của autonomous sessions."""

    def __init__(
        self,
        session_repo: IAutonomySessionRepository,
        event_streamer: IAutonomyEventStreamer,
    ) -> None:
        self.session_repo = session_repo
        self.event_streamer = event_streamer

    async def get_session(self, session_id: str) -> AutonomySession | None:
        """Lấy session theo ID."""
        return await self.session_repo.get_session(session_id)

    async def list_user_sessions(self, user_id: str) -> list[AutonomySession]:
        """Liệt kê sessions của user."""
        return await self.session_repo.get_user_history(user_id)

    async def cancel_session(self, session_id: str) -> None:
        """Hủy session đang chạy."""
        _ = await self.session_repo.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        if session.is_active:
            session.complete_session(success=False, result={"cancelled": True})
            session.goal.status = GoalStatus.CANCELLED
            await self.session_repo.save_session(session)

            # Notify cancellation
            event = AutonomyEvent(
                type="session_failed", session_id=session_id, data={"cancelled": True}
            )
            await self.event_streamer.publish_event(event)


class AutonomousLearningUseCase:
    """Use case cho learning pipeline."""

    def __init__(
        self,
        learning_pipeline: ILearningPipeline,
        session_repo: IAutonomySessionRepository,
        planner: IPlanner,
    ) -> None:
        self.learning_pipeline = learning_pipeline
        self.session_repo = session_repo
        self.planner = planner

    async def trigger_learning_cycle(self, user_id: str) -> dict[str, Any]:
        """
        Trigger một chu kỳ học từ historical sessions.

        Args:
            user_id: User để học từ data của họ

        Returns:
            Stats về quá trình học
        """
        # Get recent sessions for learning
        sessions = await self.session_repo.get_user_history(user_id, limit=100)
        completed_sessions = [
            s for s in sessions if s.goal.status == GoalStatus.COMPLETED
        ]

        if not completed_sessions:
            return {"message": "No completed sessions to learn from"}

        # Extract patterns
        patterns = await self.learning_pipeline.extract_patterns()

        # Improve planner if patterns found
        if patterns:
            await self.learning_pipeline.improve_planning(self.planner)

        # Get stats
        stats = await self.learning_pipeline.get_learning_stats()

        return {
            "sessions_analyzed": len(completed_sessions),
            "patterns_extracted": len(patterns),
            "learning_stats": stats,
        }
