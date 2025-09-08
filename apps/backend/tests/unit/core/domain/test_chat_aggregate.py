"""Test Chat Aggregate module."""

from __future__ import annotations

from apps.backend.core.domain.aggregates.chat_aggregate import ChatAggregate, ChatStatus
from apps.backend.core.domain.value_objects import DomainError


def _new_chat() -> ChatAggregate:
    return ChatAggregate.create(id="chat-1", user_id="u-1", agent_id="a-1")  # type: ignore[arg-type]


def test_chat_lifecycle() -> None:
    chat = _new_chat()
    assert chat.status == ChatStatus.NOT_STARTED
    chat = chat.start(title="Test")
    assert chat.status == ChatStatus.ACTIVE
    assert chat.started_at is not None
    chat = chat.add_user_message("hello")
    chat = chat.add_agent_message("hi")
    assert chat.get_message_count() == 2
    chat = chat.attach_memory_context(["mem1", "mem2"]).attach_memory_context(
        ["mem2", "mem3"]
    )  # dedupe
    assert len(chat.memory_context) == 3
    chat = chat.end("done")
    assert chat.status == ChatStatus.ENDED
    assert chat.ended_at is not None
    summary = chat.get_conversation_summary()
    assert summary["status"] == ChatStatus.ENDED.value


def test_invalid_transitions() -> None:
    chat = _new_chat()
    try:
        chat.add_user_message("x")
    except Exception as e:
        assert isinstance(e, DomainError)
    else:
        raise AssertionError("Expected DomainError")
    chat = chat.start()
    chat = chat.end()
    try:
        chat.add_agent_message("x")
    except Exception as e:
        assert isinstance(e, DomainError)
    else:
        raise AssertionError("Expected DomainError after end")


__all__ = [
    "chat",
    "summary",
    "test_chat_lifecycle",
    "test_invalid_transitions",
]
import AssertionError
import Exception
import e
import isinstance
import len
