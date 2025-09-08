Nhận xét nhanh (điểm cần tối ưu)

Namespace & DI: các file đang import từ app.dependencies/repo ngay trong handler → lệch chuẩn zeta_vn.app.* và phá vỡ DI (nên tiêm repo/use-case qua Depends).

RBAC/role check trùng lặp: route đã require_permissions(...) nhưng vẫn kiểm current_user.role == "admin" trong code → nên gom về RBAC + check sở hữu theo dependency (owner check).

Tổ chức router: tags=["agents"]/["plans"] thiếu tag version; chưa có aggregator v1 để main chỉ include 1 lần → dễ drift khi mở rộng.

Schema/serialization: plans_example đặt schema inline → nên tách sang core/serializers cho thống nhất; agents_example đã dùng serializer chuẩn — tốt, giữ nguyên hướng đó.

Audit/Repo import trong handler: get/delete/enable/disable đang import ...Repository ngay bên trong function → thay bằng repo/use-case tiêm qua dependency.

Bản tối ưu đề xuất (drop-in patches)

1) __init__.py (làm aggregator v1)

Mục tiêu: main chỉ include một router v1; thêm tag v1 để OpenAPI rõ version.

# zeta_vn/app/api/v1/__init__.py

"""API v1 aggregator."""

from __future__ import annotations
from fastapi import APIRouter

from .agents_example import router as agents_router
from .plans_example import router as plans_router

router = APIRouter()

# các sub-router đã prefix "/agents", "/plans" => ghép với "/api/v1" tại main

router.include_router(agents_router, tags=["v1", "agents"])
router.include_router(plans_router, tags=["v1", "plans"])

__all__ = ["router"]

Lý do: file hiện tại chưa export gì; chuyển thành aggregator để chuẩn hoá include từ main.

2) agents_example.py (chuẩn DI + RBAC + namespace)

Đổi root import zeta_vn.app.*.

Bỏ import Repository trong thân hàm; tiêm qua Depends.

Thêm tag v1. Giữ serializer hiện có.

# zeta_vn/app/api/v1/agents_example.py

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from zeta_vn.app.dependencies import (
    AuditContextDep,
    CreateAgentUC,
    UpdateAgentUC,
    get_current_user,
    require_permissions,
    get_agent_repository,   # <-- bổ sung trong dependencies
)
from zeta_vn.core.domain.entities.user import User
from zeta_vn.app.serializers.agent import AgentCreateIn, AgentOut, AgentUpdateIn
from zeta_vn.data.repositories.agent_repository import AgentRepository  # type: ignore

router = APIRouter(prefix="/agents", tags=["v1", "agents"])

CurrentUser = Annotated[User, Depends(get_current_user)]
AgentRepoDep = Annotated[AgentRepository, Depends(get_agent_repository)]

@router.post("", response_model=AgentOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permissions("agent:create"))])
async def create_agent(
    payload: AgentCreateIn,
    use_case: CreateAgentUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> AgentOut:
    try:
        vo = payload.to_vo()
        vo.owner_id = current_user.id
        agent = await use_case.execute(vo, audit_context)
        return AgentOut.from_entity(agent)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create agent")

@router.put("/{agent_id}", response_model=AgentOut,
            dependencies=[Depends(require_permissions("agent:update"))])
async def update_agent(
    agent_id: str,
    payload: AgentUpdateIn,
    use_case: UpdateAgentUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> AgentOut:
    try:
        updates = payload.to_vo()
        agent = await use_case.execute(agent_id=agent_id, updates=updates, actor_id=current_user.id, audit_context=audit_context)
        return AgentOut.from_entity(agent)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

@router.get("/{agent_id}", response_model=AgentOut,
            dependencies=[Depends(require_permissions("agent:read"))])
async def get_agent(
    agent_id: str,
    repo: AgentRepoDep,
    current_user: CurrentUser,
) -> AgentOut:
    agent = await repo.get_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    # owner-or-admin (nên thay bằng dependency require_agent_owner ở tầng deps)
    if agent.owner_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return AgentOut.from_entity(agent)

@router.get("", response_model=list[AgentOut],
            dependencies=[Depends(require_permissions("agent:read"))])
async def list_agents(
    repo: AgentRepoDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> list[AgentOut]:
    agents = await (repo.list_all(skip=skip, limit=limit) if "admin:*" in (current_user.scopes or [])
                    else repo.get_by_owner(current_user.id, skip=skip, limit=limit))
    return [AgentOut.from_entity(a) for a in agents]

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_permissions("agent:delete"))])
async def delete_agent(
    agent_id: str,
    repo: AgentRepoDep,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> None:
    from zeta_vn.core.services.audit_service import AuditService
    from zeta_vn.data.repositories.audit_repository import AuditRepository

    agent = await repo.get_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    if agent.owner_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    ok = await repo.delete(agent_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete agent")

    # audit
    audit = AuditService(AuditRepository(repo.session))  # hoặc tiêm qua Depends nếu đã có
    await audit.log_action(actor_id=current_user.id, action="agent_delete", resource_type="agent",
                           resource_id=agent_id, context=audit_context)

Lý do: loại import repo trong handler, tiêu chuẩn hoá tag/version, và thống nhất namespace, đúng kiến trúc DI.

3) plans_example.py (chuẩn DI + tách serializer + trạng thái)

Đổi root import zeta_vn.*.

Tiêm PlanRepository/AuditService qua Depends; bỏ import “trong hàm”.

Thêm tag v1. Gợi ý tách schema ra core/serializers/plan.py.

# zeta_vn/app/api/v1/plans_example.py

from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from zeta_vn.app.dependencies import (
    ApprovePlanUC, AuditContextDep, CreatePlanUC, ExecutePlanUC,
    get_current_user, require_permissions, get_plan_repository, get_audit_service
)
from zeta_vn.core.domain.entities.user import User
from zeta_vn.data.repositories.plan_repository import PlanRepository  # type: ignore
from zeta_vn.core.services.audit_service import AuditService

from pydantic import BaseModel, Field

router = APIRouter(prefix="/plans", tags=["v1", "plans"])

CurrentUser = Annotated[User, Depends(get_current_user)]
PlanRepoDep = Annotated[PlanRepository, Depends(get_plan_repository)]
AuditSvcDep = Annotated[AuditService, Depends(get_audit_service)]

# ... giữ nguyên PlanCreateIn/PlanStepCreateIn/PlanOut như hiện tại

@router.post("", response_model=PlanOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permissions("plan:create"))])
async def create_plan(
    payload: PlanCreateIn,
    use_case: CreatePlanUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    try:
        vo = payload.to_vo() | {"user_id": current_user.id}
        plan = await use_case.execute(vo, audit_context)
        return PlanOut.from_entity(plan)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create plan")

@router.post("/{plan_id}/steps", response_model=PlanOut,
             dependencies=[Depends(require_permissions("plan:update"))])
async def add_plan_step(
    plan_id: str,
    step_payload: 'PlanStepCreateIn',
    repo: PlanRepoDep,
    audit: AuditSvcDep,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    plan = await repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    if plan.user_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        plan.add_step(action=step_payload.action, description=step_payload.description,
                      parameters=step_payload.parameters, dependencies=step_payload.dependencies)
        updated = await repo.update(plan)
        await audit.log_action(actor_id=current_user.id, action="plan_step_add",
                               resource_type="plan", resource_id=plan_id, context=audit_context,
                               details={"action": step_payload.action})
        return PlanOut.from_entity(updated)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

@router.post("/{plan_id}/approve", response_model=PlanOut,
             dependencies=[Depends(require_permissions("plan:approve"))])
async def approve_plan(
    plan_id: str,
    use_case: ApprovePlanUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    try:
        plan = await use_case.execute(plan_id=plan_id, approved_by=current_user.id, audit_context=audit_context)
        return PlanOut.from_entity(plan)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

@router.post("/{plan_id}/execute", response_model=PlanOut,
             dependencies=[Depends(require_permissions("plan:execute"))])
async def execute_plan(
    plan_id: str,
    use_case: ExecutePlanUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    try:
        plan = await use_case.execute(plan_id=plan_id, executor_id=current_user.id, audit_context=audit_context)
        return PlanOut.from_entity(plan)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

@router.get("/{plan_id}", response_model=PlanOut,
            dependencies=[Depends(require_permissions("plan:read"))])
async def get_plan(
    plan_id: str,
    repo: PlanRepoDep,
    current_user: CurrentUser,
) -> PlanOut:
    plan = await repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    if plan.user_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return PlanOut.from_entity(plan)

@router.get("", response_model=list[PlanOut],
            dependencies=[Depends(require_permissions("plan:read"))])
async def list_plans(
    repo: PlanRepoDep,
    current_user: CurrentUser,
    skip: int = 0, limit: int = 100, status_filter: str | None = None,
) -> list[PlanOut]:
    plans = await (repo.list_all(skip=skip, limit=limit, status=status_filter)
                   if "admin:*" in (current_user.scopes or [])
                   else repo.get_by_user(current_user.id, skip=skip, limit=limit, status=status_filter))
    return [PlanOut.from_entity(p) for p in plans]

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_permissions("plan:delete"))])
async def delete_plan(
    plan_id: str,
    repo: PlanRepoDep,
    audit: AuditSvcDep,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> None:
    plan = await repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    if plan.user_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if plan.status.value not in ["draft", "failed", "cancelled"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can only delete draft, failed, or cancelled plans")
    ok = await repo.delete(plan_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete plan")
    await audit.log_action(actor_id=current_user.id, action="plan_delete",
                           resource_type="plan", resource_id=plan_id, context=audit_context)

Lý do: bỏ import repo trong hàm, thống nhất RBAC + owner check, tag version; mở đường tách schema ra core/serializers/plan.py.

Bổ sung nhỏ trong dependencies.py (để patch chạy mượt)

Thêm 2 factory DI: get_agent_repository, get_plan_repository, và (tùy) get_audit_service:

# zeta_vn/app/dependencies.py (bổ sung)

from fastapi import Request, Depends
from zeta_vn.app.di_container import DIContainer
from zeta_vn.data.repositories.agent_repository import AgentRepository
from zeta_vn.data.repositories.plan_repository import PlanRepository
from zeta_vn.core.services.audit_service import AuditService
from zeta_vn.data.repositories.audit_repository import AuditRepository

async def get_db_session(request: Request):
    c: DIContainer = request.state.container
    return await c.get("db_session")

async def get_agent_repository(session=Depends(get_db_session)) -> AgentRepository:
    return AgentRepository(session)

async def get_plan_repository(session=Depends(get_db_session)) -> PlanRepository:
    return PlanRepository(session)

async def get_audit_service(session=Depends(get_db_session)) -> AuditService:
    return AuditService(AuditRepository(session))

Mục tiêu/done khi áp dụng xong

Một nguồn sự thật cho v1: zeta_vn.app.api.v1.router làm aggregator; main chỉ include 1 lần.

Chuẩn DI: repo/use-case đều tiêm qua Depends, không import trong handler.

RBAC rõ ràng: dùng require_permissions, owner-check tách sang deps (sau có thể thêm require_agent_owner(...)).

Namespace thống nhất: zeta_vn.app.*/zeta_vn.data.*/zeta_vn.core.*.

OpenAPI sạch: tag v1 hiển thị đúng nhóm endpoints.

Bạn muốn mình xuất thêm file aggregator zeta_vn/app/api/v1/router.py + cập nhật main.py để include duy nhất aggregator không? Mình có thể dán code hoàn chỉnh ngay để bạn commit.
