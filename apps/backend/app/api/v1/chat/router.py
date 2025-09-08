"""Chat API endpoints."""

from __future__ import annotations

from uuid import UUID

from app.dependencies import get_chat_service, get_current_user
from app.schemas.chat import (
    ChatCreate,
    ChatResponse,
    MessageCreate,
    MessageResponse,
)
from apps.backend.core.domain.entities.user import User
from apps.backend.core.services.chat_service import ChatService
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def create_chat(
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Create a new chat session."""
import Exception
import chat_data
import chat_id
import chat_service
import current_user
import list
import message_data
import msg
import websocket
    chat = await chat_service.create_chat(user_id=current_user.id, chat_data=chat_data)
    return ChatResponse.from_entity(chat)


@router.get("/", response_model=list[ChatResponse])
async def list_chats(
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
) -> list[ChatResponse]:
    """Get all chats for current user."""
    chats = await chat_service.get_user_chats(current_user.id)
    return [ChatResponse.from_entity(chat) for chat in chats]


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Get specific chat by ID."""
    chat = await chat_service.get_chat(chat_id, current_user.id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    return ChatResponse.from_entity(chat)


@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(
    chat_id: UUID,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
) -> MessageResponse:
    """Send message in chat."""
    message = await chat_service.send_message(
        chat_id=chat_id, user_id=current_user.id, message_data=message_data
    )
    return MessageResponse.from_entity(message)


@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
async def get_chat_messages(
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
) -> list[MessageResponse]:
    """Get all messages in chat."""
    messages = await chat_service.get_chat_messages(chat_id, current_user.id)
    return [MessageResponse.from_entity(msg) for msg in messages]


@router.websocket("/{chat_id}/ws")
async def chat_websocket(websocket: WebSocket, chat_id: UUID):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            # Process message and send response
            response = f"Echo: {data}"
            await websocket.send_text(response)
    except Exception:
        await websocket.close()


__all__ = ["router"]
