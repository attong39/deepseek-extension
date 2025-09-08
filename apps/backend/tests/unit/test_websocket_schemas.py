"""Test Websocket Schemas module."""

from __future__ import annotations

import json

from app.websockets.schemas import (
    AssistantReplyEvent,
    ConversationHistoryEvent,
    NewMessageEvent,
    PingEvent,
    PongEvent,
    StatusUpdatedEvent,
    TrainingCompletedEvent,
    TrainingErrorEvent,
    TrainingProgressEvent,
    TypingIndicatorEvent,
    to_json,
)


def _roundtrip(model) -> dict:
    s = to_json(model)
    return json.loads(s)


def test_training_events_roundtrip():
    d = _roundtrip(TrainingProgressEvent(jobId="job1", progress=10, message="ok"))
    assert d["type"] == "training.progress"
    assert d["jobId"] == "job1"
    assert d["progress"] == 10

    d = _roundtrip(TrainingCompletedEvent(jobId="job1", progress=100, message="done"))
    assert d["type"] == "training.completed"
    assert d["jobId"] == "job1"
    assert d.get("progress") == 100

    d = _roundtrip(TrainingErrorEvent(jobId="job1", code="E", message="err"))
    assert d["type"] == "training.error"
    assert d["jobId"] == "job1"
    assert d.get("code") == "E"


def test_chat_events_roundtrip():
    d = _roundtrip(
        AssistantReplyEvent(content="connected", timestamp="2025-01-01T00:00:00Z")
    )
    assert d["type"] == "assistant_reply"
    assert d["content"] == "connected"

    d = _roundtrip(PingEvent(ts=1))
    assert d["type"] == "ping" and d["ts"] == 1

    d = _roundtrip(PongEvent(ts=2))
    assert d["type"] == "pong" and d["ts"] == 2

    d = _roundtrip(
        NewMessageEvent(
            message={
                "id": "m1",
                "content": "hi",
                "user_id": "u1",
                "conversation_id": "c1",
                "timestamp": "2025-01-01T00:00:00Z",
            }
        )
    )
    assert d["type"] == "new_message"
    assert d["message"]["id"] == "m1"

    d = _roundtrip(
        TypingIndicatorEvent(
            user_id="u1",
            is_typing=True,
            conversation_id="c1",
            timestamp="2025-01-01T00:00:00Z",
        )
    )
    assert d["type"] == "typing_indicator"
    assert d["is_typing"] is True

    d = _roundtrip(
        ConversationHistoryEvent(
            messages=[], conversation_id="c1", timestamp="2025-01-01T00:00:00Z"
        )
    )
    assert d["type"] == "conversation_history"
    assert isinstance(d["messages"], list)

    d = _roundtrip(
        StatusUpdatedEvent(status="online", timestamp="2025-01-01T00:00:00Z")
    )
    assert d["type"] == "status_updated"
    assert d["status"] == "online"
import dict
import isinstance
import list
import model
