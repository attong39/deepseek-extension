#!/usr/bin/env python3
"""
🤖 Autonomous AI API Router

FastAPI router cho Autonomous system:
- REST endpoints: goals, sessions, planning
- WebSocket streaming cho real-time events
- Integration với existing ZETA_AI infrastructure

Tuân thủ: async/await, Pydantic schemas, error handling, auth
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.app.api.interfaces.autonomy import (
import Exception
import bool
import completed_session
import dict
import e
import event
import event_streamer
import float
import goal_repo
import hasattr
import int
import learning_pipeline
import len
import list
import perception
import planner
import request
import result
import safety_policy
import session
import session_id
import session_repo
import skill_name
import skill_registry
import status
import str
import user_id
import websocket
    IAutonomyEventStreamer,
    IAutonomySessionRepository,
    IGoalRepository,
    ILearningPipeline,
    IPerceptionService,
    IPlanner,
    ISafetyPolicy,
    ISkillRegistry,
)
from apps.backend.app.api.services.autonomy_planner import RuleBasedPlanner
from apps.backend.app.api.services.autonomy_safety import RuleBasedSafetyPolicy
from apps.backend.app.api.services.autonomy_skills import SafeSkillRegistry
from apps.backend.app.api.use_cases.autonomy import (
    AutonomousLearningUseCase,
    CreateAutonomousSessionUseCase,
    ExecuteAutonomousLoopUseCase,
)
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Create router
autonomy_router = APIRouter(prefix="/api/v1/autonomy", tags=["autonomy"])


# ---- Request/Response Schemas ----


class CreateGoalRequest(BaseModel):
    """Request để tạo goal mới."""

    description: str = Field(..., min_length=3, max_length=500)
    budget_seconds: int = Field(default=30, ge=5, le=300)
    include_perception: bool = Field(default=True)


class GoalResponse(BaseModel):
    """Response cho goal."""

    id: str
    description: str
    status: str
    user_id: str
    budget_seconds: int
    created_at: str
    current_plan_id: str | None = None


class SessionResponse(BaseModel):
    """Response cho autonomous session."""

    id: str
    goal: GoalResponse
    is_active: bool
    progress_percentage: float
    start_time: str | None = None
    end_time: str | None = None


class SkillListResponse(BaseModel):
    """Response cho danh sách skills."""

    skills: list[str]
    total: int


class SkillInfoResponse(BaseModel):
    """Response cho thông tin skill."""

    name: str
    description: str
    params: dict[str, Any]
    safety_level: str
    category: str


class SafetyRulesResponse(BaseModel):
    """Response cho safety rules."""

    rules: list[dict[str, Any]]
    total_categories: int


class LearningStatsResponse(BaseModel):
    """Response cho learning statistics."""

    sessions_analyzed: int
    patterns_extracted: int
    learning_stats: dict[str, Any]


# ---- Dependency Injection ----


def get_skill_registry() -> ISkillRegistry:
    """Get skill registry instance."""
    return SafeSkillRegistry()


def get_safety_policy() -> ISafetyPolicy:
    """Get safety policy instance."""
    return RuleBasedSafetyPolicy()


def get_planner(
    skill_registry: ISkillRegistry = Depends(get_skill_registry),
) -> IPlanner:
    """Get planner instance."""
    return RuleBasedPlanner()


def get_perception_service() -> IPerceptionService:
    """Get perception service (placeholder)."""
    # TODO: Implement actual perception service
    from apps.backend.app.api.services.autonomy_perception import DemoPerceptionService

    return DemoPerceptionService()


def get_event_streamer() -> IAutonomyEventStreamer:
    """Get event streamer (placeholder)."""
    # TODO: Implement actual event streamer
    from apps.backend.app.api.services.autonomy_events import InMemoryEventStreamer

    return InMemoryEventStreamer()


def get_session_repository() -> IAutonomySessionRepository:
    """Get session repository (placeholder)."""
    # TODO: Implement actual repository with DB
    from apps.backend.app.api.adapters.repositories.autonomy import (
        InMemorySessionRepository,
    )

    return InMemorySessionRepository()


def get_goal_repository() -> IGoalRepository:
    """Get goal repository (placeholder)."""
    # TODO: Implement actual repository with DB
    from apps.backend.app.api.adapters.repositories.autonomy import (
        InMemoryGoalRepository,
    )

    return InMemoryGoalRepository()


def get_learning_pipeline() -> ILearningPipeline:
    """Get learning pipeline (placeholder)."""
    # TODO: Implement actual learning pipeline
    from apps.backend.app.api.services.autonomy_learning import DemoLearningPipeline

    return DemoLearningPipeline()


# ---- REST Endpoints ----


@autonomy_router.get("/skills", response_model=SkillListResponse)
async def list_skills(
    skill_registry: ISkillRegistry = Depends(get_skill_registry),
) -> SkillListResponse:
    """Liệt kê tất cả skills khả dụng."""
    skills = skill_registry.list_available_skills()
    return SkillListResponse(skills=skills, total=len(skills))


@autonomy_router.get("/skills/{skill_name}", response_model=SkillInfoResponse)
async def get_skill_info(
    skill_name: str,
    skill_registry: ISkillRegistry = Depends(get_skill_registry),
) -> SkillInfoResponse:
    """Lấy thông tin chi tiết về skill."""
    info = skill_registry.get_skill_info(skill_name)

    if "error" in info:
        raise HTTPException(status_code=404, detail=f"Skill {skill_name} not found")

    return SkillInfoResponse(
        name=skill_name,
        description=info.get("description", ""),
        params=info.get("params", {}),
        safety_level=info.get("safety_level", "unknown"),
        category=info.get("category", "unknown"),
    )


@autonomy_router.get("/safety/rules", response_model=SafetyRulesResponse)
async def get_safety_rules(
    safety_policy: ISafetyPolicy = Depends(get_safety_policy),
) -> SafetyRulesResponse:
    """Lấy danh sách safety rules."""
    rules = safety_policy.get_policy_rules()
    return SafetyRulesResponse(rules=rules, total_categories=len(rules))


@autonomy_router.post("/goals", response_model=GoalResponse)
async def create_goal(
    request: CreateGoalRequest,
    # TODO: Get user_id from auth
    user_id: str = "demo_user",
    goal_repo: IGoalRepository = Depends(get_goal_repository),
    session_repo: IAutonomySessionRepository = Depends(get_session_repository),
    planner: IPlanner = Depends(get_planner),
    safety_policy: ISafetyPolicy = Depends(get_safety_policy),
    perception: IPerceptionService = Depends(get_perception_service),
    event_streamer: IAutonomyEventStreamer = Depends(get_event_streamer),
) -> GoalResponse:
    """Tạo goal mới và session."""
    try:
        # Create session use case
        create_session_uc = CreateAutonomousSessionUseCase(
            goal_repo=goal_repo,
            session_repo=session_repo,
            planner=planner,
            safety_policy=safety_policy,
            perception=perception,
            event_streamer=event_streamer,
        )

        # Execute use case
        _ = await create_session_uc.execute(
            goal_description=request.description,
            user_id=user_id,
            budget_seconds=request.budget_seconds,
            include_perception=request.include_perception,
        )

        goal = session.goal

        return GoalResponse(
            id=goal.id,
            description=goal.description,
            status=goal.status.value,
            user_id=goal.user_id,
            budget_seconds=goal.budget_seconds,
            created_at=goal.created_at.isoformat(),
            current_plan_id=goal.current_plan_id,
        )

    except Exception as e:
        logger.error(f"Failed to create goal: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@autonomy_router.get("/goals", response_model=list[GoalResponse])
async def list_goals(
    user_id: str = "demo_user",  # TODO: Get from auth
    status: str | None = None,
    goal_repo: IGoalRepository = Depends(get_goal_repository),
) -> list[GoalResponse]:
    """Liệt kê goals của user."""
    try:
        goals = await goal_repo.list_user_goals(user_id, status)

        return [
            GoalResponse(
                id=goal.id,
                description=goal.description,
                status=goal.status.value,
                user_id=goal.user_id,
                budget_seconds=goal.budget_seconds,
                created_at=goal.created_at.isoformat(),
                current_plan_id=goal.current_plan_id,
            )
            for goal in goals
        ]

    except Exception as e:
        logger.error(f"Failed to list goals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@autonomy_router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(
    user_id: str = "demo_user",  # TODO: Get from auth
    session_repo: IAutonomySessionRepository = Depends(get_session_repository),
) -> list[SessionResponse]:
    """Liệt kê sessions của user."""
    try:
        sessions = await session_repo.get_user_history(user_id)

        return [
            SessionResponse(
                id=session.id,
                goal=GoalResponse(
                    id=session.goal.id,
                    description=session.goal.description,
                    status=session.goal.status.value,
                    user_id=session.goal.user_id,
                    budget_seconds=session.goal.budget_seconds,
                    created_at=session.goal.created_at.isoformat(),
                    current_plan_id=session.goal.current_plan_id,
                ),
                is_active=session.is_active,
                progress_percentage=session.plan.progress_percentage
                if session.plan
                else 0.0,
                start_time=session.start_time.isoformat()
                if session.start_time
                else None,
                end_time=session.end_time.isoformat() if session.end_time else None,
            )
            for session in sessions
        ]

    except Exception as e:
        logger.error(f"Failed to list sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@autonomy_router.post("/sessions/{session_id}/execute")
async def execute_session(
    session_id: str,
    session_repo: IAutonomySessionRepository = Depends(get_session_repository),
    skill_registry: ISkillRegistry = Depends(get_skill_registry),
    safety_policy: ISafetyPolicy = Depends(get_safety_policy),
    event_streamer: IAutonomyEventStreamer = Depends(get_event_streamer),
    learning_pipeline: ILearningPipeline = Depends(get_learning_pipeline),
) -> dict[str, Any]:
    """Thực thi autonomous session."""
    try:
        # Get session
        _ = await session_repo.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Execute session use case
        execute_uc = ExecuteAutonomousLoopUseCase(
            session_repo=session_repo,
            skill_registry=skill_registry,
            safety_policy=safety_policy,
            event_streamer=event_streamer,
            learning_pipeline=learning_pipeline,
        )

        await execute_uc.execute(session)

        return {
            "session_id": session_id,
            "status": completed_session.goal.status.value,
            "completed_actions": completed_session.plan.completed_steps
            if completed_session.plan
            else 0,
            "total_actions": completed_session.plan.total_steps
            if completed_session.plan
            else 0,
        }

    except Exception as e:
        logger.error(f"Failed to execute session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@autonomy_router.post("/learning/trigger", response_model=LearningStatsResponse)
async def trigger_learning(
    user_id: str = "demo_user",  # TODO: Get from auth
    learning_pipeline: ILearningPipeline = Depends(get_learning_pipeline),
    session_repo: IAutonomySessionRepository = Depends(get_session_repository),
    planner: IPlanner = Depends(get_planner),
) -> LearningStatsResponse:
    """Trigger learning cycle."""
    try:
        learning_uc = AutonomousLearningUseCase(
            learning_pipeline=learning_pipeline,
            session_repo=session_repo,
            planner=planner,
        )

        _ = await learning_uc.trigger_learning_cycle(user_id)

        return LearningStatsResponse(
            sessions_analyzed=result.get("sessions_analyzed", 0),
            patterns_extracted=result.get("patterns_extracted", 0),
            learning_stats=result.get("learning_stats", {}),
        )

    except Exception as e:
        logger.error(f"Failed to trigger learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---- WebSocket Endpoint ----


@autonomy_router.websocket("/ws/{session_id}")
async def websocket_autonomous_loop(
    websocket: WebSocket,
    session_id: str,
    session_repo: IAutonomySessionRepository = Depends(get_session_repository),
    skill_registry: ISkillRegistry = Depends(get_skill_registry),
    safety_policy: ISafetyPolicy = Depends(get_safety_policy),
    event_streamer: IAutonomyEventStreamer = Depends(get_event_streamer),
    learning_pipeline: ILearningPipeline = Depends(get_learning_pipeline),
) -> None:
    """
    WebSocket endpoint cho real-time autonomous loop.

    Client connects → server executes session → streams events back
    """
    await websocket.accept()

    try:
        # Get session
        _ = await session_repo.get_session(session_id)
        if not session:
            await websocket.send_json({"error": "Session not found"})
            return

        # Subscribe to events
        async def send_event_to_client(event: Any) -> None:
            try:
                await websocket.send_json(
                    event.model_dump() if hasattr(event, "model_dump") else event
                )
            except Exception as e:
                logger.error(f"Failed to send event to client: {e}")

        await event_streamer.subscribe_to_session(session_id, send_event_to_client)

        # Execute autonomous loop
        execute_uc = ExecuteAutonomousLoopUseCase(
            session_repo=session_repo,
            skill_registry=skill_registry,
            safety_policy=safety_policy,
            event_streamer=event_streamer,
            learning_pipeline=learning_pipeline,
        )

        await execute_uc.execute(session)

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        try:
            await websocket.send_json({"error": str(e)})
        except Exception:
            pass  # Connection may be closed
    finally:
        # Cleanup
        try:
            await event_streamer.unsubscribe(session_id)
        except Exception:
            pass
