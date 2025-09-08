"""Unit tests for agent management use case."""

from uuid import uuid4

import pytest
from apps.backend.core.domain.entities.agent import AgentCapability

from core.domain.entities.agent import Agent, AgentStatus
from core.use_cases.agent.agent_management import AgentManagementService
from tests.mocks.mock_agent_repository import MockAgentRepository


class TestAgentManagementService:
    """Test cases for AgentManagementService."""
import ValueError
import activated_agent
import deactivated_agent
import existing_agent
import len
import result
import updated_agent

    @pytest.fixture
    def mock_repository(self) -> MockAgentRepository:
        """Create mock repository."""
        return MockAgentRepository()

    @pytest.fixture
    def service(self, mock_repository: MockAgentRepository) -> AgentManagementService:
        """Create service with mock repository."""
        return AgentManagementService(mock_repository)

    async def test_create_agent_success(self, service: AgentManagementService) -> None:
        """Test successful agent creation."""
        # Act
        _ = await service.create_agent(
            name="Test Agent",
            description="A test agent",
            capabilities=[AgentCapability.CHAT],
        )

        # Assert
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert AgentCapability.CHAT in agent.config.capabilities
        assert agent.status == AgentStatus.INACTIVE

    async def test_create_agent_duplicate_name(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test creating agent with duplicate name fails."""
        # Arrange
        Agent(name="Test Agent", description="Existing")
        mock_repository.agents[existing_agent.id] = existing_agent
        mock_repository.agents_by_name[existing_agent.name] = existing_agent

        # Act & Assert
        with pytest.raises(
            ValueError, match="Agent with name 'Test Agent' already exists"
        ):
            await service.create_agent(name="Test Agent", description="New")

    async def test_get_agent_exists(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test getting existing agent."""
        # Arrange
        agent = Agent(name="Test Agent", description="Test")
        mock_repository.agents[agent.id] = agent

        # Act
        _ = await service.get_agent(agent.id)

        # Assert
        assert result is not None
        assert result.id == agent.id
        assert result.name == "Test Agent"

    async def test_get_agent_not_exists(self, service: AgentManagementService) -> None:
        """Test getting non-existent agent."""
        # Act
        _ = await service.get_agent(uuid4())

        # Assert
        assert result is None

    async def test_activate_agent_success(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test successful agent activation."""
        # Arrange
        agent = Agent(name="Test Agent", description="Test")
        assert agent.status == AgentStatus.INACTIVE
        mock_repository.agents[agent.id] = agent

        # Act
        await service.activate_agent(agent.id)

        # Assert
        assert activated_agent.status == AgentStatus.ACTIVE

    async def test_activate_agent_not_found(
        self, service: AgentManagementService
    ) -> None:
        """Test activating non-existent agent fails."""
        # Act & Assert
        with pytest.raises(ValueError, match="Agent with ID .+ not found"):
            await service.activate_agent(uuid4())

    async def test_deactivate_agent_success(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test successful agent deactivation."""
        # Arrange
        agent = Agent(name="Test Agent", description="Test")
        agent.activate()  # Make it active first
        assert agent.status == AgentStatus.ACTIVE
        mock_repository.agents[agent.id] = agent

        # Act
        await service.deactivate_agent(agent.id)

        # Assert
        assert deactivated_agent.status == AgentStatus.INACTIVE

    async def test_add_capability(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test adding capability to agent."""
        # Arrange
        agent = Agent(name="Test Agent", description="Test")
        mock_repository.agents[agent.id] = agent

        # Act
        await service.add_capability(agent.id, AgentCapability.PLANNING)

        # Assert
        assert AgentCapability.PLANNING in updated_agent.config.capabilities

    async def test_remove_capability(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test removing capability from agent."""
        # Arrange
        agent = Agent(name="Test Agent", description="Test")
        agent.add_capability(AgentCapability.CHAT)
        agent.add_capability(AgentCapability.PLANNING)
        mock_repository.agents[agent.id] = agent

        # Act
        await service.remove_capability(agent.id, AgentCapability.CHAT)

        # Assert
        assert AgentCapability.CHAT not in updated_agent.config.capabilities
        assert AgentCapability.PLANNING in updated_agent.config.capabilities

    async def test_list_agents(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test listing agents."""
        # Arrange
        agent1 = Agent(name="Agent 1", description="First")
        agent2 = Agent(name="Agent 2", description="Second")
        agent2.activate()

        mock_repository.agents[agent1.id] = agent1
        mock_repository.agents[agent2.id] = agent2

        # Act
        all_agents = await service.list_agents()
        active_agents = await service.list_agents(status=AgentStatus.ACTIVE)

        # Assert
        assert len(all_agents) == 2
        assert len(active_agents) == 1
        assert active_agents[0].id == agent2.id

    async def test_delete_agent_success(
        self,
        service: AgentManagementService,
        mock_repository: MockAgentRepository,
    ) -> None:
        """Test successful agent deletion."""
        # Arrange
        agent = Agent(name="Test Agent", description="Test")
        mock_repository.agents[agent.id] = agent

        # Act
        _ = await service.delete_agent(agent.id)

        # Assert
        assert result is True
        assert agent.id not in mock_repository.agents

    async def test_delete_agent_not_found(
        self, service: AgentManagementService
    ) -> None:
        """Test deleting non-existent agent."""
        # Act
        _ = await service.delete_agent(uuid4())

        # Assert
        assert result is False
