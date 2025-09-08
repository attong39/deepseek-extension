"""Unit tests for domain events.

Tests event creation and functionality for existing event structures.
"""

from datetime import datetime
from uuid import uuid4

import pytest

from core.domain.events.agent_events import (
import AttributeError
import TypeError
import abs
import all
import e
import i
import isinstance
import len
import range
import sorted
import str
    AgentCreatedEvent,
    AgentDeletedEvent,
    AgentDeployedEvent,
    AgentUpdatedEvent,
)
from core.domain.events.chat_events import (
    ConversationEndedEvent,
    ConversationStartedEvent,
    MessageReceivedEvent,
    MessageSentEvent,
)
from core.domain.events.memory_events import (
    MemoryCreatedEvent,
    MemoryDeletedEvent,
    MemoryRetrievedEvent,
    MemoryUpdatedEvent,
)


class TestAgentEvents:
    """Test cases for agent-related domain events."""

    def test_agent_created_event(self) -> None:
        """Test AgentCreatedEvent creation and data."""
        agent_id = str(uuid4())
        owner_id = str(uuid4())
        configuration = {
            "model": "gpt-4",
            "temperature": 0.7,
            "capabilities": ["chat", "planning"],
        }

        event = AgentCreatedEvent(
            agent_id=agent_id,
            agent_name="Test Agent",
            agent_type="conversational",
            owner_id=owner_id,
            configuration=configuration,
            created_at=datetime.now(),
        )

        assert event.agent_id == agent_id
        assert event.agent_name == "Test Agent"
        assert event.agent_type == "conversational"
        assert event.owner_id == owner_id
        assert event.configuration == configuration
        assert isinstance(event.created_at, datetime)

    def test_agent_updated_event(self) -> None:
        """Test AgentUpdatedEvent with changes."""
        agent_id = str(uuid4())
        updated_by = str(uuid4())
        updated_fields = {
            "agent_type": "advanced",
            "configuration": {"temperature": 0.8},
        }

        event = AgentUpdatedEvent(
            agent_id=agent_id,
            agent_name="Updated Agent",
            updated_fields=updated_fields,
            updated_by=updated_by,
            updated_at=datetime.now(),
        )

        assert event.agent_id == agent_id
        assert event.agent_name == "Updated Agent"
        assert event.updated_fields == updated_fields
        assert event.updated_by == updated_by
        assert isinstance(event.updated_at, datetime)

    def test_agent_deployed_event(self) -> None:
        """Test AgentDeployedEvent creation."""
        agent_id = str(uuid4())
        deployed_by = str(uuid4())
        deployment_config = {"replicas": 3, "resources": {"cpu": "500m"}}

        event = AgentDeployedEvent(
            agent_id=agent_id,
            agent_name="Deployed Agent",
            deployment_environment="production",
            deployment_config=deployment_config,
            deployed_by=deployed_by,
            deployed_at=datetime.now(),
        )

        assert event.agent_id == agent_id
        assert event.agent_name == "Deployed Agent"
        assert event.deployment_environment == "production"
        assert event.deployment_config == deployment_config
        assert event.deployed_by == deployed_by
        assert isinstance(event.deployed_at, datetime)

    def test_agent_deleted_event(self) -> None:
        """Test AgentDeletedEvent creation."""
        agent_id = str(uuid4())
        deleted_by = str(uuid4())

        event = AgentDeletedEvent(
            agent_id=agent_id,
            agent_name="Deleted Agent",
            deleted_by=deleted_by,
            deleted_at=datetime.now(),
            reason="Test deletion",
        )

        assert event.agent_id == agent_id
        assert event.agent_name == "Deleted Agent"
        assert event.deleted_by == deleted_by
        assert event.reason == "Test deletion"
        assert isinstance(event.deleted_at, datetime)


class TestChatEvents:
    """Test cases for chat-related domain events."""

    def test_conversation_started_event(self) -> None:
        """Test ConversationStartedEvent creation."""
        conversation_id = str(uuid4())
        agent_id = str(uuid4())
        user_id = str(uuid4())

        event = ConversationStartedEvent(
            conversation_id=conversation_id,
            agent_id=agent_id,
            user_id=user_id,
            initial_message="Hello, how can I help you?",
            started_at=datetime.now(),
        )

        assert event.conversation_id == conversation_id
        assert event.agent_id == agent_id
        assert event.user_id == user_id
        assert event.initial_message == "Hello, how can I help you?"
        assert isinstance(event.started_at, datetime)

    def test_message_sent_event(self) -> None:
        """Test MessageSentEvent creation."""
        message_id = str(uuid4())
        conversation_id = str(uuid4())
        sender_id = str(uuid4())

        event = MessageSentEvent(
            message_id=message_id,
            conversation_id=conversation_id,
            sender_id=sender_id,
            sender_type="user",
            content="Hello, this is a test message",
            metadata={"platform": "web"},
            sent_at=datetime.now(),
        )

        assert event.message_id == message_id
        assert event.conversation_id == conversation_id
        assert event.sender_id == sender_id
        assert event.sender_type == "user"
        assert event.content == "Hello, this is a test message"
        assert event.metadata["platform"] == "web"

    def test_conversation_ended_event(self) -> None:
        """Test ConversationEndedEvent creation."""
        conversation_id = str(uuid4())
        agent_id = str(uuid4())
        user_id = str(uuid4())

        event = ConversationEndedEvent(
            conversation_id=conversation_id,
            agent_id=agent_id,
            user_id=user_id,
            ended_at=datetime.now(),
            reason="User ended conversation",
        )

        assert event.conversation_id == conversation_id
        assert event.agent_id == agent_id
        assert event.user_id == user_id
        assert event.reason == "User ended conversation"

    def test_message_received_event(self) -> None:
        """Test MessageReceivedEvent creation."""
        message_id = str(uuid4())
        conversation_id = str(uuid4())
        receiver_id = str(uuid4())

        event = MessageReceivedEvent(
            message_id=message_id,
            conversation_id=conversation_id,
            receiver_id=receiver_id,
            receiver_type="agent",
            content="I understand your request",
            metadata={"processing_time": 0.5},
            received_at=datetime.now(),
        )

        assert event.message_id == message_id
        assert event.conversation_id == conversation_id
        assert event.receiver_id == receiver_id
        assert event.receiver_type == "agent"
        assert event.content == "I understand your request"


class TestMemoryEvents:
    """Test cases for memory-related domain events."""

    def test_memory_created_event(self) -> None:
        """Test MemoryCreatedEvent creation."""
        memory_id = str(uuid4())
        agent_id = str(uuid4())

        event = MemoryCreatedEvent(
            memory_id=memory_id,
            agent_id=agent_id,
            content="User learned something new about Python",
            memory_type="episodic",
            tags=["python", "learning"],
            importance=0.8,
            created_at=datetime.now(),
        )

        assert event.memory_id == memory_id
        assert event.agent_id == agent_id
        assert event.content == "User learned something new about Python"
        assert event.memory_type == "episodic"
        assert "python" in event.tags
        # Use approximate comparison for floats
        assert abs(event.importance - 0.8) < 0.001

    def test_memory_updated_event(self) -> None:
        """Test MemoryUpdatedEvent creation."""
        memory_id = str(uuid4())
        agent_id = str(uuid4())
        updated_fields = {"importance": 0.9, "tags": ["python", "learning", "advanced"]}

        event = MemoryUpdatedEvent(
            memory_id=memory_id,
            agent_id=agent_id,
            updated_fields=updated_fields,
            previous_content="Original content",
            updated_at=datetime.now(),
        )

        assert event.memory_id == memory_id
        assert event.agent_id == agent_id
        assert event.updated_fields == updated_fields
        assert event.previous_content == "Original content"

    def test_memory_deleted_event(self) -> None:
        """Test MemoryDeletedEvent creation."""
        memory_id = str(uuid4())
        agent_id = str(uuid4())

        event = MemoryDeletedEvent(
            memory_id=memory_id,
            agent_id=agent_id,
            deleted_at=datetime.now(),
            reason="Memory obsolete",
        )

        assert event.memory_id == memory_id
        assert event.agent_id == agent_id
        assert event.reason == "Memory obsolete"

    def test_memory_retrieved_event(self) -> None:
        """Test MemoryRetrievedEvent creation."""
        memory_id = str(uuid4())
        agent_id = str(uuid4())

        event = MemoryRetrievedEvent(
            memory_id=memory_id,
            agent_id=agent_id,
            query="python programming",
            relevance_score=0.85,
            retrieved_at=datetime.now(),
        )

        assert event.memory_id == memory_id
        assert event.agent_id == agent_id
        assert event.query == "python programming"
        # Use approximate comparison for floats
        assert abs(event.relevance_score - 0.85) < 0.001


class TestEventProperties:
    """Test cases for event properties and behavior."""

    def test_event_immutability(self) -> None:
        """Test that events are immutable (frozen dataclasses)."""
        event = MemoryCreatedEvent(
            memory_id=str(uuid4()),
            agent_id=str(uuid4()),
            content="Test content",
            memory_type="semantic",
            tags=["test"],
            importance=0.5,
            created_at=datetime.now(),
        )

        # Should not be able to modify the event
        with pytest.raises((AttributeError, TypeError)):
            event.content = "Modified content"

    def test_event_timestamp_accuracy(self) -> None:
        """Test that event timestamps are accurate."""
        before = datetime.now()

        event = AgentCreatedEvent(
            agent_id=str(uuid4()),
            agent_name="Timestamp Test Agent",
            agent_type="test",
            owner_id=str(uuid4()),
            configuration={"test": True},
            created_at=datetime.now(),
        )

        after = datetime.now()

        assert before <= event.created_at <= after

    def test_event_string_representation(self) -> None:
        """Test event string representation."""
        event = ConversationStartedEvent(
            conversation_id="conv_123",
            agent_id="agent_456",
            user_id="user_789",
            initial_message="Hello",
            started_at=datetime.now(),
        )

        str_repr = str(event)
        assert "ConversationStartedEvent" in str_repr
        assert "conv_123" in str_repr


class TestEventFactoryPatterns:
    """Test cases for event creation patterns."""

    def test_create_agent_lifecycle_events(self) -> None:
        """Test creating a sequence of agent lifecycle events."""
        agent_id = str(uuid4())
        owner_id = str(uuid4())
        deployed_by = str(uuid4())
        deleted_by = str(uuid4())
        now = datetime.now()

        # Agent creation
        created_event = AgentCreatedEvent(
            agent_id=agent_id,
            agent_name="Lifecycle Agent",
            agent_type="test",
            owner_id=owner_id,
            configuration={"test": True},
            created_at=now,
        )

        # Agent deployment
        deployed_event = AgentDeployedEvent(
            agent_id=agent_id,
            agent_name="Lifecycle Agent",
            deployment_environment="test",
            deployment_config={"replicas": 1},
            deployed_by=deployed_by,
            deployed_at=now,
        )

        # Agent deletion
        deleted_event = AgentDeletedEvent(
            agent_id=agent_id,
            agent_name="Lifecycle Agent",
            deleted_by=deleted_by,
            deleted_at=now,
            reason="Test completed",
        )

        assert (
            created_event.agent_id == deployed_event.agent_id == deleted_event.agent_id
        )
        assert all(
            event.agent_id == agent_id
            for event in [created_event, deployed_event, deleted_event]
        )

    def test_create_conversation_flow_events(self) -> None:
        """Test creating a conversation flow with multiple events."""
        conversation_id = str(uuid4())
        agent_id = str(uuid4())
        user_id = str(uuid4())
        now = datetime.now()

        # Start conversation
        started_event = ConversationStartedEvent(
            conversation_id=conversation_id,
            agent_id=agent_id,
            user_id=user_id,
            initial_message="How can I help?",
            started_at=now,
        )

        # Send message
        message_event = MessageSentEvent(
            message_id=str(uuid4()),
            conversation_id=conversation_id,
            sender_id=user_id,
            sender_type="user",
            content="I need help with Python",
            metadata={"intent": "help_request"},
            sent_at=now,
        )

        # End conversation
        ended_event = ConversationEndedEvent(
            conversation_id=conversation_id,
            agent_id=agent_id,
            user_id=user_id,
            ended_at=now,
            reason="User satisfied",
        )

        flow_events = [started_event, message_event, ended_event]
        conversation_ids = {event.conversation_id for event in flow_events}
        assert len(conversation_ids) == 1
        assert conversation_id in conversation_ids


class TestEventIntegration:
    """Test cases for event system integration."""

    def test_event_data_consistency(self) -> None:
        """Test that related events maintain data consistency."""
        agent_id = str(uuid4())
        memory_id = str(uuid4())

        # Create memory
        memory_created = MemoryCreatedEvent(
            memory_id=memory_id,
            agent_id=agent_id,
            content="Original content",
            memory_type="semantic",
            tags=["test"],
            importance=0.7,
            created_at=datetime.now(),
        )

        # Update memory
        memory_updated = MemoryUpdatedEvent(
            memory_id=memory_id,
            agent_id=agent_id,
            updated_fields={"importance": 0.9},
            previous_content="Original content",
            updated_at=datetime.now(),
        )

        assert memory_created.memory_id == memory_updated.memory_id
        assert memory_created.agent_id == memory_updated.agent_id
        assert memory_created.content == memory_updated.previous_content

    def test_event_chronological_ordering(self) -> None:
        """Test that events can be ordered chronologically."""
        agent_id = str(uuid4())

        events = []

        # Create events with slight time differences
        for i in range(3):
            event = MemoryCreatedEvent(
                memory_id=str(uuid4()),
                agent_id=agent_id,
                content=f"Memory {i}",
                memory_type="test",
                tags=["test"],
                importance=0.5,
                created_at=datetime.now(),
            )
            events.append(event)

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.created_at)

        # Verify order (should be same or chronological)
        for i in range(len(sorted_events) - 1):
            assert sorted_events[i].created_at <= sorted_events[i + 1].created_at
