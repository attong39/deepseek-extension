# Author: Duy BG VN
# Example endpoints cho Planning (tạo/validate/execute kế hoạch)
# Có hỗ trợ queue Celery nếu dự án bật worker; fallback chạy sync an toàn.

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
import Exception
import ImportError
import NotImplementedError
import bool
import dict
import exc
import getattr
import hasattr
import int
import limit
import offset
import payload
import plan_id
import result
import service
import status_eq
import str
import user

# Celery (tuỳ chọn) - import at top
try:
    from apps.backend.data.external.worker import celery_app
except Exception:
    celery_app = None  # fallback

# --- DI từ dự án ---
try:
    from apps.backend.app.dependencies import get_current_user, require_permissions
except Exception as exc:
    raise ImportError(
        "Thiếu app.dependencies. Hãy đảm bảo file app/dependencies.py tồn tại "
        "và khai báo get_current_user, require_permissions."
    ) from exc


# Mock get_plan_service nếu chưa có
def get_plan_service():
    """Mock plan service dependency - cần implement trong app.dependencies."""
    raise NotImplementedError(
        "get_plan_service chưa được implement trong app.dependencies"
    )


# --- Fallback schemas nếu import thất bại ---
try:
    from apps.backend.app.serializers.base_serializers import (
        StatusResponse,  # type: ignore
    )
except Exception:

    class StatusResponse(BaseModel):
        status: str
        detail: str | None = None


try:
    from apps.backend.app.serializers.agent import AgentOut as AgentRead  # type: ignore
except Exception:

    class AgentRead(BaseModel):
        id: str
        name: str


class PlanStep(BaseModel):
    order: int
    action: str
    params: dict[str, Any] = {}


class PlanCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=4, description="Yêu cầu bằng ngôn ngữ tự nhiên")
    goals: list[str] | None = None
    constraints: list[str] | None = None
    agent_id: str | None = None


try:
    from apps.backend.app.serializers.analytics_serializers import (
        PlanRead,  # type: ignore
    )
except Exception:

    class PlanRead(BaseModel):
        id: str
        prompt: str
        steps: list[PlanStep]
        status: str = "draft"
        agent: AgentRead | None = None


class PlanValidateResult(BaseModel):
    valid: bool
    issues: list[str] = []


# Router
router = APIRouter()


# ---- Type hints dịch vụ để IDE/Copilot hiểu ----
class PlanServiceProto:
    async def draft(
        self, req: PlanCreateRequest, created_by: str | None
    ) -> PlanRead: ...

    async def get(self, plan_id: str) -> PlanRead | None: ...

    async def validate(self, plan_id: str) -> PlanValidateResult: ...

    async def list(
        self, limit: int, offset: int, status: str | None
    ) -> list[PlanRead]: ...

    async def execute(
        self, plan_id: str, executed_by: str | None
    ) -> str: ...  # trả về job_id


# ---- Type hints dependencies ----
CurrentUser = Annotated[Any, Depends(get_current_user)]
PlanService = Annotated[Any, Depends(get_plan_service)]

# Pre-computed dependency singletons for permission checks
plans_read_permission = Depends(require_permissions("plans:read"))
plans_write_permission = Depends(require_permissions("plans:write"))
plans_execute_permission = Depends(require_permissions("plans:execute"))


# ---------- ENDPOINTS ----------


@router.get(
    "",
    summary="List plans (example)",
    response_model=list[PlanRead],
    dependencies=[plans_read_permission],
)
async def list_plans_example(
    service: PlanService,
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status_eq: str | None = Query(
        None, alias="status", description="Lọc theo trạng thái kế hoạch"
    ),
):
    plans = await service.list(limit=limit, offset=offset, status=status_eq)
    return plans


@router.post(
    "/draft",
    summary="Draft plan from natural language (example)",
    response_model=PlanRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[plans_write_permission],
)
async def draft_plan_example(
    payload: PlanCreateRequest,
    service: PlanService,
    user: CurrentUser,
):
    """
    Sinh **kế hoạch** (chuỗi bước) từ prompt tự nhiên.
    """
    plan = await service.draft(payload, created_by=getattr(user, "id", None))
    return plan


@router.get(
    "/{plan_id}",
    summary="Get plan (example)",
    response_model=PlanRead,
    dependencies=[plans_read_permission],
)
async def get_plan_example(
    service: PlanService,
    plan_id: str = Path(..., min_length=1),
):
    plan = await service.get(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )
    return plan


@router.post(
    "/{plan_id}/validate",
    summary="Validate plan feasibility/safety (example)",
    response_model=PlanValidateResult,
    dependencies=[plans_write_permission],
)
async def validate_plan_example(
    plan_id: str,
    service: PlanService,
):
    """
    Chạy **rule engine + permission** để kiểm tra an toàn/khả thi trước khi execute.
    """
    _ = await service.validate(plan_id)
    return result


@router.post(
    "/{plan_id}/execute",
    summary="Execute plan (example) — queue với Celery nếu có",
    response_model=StatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[plans_execute_permission],
)
async def execute_plan_example(
    plan_id: str,
    service: PlanService,
    user: CurrentUser,
):
    """
    Thực thi plan:
    - Nếu có `celery_app`: enqueue job → trả về job_id.
    - Nếu không có Celery: chạy async qua service (non-blocking nếu service hỗ trợ), trả về accepted.
    """
    executed_by = getattr(user, "id", None)

    if celery_app:
        # Đặt tên task tuỳ dự án (ví dụ: "tasks.execute_plan")
        try:
            # Sử dụng apply_async thay vì send_task nếu có lỗi
            if hasattr(celery_app, "send_task"):
                task = celery_app.send_task(  # type: ignore
                    "tasks.execute_plan", args=[plan_id, executed_by]
                )
            else:
                task = celery_app.apply_async(  # type: ignore
                    "tasks.execute_plan", args=[plan_id, executed_by]
                )
            return StatusResponse(status="accepted", detail=f"queued: {task.id}")
        except Exception:
            # fallback nếu cấu hình Celery lỗi → gọi service trực tiếp
            job_id = await service.execute(plan_id, executed_by=executed_by)
            return StatusResponse(
                status="accepted", detail=f"fallback-executed: {job_id}"
            )
    else:
        # Fallback: không có Celery → gọi service.execute (nên tự non-blocking)
        job_id = await service.execute(plan_id, executed_by=executed_by)
        return StatusResponse(status="accepted", detail=f"executed: {job_id}")
