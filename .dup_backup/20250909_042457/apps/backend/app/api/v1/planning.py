# Author: duy_bg_vn
from __future__ import annotations

from typing import Any

from apps.backend.app.deps.auth import require_permissions
from apps.backend.app.deps.services import get_planning_service
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import dict
import list
import payload
import plan_id
import str
import svc

router = APIRouter(prefix="/planning", tags=["planning"])


class PlanCreateIn(BaseModel):
    goal: str
    context: dict[str, Any] = Field(default_factory=dict)


class PlanOut(BaseModel):
    id: str
    steps: list[dict[str, Any]]
    status: str


@router.post(
    "/plans",
    response_model=PlanOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["plan:create"]))],
)
async def create_plan(
    payload: PlanCreateIn, svc: Any = Depends(get_planning_service)
) -> PlanOut:
    plan = await svc.create_plan(payload.model_dump())
    return PlanOut(**plan)


@router.post(
    "/plans/{plan_id}/execute",
    response_model=PlanOut,
    dependencies=[Depends(require_permissions(["plan:execute"]))],
)
async def execute_plan(
    plan_id: str, svc: Any = Depends(get_planning_service)
) -> PlanOut:
    plan = await svc.execute_plan(plan_id)
    return PlanOut(**plan)
