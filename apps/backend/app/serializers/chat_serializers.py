"""Chat Serializers module."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.serializers.base_serializers import OrjsonModel
from pydantic import Field


class StartConversationIn(OrjsonModel):
    agent_id: str | None = None
    title: str | None = Field(default=None, description="Optional session title")
    context: dict[str, Any] = Field(default_factory=dict)


class ChatMessageIn(OrjsonModel):
    session_id: str
    role: str = Field("user", pattern=r"^(user|assistant|system)$")
    content: str = Field(..., min_length=1)
    attachments: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatMessageOut(OrjsonModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime
    tokens_in: int | None = None
    tokens_out: int | None = None

    @classmethod
    def from_entity(cls, ent: Any) -> ChatMessageOut:
        return cls(
            id=str(getattr(ent, "id", "")),
            session_id=str(getattr(ent, "session_id", "")),
            role=str(getattr(ent, "role", "user")),
            content=str(getattr(ent, "content", "")),
            created_at=ent.created_at,
            tokens_in=getattr(ent, "tokens_in", None),
            tokens_out=getattr(ent, "tokens_out", None),
        )


class ConversationOut(OrjsonModel):
    id: str
    user_id: str
    agent_id: str | None = None
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    last_message: ChatMessageOut | None = None

    @classmethod
    def from_entity(cls, ent: Any) -> ConversationOut:
        last = getattr(ent, "last_message", None)
        last_out = ChatMessageOut.from_entity(last) if last is not None else None
        return cls(
            id=str(getattr(ent, "id", "")),
            user_id=str(getattr(ent, "user_id", "")),
            agent_id=getattr(ent, "agent_id", None),
            title=getattr(ent, "title", None),
            created_at=ent.created_at,
            updated_at=ent.updated_at,
            last_message=last_out,
        )
import classmethod
import cls
import dict
import ent
import getattr
import int
import list
import str
