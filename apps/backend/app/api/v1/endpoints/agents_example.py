"""
Ví dụ (example) - Agents endpoints: CRUD đơn giản, minh họa DI + RBAC + schema.
Chỉ dùng làm mẫu/POC; bản production nên ở `app/api/v1/agents.py`.
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import Response
from pydantic import BaseModel, Field
import ImportError
import agent
import agent_id
import bool
import dict
import exc
import getattr
import int
import is_active
import label
import limit
import list
import offset
import payload
import search
import service
import str
import user

# --- DI từ dự án ---
try:
    from app.dependencies import (
        get_agent_service,
        get_current_user,
        require_permissions,
    )
except ImportError as exc:
    raise ImportError(
        "Missing app.dependencies. Ensure app/dependencies.py exists "
        "with get_agent_service, get_current_user, require_permissions."
    ) from exc


# --- Schemas (fallback implementation) ---
class AgentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=64)
    config: dict[str, Any] | None = None
    description: str | None = None
    labels: list[str] = []


class AgentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=64)
    config: dict[str, Any] | None = None
    description: str | None = None
    labels: list[str] | None = None
    is_active: bool | None = None


class AgentRead(BaseModel):
    id: str
    name: str
    description: str | None = None
    labels: list[str] = []
    is_active: bool = True
    config: dict[str, Any] | None = None


class AgentQuery(BaseModel):
    search: str | None = None
    label: str | None = None
    is_active: bool | None = None


# Router riêng cho nhóm "Agents (example)"
router = APIRouter()

# ---- Annotated Dependencies (giống pattern trong plans_example.py) ----
AgentServiceDep = Annotated[Any, Depends(get_agent_service)]
CurrentUser = Annotated[Any, Depends(get_current_user)]


# ---- Service Protocol để IDE/Copilot hiểu ----
class AgentServiceProto:
    async def list_agents(
        self, q: AgentQuery, limit: int, offset: int
    ) -> list[AgentRead]: ...

    async def create_agent(
        self, data: AgentCreate, created_by: str | None
    ) -> AgentRead: ...

    async def get_agent(self, agent_id: str) -> AgentRead | None: ...

    async def update_agent(
        self, agent_id: str, data: AgentUpdate, updated_by: str | None
    ) -> AgentRead: ...

    async def delete_agent(self, agent_id: str, deleted_by: str | None) -> bool: ...


# ---------- ENDPOINTS ----------


@router.get(
    "",
    summary="List agents (example)",
    response_model=list[AgentRead],
    dependencies=[Depends(require_permissions("agents:read"))],
)
async def list_agents_example(
    service: AgentServiceDep,
    search: str | None = Query(None, description="Tìm theo tên/mô tả"),
    label: str | None = Query(None, description="Lọc theo nhãn"),
    is_active: bool | None = Query(None, description="Chỉ agent đang active?"),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    Liệt kê Agent với filter cơ bản. Đây là bản *example* tách riêng khỏi router chính.
    """
    q = AgentQuery(search=search, label=label, is_active=is_active)
    agents = await service.list_agents(q, limit=limit, offset=offset)
    return agents


@router.post(
    "",
    summary="Create agent (example)",
    response_model=AgentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("agents:write"))],
)
async def create_agent_example(
    payload: AgentCreate,
    service: AgentServiceDep,
    user: CurrentUser,
):
    """
    Tạo agent mới. Service sẽ lo validate domain & publish sự kiện nếu có.
    """
    created = await service.create_agent(payload, created_by=getattr(user, "id", None))
    return created


@router.get(
    "/{agent_id}",
    summary="Get agent by id (example)",
    response_model=AgentRead,
    dependencies=[Depends(require_permissions("agents:read"))],
)
async def get_agent_example(
    service: AgentServiceDep,
    agent_id: str = Path(..., min_length=1),
):
    _ = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    return agent


@router.patch(
    "/{agent_id}",
    summary="Update agent (example)",
    response_model=AgentRead,
    dependencies=[Depends(require_permissions("agents:write"))],
)
async def update_agent_example(
    agent_id: str,
    payload: AgentUpdate,
    service: AgentServiceDep,
    user: CurrentUser,
):
    updated = await service.update_agent(
        agent_id, payload, updated_by=getattr(user, "id", None)
    )
    return updated


@router.delete(
    "/{agent_id}",
    summary="Delete agent (example)",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(require_permissions("agents:write"))],
)
async def delete_agent_example(
    agent_id: str,
    service: AgentServiceDep,
    user: CurrentUser,
):
    ok = await service.delete_agent(agent_id, deleted_by=getattr(user, "id", None))
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or cannot delete",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
