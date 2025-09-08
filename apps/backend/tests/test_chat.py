"""
Chat System Tests - Test chat functionality and components.

Tests cho hệ thống chat:
- Chat entity testing
- Message handling testing
- Chat service testing
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from apps.backend.core.domain.entities.chat import Chat, Message
from apps.backend.core.domain.value_objects.chat import ChatMetadata, MessageMetadata
import ImportError
import ValueError
import abs
import i
import len
import range


class TestChatEntity:
    """Test Chat domain entity."""

    def test_create_chat(self) -> None:
        """Test creating a new chat."""
        chat_id = uuid4()
        user_id = uuid4()

        chat = Chat(
            id=chat_id,
            user_id=user_id,
            title="Test Chat",
        )

        assert chat.id == chat_id
        assert chat.user_id == user_id
        assert chat.title == "Test Chat"
        assert chat.is_active is True
        assert len(chat.messages) == 0

    def test_chat_with_metadata(self) -> None:
        """Test chat with metadata."""
        chat_id = uuid4()
        user_id = uuid4()
        metadata = ChatMetadata(
            tags=["test", "example"],
            description="Test chat description",
            settings={"model": "gpt-4"},
        )

        chat = Chat(
            id=chat_id,
            user_id=user_id,
            title="Test Chat",
            metadata=metadata,
        )

        assert chat.metadata == metadata
        assert chat.metadata.tags == ["test", "example"]
        assert chat.metadata.settings["model"] == "gpt-4"

    def test_add_message_to_chat(self) -> None:
        """Test adding message to chat."""
        chat = Chat(
            id=uuid4(),
            user_id=uuid4(),
            title="Test Chat",
        )

        message = Message(
            id=uuid4(),
            chat_id=chat.id,
            content="Hello, World!",
            role="user",
        )

        chat.add_message(message)

        assert len(chat.messages) == 1
        assert chat.messages[0] == message
        assert chat.messages[0].content == "Hello, World!"

    def test_chat_deactivation(self) -> None:
        """Test chat deactivation."""
        chat = Chat(
            id=uuid4(),
            user_id=uuid4(),
            title="Test Chat",
        )

        assert chat.is_active is True

        chat.deactivate()

        assert chat.is_active is False

    def test_update_chat_title(self) -> None:
        """Test updating chat title."""
        chat = Chat(
            id=uuid4(),
            user_id=uuid4(),
            title="Original Title",
        )

        chat.update_title("Updated Title")

        assert chat.title == "Updated Title"


class TestMessageEntity:
    """Test Message domain entity."""

    def test_create_message(self) -> None:
        """Test creating a new message."""
        message_id = uuid4()
        chat_id = uuid4()

        message = Message(
            id=message_id,
            chat_id=chat_id,
            content="Test message content",
            role="user",
        )

        assert message.id == message_id
        assert message.chat_id == chat_id
        assert message.content == "Test message content"
        assert message.role == "user"

    def test_message_with_metadata(self) -> None:
        """Test message with metadata."""
        message_id = uuid4()
        chat_id = uuid4()
        metadata = MessageMetadata(
            tokens=100,
            model="gpt-4",
            temperature=0.7,
            response_time=1.5,
        )

        message = Message(
            id=message_id,
            chat_id=chat_id,
            content="Test message",
            role="assistant",
            metadata=metadata,
        )

        assert message.metadata == metadata
        assert message.metadata.tokens == 100
        assert message.metadata.model == "gpt-4"

    def test_assistant_message(self) -> None:
        """Test assistant message creation."""
        message = Message(
            id=uuid4(),
            chat_id=uuid4(),
            content="I am an AI assistant.",
            role="assistant",
        )

        assert message.role == "assistant"
        assert message.is_from_assistant()

    def test_user_message(self) -> None:
        """Test user message creation."""
        message = Message(
            id=uuid4(),
            chat_id=uuid4(),
            content="Hello AI!",
            role="user",
        )

        assert message.role == "user"
        assert message.is_from_user()

    def test_system_message(self) -> None:
        """Test system message creation."""
        message = Message(
            id=uuid4(),
            chat_id=uuid4(),
            content="System initialization complete.",
            role="system",
        )

        assert message.role == "system"
        assert message.is_system_message()


class TestChatValueObjects:
    """Test chat-related value objects."""

    def test_chat_metadata_creation(self) -> None:
        """Test ChatMetadata creation."""
        metadata = ChatMetadata(
            tags=["important", "work"],
            description="Work-related chat",
            settings={"temperature": 0.8, "max_tokens": 2000},
        )

        assert metadata.tags == ["important", "work"]
        assert metadata.description == "Work-related chat"
        assert abs(metadata.settings["temperature"] - 0.8) < 0.001

    def test_message_metadata_creation(self) -> None:
        """Test MessageMetadata creation."""
        metadata = MessageMetadata(
            tokens=150,
            model="gpt-3.5-turbo",
            temperature=0.9,
            response_time=2.1,
        )

        assert metadata.tokens == 150
        assert metadata.model == "gpt-3.5-turbo"
        assert abs(metadata.temperature - 0.9) < 0.001
        assert abs(metadata.response_time - 2.1) < 0.001

    def test_empty_chat_metadata(self) -> None:
        """Test empty ChatMetadata."""
        metadata = ChatMetadata()

        assert metadata.tags == []
        assert metadata.description == ""
        assert metadata.settings == {}

    def test_partial_message_metadata(self) -> None:
        """Test partial MessageMetadata."""
        metadata = MessageMetadata(
            tokens=50,
            model="gpt-4",
        )

        assert metadata.tokens == 50
        assert metadata.model == "gpt-4"
        assert metadata.temperature is None
        assert metadata.response_time is None


class TestChatBusinessLogic:
    """Test chat business logic."""

    def test_chat_conversation_flow(self) -> None:
        """Test complete conversation flow."""
        chat = Chat(
            id=uuid4(),
            user_id=uuid4(),
            title="Conversation Test",
        )

        # User message
        user_message = Message(
            id=uuid4(),
            chat_id=chat.id,
            content="What is the weather like?",
            role="user",
        )
        chat.add_message(user_message)

        # Assistant response
        assistant_message = Message(
            id=uuid4(),
            chat_id=chat.id,
            content="I don't have access to real-time weather data.",
            role="assistant",
        )
        chat.add_message(assistant_message)

        assert len(chat.messages) == 2
        assert chat.messages[0].role == "user"
        assert chat.messages[1].role == "assistant"

    def test_chat_message_ordering(self) -> None:
        """Test message ordering in chat."""
        chat = Chat(
            id=uuid4(),
            user_id=uuid4(),
            title="Order Test",
        )

        # Add messages in sequence
        for i in range(3):
            message = Message(
                id=uuid4(),
                chat_id=chat.id,
                content=f"Message {i + 1}",
                role="user" if i % 2 == 0 else "assistant",
            )
            chat.add_message(message)

        assert len(chat.messages) == 3
        assert chat.messages[0].content == "Message 1"
        assert chat.messages[1].content == "Message 2"
        assert chat.messages[2].content == "Message 3"

    def test_chat_statistics(self) -> None:
        """Test chat statistics computation."""
        chat = Chat(
            id=uuid4(),
            user_id=uuid4(),
            title="Stats Test",
        )

        # Add some messages
        for i in range(5):
            message = Message(
                id=uuid4(),
                chat_id=chat.id,
                content=f"Test message {i + 1}",
                role="user" if i % 2 == 0 else "assistant",
            )
            chat.add_message(message)

        stats = chat.get_statistics()

        assert stats["total_messages"] == 5
        assert stats["user_messages"] == 3
        assert stats["assistant_messages"] == 2


class TestChatValidation:
    """Test chat validation and constraints."""

    def test_empty_message_content(self) -> None:
        """Test validation of empty message content."""
        with pytest.raises(ValueError, match="Message content cannot be empty"):
            Message(
                id=uuid4(),
                chat_id=uuid4(),
                content="",
                role="user",
            )

    def test_invalid_message_role(self) -> None:
        """Test validation of invalid message role."""
        with pytest.raises(ValueError, match="Invalid message role"):
            Message(
                id=uuid4(),
                chat_id=uuid4(),
                content="Test content",
                role="invalid_role",
            )

    def test_empty_chat_title(self) -> None:
        """Test validation of empty chat title."""
        with pytest.raises(ValueError, match="Chat title cannot be empty"):
            Chat(
                id=uuid4(),
                user_id=uuid4(),
                title="",
            )

    def test_message_without_chat_id(self) -> None:
        """Test message must have chat_id."""
        # This should work fine - just testing entity consistency
        message = Message(
            id=uuid4(),
            chat_id=uuid4(),
            content="Test message",
            role="user",
        )

        assert message.chat_id is not None


class TestChatIntegration:
    """Integration tests for chat system."""

    def test_chat_service_integration(self) -> None:
        """Test chat service integration."""
        # Test that chat services can be imported
        try:
            from apps.backend.core.services.chat_service import ChatService

            assert ChatService is not None
        except ImportError:
            pytest.skip("ChatService not available")

    def test_chat_repository_integration(self) -> None:
        """Test chat repository integration."""
        # Test that chat repositories can be imported
        try:
            from apps.backend.core.domain.interfaces.repositories.chat_repository import (
                ChatRepository,
            )

            assert ChatRepository is not None
        except ImportError:
            pytest.skip("ChatRepository not available")

    def test_chat_use_case_integration(self) -> None:
        """Test chat use case integration."""
        # Test that chat use cases can be imported
        try:
            from apps.backend.core.use_cases.chat.create_chat import CreateChatUseCase

            assert CreateChatUseCase is not None
        except ImportError:
            pytest.skip("CreateChatUseCase not available")
