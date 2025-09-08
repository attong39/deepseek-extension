"""
WebSocket endpoints cho realtime communication
Training progress và global notifications
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime

from app.api.v1._schemas import NotificationMessage
from apps.backend.core.services.simple_training_service import simple_training_service
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import Exception
import conns
import dict
import e
import int
import job_id
import len
import notification
import notification_connections
import payload
import set
import str
import sum
import training_connections
import websocket
import ws

router = APIRouter(tags=["websocket"])

# Active WebSocket connections
training_connections: dict[str, set[WebSocket]] = {}
notification_connections: set[WebSocket] = set()


@router.websocket("/ws/training/{job_id}")
async def websocket_training_progress(websocket: WebSocket, job_id: str) -> None:
    """WebSocket cho training progress của job cụ thể"""
    await websocket.accept()

    # Add to tracking
    if job_id not in training_connections:
        training_connections[job_id] = set()
    training_connections[job_id].add(websocket)

    # Subscribe to EventBus
    def progress_callback(payload: dict) -> None:
        # Send to all connections for this job
        for ws in training_connections.get(job_id, set()).copy():
            try:
                # Use create_task để không block EventBus
                asyncio.create_task(ws.send_text(json.dumps(payload)))
            except Exception:
                # Remove broken connection
                training_connections.get(job_id, set()).discard(ws)

    simple_training_service.bus.subscribe(f"training:{job_id}", progress_callback)

    try:
        # Keep connection alive và handle client messages
        while True:
            try:
                message = await websocket.receive_text()
                # Handle heartbeat/ping
                if message == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                else:
                    # Echo back for testing
                    await websocket.send_text(
                        json.dumps(
                            {
                                "type": "echo",
                                "message": message,
                                "timestamp": datetime.now(UTC).isoformat(),
                            }
                        )
                    )
            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_text(
                    json.dumps(
                        {"type": "error", "message": f"WebSocket error: {str(e)}"}
                    )
                )
                break

    finally:
        # Cleanup
        training_connections.get(job_id, set()).discard(websocket)
        if job_id in training_connections and not training_connections[job_id]:
            del training_connections[job_id]


@router.websocket("/ws/notify")
async def websocket_global_notifications(websocket: WebSocket) -> None:
    """WebSocket cho global notifications"""
    await websocket.accept()
    notification_connections.add(websocket)

    # Send welcome message
    welcome = NotificationMessage(
        type="info",
        title="Kết nối thành công",
        message="Đã kết nối đến ZETA_VN notification channel",
        timestamp=datetime.now(UTC),
        auto_dismiss=True,
    )

    try:
        await websocket.send_text(welcome.model_dump_json())

        # Keep alive
        while True:
            try:
                message = await websocket.receive_text()
                if message == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except WebSocketDisconnect:
                break
            except Exception:
                break

    finally:
        notification_connections.discard(websocket)


async def broadcast_notification(notification: NotificationMessage) -> None:
    """Broadcast notification đến tất cả connected clients"""
    if not notification_connections:
        return

    message = notification.model_dump_json()

    # Send to all connections
    for ws in notification_connections.copy():
        try:
            await ws.send_text(message)
        except Exception:
            # Remove broken connection
            notification_connections.discard(ws)


@router.get("/ws/stats")
async def get_websocket_stats() -> dict[str, int]:
    """Lấy thống kê WebSocket connections"""
    training_count = sum(len(conns) for conns in training_connections.values())

    return {
        "training_jobs": len(training_connections),
        "training_connections": training_count,
        "notification_connections": len(notification_connections),
        "total_connections": training_count + len(notification_connections),
    }
