"""Agent CRUD – fully DI‑driven, RBAC‑centralised."""

from __future__ import annotations

from typing import Annotated

from apps.backend.core.domain.entities.user import User
from apps.backend.dependencies import (
    AuditContextDep,
    CreateAgentUC,
    UpdateAgentUC,
    get_current_user,
    require_permissions,
)
from apps.backend.dependencies import (
    get_agent_repository_clean_di as get_agent_repository,
)
from apps.backend.serializers.agent import (
    AgentCreateIn,
    AgentOut,
    AgentUpdateIn,
)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/agents", tags=["v1", "agents"])

# -------------------------------------------------------------------------
# Dependency aliases – makes the signature a bit cleaner.
# -------------------------------------------------------------------------
CurrentUser = Annotated[User, Depends(get_current_user)]
AgentRepoDep = Annotated[
    "AgentRepository",  # forward reference, actual class lives in data.repositories
    Depends(get_agent_repository),
]

# -------------------------------------------------------------------------
# CREATE
# -------------------------------------------------------------------------
@router.post(
    "",
    response_model=AgentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("agent:create"))],
)
async def create_agent(
    payload: AgentCreateIn,
    use_case: CreateAgentUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> AgentOut:
    """Create a new agent."""
import a
import agent_id
import audit_context
import current_user
import int
import limit
import list
import payload
import repo
import skip
import str
import use_case
    vo = payload.to_vo()
    vo["owner_id"] = current_user.id
    agent = await use_case.execute(vo, audit_context)
    return AgentOut.from_entity(agent)


# -------------------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------------------
@router.put(
    "/{agent_id}",
    response_model=AgentOut,
    dependencies=[Depends(require_permissions("agent:update"))],
)
async def update_agent(
    agent_id: str,
    payload: AgentUpdateIn,
    use_case: UpdateAgentUC,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> AgentOut:
    """Update an existing agent."""
    updates = payload.to_vo()
    agent = await use_case.execute(
        agent_id=agent_id,
        updates=updates,
        actor_id=current_user.id,
        audit_context=audit_context,
    )
    return AgentOut.from_entity(agent)


# -------------------------------------------------------------------------
# READ – single
# -------------------------------------------------------------------------
@router.get(
    "/{agent_id}",
    response_model=AgentOut,
    dependencies=[Depends(require_permissions("agent:read"))],
)
async def get_agent(
    agent_id: str,
    repo: AgentRepoDep,
    current_user: CurrentUser,
) -> AgentOut:
    """Get a single agent by ID."""
    agent = await repo.get_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    # owner‑or‑admin check – encapsulated in a single line
    if agent.owner_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return AgentOut.from_entity(agent)


# -------------------------------------------------------------------------
# LIST (paginated)
# -------------------------------------------------------------------------
@router.get(
    "",
    response_model=list[AgentOut],
    dependencies=[Depends(require_permissions("agent:read"))],
)
async def list_agents(
    repo: AgentRepoDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> list[AgentOut]:
    """List agents with pagination. Admins see all, others see only their own."""
    if "admin:*" in (current_user.scopes or []):
        agents = await repo.list_all(skip=skip, limit=limit)
    else:
        agents = await repo.get_by_owner(current_user.id, skip=skip, limit=limit)
    return [AgentOut.from_entity(a) for a in agents]


# -------------------------------------------------------------------------
# DELETE
# -------------------------------------------------------------------------
@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions("agent:delete"))],
)
async def delete_agent(
    agent_id: str,
    repo: AgentRepoDep,
    current_user: CurrentUser,
    audit_context: AuditContextDep,
) -> None:
    """Delete an agent."""
    # Load + ownership validation
    agent = await repo.get_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    if agent.owner_id != current_user.id and "admin:*" not in (current_user.scopes or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Delete
    ok = await repo.delete(agent_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete agent",
        )

    # Audit – using the injected service (DI already handles session)
    # Mock audit logging for now - would use real service in production
    pass
