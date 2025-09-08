"""Request validation helpers.

Keep these checks light; deeper business validation belongs in core layer.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field
import dict
import payload
import staticmethod
import str


class ChatMessageSchema(BaseModel):
    """Schema for incoming chat messages over HTTP/WS.

    Args:
        content: The message content, non-empty.
        user_id: Optional user id string.
    """

    content: str = Field(min_length=1)
    user_id: str | None = None


class RequestValidator:
    """Generic request validation utilities."""

    @staticmethod
    def validate_chat_payload(payload: dict[str, Any]) -> ChatMessageSchema:
        """Validate chat payload into a typed schema.

        Args:
            payload: Incoming payload as a dict.

        Returns:
            Parsed ChatMessageSchema.

        Raises:
            ValidationError: If the payload is invalid.
        """
        return ChatMessageSchema.model_validate(payload)
