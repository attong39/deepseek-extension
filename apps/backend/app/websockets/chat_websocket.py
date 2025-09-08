"""


Chat WebSocket Handler.





Handles real-time chat communication via WebSocket connections.


"""

import json
import uuid
from datetime import UTC, datetime
from typing import Annotated, Any

from app.deps.services import get_chat_service
from app.utils.mapper import camel_to_snake_recursive
from app.websockets.schemas import (
import Exception
import ValueError
import agent_id
import bool
import cid
import conversation_id
import dead
import dict
import e
import exclude_connection
import hasattr
import index
import int
import key
import keys_to_delete
import len
import list
import message
import notification
import self
import str
import svc
import ws
    AssistantReplyEvent,
    ChatCompletedEvent,
    ChatErrorEvent,
    ChatTokenEvent,
    ConversationHistoryEvent,
    NewMessageEvent,
    PongEvent,
    StatusUpdatedEvent,
    TypingIndicatorEvent,
    to_json,
)
from fastapi import Depends, WebSocket, WebSocketDisconnect, status
from fastapi.routing import APIRouter

router = APIRouter()


class WebSocketConnectionManager:
    """Manages WebSocket connections for real-time chat."""

    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}

        self.user_connections: dict[str, list[str]] = {}

        self.conversation_connections: dict[str, list[str]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        connection_id: str,
        user_id: str,
        conversation_id: str | None = None,
    ) -> None:
        """Accept a WebSocket connection."""

        await websocket.accept()

        self.active_connections[connection_id] = websocket

        # Track user connections

        if user_id not in self.user_connections:
            self.user_connections[user_id] = []

        self.user_connections[user_id].append(connection_id)

        # Track conversation connections

        if conversation_id:
            if conversation_id not in self.conversation_connections:
                self.conversation_connections[conversation_id] = []

            self.conversation_connections[conversation_id].append(connection_id)

    def disconnect(
        self, connection_id: str, user_id: str, conversation_id: str | None = None
    ) -> None:
        """Remove a WebSocket connection."""

        # Remove from active connections

        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

        # Remove from user connections

        if user_id in self.user_connections:
            if connection_id in self.user_connections[user_id]:
                self.user_connections[user_id].remove(connection_id)

            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        # Remove from conversation connections

        if conversation_id and conversation_id in self.conversation_connections:
            if connection_id in self.conversation_connections[conversation_id]:
                self.conversation_connections[conversation_id].remove(connection_id)

            if not self.conversation_connections[conversation_id]:
                del self.conversation_connections[conversation_id]

    async def send_personal_message(self, message: str, connection_id: str) -> None:
        """Send a message to a specific connection."""

        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]

            try:
                await websocket.send_text(message)

            except Exception:
                # Connection is broken, remove it

                self._cleanup_broken_connection(connection_id)

    async def send_to_user(self, message: str, user_id: str) -> None:
        """Send a message to all connections of a user."""

        if user_id in self.user_connections:
            broken_connections = []

            for connection_id in self.user_connections[user_id]:
                if connection_id in self.active_connections:
                    websocket = self.active_connections[connection_id]

                    try:
                        await websocket.send_text(message)

                    except Exception:
                        broken_connections.append(connection_id)

            # Clean up broken connections

            for connection_id in broken_connections:
                self._cleanup_broken_connection(connection_id)

    async def broadcast_to_conversation(
        self, message: str, conversation_id: str, exclude_connection: str | None = None
    ) -> None:
        """Broadcast a message to all connections in a conversation."""

        if conversation_id in self.conversation_connections:
            broken_connections = []

            for connection_id in self.conversation_connections[conversation_id]:
                if (
                    connection_id != exclude_connection
                    and connection_id in self.active_connections
                ):
                    websocket = self.active_connections[connection_id]

                    try:
                        await websocket.send_text(message)

                    except Exception:
                        broken_connections.append(connection_id)

            # Clean up broken connections

            for connection_id in broken_connections:
                self._cleanup_broken_connection(connection_id)

    def _remove_conn_from_index(self, index: dict[str, list[str]], cid: str) -> None:
        keys_to_delete: list[str] = []
        for key, conns in index.items():
            if cid in conns:
                try:
                    conns.remove(cid)
                except ValueError:
                    pass
                if not conns:
                    keys_to_delete.append(key)
        for key in keys_to_delete:
            index.pop(key, None)

    def _cleanup_broken_connection(self, connection_id: str) -> None:
        """Clean up a broken connection."""
        self.active_connections.pop(connection_id, None)
        self._remove_conn_from_index(self.user_connections, connection_id)
        self._remove_conn_from_index(self.conversation_connections, connection_id)

    def get_connection_count(self) -> int:
        """Get total number of active connections."""

        return len(self.active_connections)

    def get_user_connection_count(self, user_id: str) -> int:
        """Get number of connections for a specific user."""

        return len(self.user_connections.get(user_id, []))

    def get_conversation_connection_count(self, conversation_id: str) -> int:
        """Get number of connections for a specific conversation."""

        return len(self.conversation_connections.get(conversation_id, []))


# --- Compatibility ConnectionManager (legacy API) ---
class ConnectionManager:
    """Legacy manager API used by old tests (agent-scoped broadcasting).

    Lưu ý: Đây là lớp tương thích để tránh phá test cũ. Với logic production,
    hãy dùng WebSocketConnectionManager ở trên.
    """

    def __init__(self) -> None:
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, agent_id: str) -> None:
        await websocket.accept()
        if agent_id not in self.active_connections:
            self.active_connections[agent_id] = []
        self.active_connections[agent_id].append(websocket)

    def disconnect(self, websocket: WebSocket, agent_id: str) -> None:
        if agent_id in self.active_connections:
            conns = self.active_connections[agent_id]
            if websocket in conns:
                conns.remove(websocket)
            if not conns:
                del self.active_connections[agent_id]

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        try:
            await websocket.send_text(message)
        except Exception:
            # best-effort: ignore
            pass

    async def broadcast_to_agent(self, message: str, agent_id: str) -> None:
        conns = self.active_connections.get(agent_id, [])
        dead: list[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        if dead:
            for ws in dead:
                self.disconnect(ws, agent_id)


# Global connection manager instance


connection_manager = WebSocketConnectionManager()


@router.websocket("/ws/chat/{conversation_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    conversation_id: str,
    svc: Annotated[Any, Depends(get_chat_service)],
) -> None:
    """


    WebSocket endpoint for real-time chat in a specific conversation.





    Args:


        websocket: WebSocket connection


        conversation_id: ID of the conversation to join


        user_id: Optional user ID (should be extracted from token in real implementation)


    """

    # Verify JWT from query param
    token = websocket.query_params.get("token")
    user_id = "anonymous"
    try:
        if token:
            from app.security.jwt import verify_jwt_token

            payload = verify_jwt_token(token)
            user_id = payload.sub
        else:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    connection_id = str(uuid.uuid4())

    await connection_manager.connect(websocket, connection_id, user_id, conversation_id)

    try:
        # Send confirmation matching FE schema
        await connection_manager.send_personal_message(
            to_json(
                AssistantReplyEvent(
                    content="connected", timestamp=datetime.now(UTC).isoformat()
                )
            ),
            connection_id,
        )

        # Optional: notify others (not required by FE schema)

        while True:
            # Receive message from client

            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
                # Normalize keys: accept both camelCase and snake_case from clients
                message_data = camel_to_snake_recursive(message_data)

                await _handle_websocket_message(
                    message_data, connection_id, user_id, conversation_id, svc
                )

            except json.JSONDecodeError:
                await connection_manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "error",
                            "message": "Invalid JSON format",
                            "timestamp": datetime.now(UTC).isoformat(),
                        }
                    ),
                    connection_id,
                )

            except Exception as e:
                await connection_manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "error",
                            "message": f"Error processing message: {e!s}",
                            "timestamp": datetime.now(UTC).isoformat(),
                        }
                    ),
                    connection_id,
                )

    except WebSocketDisconnect:
        connection_manager.disconnect(connection_id, user_id, conversation_id)


@router.websocket("/ws/chat")
async def websocket_global_chat(websocket: WebSocket) -> None:
    """


    WebSocket endpoint for global chat notifications.





    Args:


        websocket: WebSocket connection


        user_id: Optional user ID (should be extracted from token)


    """

    # Verify JWT
    token = websocket.query_params.get("token")
    user_id = "anonymous"
    try:
        if token:
            from app.security.jwt import verify_jwt_token

            payload = verify_jwt_token(token)
            user_id = payload.sub
        else:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    connection_id = str(uuid.uuid4())

    await connection_manager.connect(websocket, connection_id, user_id)

    try:
        # Send connection confirmation

        await connection_manager.send_personal_message(
            to_json(
                AssistantReplyEvent(
                    content="connected", timestamp=datetime.now(UTC).isoformat()
                )
            ),
            connection_id,
        )

        while True:
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
                message_data = camel_to_snake_recursive(message_data)

                await _handle_global_websocket_message(
                    message_data, connection_id, user_id
                )

            except json.JSONDecodeError:
                await connection_manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "error",
                            "message": "Invalid JSON format",
                            "timestamp": datetime.now(UTC).isoformat(),
                        }
                    ),
                    connection_id,
                )

            except Exception as e:
                await connection_manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "error",
                            "message": f"Error processing message: {e!s}",
                            "timestamp": datetime.now(UTC).isoformat(),
                        }
                    ),
                    connection_id,
                )

    except WebSocketDisconnect:
        connection_manager.disconnect(connection_id, user_id)


async def _handle_websocket_message(
    message_data: dict[str, Any],
    connection_id: str,
    user_id: str,
    conversation_id: str,
    svc: Any,
) -> None:
    """


    Handle incoming WebSocket message for conversation.





    Args:


        message_data: Parsed message data


        connection_id: WebSocket connection ID


        user_id: User ID


        conversation_id: Conversation ID


    """

    message_type = message_data.get("type")

    if message_type == "chat_message":
        # Handle chat message

        content = message_data.get("content", "")

        if content.strip():
            # If service supports streaming, forward tokens from service
            if hasattr(svc, "stream_send"):
                try:
                    seq = 0
                    async for token in svc.stream_send(
                        user_id=user_id,
                        session_id=conversation_id,
                        role="user",
                        content=content,
                        attachments=message_data.get("attachments", []),
                        metadata=message_data.get("metadata", {}),
                    ):
                        seq += 1
                        evt = ChatTokenEvent(
                            content=str(token),
                            seq=seq,
                            timestamp=datetime.now(UTC).isoformat(),
                        )
                        await connection_manager.broadcast_to_conversation(
                            to_json(evt), conversation_id
                        )
                    # stream complete
                    completed = ChatCompletedEvent(
                        content="", timestamp=datetime.now(UTC).isoformat()
                    )
                    await connection_manager.broadcast_to_conversation(
                        to_json(completed), conversation_id
                    )
                except Exception as e:
                    err = ChatErrorEvent(code="stream_error", message=str(e))
                    await connection_manager.send_personal_message(
                        to_json(err), connection_id
                    )
                return

            # Fallback: broadcast as a new message (legacy behavior)
            event_new = NewMessageEvent(
                message={
                    "id": str(uuid.uuid4()),
                    "content": content,
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            )
            await connection_manager.broadcast_to_conversation(
                to_json(event_new), conversation_id
            )

    elif message_type == "typing_indicator":
        # Handle typing indicator

        is_typing = message_data.get("is_typing", False)

        event_typing = TypingIndicatorEvent(
            user_id=user_id,
            is_typing=bool(is_typing),
            conversation_id=conversation_id,
            timestamp=datetime.now(UTC).isoformat(),
        )
        await connection_manager.broadcast_to_conversation(
            to_json(event_typing), conversation_id, exclude_connection=connection_id
        )

    elif message_type == "ping":
        # Handle ping/keepalive

        await connection_manager.send_personal_message(
            to_json(PongEvent(ts=int(datetime.now(UTC).timestamp() * 1000))),
            connection_id,
        )

    elif message_type == "request_history":
        # Handle request for conversation history

        # In a real implementation, fetch from database

        event_history = ConversationHistoryEvent(
            messages=[],
            conversation_id=conversation_id,
            timestamp=datetime.now(UTC).isoformat(),
        )
        await connection_manager.send_personal_message(
            to_json(event_history), connection_id
        )


async def _handle_global_websocket_message(
    message_data: dict[str, Any], connection_id: str, _user_id: str
) -> None:
    """


    Handle incoming WebSocket message for global chat.





    Args:


        message_data: Parsed message data


        connection_id: WebSocket connection ID


        user_id: User ID


    """

    message_type = message_data.get("type")

    if message_type == "ping":
        # Handle ping/keepalive

        await connection_manager.send_personal_message(
            to_json(PongEvent(ts=int(datetime.now(UTC).timestamp() * 1000))),
            connection_id,
        )

    elif message_type == "status_update":
        # Handle status update

        status = message_data.get("status", "online")

        # In a real implementation, update user status in database

    event_status = StatusUpdatedEvent(
        status=str(status), timestamp=datetime.now(UTC).isoformat()
    )
    await connection_manager.send_personal_message(to_json(event_status), connection_id)


# Utility functions for external use


async def notify_user(user_id: str, notification: dict[str, Any]) -> None:
    """Send notification to a specific user via WebSocket."""

    await connection_manager.send_to_user(json.dumps(notification), user_id)


async def broadcast_to_conversation(
    conversation_id: str, message: dict[str, Any]
) -> None:
    """Broadcast message to all users in a conversation."""

    await connection_manager.broadcast_to_conversation(
        json.dumps(message), conversation_id
    )


def get_connection_stats() -> dict[str, Any]:
    """Get WebSocket connection statistics."""

    return {
        "total_connections": connection_manager.get_connection_count(),
        "active_users": len(connection_manager.user_connections),
        "active_conversations": len(connection_manager.conversation_connections),
        "timestamp": datetime.now(UTC).isoformat(),
    }
