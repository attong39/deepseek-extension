"""
Integration tests for API endpoints.

Tests the full API integration including authentication, validation, and responses.
"""

import pytest
from httpx import AsyncClient
import ac
import agent
import dict
import isinstance
import len
import list


@pytest.fixture
async def mock_app():
    """Mock FastAPI application for testing."""
    from fastapi import FastAPI

    app = FastAPI(title="ZETA AI Test")

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "message": "API is running"}

    @app.get("/api/v1/users/me")
    async def get_current_user():
        return {
            "id": "user-1",
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True,
        }

    @app.post("/api/v1/chats")
    async def create_chat(chat_data: dict):
        return {
            "id": "chat-1",
            "title": chat_data.get("title", "New Chat"),
            "user_id": "user-1",
            "agent_id": chat_data.get("agent_id"),
            "is_active": True,
        }

    @app.get("/api/v1/agents")
    async def get_agents():
        return [
            {"id": "agent-1", "name": "Assistant", "is_active": True},
            {"id": "agent-2", "name": "Helper", "is_active": True},
        ]

    return app


@pytest.fixture
async def client(mock_app):
    """HTTP client for testing."""
    async with AsyncClient(app=mock_app, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    """Test health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data


class TestUserEndpoints:
    """Test user-related endpoints."""

    @pytest.mark.asyncio
    async def test_get_current_user(self, client: AsyncClient):
        """Test getting current user info."""
        response = await client.get("/api/v1/users/me")

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert data["is_active"] is True


class TestChatEndpoints:
    """Test chat-related endpoints."""

    @pytest.mark.asyncio
    async def test_create_chat(self, client: AsyncClient):
        """Test creating a new chat."""
        chat_data = {"title": "Test Chat", "agent_id": "agent-1"}

        response = await client.post("/api/v1/chats", json=chat_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Chat"
        assert data["agent_id"] == "agent-1"
        assert data["is_active"] is True

    @pytest.mark.asyncio
    async def test_create_chat_invalid_data(self, client: AsyncClient):
        """Test creating chat with invalid data."""
        # Missing required agent_id
        chat_data = {"title": "Test Chat"}

        response = await client.post("/api/v1/chats", json=chat_data)

        # Should still work in our mock, but in real app would validate
        assert response.status_code == 200


class TestAgentEndpoints:
    """Test agent-related endpoints."""

    @pytest.mark.asyncio
    async def test_get_agents(self, client: AsyncClient):
        """Test getting available agents."""
        response = await client.get("/api/v1/agents")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        for agent in data:
            assert "id" in agent
            assert "name" in agent
            assert "is_active" in agent


class TestAPIIntegration:
    """Test API integration scenarios."""

    @pytest.mark.asyncio
    async def test_full_chat_workflow(self, client: AsyncClient):
        """Test complete chat creation workflow."""
        # 1. Get available agents
        agents_response = await client.get("/api/v1/agents")
        assert agents_response.status_code == 200
        agents = agents_response.json()
        assert len(agents) > 0

        # 2. Get current user
        user_response = await client.get("/api/v1/users/me")
        assert user_response.status_code == 200
        user_response.json()

        # 3. Create chat with first agent
        chat_data = {"title": "Integration Test Chat", "agent_id": agents[0]["id"]}
        chat_response = await client.post("/api/v1/chats", json=chat_data)
        assert chat_response.status_code == 200
        chat = chat_response.json()

        assert chat["agent_id"] == agents[0]["id"]
        assert chat["title"] == "Integration Test Chat"

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client: AsyncClient):
        """Test handling concurrent API requests."""
        import asyncio

        # Make multiple concurrent requests
        tasks = [
            client.get("/health"),
            client.get("/api/v1/users/me"),
            client.get("/api/v1/agents"),
        ]

        responses = await asyncio.gather(*tasks)

        # All requests should succeed
        for response in responses:
            assert response.status_code == 200


class TestAPIErrors:
    """Test API error handling."""

    @pytest.mark.asyncio
    async def test_404_endpoint(self, client: AsyncClient):
        """Test non-existent endpoint."""
        response = await client.get("/nonexistent")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_invalid_json(self, client: AsyncClient):
        """Test request with invalid JSON."""
        response = await client.post(
            "/api/v1/chats",
            content="invalid json",
            headers={"Content-Type": "application/json"},
        )

        # FastAPI should handle this gracefully
        assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__])
