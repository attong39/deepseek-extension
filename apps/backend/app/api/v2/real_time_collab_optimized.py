from datetime import datetime
import Exception
import bool
import classmethod
import cls
import connection
import cursor_update
import dict
import e
import event_type
import initial_content
import int
import len
import list
import min
import op
import op1
import op2
import operation_request
import request
import role
import self
import session
import sessions
import set
import since_version
import staticmethod
import str
import sum
import tuple
import user
import user_cursors
import user_id
import websocket

# zeta_vn/app/api/v2/real_time_collab_optimized.py
"""
Real-time Collaboration v2 - Optimized với CRDT & Event Sourcing

Tối ưu hóa:
1. Conflict-free Replicated Data Types (CRDT) cho collaborative editing
2. Event sourcing với snapshot optimization
3. Real-time synchronization với WebSocket clustering
4. Collaborative AI với shared context và multi-user sessions
"""

from __future__ import annotations

import json
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import UTC
from enum import Enum
from typing import Any

from app.api.v1._common_audit import audit
from app.api.v1._common_cache import acached
from app.api.v1._common_idempotency import idempotency_guard
from app.api.v1._common_security import Role, User, require_roles
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from pydantic import BaseModel, Field

router = APIRouter(prefix="/real-time-collab", tags=["RealTimeCollab-V2-Optimized"])

# === Constants ===

SESSION_NOT_FOUND = "Session not found"
DOCUMENT_NOT_FOUND = "Document not found"
USER_NOT_FOUND = "User not found"
MAX_SNAPSHOT_INTERVAL = 100  # Events before taking snapshot

# === Collaboration Models ===


class DocumentType(str, Enum):
    TEXT = "text"  # Plain text document
    CODE = "code"  # Source code
    MARKDOWN = "markdown"  # Markdown document
    JSON = "json"  # JSON data
    WHITEBOARD = "whiteboard"  # Visual whiteboard
    MINDMAP = "mindmap"  # Mind mapping


class OperationType(str, Enum):
    INSERT = "insert"  # Insert text/content
    DELETE = "delete"  # Delete text/content
    RETAIN = "retain"  # Keep existing content
    FORMAT = "format"  # Apply formatting
    CURSOR = "cursor"  # Cursor movement
    SELECTION = "selection"  # Text selection


class UserRole(str, Enum):
    OWNER = "owner"  # Document owner
    EDITOR = "editor"  # Can edit
    VIEWER = "viewer"  # Can only view
    COMMENTER = "commenter"  # Can comment only


class EventType(str, Enum):
    OPERATION = "operation"  # Document operation
    CURSOR = "cursor"  # Cursor position update
    SELECTION = "selection"  # Selection change
    USER_JOIN = "user_join"  # User joined session
    USER_LEAVE = "user_leave"  # User left session
    COMMENT = "comment"  # Comment added
    AI_SUGGESTION = "ai_suggestion"  # AI suggestion
    SNAPSHOT = "snapshot"  # Document snapshot


@dataclass
class CRDTOperation:
    """Conflict-free Replicated Data Type operation"""

    op_id: str
    operation_type: OperationType
    position: int
    content: str = ""
    length: int = 0
    attributes: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: str = ""
    vector_clock: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "op_id": self.op_id,
            "operation_type": self.operation_type,
            "position": self.position,
            "content": self.content,
            "length": self.length,
            "attributes": self.attributes,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "vector_clock": self.vector_clock,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CRDTOperation:
        return cls(
            op_id=data["op_id"],
            operation_type=OperationType(data["operation_type"]),
            position=data["position"],
            content=data.get("content", ""),
            length=data.get("length", 0),
            attributes=data.get("attributes", {}),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            user_id=data["user_id"],
            vector_clock=data.get("vector_clock", {}),
        )


@dataclass
class DocumentSnapshot:
    """Document state snapshot for optimization"""

    snapshot_id: str
    content: str
    version: int
    timestamp: datetime
    operations_since_snapshot: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "content": self.content,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "operations_since_snapshot": self.operations_since_snapshot,
        }


@dataclass
class CollaborativeSession:
    """Real-time collaboration session"""

    session_id: str
    document_id: str
    document_type: DocumentType
    owner_id: str
    participants: dict[str, UserRole] = field(default_factory=dict)
    active_connections: set[str] = field(default_factory=set)
    operations: deque = field(default_factory=deque)
    vector_clock: dict[str, int] = field(default_factory=dict)
    latest_snapshot: DocumentSnapshot | None = None
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    ai_enabled: bool = True


@dataclass
class UserCursor:
    """User cursor position in document"""

    user_id: str
    position: int
    selection_start: int | None = None
    selection_end: int | None = None
    timestamp: datetime = field(default_factory=datetime.now)


class SessionCreateRequest(BaseModel):
    document_type: DocumentType
    initial_content: str = ""
    title: str = Field(min_length=1, max_length=200)
    ai_enabled: bool = True
    permissions: dict[str, UserRole] = Field(default_factory=dict)


class OperationRequest(BaseModel):
    operation_type: OperationType
    position: int
    content: str = ""
    length: int = 0
    attributes: dict[str, Any] = Field(default_factory=dict)


class JoinSessionRequest(BaseModel):
    session_id: str
    role: UserRole = UserRole.VIEWER


class CursorUpdate(BaseModel):
    position: int
    selection_start: int | None = None
    selection_end: int | None = None


class CommentRequest(BaseModel):
    content: str
    position: int
    thread_id: str | None = None


# === CRDT Engine ===


class CRDTEngine:
    """Conflict-free Replicated Data Types engine for collaborative editing"""

    @staticmethod
    def apply_operation(content: str, operation: CRDTOperation) -> str:
        """Apply CRDT operation to content"""
        if operation.operation_type == OperationType.INSERT:
            # Insert content at position
            if operation.position <= len(content):
                return (
                    content[: operation.position]
                    + operation.content
                    + content[operation.position :]
                )
            else:
                return content + operation.content

        elif operation.operation_type == OperationType.DELETE:
            # Delete content from position
            start = operation.position
            end = min(start + operation.length, len(content))
            return content[:start] + content[end:]

        elif operation.operation_type == OperationType.RETAIN:
            # Keep content as-is (used for formatting)
            return content

        return content

    @staticmethod
    def transform_operations(
        op1: CRDTOperation, op2: CRDTOperation
    ) -> tuple[CRDTOperation, CRDTOperation]:
        """Transform operations for conflict resolution (Operational Transformation)"""
        # Simplified transformation - in production use a proper OT library
        if (
            op1.operation_type == OperationType.INSERT
            and op2.operation_type == OperationType.INSERT
        ):
            if op1.position <= op2.position:
                # op1 happens first, shift op2 position
                op2_transformed = CRDTOperation(
                    op_id=op2.op_id,
                    operation_type=op2.operation_type,
                    position=op2.position + len(op1.content),
                    content=op2.content,
                    timestamp=op2.timestamp,
                    user_id=op2.user_id,
                    vector_clock=op2.vector_clock.copy(),
                )
                return op1, op2_transformed
            else:
                # op2 happens first, shift op1 position
                op1_transformed = CRDTOperation(
                    op_id=op1.op_id,
                    operation_type=op1.operation_type,
                    position=op1.position + len(op2.content),
                    content=op1.content,
                    timestamp=op1.timestamp,
                    user_id=op1.user_id,
                    vector_clock=op1.vector_clock.copy(),
                )
                return op1_transformed, op2

        # For other operation types, return as-is (simplified)
        return op1, op2

    @staticmethod
    def create_snapshot(
        operations: list[CRDTOperation], initial_content: str = ""
    ) -> DocumentSnapshot:
        """Create document snapshot from operations"""
        content = initial_content

        # Apply all operations in order
        for operation in operations:
            content = CRDTEngine.apply_operation(content, operation)

        return DocumentSnapshot(
            snapshot_id=f"snap_{uuid.uuid4().hex[:8]}",
            content=content,
            version=len(operations),
            timestamp=datetime.now(UTC),
        )


# === Event Sourcing System ===


class EventStore:
    """Event sourcing store for collaboration events"""

    def __init__(self):
        self.events: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.snapshots: dict[str, DocumentSnapshot] = {}

    async def append_event(
        self, session_id: str, event_type: EventType, data: dict[str, Any]
    ):
        """Append event to stream"""
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now(UTC).isoformat(),
            "version": len(self.events[session_id]) + 1,
        }

        self.events[session_id].append(event)

        # Create snapshot if needed
        if len(self.events[session_id]) % MAX_SNAPSHOT_INTERVAL == 0:
            await self._create_snapshot(session_id)

    async def get_events_since(
        self, session_id: str, since_version: int = 0
    ) -> list[dict[str, Any]]:
        """Get events since version"""
        events = self.events.get(session_id, [])
        return [event for event in events if event["version"] > since_version]

    async def get_latest_snapshot(self, session_id: str) -> DocumentSnapshot | None:
        """Get latest snapshot for session"""
        return self.snapshots.get(session_id)

    async def _create_snapshot(self, session_id: str):
        """Create snapshot from events"""
        events = self.events.get(session_id, [])
        if not events:
            return

        # Get operations from events
        operations = []
        for event in events:
            if event["event_type"] == EventType.OPERATION:
                op_data = event["data"]
                operation = CRDTOperation.from_dict(op_data)
                operations.append(operation)

        # Create snapshot
        snapshot = CRDTEngine.create_snapshot(operations)
        self.snapshots[session_id] = snapshot


# === WebSocket Connection Manager ===


class ConnectionManager:
    """Manages WebSocket connections for real-time collaboration"""

    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)
        self.user_sessions: dict[str, set[str]] = defaultdict(
            set
        )  # user_id -> session_ids
        self.session_users: dict[str, set[str]] = defaultdict(
            set
        )  # session_id -> user_ids

    async def connect(self, websocket: WebSocket, session_id: str, user_id: str):
        """Connect user to session"""
        await websocket.accept()
        self.connections[session_id].add(websocket)
        self.user_sessions[user_id].add(session_id)
        self.session_users[session_id].add(user_id)

    def disconnect(self, websocket: WebSocket, session_id: str, user_id: str):
        """Disconnect user from session"""
        self.connections[session_id].discard(websocket)
        self.user_sessions[user_id].discard(session_id)
        self.session_users[session_id].discard(user_id)

        # Clean up empty sets
        if not self.connections[session_id]:
            del self.connections[session_id]
        if not self.user_sessions[user_id]:
            del self.user_sessions[user_id]
        if not self.session_users[session_id]:
            del self.session_users[session_id]

    async def broadcast_to_session(
        self,
        session_id: str,
        message: dict[str, Any],
        exclude_user: str | None = None,
    ):
        """Broadcast message to all users in session"""
        if session_id not in self.connections:
            return

        message_text = json.dumps(message)

        # Get connections to broadcast to
        connections = set(self.connections[session_id])

        # Remove disconnected connections
        disconnected = set()
        for connection in connections:
            try:
                await connection.send_text(message_text)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            self.connections[session_id].discard(connection)

    def get_session_users(self, session_id: str) -> set[str]:
        """Get users connected to session"""
        return self.session_users.get(session_id, set())


# === AI Collaboration Assistant ===


class AICollaborator:
    """AI assistant for collaborative editing"""

    @staticmethod
    async def suggest_edits(content: str, cursor_position: int) -> list[dict[str, Any]]:
        """Generate AI suggestions for content improvement"""
        # Placeholder implementation - integrate with actual AI model
        suggestions = []

        # Detect potential improvements
        if "TODO" in content:
            suggestions.append(
                {
                    "type": "completion",
                    "position": content.find("TODO"),
                    "suggestion": "Complete this task",
                    "confidence": 0.8,
                }
            )

        # Grammar suggestions (simplified)
        if " teh " in content.lower():
            pos = content.lower().find(" teh ")
            suggestions.append(
                {
                    "type": "correction",
                    "position": pos + 1,
                    "original": "teh",
                    "suggestion": "the",
                    "confidence": 0.95,
                }
            )

        return suggestions

    @staticmethod
    async def summarize_changes(operations: list[CRDTOperation]) -> str:
        """Summarize recent changes for users"""
        if not operations:
            return "No recent changes"

        # Analyze operations
        inserts = sum(
            1 for op in operations if op.operation_type == OperationType.INSERT
        )
        deletes = sum(
            1 for op in operations if op.operation_type == OperationType.DELETE
        )

        # Generate summary
        summary_parts = []
        if inserts > 0:
            summary_parts.append(f"{inserts} insertions")
        if deletes > 0:
            summary_parts.append(f"{deletes} deletions")

        return (
            f"Recent changes: {', '.join(summary_parts)}"
            if summary_parts
            else "Minor edits"
        )


# === Global State ===

sessions: dict[str, CollaborativeSession] = {}
event_store = EventStore()
connection_manager = ConnectionManager()
user_cursors: dict[str, dict[str, UserCursor]] = defaultdict(
    dict
)  # session_id -> user_id -> cursor

# === API Endpoints ===


@router.post("/sessions/create")
async def create_session(
    request: SessionCreateRequest, user: User = Depends(require_roles(Role.USER))
) -> dict[str, Any]:
    """Create new collaborative session"""
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    document_id = f"doc_{uuid.uuid4().hex[:8]}"

    await audit(
        "collab.session.create",
        actor=user.sub,
        payload={
            "session_id": session_id,
            "document_type": request.document_type,
            "title": request.title,
        },
    )

    # Initialize session
    _ = CollaborativeSession(
        session_id=session_id,
        document_id=document_id,
        document_type=request.document_type,
        owner_id=user.sub,
        ai_enabled=request.ai_enabled,
    )

    # Set owner permissions
    session.participants[user.sub] = UserRole.OWNER

    # Add other participants
    for user_id, role in request.permissions.items():
        session.participants[user_id] = role

    # Create initial snapshot if content provided
    if request.initial_content:
        snapshot = DocumentSnapshot(
            snapshot_id=f"snap_{uuid.uuid4().hex[:8]}",
            content=request.initial_content,
            version=0,
            timestamp=datetime.now(UTC),
        )
        session.latest_snapshot = snapshot
        await event_store.snapshots.__setitem__(session_id, snapshot)

    sessions[session_id] = session

    # Record session creation event
    await event_store.append_event(
        session_id,
        EventType.USER_JOIN,
        {
            "user_id": user.sub,
            "role": UserRole.OWNER,
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )

    return {
        "session_id": session_id,
        "document_id": document_id,
        "status": "created",
        "participants": {
            user_id: role.value for user_id, role in session.participants.items()
        },
        "ai_enabled": session.ai_enabled,
    }


@router.post("/sessions/{session_id}/join")
async def join_session(
    session_id: str,
    request: JoinSessionRequest,
    user: User = Depends(require_roles(Role.USER)),
):
    """Join collaborative session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=SESSION_NOT_FOUND)

    _ = sessions[session_id]

    # Check permissions
    if user.sub not in session.participants:
        # Add as viewer if not in participant list
        session.participants[user.sub] = UserRole.VIEWER

    await audit(
        "collab.session.join",
        actor=user.sub,
        payload={"session_id": session_id, "role": session.participants[user.sub]},
    )

    # Record join event
    await event_store.append_event(
        session_id,
        EventType.USER_JOIN,
        {
            "user_id": user.sub,
            "role": session.participants[user.sub],
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )

    # Get current document state
    latest_snapshot = await event_store.get_latest_snapshot(session_id)
    recent_events = await event_store.get_events_since(
        session_id, latest_snapshot.version if latest_snapshot else 0
    )

    return {
        "status": "joined",
        "role": session.participants[user.sub],
        "current_snapshot": latest_snapshot.to_dict() if latest_snapshot else None,
        "recent_events": recent_events,
        "active_users": list(connection_manager.get_session_users(session_id)),
    }


@router.post("/sessions/{session_id}/operations")
async def submit_operation(
    session_id: str,
    operation_request: OperationRequest,
    user: User = Depends(require_roles(Role.USER)),
    _: str = Depends(idempotency_guard),
):
    """Submit operation to collaborative document"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=SESSION_NOT_FOUND)

    _ = sessions[session_id]

    # Check permissions
    user_role = session.participants.get(user.sub, UserRole.VIEWER)
    if user_role not in [UserRole.OWNER, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Create CRDT operation
    operation = CRDTOperation(
        op_id=f"op_{uuid.uuid4().hex[:8]}",
        operation_type=operation_request.operation_type,
        position=operation_request.position,
        content=operation_request.content,
        length=operation_request.length,
        attributes=operation_request.attributes,
        user_id=user.sub,
        vector_clock=session.vector_clock.copy(),
    )

    # Update vector clock
    session.vector_clock[user.sub] = session.vector_clock.get(user.sub, 0) + 1
    operation.vector_clock = session.vector_clock.copy()

    # Add to session operations
    session.operations.append(operation)
    session.last_activity = datetime.now(UTC)

    # Record operation event
    await event_store.append_event(session_id, EventType.OPERATION, operation.to_dict())

    await audit(
        "collab.operation.submit",
        actor=user.sub,
        payload={
            "session_id": session_id,
            "operation_type": operation_request.operation_type,
            "position": operation_request.position,
        },
    )

    # Broadcast operation to other users
    await connection_manager.broadcast_to_session(
        session_id,
        {"type": "operation", "operation": operation.to_dict(), "user_id": user.sub},
        exclude_user=user.sub,
    )

    # Generate AI suggestions if enabled
    suggestions = []
    if session.ai_enabled and operation.operation_type == OperationType.INSERT:
        # Get current content for AI analysis
        current_content = ""
        if session.latest_snapshot:
            current_content = session.latest_snapshot.content

        # Apply recent operations
        for op in session.operations:
            current_content = CRDTEngine.apply_operation(current_content, op)

        suggestions = await AICollaborator.suggest_edits(
            current_content, operation.position
        )

        if suggestions:
            await connection_manager.broadcast_to_session(
                session_id,
                {
                    "type": "ai_suggestions",
                    "suggestions": suggestions,
                    "operation_id": operation.op_id,
                },
            )

    return {
        "operation_id": operation.op_id,
        "status": "applied",
        "vector_clock": operation.vector_clock,
        "suggestions": suggestions,
    }


@router.post("/sessions/{session_id}/cursor")
async def update_cursor(
    session_id: str,
    cursor_update: CursorUpdate,
    user: User = Depends(require_roles(Role.USER)),
):
    """Update user cursor position"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=SESSION_NOT_FOUND)

    # Update cursor position
    cursor = UserCursor(
        user_id=user.sub,
        position=cursor_update.position,
        selection_start=cursor_update.selection_start,
        selection_end=cursor_update.selection_end,
    )

    user_cursors[session_id][user.sub] = cursor

    # Broadcast cursor update
    await connection_manager.broadcast_to_session(
        session_id,
        {
            "type": "cursor_update",
            "user_id": user.sub,
            "position": cursor.position,
            "selection_start": cursor.selection_start,
            "selection_end": cursor.selection_end,
        },
        exclude_user=user.sub,
    )

    return {"status": "updated"}


@router.get("/sessions/{session_id}/state")
@acached("collab:session:state", ttl=30)
async def get_session_state(session_id: str):
    """Get current session state"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=SESSION_NOT_FOUND)

    _ = sessions[session_id]

    # Get latest snapshot and events
    latest_snapshot = await event_store.get_latest_snapshot(session_id)
    recent_events = await event_store.get_events_since(
        session_id, latest_snapshot.version if latest_snapshot else 0
    )

    # Get active users and cursors
    active_users = connection_manager.get_session_users(session_id)
    session_cursors = user_cursors.get(session_id, {})

    return {
        "session_id": session_id,
        "document_type": session.document_type,
        "participants": {
            user_id: role.value for user_id, role in session.participants.items()
        },
        "active_users": list(active_users),
        "latest_snapshot": latest_snapshot.to_dict() if latest_snapshot else None,
        "recent_events": recent_events,
        "cursors": {
            user_id: {
                "position": cursor.position,
                "selection_start": cursor.selection_start,
                "selection_end": cursor.selection_end,
            }
            for user_id, cursor in session_cursors.items()
        },
        "vector_clock": session.vector_clock,
        "last_activity": session.last_activity,
        "ai_enabled": session.ai_enabled,
    }


@router.websocket("/sessions/{session_id}/connect")
async def session_websocket(websocket: WebSocket, session_id: str, user_id: str):
    """WebSocket connection for real-time collaboration"""
    if session_id not in sessions:
        await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        return

    await connection_manager.connect(websocket, session_id, user_id)

    try:
        # Send initial state
        session_state = await get_session_state(session_id)
        await websocket.send_text(
            json.dumps({"type": "initial_state", "data": session_state})
        )

        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            if message.get("type") == "heartbeat":
                await websocket.send_text(json.dumps({"type": "heartbeat_ack"}))

            elif message.get("type") == "cursor_update":
                # Broadcast cursor update to others
                await connection_manager.broadcast_to_session(
                    session_id,
                    {
                        "type": "cursor_update",
                        "user_id": user_id,
                        **message.get("data", {}),
                    },
                    exclude_user=user_id,
                )

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, session_id, user_id)

        # Broadcast user leaving
        await connection_manager.broadcast_to_session(
            session_id, {"type": "user_disconnect", "user_id": user_id}
        )

        # Record leave event
        await event_store.append_event(
            session_id,
            EventType.USER_LEAVE,
            {"user_id": user_id, "timestamp": datetime.now(UTC).isoformat()},
        )

    except Exception as e:
        await audit(
            "collab.websocket.error",
            actor=user_id,
            payload={"session_id": session_id, "error": str(e)},
        )
        connection_manager.disconnect(websocket, session_id, user_id)
