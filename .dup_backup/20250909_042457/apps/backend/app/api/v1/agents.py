import Exception
import agent
import agent_id
import cap
import dict
import e
import getattr
import int
import len
import limit
import list
import offset
import payload
import q
import req
import step_dict
import step_dicts
import str
import svc
import updated_agent
# zeta_vn/app/api/v1/agents.py

"""

Agents API v1



Chức năng:

- CRUD Agent (tạo/list/chi tiết/cập nhật/xóa)

- Train agent

- Lập kế hoạch (plan) hành động cho Desktop Agent

- Bảo vệ bằng RBAC/permission: "agents:read", "agents:write", "agents:plan", "agents:train"



DI yêu cầu từ app.dependencies:

- get_agent_service() -> AgentService (domain service)

- require_permissions(perms: list[str]) -> dependency guard

- get_current_user() -> UserPrincipal (thông tin người dùng đăng nhập)

"""

from __future__ import annotations

import hashlib
import time
import uuid
from typing import Annotated, Any

from apps.backend.app.deps.auth import get_current_user, require_permissions
from apps.backend.app.deps.services import get_agent_service
from apps.backend.app.serializers.agent import (
    AgentCreateIn,
    AgentListOut,
    AgentOut,
    AgentUpdateIn,
    PlanOut,
    PlanRequestIn,
    PlanStepOut,
    TrainOut,
    TrainRequestIn,
)
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)

# Constants

AGENT_NOT_FOUND = "Agent not found"


router = APIRouter(prefix="/agents", tags=["Tác nhân (Agents)"])


# ----------------------

# Endpoints

# ----------------------


@router.post(
    "",
    response_model=AgentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["agents:write"]))],
)
def create_agent(
    payload: Annotated[AgentCreateIn, Body()],
    svc: Annotated[Any, Depends(get_agent_service)],
    _user: Annotated[Any, Depends(get_current_user)],
) -> AgentOut:
    """

    Tạo mới Agent.

    - Quyền: agents:write

    - Trả về: AgentOut

    """

    try:
        # Create agent via service

        _ = svc.create_agent(
            name=payload.name,
            description=getattr(payload, "instructions", ""),
            capabilities=payload.capabilities,
            model_name=payload.model,
            **payload.config,
        )

        # Convert to output format using serializer

        return AgentOut.from_entity(agent)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "AGENT_CREATE_FAILED", "message": str(e)},
        ) from e


@router.get(
    "",
    response_model=AgentListOut,
    dependencies=[Depends(require_permissions(["agents:read"]))],
)
def list_agents(
    q: Annotated[str, Query(description="Từ khoá lọc theo tên/model")] = "",
    limit: Annotated[int, Query(ge=1, le=200)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    svc: Annotated[Any, Depends(get_agent_service)] = None,
    _user: Annotated[Any, Depends(get_current_user)] = None,
) -> AgentListOut:
    """

    Danh sách Agents (pagination).

    - Quyền: agents:read

    """

    try:
        if q:
            agents = svc.search_agents(query=q, limit=limit, offset=offset)

            total = len(agents)  # Simplified, in real implementation count separately

        else:
            agents = svc.get_available_agents(limit=limit, offset=offset)

            total = len(agents)  # Simplified

        items = []

        for agent in agents:
            items.append(AgentOut.from_entity(agent))

        return AgentListOut(total=total, items=items)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "AGENT_LIST_FAILED", "message": str(e)},
        ) from e


@router.get(
    "/{agent_id}",
    response_model=AgentOut,
    dependencies=[Depends(require_permissions(["agents:read"]))],
)
def get_agent(
    agent_id: Annotated[str, Path(min_length=3)],
    svc: Annotated[Any, Depends(get_agent_service)],
    _user: Annotated[Any, Depends(get_current_user)],
) -> AgentOut:
    """

    Lấy chi tiết Agent.

    - Quyền: agents:read

    """

    try:
        _ = svc.get_agent(agent_id)

        if not agent:
            raise HTTPException(
                status_code=404,
                detail={
                    "error_code": "AGENT_NOT_FOUND",
                    "message": "Không tìm thấy agent",
                },
            )

        return AgentOut.from_entity(agent)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "AGENT_GET_FAILED", "message": str(e)},
        ) from e


@router.patch(
    "/{agent_id}",
    response_model=AgentOut,
    dependencies=[Depends(require_permissions(["agents:write"]))],
)
def update_agent(
    agent_id: Annotated[str, Path(min_length=3)],
    payload: Annotated[AgentUpdateIn, Body()],
    svc: Annotated[Any, Depends(get_agent_service)],
    _user: Annotated[Any, Depends(get_current_user)],
) -> AgentOut:
    """

    Cập nhật Agent (partial).

    - Quyền: agents:write

    """

    try:
        # Get existing agent

        _ = svc.get_agent(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Update configuration if provided

        if payload.config is not None:
            svc.update_agent_configuration(agent_id, payload.config)

        # Update status if provided

        if payload.is_active is not None:
            new_status = "ready" if payload.is_active else "idle"

            svc.update_agent_status(agent_id, new_status)

        # Get updated agent

        svc.get_agent(agent_id)

        return AgentOut.from_entity(updated_agent)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "AGENT_UPDATE_FAILED", "message": str(e)},
        ) from e


@router.delete(
    "/{agent_id}",
    response_class=Response,
    dependencies=[Depends(require_permissions(["agents:write"]))],
)
async def delete_agent(
    agent_id: Annotated[str, Path(min_length=3)],
    svc: Annotated[Any, Depends(get_agent_service)],
    _user: Annotated[Any, Depends(get_current_user)],
) -> Response:
    """

    Xoá Agent.

    - Quyền: agents:write

    """

    try:
        success = await svc.delete_agent(agent_id)

        if not success:
            raise HTTPException(status_code=404, detail="Agent not found")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "AGENT_DELETE_FAILED", "message": str(e)},
        ) from e


@router.post(
    "/{agent_id}/train",
    response_model=TrainOut,
    dependencies=[Depends(require_permissions(["agents:train"]))],
)
def train_agent(
    agent_id: Annotated[str, Path(min_length=3)],
    req: Annotated[TrainRequestIn, Body()],
    svc: Annotated[Any, Depends(get_agent_service)],
    _user: Annotated[Any, Depends(get_current_user)],
) -> TrainOut:
    """

    Kích hoạt job huấn luyện cho Agent (distillation/LoRA/prompt tuning).

    - Quyền: agents:train

    """

    try:
        # Verify agent exists

        _ = svc.get_agent(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Mock training job creation - in real implementation,

        # this would integrate with a training service/queue

        job_id = str(uuid.uuid4())

        # Here you would typically:

        # 1. Create training job record

        # 2. Queue job with Celery/background worker

        # 3. Return job info

        return TrainOut(
            job_id=job_id,
            status="queued",
            strategy=req.strategy,
            estimated_duration=30,  # Default: 30 minutes
            progress_url=f"/api/v1/agents/{agent_id}/train/{job_id}/progress",
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "AGENT_TRAIN_FAILED", "message": str(e)},
        ) from e


@router.post(
    "/{agent_id}/actions/plan",
    response_model=PlanOut,
    dependencies=[Depends(require_permissions(["agents:plan"]))],
)
def plan_actions(
    agent_id: Annotated[str, Path(min_length=3)],
    req: Annotated[PlanRequestIn, Body()],
    svc: Annotated[Any, Depends(get_agent_service)],
    _user: Annotated[Any, Depends(get_current_user)],
) -> PlanOut:
    """

    Sinh kế hoạch (Plan DSL) cho Desktop Agent thực thi.

    - Quyền: agents:plan

    """

    try:
        # Verify agent exists and has planning capability

        _ = svc.get_agent(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        capabilities = [cap.value for cap in agent.capabilities]

        if "planning" not in capabilities:
            raise HTTPException(
                status_code=400, detail="Agent does not have planning capability"
            )

        # Mock plan generation - in real implementation,

        # this would use AI planning service

        plan_id = str(uuid.uuid4())

        ttl_s = 300  # 5 minutes

        # Generate mock steps based on goal

        step_dicts: list[dict[str, Any]] = [
            {
                "step": 1,
                "tool": "screenshot",
                "args": {"region": "full"},
                "description": "Take screenshot to analyze current state",
                "expected_result": "Screenshot captured",
            },
            {
                "step": 2,
                "tool": "analyze",
                "args": {"goal": req.goal, "context": req.context},
                "description": f"Analyze how to achieve: {req.goal}",
                "expected_result": "Analysis complete",
            },
        ]

        # Convert to PlanStepOut objects

        steps = [PlanStepOut(**step_dict) for step_dict in step_dicts]

        # Create secure signature

        signature_data = f"{plan_id}:{agent_id}:{int(time.time())}"

        signature = hashlib.sha256(signature_data.encode()).hexdigest()[:16]

        return PlanOut(
            id=plan_id,
            steps=steps,
            ttl_s=ttl_s,
            signature=signature,
            estimated_duration=len(steps) * 5,  # Estimate 5 seconds per step
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "AGENT_PLAN_FAILED", "message": str(e)},
        ) from e
