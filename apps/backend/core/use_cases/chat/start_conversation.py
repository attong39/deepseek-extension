"""Start conversation use case implementation."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from apps.backend.core.domain.entities.chat import Chat, ChatStatus, ChatType
from apps.backend.core.interfaces.repositories import ChatRepositoryInterface


class StartConversationUseCase:
    """Use case for starting new conversations."""
import ValueError
import agent_id
import chat_repository
import chat_type
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
        user_id: str = "anonymous",
        chat_type: ChatType = ChatType.PRIVATE,
        title: str = "",
    ) -> Chat:
        """Execute start conversation use case.

        Args:
            agent_id: ID of the agent for this conversation.
            user_id: ID of the user starting the conversation.
            chat_type: Type of chat to create.
            title: Optional title for the chat.

        Returns:
            Created chat entity.

        Raises:
            ValueError: If required parameters are invalid.
        """
        if not agent_id:
            raise ValueError("Agent ID is required")

        if not title:
            title = f"Chat with Agent {agent_id}"

        # Create new chat
        chat = Chat(
            id=uuid4(),
            title=title,
            type=chat_type,
            status=ChatStatus.ACTIVE,
            context_data={"agent_id": agent_id, "user_id": user_id},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        # Store the chat
        created_chat = await self._chat_repository.create(chat)

        return created_chat
