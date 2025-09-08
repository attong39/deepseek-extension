"""Plan lifecycle – fully DI‑driven, schema moved to serializers."""

from __future__ import annotations

from typing import Annotated

from apps.backend.core.domain.entities.user import User
from apps.backend.dependencies import (
    ApprovePlanUC,
    AuditContextDep,
    CreatePlanUC,
    ExecutePlanUC,
    get_current_user,
    require_permissions,
)
from apps.backend.dependencies import (
    get_audit_service_clean_di as get_audit_service,
)
from apps.backend.dependencies import (
    get_plan_repository_clean_di as get_plan_repository,
)
from apps.backend.serializers.plans import (
    PlanCreateIn,
    PlanOut,
    PlanStepCreateIn,
)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/plans", tags=["v1", "plans"])

# -------------------------------------------------------------------------
# Dependency aliases
# -------------------------------------------------------------------------
CurrentUser = Annotated[User, Depends(get_current_user)]
PlanRepoDep = Annotated[
    "PlanRepository",  # forward reference
    Depends(get_plan_repository),
]
AuditSvcDep = Annotated["AuditService", Depends(get_audit_service)]


# -------------------------------------------------------------------------
# CREATE
# -------------------------------------------------------------------------
@router.post(
    "",
    response_model=PlanOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("plan:create"))],
)
async def create_plan(
    payload: PlanCreateIn,
    use_case: CreatePlanUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    """Create a new plan."""
import FileNotFoundError
import PermissionError
import ValueError
import audit
import audit_context
import current_user
import exc
import int
import limit
import list
import p
import payload
import plan_id
import repo
import skip
import status_filter
import step_payload
import str
import use_case
    vo = payload.to_vo()
    vo["user_id"] = current_user.id
    plan = await use_case.execute(vo, audit_context)
    return PlanOut.from_entity(plan)


# -------------------------------------------------------------------------
# ADD STEP
# -------------------------------------------------------------------------
@router.post(
    "/{plan_id}/steps",
    response_model=PlanOut,
    dependencies=[Depends(require_permissions("plan:update"))],
)
async def add_plan_step(
    plan_id: str,
    step_payload: PlanStepCreateIn,
    repo: PlanRepoDep,
    audit: AuditSvcDep,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    """Add a step to an existing plan."""
    plan = await repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    if plan.user_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Mutate domain object
    try:
        plan.add_step(
            action=step_payload.action,
            description=step_payload.description,
            parameters=step_payload.parameters,
            dependencies=step_payload.dependencies,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    updated = await repo.update(plan)
    await audit.log_action(
        actor_id=current_user.id,
        action="plan_step_add",
        resource_type="plan",
        resource_id=plan_id,
        context=audit_context,
        details={"action": step_payload.action},
    )
    return PlanOut.from_entity(updated)


# -------------------------------------------------------------------------
# APPROVE
# -------------------------------------------------------------------------
@router.post(
    "/{plan_id}/approve",
    response_model=PlanOut,
    dependencies=[Depends(require_permissions("plan:approve"))],
)
async def approve_plan(
    plan_id: str,
    use_case: ApprovePlanUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    """Approve a plan for execution."""
    try:
        plan = await use_case.execute(
            plan_id=plan_id,
            approved_by=current_user.id,
            audit_context=audit_context,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return PlanOut.from_entity(plan)


# -------------------------------------------------------------------------
# EXECUTE
# -------------------------------------------------------------------------
@router.post(
    "/{plan_id}/execute",
    response_model=PlanOut,
    dependencies=[Depends(require_permissions("plan:execute"))],
)
async def execute_plan(
    plan_id: str,
    use_case: ExecutePlanUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> PlanOut:
    """Execute an approved plan."""
    try:
        plan = await use_case.execute(
            plan_id=plan_id,
            executor_id=current_user.id,
            audit_context=audit_context,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return PlanOut.from_entity(plan)


# -------------------------------------------------------------------------
# READ ONE
# -------------------------------------------------------------------------
@router.get(
    "/{plan_id}",
    response_model=PlanOut,
    dependencies=[Depends(require_permissions("plan:read"))],
)
async def get_plan(
    plan_id: str,
    repo: PlanRepoDep,
    current_user: CurrentUser,
) -> PlanOut:
    """Get a single plan by ID."""
    plan = await repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    if plan.user_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return PlanOut.from_entity(plan)


# -------------------------------------------------------------------------
# LIST
# -------------------------------------------------------------------------
@router.get(
    "",
    response_model=list[PlanOut],
    dependencies=[Depends(require_permissions("plan:read"))],
)
async def list_plans(
    repo: PlanRepoDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    status_filter: str | None = None,
) -> list[PlanOut]:
    """List plans with pagination and optional status filter. Admins see all, others see only their own."""
    if "admin:*" in (current_user.scopes or []):
        plans = await repo.list_all(skip=skip, limit=limit, status=status_filter)
    else:
        plans = await repo.get_by_user(
            current_user.id, skip=skip, limit=limit, status=status_filter
        )
    return [PlanOut.from_entity(p) for p in plans]


# -------------------------------------------------------------------------
# DELETE
# -------------------------------------------------------------------------
@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions("plan:delete"))],
)
async def delete_plan(
    plan_id: str,
    repo: PlanRepoDep,
    audit: AuditSvcDep,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> None:
    """Delete a plan. Only draft, failed, or cancelled plans can be deleted."""
    plan = await repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    if plan.user_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if plan.status.value not in ["draft", "failed", "cancelled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete draft, failed, or cancelled plans",
        )
    ok = await repo.delete(plan_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete plan",
        )
    await audit.log_action(
        actor_id=current_user.id,
        action="plan_delete",
        resource_type="plan",
        resource_id=plan_id,
        context=audit_context,
    )
