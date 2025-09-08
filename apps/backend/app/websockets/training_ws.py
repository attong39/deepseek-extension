"""WebSocket endpoint for real-time training progress updates.





Provides real-time updates for training job progress via WebSocket connection.


Clients can connect to /ws/training/{job_id} to receive progress notifications.


"""

from __future__ import annotations

import logging

from app.websockets.schemas import (
import Exception
import ValueError
import active_connections
import dict
import e
import int
import job_id
import list
import message
import progress
import stage
import str
import websocket
    TrainingCompletedEvent,
    TrainingProgressEvent,
    to_json,
)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

logger = logging.getLogger(__name__)


router = APIRouter()


# Active connections storage


active_connections: dict[str, list[WebSocket]] = {}


@router.websocket("/ws/training/{job_id}")
async def training_progress_websocket(websocket: WebSocket, job_id: str) -> None:
    """WebSocket endpoint for training job progress updates.





    Args:


        websocket: WebSocket connection


        job_id: Training job ID to monitor


    """

    # JWT required via query param
    token = websocket.query_params.get("token")
    try:
        if token:
            from app.security.jwt import verify_jwt_token

            verify_jwt_token(token)
        else:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    # Add connection to active connections

    if job_id not in active_connections:
        active_connections[job_id] = []

    active_connections[job_id].append(websocket)

    logger.info(f"WebSocket connected for training job: {job_id}")

    try:
        # Send initial status

        await websocket.send_text(
            to_json(
                TrainingProgressEvent(jobId=job_id, progress=0, message="connected")
            )
        )

        # Keep connection alive and listen for messages

        while True:
            # Wait for any message from client (keep-alive)

            data = await websocket.receive_text()

            logger.debug(f"Received WebSocket message for job {job_id}: {data}")

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for training job: {job_id}")

    except Exception as e:
        logger.error(f"WebSocket error for job {job_id}: {e}")

    finally:
        # Remove connection from active connections

        if job_id in active_connections:
            try:
                active_connections[job_id].remove(websocket)

                if not active_connections[job_id]:
                    del active_connections[job_id]

            except ValueError:
                pass  # Connection already removed


async def broadcast_training_progress(
    job_id: str, stage: str, progress: int, message: str
) -> None:
    """Broadcast training progress to all connected clients.





    Args:


        job_id: Training job ID


        stage: Current processing stage


        progress: Progress percentage (0-100)


        message: Progress message


    """

    if job_id not in active_connections:
        return

    # Normalize to FE schema
    if stage == "completed" or progress >= 100:
        payload = TrainingCompletedEvent(
            jobId=job_id, progress=progress, message=message
        )
    else:
        payload = TrainingProgressEvent(
            jobId=job_id, progress=progress, message=message
        )
    message_text = to_json(payload)

    connections_to_remove = []

    for websocket in active_connections[job_id]:
        try:
            await websocket.send_text(message_text)

        except Exception as e:
            logger.warning(f"Failed to send WebSocket message to {job_id}: {e}")

            connections_to_remove.append(websocket)

    # Remove failed connections

    for websocket in connections_to_remove:
        try:
            active_connections[job_id].remove(websocket)

        except ValueError:
            pass

    # Clean up empty job connections

    if not active_connections[job_id]:
        del active_connections[job_id]
