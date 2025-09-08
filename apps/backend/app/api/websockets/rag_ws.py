"""WebSocket handler for One-Click Learning progress events."""

from __future__ import annotations

import json
from typing import Any

from apps.backend.core.services.ai.rag.registry import registry
from fastapi import WebSocket


class WSProgressHandler:
    """WebSocket handler for RAG progress events."""
import Exception
import client
import data
import dict
import e
import event
import event_type
import self
import set
import str
import websocket

    def __init__(self) -> None:
        self.clients: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        """Connect a new WebSocket client."""
        await websocket.accept()
        self.clients.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Disconnect a WebSocket client."""
        self.clients.discard(websocket)

    async def broadcast_event(self, event: dict[str, Any]) -> None:
        """Broadcast event to all connected clients."""
        message = json.dumps(event)
        for client in self.clients.copy():
            try:
                await client.send_text(message)
            except Exception:
                self.clients.discard(client)

    def handle_rag_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Handle RAG events and broadcast to clients."""
        import asyncio

        task = asyncio.create_task(
            self.broadcast_event(
                {
                    "type": event_type,
                    "data": data,
                    "timestamp": data.get("timestamp", ""),
                }
            )
        )
        # Keep reference to prevent GC
        task.add_done_callback(lambda _: None)


# Global instance
ws_handler = WSProgressHandler()

# Register with orchestrator
orchestrator = registry.get("orchestrator")
orchestrator.subscribe(
    "rag.ingest.start", lambda e: ws_handler.handle_rag_event("ingest_start", e.data)
)
orchestrator.subscribe(
    "rag.ingest.progress",
    lambda e: ws_handler.handle_rag_event("ingest_progress", e.data),
)
orchestrator.subscribe(
    "rag.ingest.complete",
    lambda e: ws_handler.handle_rag_event("ingest_complete", e.data),
)
