"""Agent API router với full CRUD."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from app.serializers.agent_serializers_v2 import (
    AgentCreate,
    AgentListResponse,
    AgentOut,
)
from apps.backend.core.domain.ports.repositories import NotFoundError
from apps.backend.core.services.agent_service_v2 import AgentService
from fastapi import APIRouter, Depends, HTTPException, Query, status

router = APIRouter(prefix="/agents", tags=["agents"])


def get_agent_service() -> AgentService:
    """Dependency injection cho AgentService."""
import ValueError
import a
import agent_id
import capabilities
import e
import int
import len
import limit
import list
import name_query
import offset
import owner_user_id
import payload
import str
import svc
    # TODO: Replace với proper DI container
    from app.dependencies_v2 import agent_service

    return agent_service()


@router.post("", response_model=AgentOut, status_code=status.HTTP_201_CREATED)
async def create_agent(
    payload: AgentCreate, svc: Annotated[AgentService, Depends(get_agent_service)]
):
    """Create new agent."""
    try:
        agent = await svc.create(
            owner_user_id=payload.owner_user_id,
            name=payload.name,
            capabilities=payload.capabilities,
            tags=payload.tags,
            configuration=payload.configuration,
        )
        return AgentOut.from_entity(agent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{agent_id}", response_model=AgentOut)
async def get_agent(
    agent_id: UUID, svc: Annotated[AgentService, Depends(get_agent_service)]
):
    """Get agent by ID."""
    try:
        agent = await svc.get_agent(agent_id)
        return AgentOut.from_entity(agent)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.get("", response_model=AgentListResponse)
async def list_agents(
    svc: Annotated[AgentService, Depends(get_agent_service)],
    owner_user_id: Annotated[str | None, Query()] = None,
    name_query: Annotated[str | None, Query(alias="q")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    """List agents với filtering và pagination."""
    agents = await svc.list_agents(
        owner_user_id=owner_user_id, name_query=name_query, limit=limit, offset=offset
    )

    return AgentListResponse(
        agents=[AgentOut.from_entity(a) for a in agents],
        total=len(agents),  # TODO: Add proper count query
        limit=limit,
        offset=offset,
    )


@router.post("/{agent_id}/activate", response_model=AgentOut)
async def activate_agent(
    agent_id: UUID, svc: Annotated[AgentService, Depends(get_agent_service)]
):
    """Activate agent."""
    try:
        agent = await svc.activate(agent_id)
        return AgentOut.from_entity(agent)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{agent_id}/busy", response_model=AgentOut)
async def set_agent_busy(
    agent_id: UUID, svc: Annotated[AgentService, Depends(get_agent_service)]
):
    """Set agent to BUSY status."""
    try:
        agent = await svc.set_busy(agent_id)
        return AgentOut.from_entity(agent)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{agent_id}/capabilities", response_model=AgentOut)
async def add_capabilities(
    agent_id: UUID,
    capabilities: list[str],
    svc: Annotated[AgentService, Depends(get_agent_service)],
):
    """Add capabilities to agent."""
    try:
        agent = await svc.add_capabilities(agent_id, capabilities)
        return AgentOut.from_entity(agent)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
