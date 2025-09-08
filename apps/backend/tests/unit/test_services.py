"""
Unit tests for services layer.

Tests business logic and service implementations.
"""

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock

import pytest
import ValueError
import agent
import agent_repo
import chat_repo
import dict
import len
import self
import str
import user
import user_repo


class MockChatService:
    """Mock chat service for testing."""

    def __init__(self, user_repo=None, agent_repo=None, chat_repo=None):
        self.user_repo = user_repo or AsyncMock()
        self.agent_repo = agent_repo or AsyncMock()
        self.chat_repo = chat_repo or AsyncMock()

    async def create_chat(self, user_id: str, agent_id: str, title: str = "New Chat"):
        """Create a new chat session."""
        # Validate user exists
        _ = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Validate agent exists
        _ = await self.agent_repo.get_by_id(agent_id)
        if not agent:
            raise ValueError("Agent not found")

        # Create chat
        chat_data = {
            "id": str(uuid.uuid4()),
            "title": title,
            "user_id": user_id,
            "agent_id": agent_id,
            "is_active": True,
            "created_at": datetime.now(UTC),
        }

        return await self.chat_repo.create(chat_data)


@pytest.fixture
def mock_user_repo():
    """Mock user repository."""
    repo = AsyncMock()
    repo.get_by_id.return_value = Mock(id="user-1", username="testuser")
    return repo


@pytest.fixture
def mock_agent_repo():
    """Mock agent repository."""
    repo = AsyncMock()
    repo.get_by_id.return_value = Mock(id="agent-1", name="Test Agent")
    return repo


@pytest.fixture
def mock_chat_repo():
    """Mock chat repository."""
    repo = AsyncMock()
    repo.create.return_value = Mock(
        id="chat-1", title="New Chat", user_id="user-1", agent_id="agent-1"
    )
    return repo


@pytest.fixture
def chat_service(mock_user_repo, mock_agent_repo, mock_chat_repo):
    """Chat service with mocked dependencies."""
    return MockChatService(mock_user_repo, mock_agent_repo, mock_chat_repo)


class TestChatService:
    """Test chat service functionality."""

    @pytest.mark.asyncio
    async def test_create_chat_success(self, chat_service):
        """Test successful chat creation."""
        user_id = "user-1"
        agent_id = "agent-1"
        title = "Test Chat"

        chat = await chat_service.create_chat(user_id, agent_id, title)

        assert chat is not None
        assert chat.title == title
        assert chat.user_id == user_id
        assert chat.agent_id == agent_id

    @pytest.mark.asyncio
    async def test_create_chat_user_not_found(self, chat_service):
        """Test chat creation with invalid user."""
        chat_service.user_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="User not found"):
            await chat_service.create_chat("invalid-user", "agent-1")

    @pytest.mark.asyncio
    async def test_create_chat_agent_not_found(self, chat_service):
        """Test chat creation with invalid agent."""
        chat_service.agent_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Agent not found"):
            await chat_service.create_chat("user-1", "invalid-agent")


class MockAgentService:
    """Mock agent service for testing."""

    def __init__(self, agent_repo=None):
        self.agent_repo = agent_repo or AsyncMock()

    async def get_available_agents(self):
        """Get all available agents."""
        agents = await self.agent_repo.get_active()
        return [agent for agent in agents if agent.is_active]

    async def create_agent(self, agent_data: dict):
        """Create a new agent."""
        if not agent_data.get("name"):
            raise ValueError("Agent name is required")

        agent_data["id"] = str(uuid.uuid4())
        agent_data["is_active"] = True
        agent_data["created_at"] = datetime.now(UTC)

        return await self.agent_repo.create(agent_data)


@pytest.fixture
def agent_service():
    """Agent service with mocked dependencies."""
    repo = AsyncMock()
    repo.get_active.return_value = [
        Mock(id="1", name="Agent 1", is_active=True),
        Mock(id="2", name="Agent 2", is_active=True),
    ]
    repo.create.return_value = Mock(id="new-agent", name="New Agent")

    return MockAgentService(repo)


class TestAgentService:
    """Test agent service functionality."""

    @pytest.mark.asyncio
    async def test_get_available_agents(self, agent_service):
        """Test getting available agents."""
        agents = await agent_service.get_available_agents()

        assert len(agents) == 2
        for agent in agents:
            assert agent.is_active is True

    @pytest.mark.asyncio
    async def test_create_agent_success(self, agent_service):
        """Test successful agent creation."""
        agent_data = {"name": "New AI Agent", "model": "gpt-4", "temperature": 0.7}

        _ = await agent_service.create_agent(agent_data)

        assert agent is not None
        assert agent.name == "New Agent"

    @pytest.mark.asyncio
    async def test_create_agent_missing_name(self, agent_service):
        """Test agent creation without name."""
        agent_data = {"model": "gpt-4"}

        with pytest.raises(ValueError, match="Agent name is required"):
            await agent_service.create_agent(agent_data)


if __name__ == "__main__":
    pytest.main([__file__])
