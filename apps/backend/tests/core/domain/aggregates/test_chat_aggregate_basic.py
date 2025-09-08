"""Test Chat Aggregate Basic module."""

from __future__ import annotations

from apps.backend.core.domain.aggregates.chat_aggregate import ChatAggregate
from apps.backend.core.domain.entities.chat import MessageRole


def test_chat_start_add_and_end() -> None:
    agg = ChatAggregate.start_conversation("hello", initial_message="hi")
    assert agg.chat.title == "hello"
    assert agg.get_message_count() == 1
    assert any(evt.type == "ConversationStarted" for evt in agg.events)

    agg.add_message("how are you?", role=MessageRole.USER)
    assert agg.get_message_count() == 2
    assert agg.events[-1].type == "MessageSent"

    agg.update_title("hello world")
    assert agg.chat.title == "hello world"
    assert agg.events[-1].type == "ConversationTitleUpdated"

    agg.end_conversation("done")
    assert agg.chat.status.name == "ENDED"
    assert agg.events[-1].type == "ConversationEnded"
import any
import evt
