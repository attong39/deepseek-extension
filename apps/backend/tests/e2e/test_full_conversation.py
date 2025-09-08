import os
import Exception
import ValueError
import a
import all
import auth_result
import conversation_result
import created_agent
import enumerate
import i
import isinstance
import len
import message
import message_content
import msg
import q
import result
import str
import user_msg

"""
🧪 E2E Tests for Full Conversation Flow - ZETA AI SERVER
======================================================

End-to-end tests for complete conversation workflows covering:
- Agent creation and configuration
- Message sending and receiving
- Memory storage and retrieval
- Conversation state management
- Error handling and recovery

These tests validate the entire conversation pipeline using
mocked repositories to focus on business logic integration.
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from core.domain.entities.agent import Agent, AgentCapability, AgentConfig, AgentStatus
from core.domain.entities.chat import ChatMessage
from core.domain.entities.memory import Memory, MemoryImportance, MemoryType
from core.domain.entities.user import User
from core.use_cases.agent.create_agent import CreateAgent
from core.use_cases.auth.authenticate_user import AuthenticateUser
from core.use_cases.chat.send_message import SendMessageUseCase
from core.use_cases.memory.store_memory import StoreMemory
from core.value_objects.auth import LoginRequest


@pytest.mark.e2e
@pytest.mark.asyncio
class TestFullConversationE2E:
    """End-to-end tests for full conversation workflows."""

    @pytest.fixture
    def mock_user_repo(self) -> Mock:
        """Create mock user repository."""
        return Mock()

    @pytest.fixture
    def mock_agent_repo(self) -> Mock:
        """Create mock agent repository."""
        return Mock()

    @pytest.fixture
    def mock_chat_repo(self) -> Mock:
        """Create mock chat repository."""
        return Mock()

    @pytest.fixture
    def mock_memory_repo(self) -> Mock:
        """Create mock memory repository."""
        return Mock()

    @pytest.fixture
    def test_user(self) -> User:
        """Create test user."""
        return User(
            id=str(uuid4()),
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            password_hash="$2b$12$hashed_password",
            is_active=True,
        )

    @pytest.fixture
    def test_agent(self) -> Agent:
        """Create test agent."""
        return Agent(
            name="ConversationBot",
            description="AI assistant for testing conversations",
            config=AgentConfig(
                capabilities=[AgentCapability.CHAT, AgentCapability.MEMORY],
                model_name="gpt-3.5-turbo",
                temperature=0.7,
            ),
            status=AgentStatus.ACTIVE,
        )

    async def test_complete_conversation_workflow(
        self,
        mock_user_repo: Mock,
        mock_agent_repo: Mock,
        mock_chat_repo: Mock,
        mock_memory_repo: Mock,
        test_user: User,
        test_agent: Agent,
    ) -> None:
        """Test complete conversation workflow from authentication to memory storage."""

        # Step 1: User Authentication
        auth_use_case = AuthenticateUser(mock_user_repo)
        login_request = LoginRequest(
            email=test_user.email, password=os.getenv("PASSWORD")
        )

        # Mock authentication
        mock_user_repo.get_by_email = AsyncMock(return_value=test_user)

        with (
            patch("bcrypt.checkpw", return_value=True),
            patch("jwt.encode", return_value="test_token"),
        ):
            _ = await auth_use_case(login_request)
            assert auth_result.access_token == "test_token"

        # Step 2: Create Agent
        create_agent_use_case = CreateAgent(mock_agent_repo)
        mock_agent_repo.create = AsyncMock(return_value=test_agent)

        await create_agent_use_case(
            name=test_agent.name,
            description=test_agent.description or "Test agent for conversation",
            capabilities=["chat", "memory"],
            config_data={"temperature": 0.7},
        )
        assert created_agent.name == test_agent.name
        assert AgentCapability.CHAT in created_agent.config.capabilities

        # Step 3: Send Messages
        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        messages = [
            "Hello, I need help with Python programming.",
            "Can you explain how to use decorators?",
            "What are the best practices for error handling?",
        ]

        conversation_history = []

        for i, message_content in enumerate(messages):
            # Mock agent response
            agent_response = ChatMessage(
                id=f"agent_msg_{i + 1}",
                content=f"I'd be happy to help with: {message_content}",
                sender_type="agent",
                sender_id=str(test_agent.id),
                agent_id=str(test_agent.id),
                timestamp=datetime.now(UTC),
            )

            mock_chat_repo.send_message = AsyncMock(return_value=agent_response)

            _ = await send_message_use_case.execute(
                agent_id=str(test_agent.id),
                content=message_content,
                user_id=test_user.id,
            )

            conversation_history.append(result)

            # Validate response
            assert isinstance(result, ChatMessage)
            assert result.content is not None
            assert result.agent_id == str(test_agent.id)
            assert (
                message_content.lower() in result.content.lower()
                or "help" in result.content.lower()
            )

        # Step 4: Store Conversation Memory
        store_memory_use_case = StoreMemory(mock_memory_repo)

        memory_content = (
            f"Conversation about Python programming covering: {', '.join(messages)}"
        )

        memory = Memory(
            content=memory_content,
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.HIGH,
            agent_id=test_agent.id,
            context={
                "user_id": test_user.id,
                "topic": "python_programming",
                "message_count": len(messages),
            },
            tags=["python", "programming", "conversation"],
        )

        mock_memory_repo.create = AsyncMock(return_value=memory)

        stored_memory = await store_memory_use_case(
            content=memory_content,
            memory_type="episodic",
            importance="high",
            agent_id=test_agent.id,
            context=memory.context,
            tags=memory.tags,
        )

        # Validate complete workflow
        assert isinstance(stored_memory, Memory)
        assert stored_memory.content == memory_content
        assert stored_memory.agent_id == test_agent.id
        assert len(conversation_history) == len(messages)
        assert all(isinstance(msg, ChatMessage) for msg in conversation_history)

    async def test_conversation_with_context_retention(
        self,
        mock_chat_repo: Mock,
        mock_memory_repo: Mock,
        test_user: User,
        test_agent: Agent,
    ) -> None:
        """Test conversation with context retention across multiple exchanges."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)
        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Simulate conversation with context
        context_messages = [
            "My name is Alice and I'm learning machine learning.",
            "What are the key concepts I should know?",
            "Can you recommend some resources for Alice?",  # Reference to earlier context
        ]

        conversation_context = {"user_name": "Alice", "topic": "machine_learning"}

        for i, message in enumerate(context_messages):
            # Mock context-aware response
            if "Alice" in message and i > 0:
                response_content = "Of course, Alice! Based on our previous discussion about machine learning, I recommend these resources..."
            else:
                response_content = f"Thank you for your question about: {message}"

            agent_response = ChatMessage(
                id=f"context_msg_{i + 1}",
                content=response_content,
                sender_type="agent",
                sender_id=str(test_agent.id),
                agent_id=str(test_agent.id),
                timestamp=datetime.now(UTC),
            )

            mock_chat_repo.send_message = AsyncMock(return_value=agent_response)

            _ = await send_message_use_case.execute(
                agent_id=str(test_agent.id),
                content=message,
                user_id=test_user.id,
            )

            # Validate context awareness
            if i == 2:  # Third message references Alice
                assert "Alice" in result.content
                assert (
                    "previous discussion" in result.content
                    or "based on" in result.content
                )

        # Store context memory
        context_memory = Memory(
            content="Conversation with Alice about machine learning fundamentals",
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            agent_id=test_agent.id,
            context=conversation_context,
            tags=["machine_learning", "alice", "education"],
        )

        mock_memory_repo.create = AsyncMock(return_value=context_memory)

        stored_context = await store_memory_use_case(
            content=context_memory.content,
            memory_type="episodic",
            importance="medium",
            agent_id=test_agent.id,
            context=conversation_context,
            tags=context_memory.tags,
        )

        assert stored_context.context["user_name"] == "Alice"
        assert stored_context.context["topic"] == "machine_learning"

    async def test_conversation_error_handling(
        self,
        mock_chat_repo: Mock,
        test_user: User,
        test_agent: Agent,
    ) -> None:
        """Test conversation error handling and recovery."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        # Test empty message handling
        with pytest.raises(ValueError, match="Message content cannot be empty"):
            await send_message_use_case.execute(
                agent_id=str(test_agent.id),
                content="   ",  # Empty/whitespace
                user_id=test_user.id,
            )

        # Test missing agent handling
        with pytest.raises(ValueError, match="Agent ID is required"):
            await send_message_use_case.execute(
                agent_id="",
                content="Valid message",
                user_id=test_user.id,
            )

        # Test repository error handling
        mock_chat_repo.send_message = AsyncMock(
            side_effect=Exception("Database connection failed")
        )

        with pytest.raises(Exception, match="Database connection failed"):
            await send_message_use_case.execute(
                agent_id=str(test_agent.id),
                content="Test message",
                user_id=test_user.id,
            )

    async def test_memory_integration_workflow(
        self,
        mock_memory_repo: Mock,
        mock_chat_repo: Mock,
        test_user: User,
        test_agent: Agent,
    ) -> None:
        """Test integration between conversation and memory systems."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)
        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Have a conversation about a specific topic
        topic_message = "I want to learn about quantum computing principles."

        # Mock agent response with educational content
        educational_response = ChatMessage(
            id="educational_msg_1",
            content="Quantum computing is based on quantum mechanics principles like superposition and entanglement. Let me explain each concept...",
            sender_type="agent",
            sender_id=str(test_agent.id),
            agent_id=str(test_agent.id),
            timestamp=datetime.now(UTC),
        )

        mock_chat_repo.send_message = AsyncMock(return_value=educational_response)

        await send_message_use_case.execute(
            agent_id=str(test_agent.id),
            content=topic_message,
            user_id=test_user.id,
        )

        # Store the educational conversation as semantic memory
        semantic_memory = Memory(
            content=f"User inquiry: {topic_message}. Agent response: {conversation_result.content}",
            type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            agent_id=test_agent.id,
            context={
                "topic": "quantum_computing",
                "learning_session": True,
                "user_id": test_user.id,
            },
            tags=["quantum_computing", "education", "principles"],
        )

        mock_memory_repo.create = AsyncMock(return_value=semantic_memory)

        stored_education = await store_memory_use_case(
            content=semantic_memory.content,
            memory_type="semantic",
            importance="high",
            agent_id=test_agent.id,
            context=semantic_memory.context,
            tags=semantic_memory.tags,
        )

        # Validate memory-conversation integration
        assert stored_education.type == MemoryType.SEMANTIC
        assert stored_education.context["topic"] == "quantum_computing"
        assert stored_education.context["learning_session"] is True
        assert "quantum computing" in stored_education.content.lower()

    async def test_multi_turn_conversation_flow(
        self,
        mock_chat_repo: Mock,
        mock_memory_repo: Mock,
        test_user: User,
        test_agent: Agent,
    ) -> None:
        """Test multi-turn conversation flow with progressive context building."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)
        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Progressive conversation building context
        conversation_turns = [
            (
                "What is machine learning?",
                "Machine learning is a subset of AI that enables computers to learn from data...",
            ),
            (
                "What are the main types?",
                "There are three main types: supervised, unsupervised, and reinforcement learning...",
            ),
            (
                "Can you give examples of supervised learning?",
                "Examples include linear regression, decision trees, and neural networks...",
            ),
            (
                "How do neural networks work?",
                "Neural networks consist of interconnected nodes that process information...",
            ),
        ]

        conversation_memory = []

        for i, (user_msg, agent_response) in enumerate(conversation_turns):
            # Mock agent response
            response = ChatMessage(
                id=f"turn_{i + 1}",
                content=agent_response,
                sender_type="agent",
                sender_id=str(test_agent.id),
                agent_id=str(test_agent.id),
                timestamp=datetime.now(UTC),
            )

            mock_chat_repo.send_message = AsyncMock(return_value=response)

            _ = await send_message_use_case.execute(
                agent_id=str(test_agent.id),
                content=user_msg,
                user_id=test_user.id,
            )

            conversation_memory.append((user_msg, result.content))

            # Validate progressive context
            assert isinstance(result, ChatMessage)
            assert len(result.content) > 20  # Substantial response

        # Store complete conversation as episodic memory
        full_conversation = "; ".join(
            [f"Q: {q} A: {a}" for q, a in conversation_memory]
        )

        episodic_memory = Memory(
            content=full_conversation,
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.HIGH,
            agent_id=test_agent.id,
            context={
                "conversation_type": "educational",
                "topic": "machine_learning",
                "turn_count": len(conversation_turns),
                "user_id": test_user.id,
            },
            tags=["machine_learning", "education", "multi_turn"],
        )

        mock_memory_repo.create = AsyncMock(return_value=episodic_memory)

        stored_conversation = await store_memory_use_case(
            content=episodic_memory.content,
            memory_type="episodic",
            importance="high",
            agent_id=test_agent.id,
            context=episodic_memory.context,
            tags=episodic_memory.tags,
        )

        # Validate conversation storage
        assert stored_conversation.context["turn_count"] == len(conversation_turns)
        assert "machine learning" in stored_conversation.content.lower()
        assert "neural networks" in stored_conversation.content.lower()
