"""
WebSocket Chat Router for Real-time RAG

Type-safe WebSocket endpoints with authentication and RAG integration.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from pydantic import BaseModel, ValidationError

from ..dependencies import get_current_user_websocket, get_rag_engine
import Exception
import dict
import e
import len
import list
import rag_engine
import result
import self
import str
import user
import websocket

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["websocket", "chat", "rag"])


class ChatMessage(BaseModel):
    """Chat message structure."""
    type: str = "message"
    content: str
    metadata: dict[str, Any] = {}


class ChatResponse(BaseModel):
    """Chat response structure."""
    type: str
    content: str
    sources: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {}


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        """Accept a new connection."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected via WebSocket")
    
    def disconnect(self, user_id: str) -> None:
        """Remove a connection."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected from WebSocket")
    
    async def send_message(self, user_id: str, message: dict[str, Any]) -> None:
        """Send message to specific user."""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send message to {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast(self, message: dict[str, Any]) -> None:
        """Broadcast message to all connected users."""
        for user_id, websocket in list(self.active_connections.items()):
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to broadcast to {user_id}: {e}")
                self.disconnect(user_id)


# Global connection manager
manager = ConnectionManager()


@router.websocket("/chat")
async def chat_websocket(
    websocket: WebSocket,
    user=Depends(get_current_user_websocket),
    rag_engine=Depends(get_rag_engine),
) -> None:
    """
    Real-time chat with RAG integration.
    
    Message format:
    {
        "type": "message",
        "content": "Your question here",
        "metadata": {"session_id": "optional"}
    }
    
    Response format:
    {
        "type": "response",
        "content": "AI response",
        "sources": [{"text": "...", "score": 0.85}],
        "metadata": {"timestamp": "..."}
    }
    """
    user_id = str(user.id)
    
    try:
        await manager.connect(websocket, user_id)
        
        # Send welcome message
        welcome = ChatResponse(
            type="welcome",
            content=f"Welcome to ZETA AI Chat, {user.username}! Ask me anything.",
            metadata={"user_id": user_id, "rag_enabled": True},
        )
        await websocket.send_text(welcome.model_dump_json())
        
        while True:
            # Receive message
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Validate message
                try:
                    message = ChatMessage(**message_data)
                except ValidationError as e:
                    error_response = ChatResponse(
                        type="error",
                        content=f"Invalid message format: {e}",
                    )
                    await websocket.send_text(error_response.model_dump_json())
                    continue
                
                # Process message
                if message.type == "message":
                    response = await process_chat_message(message, rag_engine, user_id)
                    await websocket.send_text(response.model_dump_json())
                
                elif message.type == "ping":
                    pong = ChatResponse(type="pong", content="pong")
                    await websocket.send_text(pong.model_dump_json())
                
                else:
                    error_response = ChatResponse(
                        type="error",
                        content=f"Unknown message type: {message.type}",
                    )
                    await websocket.send_text(error_response.model_dump_json())
                
            except json.JSONDecodeError:
                error_response = ChatResponse(
                    type="error",
                    content="Invalid JSON format",
                )
                await websocket.send_text(error_response.model_dump_json())
            
            except Exception as e:
                logger.error(f"Error processing message from {user_id}: {e}")
                error_response = ChatResponse(
                    type="error",
                    content="Internal server error",
                )
                await websocket.send_text(error_response.model_dump_json())
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user_id}")
    
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
    
    finally:
        manager.disconnect(user_id)


async def process_chat_message(
    message: ChatMessage,
    rag_engine: Any,  # RAGEngine from dependencies
    user_id: str,
) -> ChatResponse:
    """Process a chat message with RAG."""
    try:
        # Search relevant documents
        search_results = rag_engine.search(
            query=message.content,
            k=3,
            score_threshold=0.1,
        )
        
        # Format sources
        sources = []
        context_texts = []
        
        for result in search_results:
            sources.append({
                "text": result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"],
                "score": result["score"],
                "metadata": result.get("metadata", {}),
            })
            context_texts.append(result["text"])
        
        # Generate response
        if context_texts:
            context = "\n".join(context_texts)
            ai_response = f"Based on the available information: {context[:500]}...\n\nI found {len(sources)} relevant sources for your question about: {message.content}"
        else:
            ai_response = f"I don't have specific information about: {message.content}. Could you provide more context or ask about something else?"
        
        response = ChatResponse(
            type="response",
            content=ai_response,
            sources=sources,
            metadata={
                "user_id": user_id,
                "query": message.content,
                "sources_count": len(sources),
            },
        )
        
        logger.info(f"Processed chat message for user {user_id}: {len(sources)} sources found")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        return ChatResponse(
            type="error",
            content="Sorry, I encountered an error processing your message.",
        )


@router.websocket("/notifications")
async def notifications_websocket(
    websocket: WebSocket,
    user=Depends(get_current_user_websocket),
) -> None:
    """WebSocket for system notifications."""
    user_id = str(user.id)
    
    try:
        await manager.connect(websocket, f"notif_{user_id}")
        
        # Keep connection alive
        while True:
            try:
                # Send periodic heartbeat
                await websocket.send_text(json.dumps({"type": "heartbeat"}))
                await websocket.receive_text()  # Wait for client response
            except WebSocketDisconnect:
                break
    
    except Exception as e:
        logger.error(f"Notifications WebSocket error for user {user_id}: {e}")
    
    finally:
        manager.disconnect(f"notif_{user_id}")


# Health check endpoint for WebSocket
@router.get("/health")
async def websocket_health() -> dict[str, Any]:
    """Health check for WebSocket service."""
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections),
        "endpoints": ["/ws/chat", "/ws/notifications"],
    }


# Export the manager for use in other modules
__all__ = ["router", "manager", "ChatMessage", "ChatResponse"]
