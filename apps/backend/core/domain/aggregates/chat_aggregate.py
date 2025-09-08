from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.aggregates.base import AggregateRoot, DomainEvent, ensure
import agent_id
import content
import dict
import getattr
import len
import list
import m
import memory_ids
import messages
import meta
import reason
import self
import set
import str
import user_id


def utcnow():
    return datetime.now(UTC)


# Error message constants
CHAT_NOT_STARTED = "Chat not started."
CHAT_ALREADY_ENDED = "Chat already ended."


class ChatAggregate(AggregateRoot[DomainModel]):
    """
    Aggregate for chat conversations (thread + messages + memory context link).

    Invariants:
    - chat must start before sending messages
    - ended chat cannot accept new messages
    """

    AGG = "chat"

    def start(self, user_id: str, agent_id: str) -> None:
        current_started = getattr(self.entity, "started_at", None)
        ensure(not current_started, "Chat already started.")
        self._replace(user_id=user_id, agent_id=agent_id, started_at=utcnow())
        self._record(
            DomainEvent.make(
                "ChatStarted", self.AGG, self.id, user_id=user_id, agent_id=agent_id
            )
        )

    def attach_memory_context(self, memory_ids: Iterable[str]) -> None:
        current_context = getattr(self.entity, "memory_context", []) or []
        existing = set(current_context)
        new_ids = [m for m in memory_ids if m not in existing]
        if not new_ids:
            return
        self._replace(memory_context=list(existing | set(new_ids)))
        self._record(
            DomainEvent.make(
                "ChatMemoryAttached", self.AGG, self.id, memory_ids=new_ids
            )
        )

    def add_user_message(self, content: str, meta: dict | None = None) -> None:
        current_started = getattr(self.entity, "started_at", None)
        current_ended = getattr(self.entity, "ended_at", None)
        ensure(current_started is not None, CHAT_NOT_STARTED)
        ensure(current_ended is None, CHAT_ALREADY_ENDED)

        current_messages = getattr(self.entity, "messages", []) or []
        messages: list[dict] = list(current_messages)
        msg = {
            "id": f"m_{len(messages) + 1}",
            "role": "user",
            "content": content,
            "metadata": meta or {},
            "created_at": utcnow(),
        }
        messages.append(msg)
        self._replace(messages=messages)
        self._record(
            DomainEvent.make("ChatMessageAdded", self.AGG, self.id, role="user")
        )

    def add_agent_message(self, content: str, meta: dict | None = None) -> None:
        current_started = getattr(self.entity, "started_at", None)
        current_ended = getattr(self.entity, "ended_at", None)
        ensure(current_started is not None, CHAT_NOT_STARTED)
        ensure(current_ended is None, CHAT_ALREADY_ENDED)

        current_messages = getattr(self.entity, "messages", []) or []
        messages: list[dict] = list(current_messages)
        msg = {
            "id": f"m_{len(messages) + 1}",
            "role": "assistant",
            "content": content,
            "metadata": meta or {},
            "created_at": utcnow(),
        }
        messages.append(msg)
        self._replace(messages=messages)
        self._record(
            DomainEvent.make("ChatMessageAdded", self.AGG, self.id, role="assistant")
        )

    def end(self, reason: str | None = None) -> None:
        current_started = getattr(self.entity, "started_at", None)
        current_ended = getattr(self.entity, "ended_at", None)
        ensure(current_started is not None, CHAT_NOT_STARTED)
        ensure(current_ended is None, CHAT_ALREADY_ENDED)
        self._replace(ended_at=utcnow())
        self._record(
            DomainEvent.make("ChatEnded", self.AGG, self.id, reason=reason or "")
        )
