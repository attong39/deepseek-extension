"""Tests for Session domain entity.

Tests the Session entity's DDD compliance, invariants, and business logic.
"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from core.domain.entities.session import Session, SessionStatus, SessionType
from core.domain.value_objects.conversation_context import ConversationContext
from core.domain.value_objects.security_context import SecurityContext
import ValueError
import isinstance
import len
import str


class TestSessionEntity:
    """Test cases for Session entity."""

    def test_session_creation_with_defaults(self) -> None:
        """Test session creation with default values."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        assert session.user_id == user_id
        assert session.agent_id is None
        assert session.session_type == SessionType.CONVERSATION
        assert session.status == SessionStatus.ACTIVE
        assert session.message_count == 0
        assert session.chat_count == 0
        assert isinstance(session.context, ConversationContext)
        assert isinstance(session.security_context, SecurityContext)
        assert session.metadata == {}

    def test_session_create_factory_method(self) -> None:
        """Test Session.create factory method."""
        user_id = uuid4()
        agent_id = uuid4()

        _ = Session.create(
            user_id=user_id,
            agent_id=agent_id,
            session_type=SessionType.AGENT_INTERACTION,
            ip_address="192.168.1.1",
            user_agent="TestAgent/1.0",
            test_meta="test_value",
        )

        assert session.user_id == user_id
        assert session.agent_id == agent_id
        assert session.session_type == SessionType.AGENT_INTERACTION
        assert session.ip_address == "192.168.1.1"
        assert session.user_agent == "TestAgent/1.0"
        assert session.metadata["test_meta"] == "test_value"

        # Check events
        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.created"
        assert events[0].data["session_id"] == str(session.id)
        assert events[0].data["user_id"] == str(user_id)
        assert events[0].data["agent_id"] == str(agent_id)

    def test_session_create_validation(self) -> None:
        """Test Session.create validation."""
        with pytest.raises(ValueError, match="User ID is required"):
            Session.create(user_id=None)

    def test_session_open(self) -> None:
        """Test session open/activation."""
        user_id = uuid4()
        session = Session(user_id=user_id, status=SessionStatus.INACTIVE)

        session.open()

        assert session.status == SessionStatus.ACTIVE
        assert session.started_at is not None
        assert session.last_activity_at is not None

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.opened"

    def test_session_close(self) -> None:
        """Test session close/termination."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        session.close(reason="user_logout")

        assert session.status == SessionStatus.TERMINATED
        assert session.ended_at is not None

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.closed"
        assert events[0].data["reason"] == "user_logout"

    def test_session_switch_agent(self) -> None:
        """Test switching agent binding."""
        user_id = uuid4()
        agent_id1 = uuid4()
        agent_id2 = uuid4()

        session = Session(user_id=user_id, agent_id=agent_id1)

        session.switch_agent(agent_id2)

        assert session.agent_id == agent_id2

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.agent_switched"
        assert events[0].data["old_agent_id"] == str(agent_id1)
        assert events[0].data["new_agent_id"] == str(agent_id2)

    def test_session_switch_agent_to_none(self) -> None:
        """Test removing agent binding."""
        user_id = uuid4()
        agent_id = uuid4()

        session = Session(user_id=user_id, agent_id=agent_id)

        session.switch_agent(None)

        assert session.agent_id is None

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.agent_switched"
        assert events[0].data["old_agent_id"] == str(agent_id)
        assert events[0].data["new_agent_id"] is None

    def test_session_update_context(self) -> None:
        """Test updating conversation context."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        session.update_context(
            topic="AI Development",
            language="en",
            project="zeta",
        )

        assert session.context.topic == "AI Development"
        assert session.context.metadata["language"] == "en"
        assert session.context.metadata["project"] == "zeta"

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.context_updated"

    def test_session_activity_tracking(self) -> None:
        """Test session activity tracking."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        initial_activity = session.last_activity_at

        session.record_activity()
        assert session.last_activity_at > initial_activity

        session.increment_message_count()
        assert session.message_count == 1

        session.increment_chat_count()
        assert session.chat_count == 1

    def test_session_expiration_handling(self) -> None:
        """Test session expiration logic."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        # Session should not be expired initially
        assert not session.is_expired()
        assert session.is_active()
        assert session.is_valid()

        # Manually set expiration in the past
        past_time = datetime.now(UTC) - timedelta(hours=1)
        session.expires_at = past_time

        assert session.is_expired()
        assert not session.is_active()
        assert not session.is_valid()

    def test_session_extend_expiration(self) -> None:
        """Test extending session expiration."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        original_expiry = session.expires_at

        session.extend_expiration(hours=48)

        assert session.expires_at > original_expiry

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.extended"
        assert events[0].data["extension_hours"] == 48

    def test_session_deactivate(self) -> None:
        """Test session deactivation."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        session.deactivate()

        assert session.status == SessionStatus.INACTIVE

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.deactivated"

    def test_session_expire(self) -> None:
        """Test session expiration."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        session.expire()

        assert session.status == SessionStatus.EXPIRED
        assert session.ended_at is not None

        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.expired"

    def test_session_security_context_update(self) -> None:
        """Test updating security context."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        session.update_security_context(
            scopes=("read", "write"),
            token_type="bearer",
            client_id="test_client",
        )

        assert session.security_context.scopes == ("read", "write")
        assert session.security_context.get("token_type") == "bearer"
        assert session.security_context.get("client_id") == "test_client"

    def test_session_metadata_management(self) -> None:
        """Test session metadata operations."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        session.update_metadata(
            client_version="1.0.0",
            feature_flags=["flag1", "flag2"],
        )

        assert session.get_metadata_value("client_version") == "1.0.0"
        assert session.get_metadata_value("feature_flags") == ["flag1", "flag2"]
        assert session.get_metadata_value("non_existent", "default") == "default"

    def test_session_duration_calculation(self) -> None:
        """Test session duration calculations."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        # Test with active session
        duration = session.get_duration_seconds()
        assert duration >= 0

        # Test with ended session
        session.close()
        duration_after_close = session.get_duration_seconds()
        assert duration_after_close >= duration

    def test_session_inactivity_calculation(self) -> None:
        """Test session inactivity calculations."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        inactivity = session.get_inactivity_seconds()
        assert inactivity >= 0

        # After recording activity, inactivity should reset
        session.record_activity()
        new_inactivity = session.get_inactivity_seconds()
        assert new_inactivity < inactivity

    def test_session_helper_methods(self) -> None:
        """Test session helper methods."""
        user_id = uuid4()
        agent_id = uuid4()

        session = Session(user_id=user_id, agent_id=agent_id)

        assert session.has_agent()

        session.switch_agent(None)
        assert not session.has_agent()

        session.update_context(topic="Test Topic")
        assert session.has_context_topic()

    def test_session_to_dict(self) -> None:
        """Test session dictionary representation."""
        user_id = uuid4()
        agent_id = uuid4()

        session = Session(
            user_id=user_id,
            agent_id=agent_id,
            session_type=SessionType.API_SESSION,
            ip_address="192.168.1.1",
        )

        session_dict = session.to_dict()

        assert session_dict["user_id"] == str(user_id)
        assert session_dict["agent_id"] == str(agent_id)
        assert session_dict["session_type"] == SessionType.API_SESSION
        assert session_dict["ip_address"] == "192.168.1.1"
        assert "is_active" in session_dict
        assert "is_expired" in session_dict
        assert "duration_seconds" in session_dict

    def test_session_refresh(self) -> None:
        """Test session refresh functionality."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        original_expiry = session.expires_at
        original_activity = session.last_activity_at

        session.refresh()

        assert session.expires_at > original_expiry
        assert session.last_activity_at > original_activity

    def test_session_time_until_expiry(self) -> None:
        """Test time until expiry calculation."""
        user_id = uuid4()
        session = Session(user_id=user_id)

        time_remaining = session.time_until_expiry()
        assert time_remaining.total_seconds() > 0

        # Set expiry in the past
        session.expires_at = datetime.now(UTC) - timedelta(hours=1)
        time_remaining = session.time_until_expiry()
        assert time_remaining.total_seconds() == 0

    def test_session_events_management(self) -> None:
        """Test domain events management."""
        user_id = uuid4()
        _ = Session.create(user_id=user_id)

        # Should have creation event
        events = session.get_events()
        assert len(events) == 1
        assert events[0].event_type == "session.created"

        # Events should be cleared after getting them
        events_again = session.get_events()
        assert len(events_again) == 0

        # New operations should create new events
        session.open()
        session.close()

        events = session.get_events()
        assert len(events) == 2
        assert events[0].event_type == "session.opened"
        assert events[1].event_type == "session.closed"
