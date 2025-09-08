from datetime import datetime
import ast
import os
import sys
"""
🧪 E2E Tests for Multi-User Operations - ZETA AI SERVER
=====================================================

End-to-end tests for multi-user scenarios covering:
- Concurrent user authentication
- Isolated user sessions and data
- Multi-user agent interactions
- User-specific memory and preferences
- Cross-user security and isolation
- Shared resources and collaboration

These tests validate proper user isolation and concurrent
user operations in a multi-tenant environment.
"""

import asyncio
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from core.domain.entities.agent import Agent, AgentCapability, AgentConfig, AgentStatus
from core.domain.entities.chat import ChatMessage
from core.domain.entities.memory import Memory, MemoryImportance, MemoryType
from core.domain.entities.user import User
from core.domain.value_objects.auth import LoginRequest
from core.use_cases.agent.create_agent import CreateAgent
from core.use_cases.auth.authenticate_user import AuthenticateUser
from core.use_cases.chat.send_message import SendMessageUseCase
from core.use_cases.memory.store_memory import StoreMemory

@pytest.mark.e2e
@pytest.mark.asyncio
class TestMultiUserE2E:
    """End-to-end tests for multi-user operations."""

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
    def test_users(self) -> list[User]:
        """Create multiple test users."""
        return [
            User(
                id=str(uuid4()),
                email="alice@example.com",
                username="alice",
                full_name="Alice Johnson",
                password_hash="$2b$12$hashed_password_alice",
                is_active=True,
            ),
            User(
                id=str(uuid4()),
                email="bob@example.com",
                username="bob",
                full_name="Bob Smith",
                password_hash="$2b$12$hashed_password_bob",
                is_active=True,
            ),
            User(
                id=str(uuid4()),
                email="charlie@example.com",
                username="charlie",
                full_name="Charlie Brown",
                password_hash="$2b$12$hashed_password_charlie",
                is_active=True,
            ),
        ]

    async def test_concurrent_user_authentication(
        self,
        mock_user_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test concurrent authentication of multiple users."""

        auth_use_case = AuthenticateUser(mock_user_repo)

        # Mock user lookups
        user_lookup = {user.email: user for user in test_users}
        mock_user_repo.get_by_email = AsyncMock(side_effect=lambda email: user_lookup.get(email))

        # Create concurrent authentication tasks
        auth_tasks = []

        for user in test_users:
            login_request = LoginRequest(email=user.email, password=os.getenv("PASSWORD"))

            # Use async context manager for each auth
    from unittest.mock import patch

            with (
                patch("bcrypt.checkpw", return_value=True),
                patch("jwt.encode", return_value=f"token_{user.username}"),
            ):
                task = auth_use_case(login_request)
                auth_tasks.append(task)

        # Execute all authentications concurrently
        auth_results = await asyncio.gather(*auth_tasks)

        # Validate all users authenticated successfully
        assert len(auth_results) == len(test_users)
        assert all(result.access_token is not None for result in auth_results)
        assert all(result.token_type == "bearer" for result in auth_results)

        # Verify unique tokens for each user
        tokens = [result.access_token for result in auth_results]
        assert len(set(tokens)) == len(tokens)  # All tokens unique

    async def test_user_isolation_in_agents(
        self,
        mock_agent_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test that each user's agents are isolated from others."""

        create_agent_use_case = CreateAgent(mock_agent_repo)

        # Create agents for different users
        user_agents = {}

        for i, user in enumerate(test_users):
            _ = Agent(
                name=f"Agent_{user.username}",
                description=f"Personal agent for {user.full_name}",
                config=AgentConfig(
                    capabilities=[AgentCapability.CHAT, AgentCapability.MEMORY],
                    model_name="gpt-3.5-turbo",
                ),
                status=AgentStatus.ACTIVE,
            )

            mock_agent_repo.create = AsyncMock(return_value=agent)

            await create_agent_use_case(
                name=agent.name,
                description=agent.description or "Personal agent",
                capabilities=["chat", "memory"],
                config_data={"temperature": 0.7},
            )

            user_agents[user.id] = created_agent

            # Validate agent properties
            assert created_agent.name == f"Agent_{user.username}"
            assert user.username.lower() in created_agent.name.lower()

        # Verify each user has their own agent
        assert len(user_agents) == len(test_users)
        agent_names = [agent.name for agent in user_agents.values()]
        assert len(set(agent_names)) == len(agent_names)  # All names unique

    async def test_isolated_user_conversations(
        self,
        mock_chat_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test that user conversations are properly isolated."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        # Create agents for users
        user_agents = []
        for user in test_users:
            _ = Agent(
                name=f"Agent_{user.username}",
                description=f"Agent for {user.username}",
                config=AgentConfig(capabilities=[AgentCapability.CHAT]),
                status=AgentStatus.ACTIVE,
            )
            user_agents.append(agent)

        # Simulate concurrent conversations
        conversation_tasks = []
        expected_responses = []

        for i, (user, agent) in enumerate(zip(test_users, user_agents, strict=False)):
            message_content = f"Hello from {user.full_name}, this is my private message #{i + 1}"

            # Mock unique response for each user
            response = ChatMessage(
                id=f"response_{user.username}_{i + 1}",
                content=f"Hello {user.full_name}! I'm your personal assistant responding to: {message_content}",
                sender_type="agent",
                sender_id=str(agent.id),
                agent_id=str(agent.id),
                timestamp=datetime.now(UTC),
            )

            expected_responses.append((user.id, response))

            # Mock repository to return user-specific response
            mock_chat_repo.send_message = AsyncMock(return_value=response)

            task = send_message_result = send_message_use_case.execute(
                agent_id=str(agent.id),
                content=message_content,
                user_id=user.id,
            )
            conversation_tasks.append(task)

        # Execute all conversations concurrently
        results = await asyncio.gather(*conversation_tasks)

        # Validate isolation and uniqueness
        assert len(results) == len(test_users)

        for i, (result, (user_id, expected)) in enumerate(
            zip(results, expected_responses, strict=False)
        ):
            assert isinstance(result, ChatMessage)
            if result.content and test_users[i].full_name:
                assert test_users[i].full_name in result.content
            assert f"#{i + 1}" in expected.content  # Verify unique message numbering

    async def test_user_specific_memory_storage(
        self,
        mock_memory_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test that each user's memories are stored separately."""

        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Create agents for users
        user_agents = []
        for user in test_users:
            _ = Agent(
                name=f"MemoryAgent_{user.username}",
                description=f"Memory agent for {user.username}",
                config=AgentConfig(capabilities=[AgentCapability.MEMORY]),
                status=AgentStatus.ACTIVE,
            )
            user_agents.append(agent)

        # Store user-specific memories
        stored_memories = {}

        for user, agent in zip(test_users, user_agents, strict=False):
            memory_content = (
                f"{user.full_name}'s personal knowledge about machine learning preferences"
            )

            memory = Memory(
                content=memory_content,
                type=MemoryType.EPISODIC,
                importance=MemoryImportance.MEDIUM,
                agent_id=agent.id,
                context={
                    "user_id": user.id,
                    "user_name": user.full_name,
                    "privacy": "private",
                },
                tags=[f"user_{user.username}", "personal", "preferences"],
            )

            mock_memory_repo.create = AsyncMock(return_value=memory)

            stored_memory = await store_memory_use_case(
                content=memory_content,
                memory_type="episodic",
                importance="medium",
                agent_id=agent.id,
                context=memory.context,
                tags=memory.tags,
            )

            stored_memories[user.id] = stored_memory

            # Validate user-specific memory
            assert user.full_name in stored_memory.content
            assert stored_memory.context["user_id"] == user.id
            assert f"user_{user.username}" in stored_memory.tags

        # Verify memory isolation
        assert len(stored_memories) == len(test_users)

        # Check that each memory is unique to its user
        for user_id, memory in stored_memories.items():
            _ = next(u for u in test_users if u.id == user_id)
            if memory.content and user.full_name:
                assert user.full_name in memory.content
            assert memory.context["user_id"] == user_id

    async def test_multi_user_resource_sharing(
        self,
        mock_memory_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test controlled resource sharing between users."""

        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Create a shared agent (system agent)
        Agent(
            name="SystemAgent",
            description="Shared system knowledge agent",
            config=AgentConfig(capabilities=[AgentCapability.MEMORY]),
            status=AgentStatus.ACTIVE,
        )

        # Store shared knowledge that multiple users can access
        shared_memory_content = "General programming best practices for Python development"

        shared_memory = Memory(
            content=shared_memory_content,
            type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            agent_id=shared_agent.id,
            context={
                "shared": True,
                "access_level": "public",
                "domain": "programming",
            },
            tags=["python", "best_practices", "shared", "public"],
        )

        mock_memory_repo.create = AsyncMock(return_value=shared_memory)

        stored_shared_memory = await store_memory_use_case(
            content=shared_memory_content,
            memory_type="semantic",
            importance="high",
            agent_id=shared_agent.id,
            context=shared_memory.context,
            tags=shared_memory.tags,
        )

        # Simulate multiple users accessing shared resource
        access_results = []

        for user in test_users:
            # Mock repository returning shared memory for all users
            mock_memory_repo.get_shared_knowledge = AsyncMock(return_value=[stored_shared_memory])

            shared_knowledge = await mock_memory_repo.get_shared_knowledge(
                domain="programming",
                user_id=user.id,
            )

            access_results.append((user.id, shared_knowledge))

        # Validate shared access
        assert len(access_results) == len(test_users)

        for user_id, knowledge in access_results:
            assert len(knowledge) == 1
            assert knowledge[0].content == shared_memory_content
            assert knowledge[0].context["shared"] is True
            assert "public" in knowledge[0].tags

    async def test_user_permission_boundaries(
        self,
        mock_user_repo: Mock,
        mock_memory_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test that users cannot access each other's private data."""

        # Setup: Create private memories for each user
        alice, bob, _ = test_users

        # Alice's private memory
        Agent(
            name="AliceAgent",
            description="Alice's private agent",
            config=AgentConfig(capabilities=[AgentCapability.MEMORY]),
            status=AgentStatus.ACTIVE,
        )

        alice_private_memory = Memory(
            content="Alice's confidential business strategy notes",
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.HIGH,
            agent_id=alice_agent.id,
            context={
                "user_id": alice.id,
                "privacy": "private",
                "access_level": "owner_only",
            },
            tags=["alice", "private", "confidential"],
        )

        # Simulate Bob trying to access Alice's private memory
        mock_memory_repo.get_user_memories = AsyncMock(
            side_effect=lambda user_id, **kwargs: [alice_private_memory]
            if user_id == alice.id
            else []
        )

        # Bob should not see Alice's private memories
        bob_accessible_memories = await mock_memory_repo.get_user_memories(
            user_id=bob.id,
            include_private=True,
        )

        alice_accessible_memories = await mock_memory_repo.get_user_memories(
            user_id=alice.id,
            include_private=True,
        )

        # Validate access control
        assert len(bob_accessible_memories) == 0  # Bob sees nothing
        assert len(alice_accessible_memories) == 1  # Alice sees her own memory
        assert alice_accessible_memories[0].content == alice_private_memory.content

    async def test_concurrent_multi_user_operations(
        self,
        mock_user_repo: Mock,
        mock_agent_repo: Mock,
        mock_chat_repo: Mock,
        mock_memory_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test concurrent operations across multiple users."""

        # Setup use cases
        auth_use_case = AuthenticateUser(mock_user_repo)
        create_agent_use_case = CreateAgent(mock_agent_repo)
        send_message_use_case = SendMessageUseCase(mock_chat_repo)
        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Create complex concurrent workflow
        async def user_workflow(user: User, user_index: int) -> dict[str, Any]:
            """Complete workflow for a single user."""

            # Step 1: Authenticate
            login_request = LoginRequest(email=user.email, password=os.getenv("PASSWORD"))

            mock_user_repo.get_by_email = AsyncMock(return_value=user)

    from unittest.mock import patch

            with (
                patch("bcrypt.checkpw", return_value=True),
                patch("jwt.encode", return_value=f"token_{user.username}"),
            ):
                _ = await auth_use_case(login_request)

            # Step 2: Create agent
            _ = Agent(
                name=f"ConcurrentAgent_{user.username}",
                description=f"Agent for concurrent testing - {user.username}",
                config=AgentConfig(capabilities=[AgentCapability.CHAT, AgentCapability.MEMORY]),
                status=AgentStatus.ACTIVE,
            )

            mock_agent_repo.create = AsyncMock(return_value=agent)

            await create_agent_use_case(
                name=agent.name,
                description=agent.description or "Concurrent test agent",
                capabilities=["chat", "memory"],
                config_data={"temperature": 0.5},
            )

            # Step 3: Send message
            message_content = f"Concurrent message #{user_index + 1} from {user.full_name}"

            response = ChatMessage(
                id=f"concurrent_response_{user.username}",
                content=f"Response to {user.full_name}: {message_content}",
                sender_type="agent",
                sender_id=str(created_agent.id),
                agent_id=str(created_agent.id),
                timestamp=datetime.now(UTC),
            )

            mock_chat_repo.send_message = AsyncMock(return_value=response)

            _ = send_message_result = await send_message_result = send_message_use_case.execute(
                agent_id=str(created_agent.id),
                content=message_content,
                user_id=user.id,
            )

            # Step 4: Store memory
            memory_content = f"Concurrent operation memory for {user.full_name}"

            memory = Memory(
                content=memory_content,
                type=MemoryType.EPISODIC,
                importance=MemoryImportance.MEDIUM,
                agent_id=created_agent.id,
                context={"user_id": user.id, "concurrent_test": True},
                tags=[f"user_{user.username}", "concurrent", "test"],
            )

            mock_memory_repo.create = AsyncMock(return_value=memory)

            _ = await store_memory_use_case(
                content=memory_content,
                memory_type="episodic",
                importance="medium",
                agent_id=created_agent.id,
                context=memory.context,
                tags=memory.tags,
            )

            return {
                "user": user,
                "auth": auth_result,
                "agent": created_agent,
                "chat": chat_result,
                "memory": memory_result,
            }

        # Execute workflows for all users concurrently
        workflow_tasks = [user_workflow(user, i) for i, user in enumerate(test_users)]

        workflow_results = await asyncio.gather(*workflow_tasks)

        # Validate all workflows completed successfully
        assert len(workflow_results) == len(test_users)

        for i, result in enumerate(workflow_results):
            _ = test_users[i]

            # Validate each workflow step
            assert result["auth"].access_token is not None
            assert result["agent"].name == f"ConcurrentAgent_{user.username}"
            assert user.full_name in result["chat"].content
            assert result["memory"].context["user_id"] == user.id
            assert f"user_{user.username}" in result["memory"].tags

        # Verify isolation - each user got unique results
        agent_names = [result["agent"].name for result in workflow_results]
        assert len(set(agent_names)) == len(agent_names)

        chat_contents = [result["chat"].content for result in workflow_results]
        assert len(set(chat_contents)) == len(chat_contents)

    async def test_user_session_cleanup(
        self,
        mock_user_repo: Mock,
        test_users: list[User],
    ) -> None:
        """Test proper cleanup of user sessions and resources."""

        # Simulate user sessions
        active_sessions = {}

        for user in test_users:
            session_data = {
                "user_id": user.id,
                "token": f"session_token_{user.username}",
                "created_at": datetime.now(UTC),
                "last_activity": datetime.now(UTC),
                "resources": {
                    "agents": [f"agent_{user.username}"],
                    "active_chats": [f"chat_{user.username}"],
                    "memory_cache": f"cache_{user.username}",
                },
            }
            active_sessions[user.id] = session_data

        # Simulate session cleanup
        mock_user_repo.cleanup_user__ = AsyncMock(
            side_effect=lambda user_id: active_sessions.pop(user_id, None)
        )

        # Clean up sessions for users
        cleanup_results = []
        for user in test_users:
            await mock_user_repo.cleanup_user_session(user.id)
            cleanup_results.append(cleanup_result)

        # Validate cleanup
        assert len(cleanup_results) == len(test_users)
        assert all(result is not None for result in cleanup_results)
        assert len(active_sessions) == 0  # All sessions cleaned up

        # Verify each cleaned session had correct data
        for i, result in enumerate(cleanup_results):
            _ = test_users[i]
            assert result["user_id"] == user.id
            assert f"agent_{user.username}" in result["resources"]["agents"]
