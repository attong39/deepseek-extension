"""
Basic agent functionality smoke tests.
Quick integration tests for core agent team operations.
"""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock
import len


def test_agent_team_model_validation():
    """Test that AgentTeam model validation works correctly."""
    from app.core.models.agents import AgentTeam, Agent
    
    # Valid team should pass
    agent = Agent(id="test-agent", role="analyst", capabilities=["analyze"])
    team = AgentTeam(
        id="test-team",
        name="Test Team", 
        agents=[agent],
        workflow_spec={"steps": [{"agent": "test-agent", "action": "analyze"}]}
    )
    
    assert team.id == "test-team"
    assert team.name == "Test Team"
    assert len(team.agents) == 1
    assert team.agents[0].id == "test-agent"


def test_orchestrator_basic_initialization():
    """Test that MultiAgentOrchestrator can be initialized."""
    from app.core.agents.orchestrator import MultiAgentOrchestrator
    
    # Mock knowledge graph
    mock_kg = MagicMock()
    mock_kg.find_path = AsyncMock(return_value=["step1", "step2"])
    
    orchestrator = MultiAgentOrchestrator(knowledge_graph=mock_kg)
    assert orchestrator is not None
    assert orchestrator.knowledge_graph == mock_kg


def test_knowledge_graph_basic_operations():
    """Test that KnowledgeGraph supports basic operations."""
    from app.core.knowledge.graph import KnowledgeGraph
    
    kg = KnowledgeGraph()
    
    # Add entity
    kg.add_entity("entity1", "test_type", {"name": "Test Entity"})
    
    # Check entity exists
    entity = kg.get_entity("entity1")
    assert entity is not None
    assert entity["type"] == "test_type"
    assert entity["attributes"]["name"] == "Test Entity"


async def async_test_websocket_connection_manager():
    """Test that WebSocket connection manager works."""
    from app.core.websocket.manager import WebSocketManager
    from unittest.mock import AsyncMock
    
    manager = WebSocketManager()
    
    # Mock WebSocket
    mock_ws = AsyncMock()
    mock_ws.accept = AsyncMock()
    mock_ws.send_text = AsyncMock()
    mock_ws.close = AsyncMock()
    
    # Test connection registration
    await manager.connect(mock_ws, "test-client")
    assert "test-client" in manager.active_connections
    
    # Test message sending
    await manager.send_personal_message("test message", "test-client")
    mock_ws.send_text.assert_called_once()
    
    # Test disconnection
    manager.disconnect("test-client")
    assert "test-client" not in manager.active_connections


def test_websocket_connection_manager():
    """Wrapper to run async WebSocket test."""
    asyncio.run(async_test_websocket_connection_manager())
