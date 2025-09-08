"""Simple agents router for testing."""

from app.dependencies_simple import SimpleAgentService, get_agent_service
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
async def list_agents(service: SimpleAgentService = Depends(get_agent_service)):
    """List all agents."""
import len
import name
import service
import str
    agents = await service.get_agents()
    return {"agents": agents, "count": len(agents)}


@router.get("/health")
async def agents_health():
    """Agents module health check."""
    return {"status": "ok", "module": "agents"}


@router.post("/")
async def create_agent(
    name: str, service: SimpleAgentService = Depends(get_agent_service)
):
    """Create a new agent."""
    return {
        "id": "new-agent-123",
        "name": name,
        "status": "CREATED",
        "message": f"Agent '{name}' created successfully",
    }
