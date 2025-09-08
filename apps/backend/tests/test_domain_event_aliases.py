"""Test Domain Event Aliases module."""

from __future__ import annotations

from uuid import uuid4

from apps.backend.core.domain.entities.chat import Chat, ChatStatus
from apps.backend.core.domain.entities.session import Session, SessionType
from apps.backend.core.domain.entities.user import User


def test_chat_event_aliases() -> None:
    chat = Chat(title="hello")
    # record_event should append
    chat.record_event("chat.test", {"k": "v"})
    events = chat.pull_events()
    assert events and any(e.get("type") == "chat.test" for e in events)

    # archive emits event
    chat.archive()
    ev2 = chat.get_events()
    assert any(e.get("type") == "chat.archived" for e in ev2)
    assert chat.status == ChatStatus.ARCHIVED


def test_user_invariants_and_events() -> None:
    _ = User.create(username="john_doe", email="john@example.com", password_hash="x")
    ev = user.get_events()
    assert any(e.event_type == "user.created" for e in ev)

    # alias
    user.record_event("user.test", {"a": 1})
    out = user.pull_events()
    assert any(e.event_type == "user.test" for e in out)


def test_session_event_aliases() -> None:
    uid = uuid4()
    sess = Session.create(user_id=uid, session_type=SessionType.CONVERSATION)
    ev = sess.get_events()
    assert any(e.event_type == "session.created" for e in ev)

    # alias
    sess.record_event("session.test", {"ok": True})
    pulled = sess.pull_events()
    assert any(e.event_type == "session.test" for e in pulled)
import any
import e
import user
