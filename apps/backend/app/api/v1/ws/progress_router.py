from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ....core.pipeline import close_subscription, subscribe
import Exception
import TimeoutError
import run_id
import str
import websocket

"""
WebSocket Endpoints for Real-time Progress Tracking
Progress updates for async RAG pipeline operations
"""
router = APIRouter()


@router.websocket("/progress/{run_id}")
async def ws_progress(websocket: WebSocket, run_id: str) -> None:
    """
    WebSocket endpoint for real-time progress tracking.
    Clients connect with a run_id and receive progress events from the pipeline.
    Events:
    - hello: Connection established
    - stage: Pipeline stage updates (chunk, persist, embed, index)
    - done: Pipeline completed successfully
    - error: Pipeline error occurred
    - ping: Heartbeat for connection keep-alive
    Args:
        websocket: WebSocket connection
        run_id: Unique identifier for the pipeline run
    """
    await websocket.accept()
    event_queue = subscribe(run_id)
    try:
        await websocket.send_json(
            {
                "event": "hello",
                "run_id": run_id,
                "message": "Connected to progress tracking",
            }
        )
        while True:
            try:
                event = await asyncio.wait_for(event_queue.get(), timeout=30.0)
                await websocket.send_json(event)
                if event.get("event") == "done":
                    break
                if event.get("event") == "error":
                    break
            except TimeoutError:
                await websocket.send_json({"event": "ping"})
    except WebSocketDisconnect:
        # Client disconnected during health check; nothing to do
        return
    except Exception:
        logging.exception("Unhandled exception in ws_progress for run_id=%s", run_id)
    finally:
        try:
            await close_subscription(run_id)
        except Exception:
            logging.exception("Failed to close_subscription for run_id=%s", run_id)
        try:
            await websocket.close()
        except Exception:
            logging.exception("Failed to close websocket for run_id=%s", run_id)


@router.websocket("/health")
async def ws_health(websocket: WebSocket) -> None:
    """
    WebSocket health check endpoint.
    Simple endpoint to test WebSocket connectivity.
    """
    await websocket.accept()
    try:
        await websocket.send_json(
            {
                "event": "health",
                "status": "connected",
                "message": "WebSocket connection healthy",
            }
        )
        await asyncio.sleep(1.0)
        await websocket.send_json(
            {"event": "close", "message": "Health check complete"}
        )
    except WebSocketDisconnect:
        return
    finally:
        try:
            await websocket.close()
        except Exception:
            logging.exception("Failed to close websocket in ws_health")


__all__ = ["router"]
