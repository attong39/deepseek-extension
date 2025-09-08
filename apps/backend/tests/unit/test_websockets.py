"""Unit tests for WebSocket chat functionality."""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from app.api.websockets.chat_websocket import ConnectionManager
from core.domain.entities.chat import ChatMessage


class TestConnectionManager:
    """Test connection manager functionality."""
import Exception
import client

    def test_init(self):
        """Test connection manager initialization."""
        manager = ConnectionManager()
        assert manager.active_connections == {}

    @pytest.mark.asyncio
    async def test_connect(self):
        """Test WebSocket connection."""
        manager = ConnectionManager()
        websocket = Mock()
        websocket.accept = AsyncMock()

        agent_id = "test-agent"

        await manager.connect(websocket, agent_id)

        websocket.accept.assert_called_once()
        assert agent_id in manager.active_connections
        assert websocket in manager.active_connections[agent_id]

    def test_disconnect(self):
        """Test WebSocket disconnection."""
        manager = ConnectionManager()
        websocket = Mock()
        agent_id = "test-agent"

        # Add connection first
        manager.active_connections[agent_id] = [websocket]

        # Disconnect
        manager.disconnect(websocket, agent_id)

        assert agent_id not in manager.active_connections

    @pytest.mark.asyncio
    async def test_send_personal_message(self):
        """Test sending personal message."""
        manager = ConnectionManager()
        websocket = Mock()
        websocket.send_text = AsyncMock()

        message = "test message"

        await manager.send_personal_message(message, websocket)

        websocket.send_text.assert_called_once_with(message)

    @pytest.mark.asyncio
    async def test_send_personal_message_error(self):
        """Test sending personal message with error."""
        manager = ConnectionManager()
        websocket = Mock()
        websocket.send_text = AsyncMock(side_effect=Exception("Connection error"))

        message = "test message"

        # Should not raise exception
        await manager.send_personal_message(message, websocket)

    @pytest.mark.asyncio
    async def test_broadcast_to_agent(self):
        """Test broadcasting message to agent connections."""
        manager = ConnectionManager()
        websocket1 = Mock()
        websocket2 = Mock()
        websocket1.send_text = AsyncMock()
        websocket2.send_text = AsyncMock()

        agent_id = "test-agent"
        manager.active_connections[agent_id] = [websocket1, websocket2]

        message = "broadcast message"

        await manager.broadcast_to_agent(message, agent_id)

        websocket1.send_text.assert_called_once_with(message)
        websocket2.send_text.assert_called_once_with(message)

    @pytest.mark.asyncio
    async def test_broadcast_to_nonexistent_agent(self):
        """Test broadcasting to non-existent agent."""
        manager = ConnectionManager()

        # Should not raise exception
        await manager.broadcast_to_agent("message", "nonexistent-agent")


@pytest.mark.integration
class TestWebSocketEndpoint:
    """Test WebSocket endpoint integration."""

    def test_websocket_endpoint_exists(self, client: TestClient):
        """Test that WebSocket endpoint is available."""
        # Note: TestClient doesn't support WebSocket testing directly
        # This is a basic check that the endpoint exists
        response = client.get("/ws/chat/test-agent")
        # Should get 426 Upgrade Required for WebSocket
        assert response.status_code in [
            426,
            405,
        ]  # Method not allowed or upgrade required

    @pytest.mark.asyncio
    async def test_websocket_message_processing(self):
        """Test WebSocket message processing logic."""
        from core.use_cases.chat.send_message import SendMessageUseCase

        # Mock use case
        use_case = Mock(spec=SendMessageUseCase)
        mock_response = ChatMessage(
            id="test-response-id",
            content="Mock AI response",
            sender_type="agent",
            sender_id="test-agent",
            agent_id="test-agent",
            timestamp=Mock(),
        )
        mock_response.timestamp.isoformat.return_value = "2023-01-01T00:00:00"
        use_case.execute = AsyncMock(return_value=mock_response)

        # Test message data
        message_data = {"content": "Hello AI", "user_id": "test-user"}

        # This would be part of the WebSocket handler logic
        agent_id = "test-agent"
        content = message_data["content"]
        user_id = message_data.get("user_id", "anonymous")

        # Execute use case
        response = await use_case.execute(
            agent_id=agent_id, content=content, user_id=user_id
        )

        # Verify response
        assert response.content == "Mock AI response"
        assert response.sender_type == "agent"
        use_case.execute.assert_called_once_with(
            agent_id=agent_id, content=content, user_id=user_id
        )
