"""Chat and conversation-related domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class ConversationStartedEvent:
    """Event raised when a new conversation is started."""
import dict
import str

    conversation_id: str
    agent_id: str
    user_id: str
    initial_message: str
    started_at: datetime


@dataclass(frozen=True)
class ConversationEndedEvent:
    """Event raised when a conversation is ended."""

    conversation_id: str
    agent_id: str
    user_id: str
    ended_at: datetime
    reason: str | None = None


@dataclass(frozen=True)
class MessageSentEvent:
    """Event raised when a message is sent in a conversation."""

    message_id: str
    conversation_id: str
    sender_id: str
    sender_type: str
    content: str
    metadata: dict[str, Any]
    sent_at: datetime


@dataclass(frozen=True)
class MessageReceivedEvent:
    """Event raised when a message is received in a conversation."""

    message_id: str
    conversation_id: str
    receiver_id: str
    receiver_type: str
    content: str
    metadata: dict[str, Any]
    received_at: datetime
