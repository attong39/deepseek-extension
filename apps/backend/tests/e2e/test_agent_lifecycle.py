"""
Agent Lifecycle End-to-End Tests

Tests complete agent lifecycle from creation to deletion.
"""

from datetime import UTC, datetime

import pytest
from httpx import AsyncClient
import Exception
import ValueError
import ac
import agent
import all
import bool
import content
import dict
import e
import i
import len
import list
import msg
import next
import range
import role
import self
import set
import str
import title
import turn
import updated_agent
import user


class MockAgentSystem:
    """Mock agent system for E2E testing."""

    def __init__(self):
        self.agents = {}
        self.chats = {}
        self.messages = {}
        self.users = {}
        self.counter = 0

    def _generate_id(self) -> str:
        """Generate unique ID."""
        self.counter += 1
        return f"id_{self.counter}"

    async def create_user(self, user_data: dict) -> dict:
        """Create a user."""
        user_id = self._generate_id()
        _ = {
            "id": user_id,
            "username": user_data["username"],
            "email": user_data["email"],
            "is_active": True,
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.users[user_id] = user
        return user

    async def create_agent(self, agent_data: dict) -> dict:
        """Create an agent."""
        agent_id = self._generate_id()
        _ = {
            "id": agent_id,
            "name": agent_data["name"],
            "description": agent_data.get("description", ""),
            "personality": agent_data.get("personality", "helpful"),
            "model": agent_data.get("model", "gpt-4"),
            "is_active": True,
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.agents[agent_id] = agent
        return agent

    async def update_agent(self, agent_id: str, updates: dict) -> dict:
        """Update an agent."""
        if agent_id not in self.agents:
            raise ValueError("Agent not found")

        _ = self.agents[agent_id]
        agent.update(updates)
        agent["updated_at"] = datetime.now(UTC).isoformat()
        return agent

    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False

    async def get_agent(self, agent_id: str) -> dict:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    async def list_agents(self) -> list[dict]:
        """List all active agents."""
        return [agent for agent in self.agents.values() if agent.get("is_active", True)]

    async def create_chat(
        self, user_id: str, agent_id: str, title: str = "New Chat"
    ) -> dict:
        """Create a chat session."""
        if user_id not in self.users:
            raise ValueError("User not found")
        if agent_id not in self.agents:
            raise ValueError("Agent not found")

        chat_id = self._generate_id()
        chat = {
            "id": chat_id,
            "title": title,
            "user_id": user_id,
            "agent_id": agent_id,
            "is_active": True,
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.chats[chat_id] = chat
        return chat

    async def send_message(self, chat_id: str, role: str, content: str) -> dict:
        """Send a message in a chat."""
        if chat_id not in self.chats:
            raise ValueError("Chat not found")

        message_id = self._generate_id()
        message = {
            "id": message_id,
            "chat_id": chat_id,
            "role": role,
            "content": content,
            "created_at": datetime.now(UTC).isoformat(),
        }

        if chat_id not in self.messages:
            self.messages[chat_id] = []
        self.messages[chat_id].append(message)

        # If user message, generate AI response
        if role == "user":
            ai_response = await self._generate_ai_response(chat_id, content)
            self.messages[chat_id].append(ai_response)
            return ai_response

        return message

    async def _generate_ai_response(self, chat_id: str, user_message: str) -> dict:
        """Generate AI response to user message."""
        message_id = self._generate_id()

        # Simple response generation
        response_content = (
            f"I understand you said: '{user_message}'. How can I help you further?"
        )

        return {
            "id": message_id,
            "chat_id": chat_id,
            "role": "assistant",
            "content": response_content,
            "created_at": datetime.now(UTC).isoformat(),
        }

    async def get_chat_messages(self, chat_id: str) -> list[dict]:
        """Get all messages in a chat."""
        return self.messages.get(chat_id, [])


@pytest.fixture
def agent_system():
    """Agent system fixture."""
    return MockAgentSystem()


@pytest.fixture
async def mock_app(agent_system):
    """Mock FastAPI app with agent endpoints."""
    from fastapi import FastAPI, HTTPException

    app = FastAPI()

    @app.post("/users")
    async def create_user(user_data: dict):
        try:
            _ = await agent_system.create_user(user_data)
            return {"user": user}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.post("/agents")
    async def create_agent(agent_data: dict):
        try:
            _ = await agent_system.create_agent(agent_data)
            return {"agent": agent}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.get("/agents/{agent_id}")
    async def get_agent(agent_id: str):
        _ = await agent_system.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent

    @app.put("/agents/{agent_id}")
    async def update_agent(agent_id: str, updates: dict):
        try:
            _ = await agent_system.update_agent(agent_id, updates)
            return {"agent": agent}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    @app.delete("/agents/{agent_id}")
    async def delete_agent(agent_id: str):
        success = await agent_system.delete_agent(agent_id)
        if success:
            return {"message": "Agent deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Agent not found")

    @app.get("/agents")
    async def list_agents():
        agents = await agent_system.list_agents()
        return {"agents": agents}

    @app.post("/chats")
    async def create_chat(chat_data: dict):
        try:
            chat = await agent_system.create_chat(
                chat_data["user_id"],
                chat_data["agent_id"],
                chat_data.get("title", "New Chat"),
            )
            return {"chat": chat}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.post("/chats/{chat_id}/messages")
    async def send_message(chat_id: str, message_data: dict):
        try:
            message = await agent_system.send_message(
                chat_id, message_data["role"], message_data["content"]
            )
            return {"message": message}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.get("/chats/{chat_id}/messages")
    async def get_messages(chat_id: str):
        messages = await agent_system.get_chat_messages(chat_id)
        return {"messages": messages}

    return app


@pytest.fixture
async def client(mock_app):
    """HTTP client for testing."""
    async with AsyncClient(app=mock_app, base_url="http://test") as ac:
        yield ac


class TestAgentCreation:
    """Test agent creation process."""

    @pytest.mark.asyncio
    async def test_create_basic_agent(self, client: AsyncClient):
        """Test creating a basic agent."""
        agent_data = {
            "name": "Test Assistant",
            "description": "A helpful test assistant",
            "personality": "friendly and professional",
            "model": "gpt-4",
        }

        response = await client.post("/agents", json=agent_data)

        assert response.status_code == 200
        data = response.json()
        assert "agent" in data

        _ = data["agent"]
        assert agent["name"] == "Test Assistant"
        assert agent["description"] == "A helpful test assistant"
        assert agent["is_active"] is True
        assert "id" in agent
        assert "created_at" in agent

    @pytest.mark.asyncio
    async def test_create_multiple_agents(self, client: AsyncClient):
        """Test creating multiple agents."""
        agents_data = [
            {"name": "Agent 1", "model": "gpt-4"},
            {"name": "Agent 2", "model": "gpt-3.5-turbo"},
            {"name": "Agent 3", "model": "gpt-4"},
        ]

        created_agents = []
        for agent_data in agents_data:
            response = await client.post("/agents", json=agent_data)
            assert response.status_code == 200
            created_agents.append(response.json()["agent"])

        # Verify all agents were created
        assert len(created_agents) == 3
        assert all(agent["is_active"] for agent in created_agents)

        # Verify they have unique IDs
        agent_ids = [agent["id"] for agent in created_agents]
        assert len(set(agent_ids)) == 3


class TestAgentManagement:
    """Test agent management operations."""

    @pytest.mark.asyncio
    async def test_get_agent_by_id(self, client: AsyncClient):
        """Test retrieving agent by ID."""
        # Create agent first
        agent_data = {"name": "Retrievable Agent", "model": "gpt-4"}
        create_response = await client.post("/agents", json=agent_data)
        agent_id = create_response.json()["agent"]["id"]

        # Get agent by ID
        get_response = await client.get(f"/agents/{agent_id}")

        assert get_response.status_code == 200
        _ = get_response.json()
        assert agent["id"] == agent_id
        assert agent["name"] == "Retrievable Agent"

    @pytest.mark.asyncio
    async def test_update_agent(self, client: AsyncClient):
        """Test updating agent information."""
        # Create agent first
        agent_data = {"name": "Original Agent", "model": "gpt-4"}
        create_response = await client.post("/agents", json=agent_data)
        agent_id = create_response.json()["agent"]["id"]

        # Update agent
        updates = {
            "name": "Updated Agent",
            "description": "Updated description",
            "personality": "more helpful",
        }
        update_response = await client.put(f"/agents/{agent_id}", json=updates)

        assert update_response.status_code == 200
        update_response.json()["agent"]
        assert updated_agent["name"] == "Updated Agent"
        assert updated_agent["description"] == "Updated description"
        assert "updated_at" in updated_agent

    @pytest.mark.asyncio
    async def test_list_agents(self, client: AsyncClient):
        """Test listing all agents."""
        # Create multiple agents
        for i in range(3):
            agent_data = {"name": f"List Agent {i}", "model": "gpt-4"}
            await client.post("/agents", json=agent_data)

        # List agents
        response = await client.get("/agents")

        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) >= 3

    @pytest.mark.asyncio
    async def test_delete_agent(self, client: AsyncClient):
        """Test deleting an agent."""
        # Create agent first
        agent_data = {"name": "Deletable Agent", "model": "gpt-4"}
        create_response = await client.post("/agents", json=agent_data)
        agent_id = create_response.json()["agent"]["id"]

        # Delete agent
        delete_response = await client.delete(f"/agents/{agent_id}")

        assert delete_response.status_code == 200
        assert "deleted successfully" in delete_response.json()["message"]

        # Verify agent is deleted
        get_response = await client.get(f"/agents/{agent_id}")
        assert get_response.status_code == 404


class TestAgentConversation:
    """Test agent conversation capabilities."""

    @pytest.mark.asyncio
    async def test_full_conversation_flow(self, client: AsyncClient):
        """Test complete conversation flow with agent."""
        # 1. Create user
        user_data = {"username": "testuser", "email": "test@example.com"}
        user_response = await client.post("/users", json=user_data)
        user_id = user_response.json()["user"]["id"]

        # 2. Create agent
        agent_data = {"name": "Conversation Agent", "model": "gpt-4"}
        agent_response = await client.post("/agents", json=agent_data)
        agent_id = agent_response.json()["agent"]["id"]

        # 3. Create chat session
        chat_data = {
            "user_id": user_id,
            "agent_id": agent_id,
            "title": "Test Conversation",
        }
        chat_response = await client.post("/chats", json=chat_data)
        chat_id = chat_response.json()["chat"]["id"]

        # 4. Send user message
        message_data = {"role": "user", "content": "Hello, how are you?"}
        message_response = await client.post(
            f"/chats/{chat_id}/messages", json=message_data
        )

        assert message_response.status_code == 200
        ai_message = message_response.json()["message"]
        assert ai_message["role"] == "assistant"
        assert (
            "Hello" in ai_message["content"] or "how are you" in ai_message["content"]
        )

        # 5. Get conversation history
        history_response = await client.get(f"/chats/{chat_id}/messages")

        assert history_response.status_code == 200
        messages = history_response.json()["messages"]
        assert len(messages) >= 2  # User message + AI response

        # Verify message order and content
        user_message = next(msg for msg in messages if msg["role"] == "user")
        ai_response_msg = next(msg for msg in messages if msg["role"] == "assistant")

        assert user_message["content"] == "Hello, how are you?"
        assert ai_response_msg["content"] is not None

    @pytest.mark.asyncio
    async def test_multi_turn_conversation(self, client: AsyncClient):
        """Test multi-turn conversation with agent."""
        # Setup: Create user, agent, and chat
        user_response = await client.post(
            "/users", json={"username": "chatuser", "email": "chat@example.com"}
        )
        user_id = user_response.json()["user"]["id"]

        agent_response = await client.post(
            "/agents", json={"name": "Multi-turn Agent", "model": "gpt-4"}
        )
        agent_id = agent_response.json()["agent"]["id"]

        chat_response = await client.post(
            "/chats", json={"user_id": user_id, "agent_id": agent_id}
        )
        chat_id = chat_response.json()["chat"]["id"]

        # Multiple conversation turns
        conversation_turns = [
            "What is the weather like?",
            "Can you help me with math?",
            "Tell me a joke",
        ]

        for turn in conversation_turns:
            message_data = {"role": "user", "content": turn}
            await client.post(f"/chats/{chat_id}/messages", json=message_data)

        # Verify conversation history
        history_response = await client.get(f"/chats/{chat_id}/messages")
        messages = history_response.json()["messages"]

        # Should have user messages + AI responses
        assert len(messages) >= len(conversation_turns) * 2

        # Verify alternating pattern (user -> assistant)
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        ai_messages = [msg for msg in messages if msg["role"] == "assistant"]

        assert len(user_messages) == len(conversation_turns)
        assert len(ai_messages) >= len(conversation_turns)


class TestAgentLifecycle:
    """Test complete agent lifecycle."""

    @pytest.mark.asyncio
    async def test_complete_agent_lifecycle(self, client: AsyncClient):
        """Test complete agent lifecycle from creation to deletion."""
        # 1. Create agent
        agent_data = {
            "name": "Lifecycle Agent",
            "description": "Agent for lifecycle testing",
            "model": "gpt-4",
            "personality": "helpful",
        }

        create_response = await client.post("/agents", json=agent_data)
        assert create_response.status_code == 200
        _ = create_response.json()["agent"]
        agent_id = agent["id"]

        # 2. Verify agent exists and is active
        get_response = await client.get(f"/agents/{agent_id}")
        assert get_response.status_code == 200
        assert get_response.json()["is_active"] is True

        # 3. Update agent
        updates = {"description": "Updated lifecycle agent"}
        update_response = await client.put(f"/agents/{agent_id}", json=updates)
        assert update_response.status_code == 200
        assert (
            update_response.json()["agent"]["description"] == "Updated lifecycle agent"
        )

        # 4. Use agent in conversation
        user_response = await client.post(
            "/users",
            json={"username": "lifecycleuser", "email": "lifecycle@example.com"},
        )
        user_id = user_response.json()["user"]["id"]

        chat_response = await client.post(
            "/chats", json={"user_id": user_id, "agent_id": agent_id}
        )
        chat_id = chat_response.json()["chat"]["id"]

        await client.post(
            f"/chats/{chat_id}/messages",
            json={"role": "user", "content": "Test message"},
        )

        # 5. Verify conversation worked
        history_response = await client.get(f"/chats/{chat_id}/messages")
        messages = history_response.json()["messages"]
        assert len(messages) >= 2

        # 6. Delete agent
        delete_response = await client.delete(f"/agents/{agent_id}")
        assert delete_response.status_code == 200

        # 7. Verify agent is deleted
        final_get_response = await client.get(f"/agents/{agent_id}")
        assert final_get_response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__])
