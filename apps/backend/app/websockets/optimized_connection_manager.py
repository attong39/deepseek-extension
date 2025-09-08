"""
Optimized WebSocket Connection Manager.

High-performance WebSocket management with connection pooling,
message compression, and room-based broadcasting.
"""

from __future__ import annotations

import asyncio
import gzip
import json
import time
from collections import defaultdict
from typing import Any
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import Exception
import bool
import compress
import connection
import dict
import e
import enable_compression
import exclude
import int
import isinstance
import len
import list
import print
import result
import round
import self
import set
import str
import user_id
import websocket
import zip


class OptimizedConnectionManager:
    """WebSocket connection manager with performance optimizations."""

    def __init__(self, enable_compression: bool = True) -> None:
        # Connection storage by room
        self.active_connections: dict[str, set[WebSocket]] = defaultdict(set)

        # Connection metadata
        self.connection_metadata: dict[WebSocket, dict[str, Any]] = {}

        # Message compression
        self.enable_compression = enable_compression

        # Performance metrics
        self.connection_count = 0
        self.message_count = 0
        self.broadcast_count = 0

        # Connection tasks for cleanup
        self.connection_tasks: dict[WebSocket, asyncio.Task[None]] = {}

    async def connect(
        self, websocket: WebSocket, room: str = "default", user_id: str | None = None
    ) -> str:
        """Accept and register a WebSocket connection.

        Args:
            websocket: WebSocket connection
            room: Room to join (for broadcasting)
            user_id: Optional user identifier

        Returns:
            Connection ID for tracking
        """
        await websocket.accept()

        # Generate connection ID
        connection_id = str(uuid4())

        # Store connection
        self.active_connections[room].add(websocket)

        # Store metadata
        self.connection_metadata[websocket] = {
            "id": connection_id,
            "room": room,
            "user_id": user_id,
            "connected_at": time.time(),
            "last_ping": time.time(),
            "message_count": 0,
        }

        self.connection_count += 1

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(self._heartbeat_loop(websocket))
        self.connection_tasks[websocket] = heartbeat_task

        print(f"✅ WebSocket connected: {connection_id} in room '{room}'")
        return connection_id

    def disconnect(self, websocket: WebSocket) -> None:
        """Disconnect and clean up a WebSocket connection."""
        if websocket in self.connection_metadata:
            metadata = self.connection_metadata[websocket]
            room = metadata["room"]
            connection_id = metadata["id"]

            # Remove from room
            self.active_connections[room].discard(websocket)

            # Clean up empty rooms
            if not self.active_connections[room]:
                del self.active_connections[room]

            # Remove metadata
            del self.connection_metadata[websocket]

            # Cancel heartbeat task
            if websocket in self.connection_tasks:
                task = self.connection_tasks[websocket]
                task.cancel()
                del self.connection_tasks[websocket]

            self.connection_count -= 1
            print(f"❌ WebSocket disconnected: {connection_id} from room '{room}'")

    async def send_personal_message(
        self,
        message: dict[str, Any],
        websocket: WebSocket,
        compress: bool | None = None,
    ) -> bool:
        """Send message to a specific WebSocket connection.

        Args:
            message: Message data to send
            websocket: Target WebSocket connection
            compress: Override compression setting

        Returns:
            True if message was sent successfully
        """
        try:
            # Update message count
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]["message_count"] += 1

            message_text = self._prepare_message(message, compress)
            await websocket.send_text(message_text)

            self.message_count += 1
            return True

        except (ConnectionClosed, WebSocketDisconnect):
            self.disconnect(websocket)
            return False
        except Exception as e:
            print(f"Error sending personal message: {e}")
            return False

    async def broadcast_to_room(
        self,
        message: dict[str, Any],
        room: str,
        exclude: WebSocket | None = None,
        compress: bool | None = None,
    ) -> int:
        """Broadcast message to all connections in a room.

        Args:
            message: Message data to send
            room: Target room
            exclude: Connection to exclude from broadcast
            compress: Override compression setting

        Returns:
            Number of connections that received the message
        """
        if room not in self.active_connections:
            return 0

        connections = self.active_connections[room].copy()
        if exclude:
            connections.discard(exclude)

        if not connections:
            return 0

        # Prepare message once for all connections
        message_text = self._prepare_message(message, compress)

        # Send to all connections concurrently
        tasks = []
        for connection in connections:
            task = asyncio.create_task(
                self._send_to_connection(connection, message_text)
            )
            tasks.append(task)

        # Wait for all sends to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Count successful sends and clean up failed connections
        successful_sends = 0
        for connection, result in zip(connections, results, strict=False):
            if isinstance(result, Exception):
                print(f"Failed to send to connection: {result}")
                self.disconnect(connection)
            else:
                successful_sends += 1
                # Update message count
                if connection in self.connection_metadata:
                    self.connection_metadata[connection]["message_count"] += 1

        self.broadcast_count += 1
        self.message_count += successful_sends

        return successful_sends

    async def broadcast_to_all(
        self, message: dict[str, Any], compress: bool | None = None
    ) -> int:
        """Broadcast message to all connected clients.

        Args:
            message: Message data to send
            compress: Override compression setting

        Returns:
            Total number of connections that received the message
        """
        total_sent = 0

        for room in self.active_connections:
            sent = await self.broadcast_to_room(message, room, compress=compress)
            total_sent += sent

        return total_sent

    def _prepare_message(
        self, message: dict[str, Any], compress: bool | None = None
    ) -> str:
        """Prepare message for sending (with optional compression)."""
        # Convert to JSON
        message_json = json.dumps(message, ensure_ascii=False)

        # Apply compression if enabled
        should_compress = compress if compress is not None else self.enable_compression

        if (
            should_compress and len(message_json.encode()) > 1024
        ):  # Only compress larger messages
            try:
                compressed = gzip.compress(message_json.encode())
                # Only use compression if it actually reduces size
                if len(compressed) < len(message_json.encode()) * 0.9:
                    # Add compression header info
                    compressed_message = {
                        "_compressed": True,
                        "_original_size": len(message_json.encode()),
                        "_data": compressed.hex(),
                    }
                    return json.dumps(compressed_message)
            except Exception as e:
                print(f"Compression failed: {e}")

        return message_json

    async def _send_to_connection(self, websocket: WebSocket, message: str) -> None:
        """Send message to a single connection."""
        try:
            await websocket.send_text(message)
        except (ConnectionClosed, WebSocketDisconnect):
            # Connection will be cleaned up by the caller
            raise
        except Exception as e:
            print(f"Error sending to connection: {e}")
            raise

    async def _heartbeat_loop(self, websocket: WebSocket) -> None:
        """Heartbeat loop to keep connection alive and detect disconnections."""
        try:
            while True:
                await asyncio.sleep(30)  # Send ping every 30 seconds

                if websocket in self.connection_metadata:
                    try:
                        ping_message = {"type": "ping", "timestamp": time.time()}
                        await websocket.send_text(json.dumps(ping_message))
                        self.connection_metadata[websocket]["last_ping"] = time.time()
                    except (ConnectionClosed, WebSocketDisconnect):
                        break
                    except Exception as e:
                        print(f"Heartbeat error: {e}")
                        break
                else:
                    break

        except asyncio.CancelledError:
            # Task was cancelled, normal cleanup
            raise
        except Exception as e:
            print(f"Heartbeat loop error: {e}")
        finally:
            # Ensure cleanup
            if websocket in self.connection_metadata:
                self.disconnect(websocket)

    def get_connection_stats(self) -> dict[str, Any]:
        """Get connection statistics."""
        room_stats = {}
        for room, connections in self.active_connections.items():
            room_stats[room] = len(connections)

        # Calculate average connection time
        total_connection_time = 0
        active_connections_count = 0
        current_time = time.time()

        for metadata in self.connection_metadata.values():
            total_connection_time += current_time - metadata["connected_at"]
            active_connections_count += 1

        avg_connection_time = (
            total_connection_time / active_connections_count
            if active_connections_count > 0
            else 0
        )

        return {
            "total_connections": self.connection_count,
            "active_connections": active_connections_count,
            "total_messages": self.message_count,
            "total_broadcasts": self.broadcast_count,
            "rooms": room_stats,
            "compression_enabled": self.enable_compression,
            "avg_connection_time_seconds": round(avg_connection_time, 2),
        }

    def get_room_connections(self, room: str) -> list[dict[str, Any]]:
        """Get information about connections in a specific room."""
        if room not in self.active_connections:
            return []

        connections_info = []
        for websocket in self.active_connections[room]:
            if websocket in self.connection_metadata:
                metadata = self.connection_metadata[websocket].copy()
                # Remove sensitive data and add computed fields
                metadata["uptime_seconds"] = round(
                    time.time() - metadata["connected_at"], 2
                )
                metadata.pop("connected_at", None)
                connections_info.append(metadata)

        return connections_info

    async def cleanup_all(self) -> None:
        """Clean up all connections and tasks."""
        print("🧹 Cleaning up all WebSocket connections...")

        # Cancel all heartbeat tasks
        for task in self.connection_tasks.values():
            task.cancel()

        # Wait for tasks to complete
        if self.connection_tasks:
            await asyncio.gather(
                *self.connection_tasks.values(), return_exceptions=True
            )

        # Clear all data
        self.active_connections.clear()
        self.connection_metadata.clear()
        self.connection_tasks.clear()

        self.connection_count = 0
        print("✅ WebSocket cleanup completed")


# Global connection manager instance
connection_manager = OptimizedConnectionManager(enable_compression=True)


# Utility functions for FastAPI WebSocket endpoints
async def handle_websocket_connection(
    websocket: WebSocket, room: str = "default", user_id: str | None = None
) -> None:
    """Standard WebSocket connection handler.

    Usage in FastAPI:
        @app.websocket("/ws/{room}")
        async def websocket_endpoint(websocket: WebSocket, room: str):
            await handle_websocket_connection(websocket, room)
    """
    await connection_manager.connect(websocket, room, user_id)

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()

            try:
                message = json.loads(data)

                # Handle different message types
                message_type = message.get("type", "chat")

                if message_type == "ping":
                    # Respond to ping
                    await connection_manager.send_personal_message(
                        {"type": "pong", "timestamp": time.time()}, websocket
                    )
                elif message_type == "broadcast":
                    # Broadcast to room
                    broadcast_message = {
                        "type": "message",
                        "user_id": user_id,
                        "content": message.get("content", ""),
                        "timestamp": time.time(),
                    }
                    await connection_manager.broadcast_to_room(
                        broadcast_message, room, exclude=websocket
                    )
                else:
                    # Echo message back (or handle custom logic)
                    echo_message = {
                        "type": "echo",
                        "original": message,
                        "timestamp": time.time(),
                    }
                    await connection_manager.send_personal_message(
                        echo_message, websocket
                    )

            except json.JSONDecodeError:
                error_message = {
                    "type": "error",
                    "message": "Invalid JSON format",
                    "timestamp": time.time(),
                }
                await connection_manager.send_personal_message(error_message, websocket)

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        connection_manager.disconnect(websocket)
