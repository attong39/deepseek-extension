"""
WebSocket Integration Tests

Tests WebSocket functionality including real-time communication, connection management, and message handling.
"""

import asyncio
from datetime import UTC, datetime
from typing import Any

import pytest
import ConnectionError
import all
import bool
import conn_ids
import content
import dict
import enumerate
import exclude_connection
import i
import int
import len
import list
import msg
import offline_user
import ping_result
import pong_result
import range
import reason
import room_connections
import self
import sender_name
import sent_msg
import str
import sum
import user


class MockWebSocketConnection:
    """Mock WebSocket connection for testing."""

    def __init__(self, connection_id: str, user_id: str = None):
        self.connection_id = connection_id
        self.user_id = user_id
        self.is_connected = False
        self.messages_sent = []
        self.messages_received = []
        self.last_ping = None
        self.last_pong = None
        self.created_at = datetime.now(UTC)
        self.closed_at = None
        self.close_reason = None

    async def connect(self) -> dict[str, Any]:
        """Simulate WebSocket connection."""
        self.is_connected = True
        connection_info = {
            "connection_id": self.connection_id,
            "user_id": self.user_id,
            "connected_at": datetime.now(UTC).isoformat(),
            "status": "connected",
        }
        return connection_info

    async def disconnect(self, reason: str = "client_disconnect") -> dict[str, Any]:
        """Simulate WebSocket disconnection."""
        self.is_connected = False
        self.closed_at = datetime.now(UTC)
        self.close_reason = reason

        return {
            "connection_id": self.connection_id,
            "closed_at": self.closed_at.isoformat(),
            "reason": reason,
            "status": "disconnected",
        }

    async def send_message(self, message: dict[str, Any]) -> dict[str, Any]:
        """Send message through WebSocket."""
        if not self.is_connected:
            raise ConnectionError("WebSocket not connected")

        # Simulate network delay
        await asyncio.sleep(0.001)

        sent_message = {
            "id": f"msg_{len(self.messages_sent) + 1}",
            "connection_id": self.connection_id,
            "type": message.get("type", "message"),
            "data": message.get("data", {}),
            "sent_at": datetime.now(UTC).isoformat(),
        }

        self.messages_sent.append(sent_message)
        return sent_message

    async def receive_message(self, message: dict[str, Any]) -> None:
        """Receive message from WebSocket."""
        if not self.is_connected:
            return

        received_message = {
            "id": f"recv_{len(self.messages_received) + 1}",
            "connection_id": self.connection_id,
            "type": message.get("type", "message"),
            "data": message.get("data", {}),
            "received_at": datetime.now(UTC).isoformat(),
        }

        self.messages_received.append(received_message)

    async def ping(self) -> dict[str, Any]:
        """Send ping frame."""
        if not self.is_connected:
            raise ConnectionError("WebSocket not connected")

        self.last_ping = datetime.now(UTC)
        return {"type": "ping", "timestamp": self.last_ping.isoformat()}

    async def pong(self) -> dict[str, Any]:
        """Send pong frame."""
        if not self.is_connected:
            raise ConnectionError("WebSocket not connected")

        self.last_pong = datetime.now(UTC)
        return {"type": "pong", "timestamp": self.last_pong.isoformat()}


class MockWebSocketManager:
    """Mock WebSocket manager for testing."""

    def __init__(self):
        self.connections: dict[str, MockWebSocketConnection] = {}
        self.user_connections: dict[str, list[str]] = {}  # user_id -> [connection_ids]
        self.rooms: dict[str, list[str]] = {}  # room_id -> [connection_ids]
        self.connection_counter = 0
        self.message_counter = 0

    async def create_connection(self, user_id: str = None) -> MockWebSocketConnection:
        """Create new WebSocket connection."""
        self.connection_counter += 1
        connection_id = f"ws_conn_{self.connection_counter}"

        connection = MockWebSocketConnection(connection_id, user_id)
        await connection.connect()

        self.connections[connection_id] = connection

        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(connection_id)

        return connection

    async def close_connection(
        self, connection_id: str, reason: str = "server_close"
    ) -> bool:
        """Close WebSocket connection."""
        if connection_id not in self.connections:
            return False

        connection = self.connections[connection_id]
        await connection.disconnect(reason)

        # Remove from user connections
        if connection.user_id and connection.user_id in self.user_connections:
            if connection_id in self.user_connections[connection.user_id]:
                self.user_connections[connection.user_id].remove(connection_id)
                if not self.user_connections[connection.user_id]:
                    del self.user_connections[connection.user_id]

        # Remove from rooms
        for room_id, room_connections in self.rooms.items():
            if connection_id in room_connections:
                room_connections.remove(connection_id)

        return True

    async def send_to_connection(
        self, connection_id: str, message: dict[str, Any]
    ) -> bool:
        """Send message to specific connection."""
        if connection_id not in self.connections:
            return False

        connection = self.connections[connection_id]
        if not connection.is_connected:
            return False

        await connection.send_message(message)
        return True

    async def send_to_user(self, user_id: str, message: dict[str, Any]) -> int:
        """Send message to all connections of a user."""
        if user_id not in self.user_connections:
            return 0

        sent_count = 0
        for connection_id in self.user_connections[user_id]:
            if await self.send_to_connection(connection_id, message):
                sent_count += 1

        return sent_count

    async def join_room(self, connection_id: str, room_id: str) -> bool:
        """Add connection to room."""
        if connection_id not in self.connections:
            return False

        if room_id not in self.rooms:
            self.rooms[room_id] = []

        if connection_id not in self.rooms[room_id]:
            self.rooms[room_id].append(connection_id)

        return True

    async def leave_room(self, connection_id: str, room_id: str) -> bool:
        """Remove connection from room."""
        if room_id not in self.rooms:
            return False

        if connection_id in self.rooms[room_id]:
            self.rooms[room_id].remove(connection_id)
            return True

        return False

    async def send_to_room(
        self, room_id: str, message: dict[str, Any], exclude_connection: str = None
    ) -> int:
        """Send message to all connections in room."""
        if room_id not in self.rooms:
            return 0

        sent_count = 0
        for connection_id in self.rooms[room_id]:
            if connection_id != exclude_connection:
                if await self.send_to_connection(connection_id, message):
                    sent_count += 1

        return sent_count

    async def broadcast(
        self, message: dict[str, Any], exclude_connection: str = None
    ) -> int:
        """Broadcast message to all active connections."""
        sent_count = 0
        for connection_id, connection in self.connections.items():
            if connection_id != exclude_connection and connection.is_connected:
                if await self.send_to_connection(connection_id, message):
                    sent_count += 1

        return sent_count

    async def get_connection_stats(self) -> dict[str, Any]:
        """Get WebSocket connection statistics."""
        active_connections = sum(
            1 for conn in self.connections.values() if conn.is_connected
        )
        total_connections = len(self.connections)
        active_users = len(
            [user_id for user_id, conn_ids in self.user_connections.items() if conn_ids]
        )
        total_rooms = len(self.rooms)

        # Calculate message stats
        total_messages_sent = sum(
            len(conn.messages_sent) for conn in self.connections.values()
        )
        total_messages_received = sum(
            len(conn.messages_received) for conn in self.connections.values()
        )

        return {
            "active_connections": active_connections,
            "total_connections": total_connections,
            "active_users": active_users,
            "total_rooms": total_rooms,
            "total_messages_sent": total_messages_sent,
            "total_messages_received": total_messages_received,
            "rooms": {
                room_id: len(conn_ids) for room_id, conn_ids in self.rooms.items()
            },
        }


@pytest.fixture
def ws_manager():
    """WebSocket manager fixture."""
    return MockWebSocketManager()


class TestWebSocketConnection:
    """Test WebSocket connection functionality."""

    @pytest.mark.asyncio
    async def test_create_connection(self, ws_manager):
        """Test creating WebSocket connection."""
        user_id = "test_user_1"

        connection = await ws_manager.create_connection(user_id)

        assert connection.connection_id is not None
        assert connection.user_id == user_id
        assert connection.is_connected is True
        assert connection.created_at is not None

        # Verify connection is tracked
        assert connection.connection_id in ws_manager.connections
        assert user_id in ws_manager.user_connections
        assert connection.connection_id in ws_manager.user_connections[user_id]

    @pytest.mark.asyncio
    async def test_close_connection(self, ws_manager):
        """Test closing WebSocket connection."""
        connection = await ws_manager.create_connection("test_user_2")
        connection_id = connection.connection_id

        # Close connection
        success = await ws_manager.close_connection(connection_id, "test_close")

        assert success is True
        assert connection.is_connected is False
        assert connection.close_reason == "test_close"
        assert connection.closed_at is not None

    @pytest.mark.asyncio
    async def test_multiple_connections_same_user(self, ws_manager):
        """Test multiple connections for same user."""
        user_id = "multi_conn_user"

        # Create multiple connections for same user
        conn1 = await ws_manager.create_connection(user_id)
        conn2 = await ws_manager.create_connection(user_id)
        conn3 = await ws_manager.create_connection(user_id)

        # Verify all connections are tracked
        assert len(ws_manager.user_connections[user_id]) == 3
        assert conn1.connection_id in ws_manager.user_connections[user_id]
        assert conn2.connection_id in ws_manager.user_connections[user_id]
        assert conn3.connection_id in ws_manager.user_connections[user_id]

        # Close one connection
        await ws_manager.close_connection(conn2.connection_id)

        # Verify only closed connection is removed
        assert len(ws_manager.user_connections[user_id]) == 2
        assert conn1.connection_id in ws_manager.user_connections[user_id]
        assert conn2.connection_id not in ws_manager.user_connections[user_id]
        assert conn3.connection_id in ws_manager.user_connections[user_id]


class TestWebSocketMessaging:
    """Test WebSocket messaging functionality."""

    @pytest.mark.asyncio
    async def test_send_to_connection(self, ws_manager):
        """Test sending message to specific connection."""
        connection = await ws_manager.create_connection("test_user")

        message = {
            "type": "chat_message",
            "data": {
                "content": "Hello WebSocket!",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        }

        success = await ws_manager.send_to_connection(connection.connection_id, message)

        assert success is True
        assert len(connection.messages_sent) == 1

        sent_message = connection.messages_sent[0]
        assert sent_message["type"] == "chat_message"
        assert sent_message["data"]["content"] == "Hello WebSocket!"

    @pytest.mark.asyncio
    async def test_send_to_user(self, ws_manager):
        """Test sending message to all user connections."""
        user_id = "broadcast_user"

        # Create multiple connections for user
        conn1 = await ws_manager.create_connection(user_id)
        conn2 = await ws_manager.create_connection(user_id)
        conn3 = await ws_manager.create_connection(user_id)

        message = {"type": "notification", "data": {"text": "New message for you!"}}

        sent_count = await ws_manager.send_to_user(user_id, message)

        assert sent_count == 3

        # Verify all connections received message
        for conn in [conn1, conn2, conn3]:
            assert len(conn.messages_sent) == 1
            assert conn.messages_sent[0]["type"] == "notification"

    @pytest.mark.asyncio
    async def test_send_to_disconnected_connection(self, ws_manager):
        """Test sending message to disconnected connection."""
        connection = await ws_manager.create_connection("test_user")
        connection_id = connection.connection_id

        # Disconnect connection
        await ws_manager.close_connection(connection_id)

        # Try to send message
        message = {"type": "test", "data": {}}
        success = await ws_manager.send_to_connection(connection_id, message)

        assert success is False
        assert len(connection.messages_sent) == 0

    @pytest.mark.asyncio
    async def test_concurrent_messaging(self, ws_manager):
        """Test concurrent message sending."""
        connection = await ws_manager.create_connection("test_user")

        # Send multiple messages concurrently
        messages = [
            {"type": "msg", "data": {"id": i, "content": f"Message {i}"}}
            for i in range(10)
        ]

        tasks = [
            ws_manager.send_to_connection(connection.connection_id, msg)
            for msg in messages
        ]

        results = await asyncio.gather(*tasks)

        # All messages should be sent successfully
        assert all(results)
        assert len(connection.messages_sent) == 10

        # Verify message order (might not be guaranteed in real implementation)
        sent_messages = connection.messages_sent
        for i, sent_msg in enumerate(sent_messages):
            assert sent_msg["data"]["id"] == i


class TestWebSocketRooms:
    """Test WebSocket room functionality."""

    @pytest.mark.asyncio
    async def test_join_room(self, ws_manager):
        """Test joining WebSocket room."""
        connection = await ws_manager.create_connection("test_user")
        room_id = "test_room"

        success = await ws_manager.join_room(connection.connection_id, room_id)

        assert success is True
        assert room_id in ws_manager.rooms
        assert connection.connection_id in ws_manager.rooms[room_id]

    @pytest.mark.asyncio
    async def test_leave_room(self, ws_manager):
        """Test leaving WebSocket room."""
        connection = await ws_manager.create_connection("test_user")
        room_id = "test_room"

        # Join room first
        await ws_manager.join_room(connection.connection_id, room_id)

        # Leave room
        success = await ws_manager.leave_room(connection.connection_id, room_id)

        assert success is True
        assert connection.connection_id not in ws_manager.rooms[room_id]

    @pytest.mark.asyncio
    async def test_send_to_room(self, ws_manager):
        """Test sending message to room."""
        room_id = "chat_room"

        # Create multiple connections and add to room
        connections = []
        for i in range(3):
            conn = await ws_manager.create_connection(f"user_{i}")
            await ws_manager.join_room(conn.connection_id, room_id)
            connections.append(conn)

        message = {
            "type": "room_message",
            "data": {"content": "Hello room!", "room": room_id},
        }

        sent_count = await ws_manager.send_to_room(room_id, message)

        assert sent_count == 3

        # Verify all connections in room received message
        for conn in connections:
            assert len(conn.messages_sent) == 1
            assert conn.messages_sent[0]["type"] == "room_message"

    @pytest.mark.asyncio
    async def test_send_to_room_with_exclusion(self, ws_manager):
        """Test sending message to room excluding sender."""
        room_id = "chat_room"

        # Create connections
        sender = await ws_manager.create_connection("sender")
        receiver1 = await ws_manager.create_connection("receiver1")
        receiver2 = await ws_manager.create_connection("receiver2")

        # Add all to room
        for conn in [sender, receiver1, receiver2]:
            await ws_manager.join_room(conn.connection_id, room_id)

        message = {
            "type": "user_message",
            "data": {"content": "Hello everyone!", "sender": "sender"},
        }

        # Send to room excluding sender
        sent_count = await ws_manager.send_to_room(
            room_id, message, exclude_connection=sender.connection_id
        )

        assert sent_count == 2  # Only receivers should get message

        # Verify sender didn't receive message
        assert len(sender.messages_sent) == 0

        # Verify receivers got message
        assert len(receiver1.messages_sent) == 1
        assert len(receiver2.messages_sent) == 1


class TestWebSocketBroadcast:
    """Test WebSocket broadcast functionality."""

    @pytest.mark.asyncio
    async def test_broadcast_to_all(self, ws_manager):
        """Test broadcasting message to all connections."""
        # Create multiple connections
        connections = []
        for i in range(5):
            conn = await ws_manager.create_connection(f"user_{i}")
            connections.append(conn)

        message = {
            "type": "system_announcement",
            "data": {"message": "System maintenance in 5 minutes"},
        }

        sent_count = await ws_manager.broadcast(message)

        assert sent_count == 5

        # Verify all connections received broadcast
        for conn in connections:
            assert len(conn.messages_sent) == 1
            assert conn.messages_sent[0]["type"] == "system_announcement"

    @pytest.mark.asyncio
    async def test_broadcast_with_exclusion(self, ws_manager):
        """Test broadcasting with exclusion."""
        # Create connections
        admin = await ws_manager.create_connection("admin")
        users = []
        for i in range(3):
            _ = await ws_manager.create_connection(f"user_{i}")
            users.append(user)

        message = {"type": "admin_message", "data": {"message": "New policy update"}}

        # Broadcast excluding admin
        sent_count = await ws_manager.broadcast(
            message, exclude_connection=admin.connection_id
        )

        assert sent_count == 3  # Only users should receive

        # Verify admin didn't receive message
        assert len(admin.messages_sent) == 0

        # Verify users received message
        for user in users:
            assert len(user.messages_sent) == 1

    @pytest.mark.asyncio
    async def test_broadcast_with_disconnected_connections(self, ws_manager):
        """Test broadcasting when some connections are disconnected."""
        # Create connections
        connections = []
        for i in range(4):
            conn = await ws_manager.create_connection(f"user_{i}")
            connections.append(conn)

        # Disconnect some connections
        await ws_manager.close_connection(connections[1].connection_id)
        await ws_manager.close_connection(connections[3].connection_id)

        message = {
            "type": "active_users_message",
            "data": {"message": "Only active users see this"},
        }

        sent_count = await ws_manager.broadcast(message)

        assert sent_count == 2  # Only active connections

        # Verify only active connections received message
        assert len(connections[0].messages_sent) == 1  # Active
        assert len(connections[1].messages_sent) == 0  # Disconnected
        assert len(connections[2].messages_sent) == 1  # Active
        assert len(connections[3].messages_sent) == 0  # Disconnected


class TestWebSocketConnectionManagement:
    """Test WebSocket connection management."""

    @pytest.mark.asyncio
    async def test_ping_pong(self, ws_manager):
        """Test WebSocket ping/pong mechanism."""
        connection = await ws_manager.create_connection("test_user")

        # Send ping
        await connection.ping()
        assert ping_result["type"] == "ping"
        assert connection.last_ping is not None

        # Send pong
        await connection.pong()
        assert pong_result["type"] == "pong"
        assert connection.last_pong is not None

        # Pong should be after ping
        assert connection.last_pong >= connection.last_ping

    @pytest.mark.asyncio
    async def test_connection_statistics(self, ws_manager):
        """Test getting connection statistics."""
        # Create various connections and rooms
        users = []
        for i in range(3):
            user_id = f"stats_user_{i}"
            conn = await ws_manager.create_connection(user_id)
            users.append((user_id, conn))

            # Join some rooms
            await ws_manager.join_room(conn.connection_id, f"room_{i}")
            if i < 2:  # First two users join common room
                await ws_manager.join_room(conn.connection_id, "common_room")

        # Send some messages
        for user_id, conn in users:
            await ws_manager.send_to_connection(
                conn.connection_id, {"type": "test", "data": {"user": user_id}}
            )

        # Disconnect one user
        await ws_manager.close_connection(users[2][1].connection_id)

        stats = await ws_manager.get_connection_stats()

        assert stats["total_connections"] == 3
        assert stats["active_connections"] == 2  # One disconnected
        assert stats["active_users"] == 2  # One user disconnected
        assert stats["total_rooms"] == 4  # room_0, room_1, room_2, common_room
        assert stats["total_messages_sent"] == 3

        # Check room stats
        assert stats["rooms"]["common_room"] == 2  # Two users still in common room
        assert stats["rooms"]["room_2"] == 0  # User left when disconnected


class TestWebSocketRealTimeFeatures:
    """Test real-time WebSocket features."""

    @pytest.mark.asyncio
    async def test_chat_conversation_flow(self, ws_manager):
        """Test real-time chat conversation flow."""
        # Create chat participants
        user1 = await ws_manager.create_connection("user1")
        user2 = await ws_manager.create_connection("user2")

        chat_room = "chat_123"

        # Users join chat room
        await ws_manager.join_room(user1.connection_id, chat_room)
        await ws_manager.join_room(user2.connection_id, chat_room)

        # Simulate conversation
        messages = [
            ("user1", "Hello! How are you?"),
            ("user2", "Hi! I'm doing great, thanks!"),
            ("user1", "That's wonderful to hear!"),
            ("user2", "How about you?"),
            ("user1", "I'm doing well too!"),
        ]

        for sender_name, content in messages:
            sender_conn = user1 if sender_name == "user1" else user2

            message = {
                "type": "chat_message",
                "data": {
                    "sender": sender_name,
                    "content": content,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            }

            # Send to room excluding sender
            await ws_manager.send_to_room(
                chat_room, message, exclude_connection=sender_conn.connection_id
            )

        # Verify message counts
        # user1 should receive messages from user2 (2 messages)
        user1_received = [
            msg for msg in user1.messages_sent if msg["data"]["sender"] == "user2"
        ]
        assert len(user1_received) == 2

        # user2 should receive messages from user1 (3 messages)
        user2_received = [
            msg for msg in user2.messages_sent if msg["data"]["sender"] == "user1"
        ]
        assert len(user2_received) == 3

    @pytest.mark.asyncio
    async def test_typing_indicators(self, ws_manager):
        """Test real-time typing indicators."""
        # Create chat participants
        user1 = await ws_manager.create_connection("user1")
        user2 = await ws_manager.create_connection("user2")
        user3 = await ws_manager.create_connection("user3")

        chat_room = "typing_test_room"

        # All join chat room
        for user in [user1, user2, user3]:
            await ws_manager.join_room(user.connection_id, chat_room)

        # user1 starts typing
        typing_message = {
            "type": "typing_start",
            "data": {"user": "user1", "timestamp": datetime.now(UTC).isoformat()},
        }

        await ws_manager.send_to_room(
            chat_room, typing_message, exclude_connection=user1.connection_id
        )

        # user1 stops typing
        stop_typing_message = {
            "type": "typing_stop",
            "data": {"user": "user1", "timestamp": datetime.now(UTC).isoformat()},
        }

        await ws_manager.send_to_room(
            chat_room, stop_typing_message, exclude_connection=user1.connection_id
        )

        # Verify other users received typing indicators
        for user in [user2, user3]:
            assert len(user.messages_sent) == 2
            assert user.messages_sent[0]["type"] == "typing_start"
            assert user.messages_sent[1]["type"] == "typing_stop"

    @pytest.mark.asyncio
    async def test_presence_updates(self, ws_manager):
        """Test real-time presence updates."""
        # Create users
        users = []
        for i in range(4):
            _ = await ws_manager.create_connection(f"presence_user_{i}")
            users.append(user)

        presence_room = "presence_room"

        # Users join presence room
        for user in users:
            await ws_manager.join_room(user.connection_id, presence_room)

            # Announce user joined
            join_message = {
                "type": "user_joined",
                "data": {
                    "user_id": user.user_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            }

            await ws_manager.send_to_room(
                presence_room, join_message, exclude_connection=user.connection_id
            )

        # One user goes offline
        users[2]
        await ws_manager.close_connection(offline_user.connection_id)

        # Announce user left
        leave_message = {
            "type": "user_left",
            "data": {
                "user_id": offline_user.user_id,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        }

        await ws_manager.send_to_room(presence_room, leave_message)

        # Verify presence messages received
        # users[0] should have received 3 join messages (from users 1,2,3) + 1 leave message
        online_users = [users[0], users[1], users[3]]  # Exclude offline user

        for user in online_users:
            join_messages = [
                msg for msg in user.messages_sent if msg["type"] == "user_joined"
            ]
            leave_messages = [
                msg for msg in user.messages_sent if msg["type"] == "user_left"
            ]

            assert len(join_messages) == 3  # Received joins from other 3 users
            assert len(leave_messages) == 1  # Received one leave notification


if __name__ == "__main__":
    pytest.main([__file__])
