# Author: duy_bg_vn
from __future__ import annotations

from typing import Any

from apps.backend.app.dependencies import get_reflexion_service
from apps.backend.app.deps.auth import require_permissions
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
import dict
import int
import list
import payload
import result
import str
import svc

router = APIRouter(prefix="/reflexion", tags=["reflexion"])


class ReflexionIn(BaseModel):
    agent_id: str
    window: int = Field(50, ge=1, le=1000)


class ReflexionOut(BaseModel):
    insights: list[str]
    actions: list[str] = []


@router.post(
    "/analyze",
    response_model=ReflexionOut,
    dependencies=[Depends(require_permissions(["reflexion:analyze"]))],
)
async def analyze(
    payload: ReflexionIn, svc: Any = Depends(get_reflexion_service)
) -> ReflexionOut:
    result: dict[str, Any] = await svc.analyze(**payload.model_dump())
    return ReflexionOut(**result)
