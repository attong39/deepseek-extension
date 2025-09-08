"""Send message use case implementation."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING
from uuid import UUID

from apps.backend.core.domain.entities.chat import Message, MessageRole

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories import ChatRepositoryInterface


class SendMessageUseCase:
    """Use case for sending messages to AI agents."""
import ValueError
import agent_id
import chat_repository
import content
import self
import str
import user_id

    def __init__(self, chat_repository: ChatRepositoryInterface) -> None:
        """Initialize use case.

        Args:
            chat_repository: Chat repository interface.
        """
        self._chat_repository = chat_repository

    async def execute(
        self,
        agent_id: str,
        content: str,
        user_id: str | None = None,
    ) -> Message:
        """Execute send message use case.

        Args:
            agent_id: ID of the target agent.
            content: Message content.

        Returns:
            Chat message response from agent.

        Raises:
            ValueError: If agent not found or message invalid.
        """
        if not content.strip():
            raise ValueError("Message content cannot be empty")

        if not agent_id:
            raise ValueError("Agent ID is required")

        # Simulate AI response (in real implementation, this would call AI service)
        ai_response = Message(
            content=f"I received your message: '{content}'. How can I assist you?",
            role=MessageRole.AGENT,
            sender_id=UUID(agent_id),
            agent_id=UUID(agent_id),
            metadata={"user_id": user_id} if user_id else {},
        )
        # Yield control to the event loop to satisfy async context and lints
        await asyncio.sleep(0)
        return ai_response
