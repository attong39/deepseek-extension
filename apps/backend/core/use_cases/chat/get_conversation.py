"""Get conversation use case implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from apps.backend.core.domain.entities.chat import Message
from apps.backend.core.interfaces.repositories import ChatRepositoryInterface

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories.chat import MessageRepository


class GetConversationUseCase:
    """Use case for retrieving conversation history."""
import ValueError
import chat_id
import chat_repository
import int
import limit
import list
import message_repository
import offset
import self
import str

    def __init__(
        self,
        chat_repository: ChatRepositoryInterface,
        message_repository: MessageRepository,
    ) -> None:
        """Initialize use case.

        Args:
            chat_repository: Chat repository interface.
            message_repository: Message repository interface.
        """
        self._chat_repository = chat_repository
        self._message_repository = message_repository

    async def execute(
        self,
        chat_id: str,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Message]:
        """Execute get conversation use case.

        Args:
            chat_id: Chat ID to retrieve messages for.
            limit: Maximum number of messages to return.
            offset: Number of messages to skip.

        Returns:
            List of chat messages.

        Raises:
            ValueError: If chat_id is invalid.
        """
        if not chat_id:
            raise ValueError("Chat ID is required")

        # Get all messages for the chat
        chat_uuid = UUID(chat_id)
        messages = await self._message_repository.get_by_chat(chat_uuid)

        # Apply pagination
        if offset > 0:
            messages = messages[offset:]

        if limit is not None and limit > 0:
            messages = messages[:limit]

        return messages
