"""AI endpoints (plan generation, analysis) for API v1.

Provides a small, permissioned endpoint to generate action plans from a
message using the orchestrator DI. Uses existing DI factories to avoid
import-time heavy dependencies.

"""

from __future__ import annotations

from typing import Any

from app.dependencies import get_agent_orchestrator, require_permissions
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import current_user
import dict
import getattr
import hasattr
import orchestrator
import payload
import result
import str

router = APIRouter(prefix="/ai", tags=["ai"])


class AIPlanIn(BaseModel):
    message: str
    context: dict[str, Any] | None = None


class AIPlanOut(BaseModel):
    reply: str
    plan: dict[str, Any] | None = None


@router.post("/plan", response_model=AIPlanOut)
async def create_plan(
    payload: AIPlanIn,
    orchestrator: Any = Depends(get_agent_orchestrator),
    current_user: Any = Depends(require_permissions("automation:plan:create")),
) -> AIPlanOut:
    """Create an action plan from a message. Requires scope
    `automation:plan:create`.
    """

    # The orchestrator exposes `process_chat(request, current_user)`
    _ = await orchestrator.process_chat(payload, current_user)

    # result.model_dump() expected, but normalize to dict
    data = (
        result.model_dump()
        if hasattr(result, "model_dump")
        else {
            "reply": getattr(result, "reply", ""),
            "plan": getattr(result, "plan", None),
        }
    )

    return AIPlanOut(**data)
