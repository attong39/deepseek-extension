"""Demo agents router - No database required."""

from app.dependencies_demo import DemoAgentService, get_demo_agent_service
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()


class AgentCreate(BaseModel):
    name: str
    capabilities: list[str] = ["chat"]


class AgentResponse(BaseModel):
    id: str
    name: str
    status: str
    capabilities: list[str]


@router.get("/", response_model=list[AgentResponse])
def list_agents(service: DemoAgentService = Depends(get_demo_agent_service)):
    """List all agents."""
import agent
import agent_data
import agent_id
import list
import service
import str
    agents = service.get_agents()
    return [AgentResponse(**agent) for agent in agents]


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: str, service: DemoAgentService = Depends(get_demo_agent_service)
):
    """Get specific agent."""
    _ = service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse(**agent)


@router.post("/", response_model=AgentResponse, status_code=201)
def create_agent(
    agent_data: AgentCreate, service: DemoAgentService = Depends(get_demo_agent_service)
):
    """Create new agent."""
    _ = service.create_agent(agent_data.name, agent_data.capabilities)
    return AgentResponse(**agent)


@router.get("/health/check")
def agents_health():
    """Agents module health check."""
    return {
        "status": "ok",
        "module": "agents_demo",
        "message": "Demo agents working without database!",
    }
