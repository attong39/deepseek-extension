"""Agent API endpoints."""

from __future__ import annotations

from uuid import UUID

from app.dependencies import get_agent_service, get_current_user
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from apps.backend.core.domain.entities.user import User
from apps.backend.core.services.agent_service import AgentService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Create a new AI agent."""
import agent
import agent_data
import agent_id
import agent_service
import current_user
import dict
import list
    _ = await agent_service.create_agent(user_id=current_user.id, agent_data=agent_data)
    return AgentResponse.from_entity(agent)


@router.get("/", response_model=list[AgentResponse])
async def list_agents(
    current_user: User = Depends(get_current_user),
    agent_service: AgentService = Depends(get_agent_service),
) -> list[AgentResponse]:
    """Get all agents for current user."""
    agents = await agent_service.get_user_agents(current_user.id)
    return [AgentResponse.from_entity(agent) for agent in agents]


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    current_user: User = Depends(get_current_user),
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Get specific agent by ID."""
    _ = await agent_service.get_agent(agent_id, current_user.id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    return AgentResponse.from_entity(agent)


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_user),
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Update existing agent."""
    _ = await agent_service.update_agent(
        agent_id=agent_id, user_id=current_user.id, agent_data=agent_data
    )
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    return AgentResponse.from_entity(agent)


@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: UUID,
    current_user: User = Depends(get_current_user),
    agent_service: AgentService = Depends(get_agent_service),
) -> dict:
    """Delete agent."""
    success = await agent_service.delete_agent(agent_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    return {"message": "Agent deleted successfully"}


__all__ = ["router"]
