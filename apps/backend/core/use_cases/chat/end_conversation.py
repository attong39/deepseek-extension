"""End conversation use case.

This module implements ending/closing chat conversations following Clean Architecture principles.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.entities.chat import ChatStatus
import Exception
import RuntimeError
import ValueError
import archive
import bool
import chat_id
import chat_ids
import chat_repository
import dict
import e
import len
import list
import reason
import self
import str
import summary

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import ChatRepository


class EndConversationUseCase:
    """Use case for ending/closing chat conversations."""

    def __init__(self, chat_repository: ChatRepository) -> None:
        """Initialize the end conversation use case.

        Args:
            chat_repository: Repository for chat data access.
        """
        self.chat_repository = chat_repository

    async def execute(
        self,
        chat_id: UUID,
        reason: str | None = None,
        summary: str | None = None,
        archive: bool = False,
    ) -> bool:
        """End a chat conversation.

        Args:
            chat_id: Unique identifier of the chat to end.
            reason: Optional reason for ending the conversation.
            summary: Optional summary of the conversation.
            archive: Whether to archive the conversation after ending.

        Returns:
            True if conversation was successfully ended.

        Raises:
            ValueError: If chat is not found or already ended.
            RuntimeError: If operation fails.
        """
        # Get the chat
        chat = await self.chat_repository.get_by_id(chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found")

        # Check if chat is already ended
        if chat.status == ChatStatus.ENDED:
            raise ValueError("Chat is already ended")

        try:
            # Update chat status
            chat.status = ChatStatus.ENDED
            chat.ended_at = self._get_current_time()

            # Add ending metadata
            if "ending_info" not in chat.context_data:
                chat.context_data["ending_info"] = {}

            chat.context_data["ending_info"]["ended_at"] = chat.ended_at.isoformat()

            if reason:
                chat.context_data["ending_info"]["reason"] = reason

            if summary:
                chat.context_data["ending_info"]["summary"] = summary

            # Archive if requested
            if archive:
                chat.archive()
                chat.context_data["ending_info"]["archived"] = True

            # Update the chat
            updated_chat = await self.chat_repository.update(chat)

            return updated_chat is not None

        except Exception as e:
            raise RuntimeError(f"Failed to end conversation: {e!s}") from e

    async def force_end(self, chat_id: UUID, reason: str = "Force ended") -> bool:
        """Force end a conversation regardless of current status.

        Args:
            chat_id: Unique identifier of the chat to force end.
            reason: Reason for force ending.

        Returns:
            True if conversation was successfully force ended.

        Raises:
            ValueError: If chat is not found.
            RuntimeError: If operation fails.
        """
        # Get the chat
        chat = await self.chat_repository.get_by_id(chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found")

        try:
            # Force end regardless of current status
            chat.status = ChatStatus.ENDED
            chat.ended_at = self._get_current_time()

            # Add force ending metadata
            if "ending_info" not in chat.context_data:
                chat.context_data["ending_info"] = {}

            chat.context_data["ending_info"]["ended_at"] = chat.ended_at.isoformat()
            chat.context_data["ending_info"]["reason"] = reason
            chat.context_data["ending_info"]["force_ended"] = True

            # Update the chat
            updated_chat = await self.chat_repository.update(chat)

            return updated_chat is not None

        except Exception as e:
            raise RuntimeError(f"Failed to force end conversation: {e!s}") from e

    async def archive_conversation(self, chat_id: UUID) -> bool:
        """Archive a conversation.

        Args:
            chat_id: Unique identifier of the chat to archive.

        Returns:
            True if conversation was successfully archived.

        Raises:
            ValueError: If chat is not found.
            RuntimeError: If operation fails.
        """
        # Get the chat
        chat = await self.chat_repository.get_by_id(chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found")

        try:
            # Archive the conversation using domain method
            chat.archive()

            # Add archiving metadata
            if "archive_info" not in chat.context_data:
                chat.context_data["archive_info"] = {}

            chat.context_data["archive_info"]["archived_at"] = (
                self._get_current_time().isoformat()
            )

            # Update the chat
            updated_chat = await self.chat_repository.update(chat)

            return updated_chat is not None

        except Exception as e:
            raise RuntimeError(f"Failed to archive conversation: {e!s}") from e

    async def get_conversation_summary(self, chat_id: UUID) -> dict[str, Any]:
        """Get a summary of the conversation before ending.

        Args:
            chat_id: Unique identifier of the chat.

        Returns:
            Dictionary containing conversation summary.

        Raises:
            ValueError: If chat is not found.
        """
        # Get the chat
        chat = await self.chat_repository.get_by_id(chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found")

        # Calculate duration
        duration = None
        if chat.started_at and chat.ended_at:
            duration = (chat.ended_at - chat.started_at).total_seconds()
        elif chat.started_at:
            duration = (self._get_current_time() - chat.started_at).total_seconds()

        return {
            "chat_id": str(chat.id),
            "title": chat.title,
            "type": chat.type,
            "status": chat.status,
            "created_at": chat.created_at.isoformat(),
            "started_at": chat.started_at.isoformat() if chat.started_at else None,
            "ended_at": chat.ended_at.isoformat() if chat.ended_at else None,
            "last_message_at": chat.last_message_at.isoformat()
            if chat.last_message_at
            else None,
            "duration_seconds": duration,
            "message_count": chat.message_count,
            "participant_count": len(chat.participant_ids),
            "is_archived": chat.is_archived,
            "tags": chat.tags,
            "ending_info": chat.context_data.get("ending_info"),
            "sentiment_analysis": chat.context_data.get("sentiment_history"),
        }

    async def batch_end_conversations(
        self,
        chat_ids: list[UUID],
        reason: str | None = None,
        archive: bool = False,
    ) -> dict[str, Any]:
        """End multiple conversations in batch.

        Args:
            chat_ids: List of chat IDs to end.
            reason: Optional reason for ending conversations.
            archive: Whether to archive conversations after ending.

        Returns:
            Dictionary with success/failure counts and details.
        """
        results = {
            "total": len(chat_ids),
            "success": 0,
            "failed": 0,
            "errors": [],
            "ended_chats": [],
        }

        for chat_id in chat_ids:
            try:
                success = await self.execute(chat_id, reason=reason, archive=archive)
                if success:
                    results["success"] += 1
                    results["ended_chats"].append(str(chat_id))
                else:
                    results["failed"] += 1
                    results["errors"].append(
                        f"Failed to end chat {chat_id}: Unknown error"
                    )

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Failed to end chat {chat_id}: {e!s}")

        return results

    def _get_current_time(self):
        """Get current UTC time."""
        return datetime.now(UTC)
