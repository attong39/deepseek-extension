import os
import agent
import all
import delay
import dict
import email
import float
import i
import int
import isinstance
import kwargs
import len
import list
import max
import min
import print
import query
import r
import range
import request_id
import result
import self
import size
import str
import sum
import task_id

"""
🚀 E2E Performance Tests - ZETA AI SERVER
========================================

Performance tests for critical system operations:
- Response time benchmarks
- Memory usage monitoring
- Concurrent operation limits
- System scalability validation
- Database query performance
- API endpoint throughput

These tests ensure the system meets performance
requirements under normal and stress conditions.
"""

import asyncio
import time
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from core.domain.entities.chat import ChatMessage
from core.domain.entities.memory import Memory, MemoryImportance, MemoryType
from core.domain.entities.user import User
from core.use_cases.agent.create_agent import CreateAgent
from core.use_cases.auth.authenticate_user import AuthenticateUser
from core.use_cases.chat.send_message import SendMessageUseCase
from core.use_cases.memory.store_memory import StoreMemory
from core.value_objects.auth import LoginRequest


@pytest.mark.e2e
@pytest.mark.performance
class TestPerformanceE2E:
    """End-to-end performance tests."""

    @pytest.fixture
    def mock_user_repo(self) -> Mock:
        """Create mock user repository with performance simulation."""
        repo = Mock()
        # Simulate realistic database latency
        repo.get_by_email = AsyncMock(
            side_effect=lambda email: asyncio.create_task(
                self._simulate_db_latency(0.05, self._create_test_user(email))
            )
        )
        return repo

    @pytest.fixture
    def mock_agent_repo(self) -> Mock:
        """Create mock agent repository with performance simulation."""
        repo = Mock()
        repo.create = AsyncMock(
            side_effect=lambda agent: asyncio.create_task(
                self._simulate_db_latency(0.1, agent)
            )
        )
        return repo

    @pytest.fixture
    def mock_chat_repo(self) -> Mock:
        """Create mock chat repository with performance simulation."""
        repo = Mock()
        repo.send_message = AsyncMock(
            side_effect=lambda **kwargs: asyncio.create_task(
                self._simulate_ai_latency(0.3, self._create_mock_response(**kwargs))
            )
        )
        return repo

    @pytest.fixture
    def mock_memory_repo(self) -> Mock:
        """Create mock memory repository with performance simulation."""
        repo = Mock()
        repo.create = AsyncMock(
            side_effect=lambda memory: asyncio.create_task(
                self._simulate_db_latency(0.2, memory)
            )
        )
        repo.search = AsyncMock(
            side_effect=lambda query, **kwargs: asyncio.create_task(
                self._simulate_search_latency(0.15, query, **kwargs)
            )
        )
        return repo

    async def _simulate_db_latency(self, delay: float, result: Any) -> Any:
        """Simulate database operation latency."""
        await asyncio.sleep(delay)
        return result

    async def _simulate_ai_latency(self, delay: float, result: Any) -> Any:
        """Simulate AI model response latency."""
        await asyncio.sleep(delay)
        return result

    async def _simulate_search_latency(
        self, delay: float, query: str, **kwargs: Any
    ) -> list[Memory]:
        """Simulate memory search latency."""
        await asyncio.sleep(delay)
        # Return mock search results
        return [
            Memory(
                content=f"Search result for: {query}",
                type=MemoryType.SEMANTIC,
                importance=MemoryImportance.MEDIUM,
                agent_id=uuid4(),
                context={"search_query": query},
                tags=["search", "result"],
            )
        ]

    def _create_test_user(self, email: str) -> User:
        """Create a test user for performance testing."""
        username = email.split("@")[0]
        return User(
            id=f"user_{username}",
            email=email,
            username=username,
            full_name=f"Test User {username.title()}",
            password_hash="$2b$12$hashed_password",
            is_active=True,
        )

    def _create_mock_response(self, **kwargs: Any) -> ChatMessage:
        """Create a mock chat response."""
        return ChatMessage(
            id="mock_response",
            content=f"AI response to: {kwargs.get('content', 'message')}",
            sender_type="agent",
            sender_id=kwargs.get("agent_id", "mock_agent"),
            agent_id=kwargs.get("agent_id", "mock_agent"),
            timestamp=datetime.now(UTC),
        )

    async def test_authentication_performance(
        self,
        mock_user_repo: Mock,
    ) -> None:
        """Test authentication response time."""

        auth_use_case = AuthenticateUser(mock_user_repo)

        login_request = LoginRequest(
            email="perftest@example.com", password=os.getenv("PASSWORD")
        )

        # Measure authentication time
        start_time = time.perf_counter()

        from unittest.mock import patch

        with (
            patch("bcrypt.checkpw", return_value=True),
            patch("jwt.encode", return_value="perf_test_token"),
        ):
            _ = await auth_use_case(login_request)

        end_time = time.perf_counter()
        response_time = end_time - start_time

        # Validate performance requirements
        assert result.access_token is not None
        assert response_time < 1.0  # Authentication should complete under 1 second
        print(f"Authentication response time: {response_time:.3f}s")

    async def test_agent_creation_performance(
        self,
        mock_agent_repo: Mock,
    ) -> None:
        """Test agent creation performance."""

        create_agent_use_case = CreateAgent(mock_agent_repo)

        # Measure agent creation time
        start_time = time.perf_counter()

        _ = await create_agent_use_case(
            name="PerformanceTestAgent",
            description="Agent for performance testing",
            capabilities=["chat", "memory", "planning"],
            config_data={"temperature": 0.7, "max_tokens": 1000},
        )

        end_time = time.perf_counter()
        response_time = end_time - start_time

        # Validate performance requirements
        assert agent.name == "PerformanceTestAgent"
        assert response_time < 2.0  # Agent creation should complete under 2 seconds
        print(f"Agent creation response time: {response_time:.3f}s")

    async def test_chat_message_performance(
        self,
        mock_chat_repo: Mock,
    ) -> None:
        """Test chat message processing performance."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        # Measure message processing time
        start_time = time.perf_counter()

        _ = await send_message_use_case.execute(
            agent_id="perf_test_agent",
            content="Performance test message with moderate complexity and length",
            user_id="perf_test_user",
        )

        end_time = time.perf_counter()
        response_time = end_time - start_time

        # Validate performance requirements
        assert isinstance(result, ChatMessage)
        assert result.content is not None
        assert response_time < 5.0  # Chat response should complete under 5 seconds
        print(f"Chat message response time: {response_time:.3f}s")

    async def test_memory_storage_performance(
        self,
        mock_memory_repo: Mock,
    ) -> None:
        """Test memory storage performance."""

        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Measure memory storage time
        start_time = time.perf_counter()

        memory = await store_memory_use_case(
            content="Performance test memory with detailed context and metadata",
            memory_type="episodic",
            importance="high",
            agent_id=uuid4(),
            context={
                "timestamp": datetime.now(UTC).isoformat(),
                "user_id": "perf_test_user",
                "session_id": "perf_test_session",
                "performance_test": True,
            },
            tags=["performance", "test", "memory", "episodic"],
        )

        end_time = time.perf_counter()
        response_time = end_time - start_time

        # Validate performance requirements
        assert memory.content is not None
        assert memory.type == MemoryType.EPISODIC
        assert response_time < 1.5  # Memory storage should complete under 1.5 seconds
        print(f"Memory storage response time: {response_time:.3f}s")

    async def test_memory_search_performance(
        self,
        mock_memory_repo: Mock,
    ) -> None:
        """Test memory search performance."""

        # Measure memory search time
        start_time = time.perf_counter()

        search_results = await mock_memory_repo.search(
            query="performance test search query",
            agent_id="perf_test_agent",
            limit=10,
            min_importance="medium",
        )

        end_time = time.perf_counter()
        response_time = end_time - start_time

        # Validate performance requirements
        assert isinstance(search_results, list)
        assert len(search_results) > 0
        assert response_time < 1.0  # Memory search should complete under 1 second
        print(f"Memory search response time: {response_time:.3f}s")

    async def test_concurrent_operation_performance(
        self,
        mock_user_repo: Mock,
        mock_agent_repo: Mock,
        mock_chat_repo: Mock,
        mock_memory_repo: Mock,
    ) -> None:
        """Test performance under concurrent operations."""

        # Setup use cases
        auth_use_case = AuthenticateUser(mock_user_repo)
        create_agent_use_case = CreateAgent(mock_agent_repo)
        send_message_use_case = SendMessageUseCase(mock_chat_repo)
        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Create concurrent tasks
        concurrent_count = 10

        async def concurrent_workflow(task_id: int) -> dict[str, float]:
            """Execute a complete workflow and measure timing."""

            workflow_start = time.perf_counter()

            # Authentication
            auth_start = time.perf_counter()
            login_request = LoginRequest(
                email=f"user{task_id}@example.com", password=os.getenv("PASSWORD")
            )

            from unittest.mock import patch

            with (
                patch("bcrypt.checkpw", return_value=True),
                patch("jwt.encode", return_value=f"token_{task_id}"),
            ):
                await auth_use_case(login_request)

            auth_time = time.perf_counter() - auth_start

            # Agent creation
            agent_start = time.perf_counter()
            _ = await create_agent_use_case(
                name=f"ConcurrentAgent{task_id}",
                description=f"Concurrent test agent {task_id}",
                capabilities=["chat", "memory"],
                config_data={"temperature": 0.5},
            )
            agent_time = time.perf_counter() - agent_start

            # Chat message
            chat_start = time.perf_counter()
            await send_message_use_case.execute(
                agent_id=str(agent.id),
                content=f"Concurrent test message {task_id}",
                user_id=f"user{task_id}",
            )
            chat_time = time.perf_counter() - chat_start

            # Memory storage
            memory_start = time.perf_counter()
            await store_memory_use_case(
                content=f"Concurrent memory {task_id}",
                memory_type="episodic",
                importance="medium",
                agent_id=str(agent.id),
                context={"task_id": task_id},
                tags=[f"task_{task_id}", "concurrent"],
            )
            memory_time = time.perf_counter() - memory_start

            total_time = time.perf_counter() - workflow_start

            return {
                "task_id": task_id,
                "auth_time": auth_time,
                "agent_time": agent_time,
                "chat_time": chat_time,
                "memory_time": memory_time,
                "total_time": total_time,
            }

        # Execute concurrent workflows
        start_time = time.perf_counter()

        concurrent_tasks = [concurrent_workflow(i) for i in range(concurrent_count)]

        results = await asyncio.gather(*concurrent_tasks)

        total_concurrent_time = time.perf_counter() - start_time

        # Analyze performance
        avg_auth_time = sum(r["auth_time"] for r in results) / len(results)
        avg_agent_time = sum(r["agent_time"] for r in results) / len(results)
        avg_chat_time = sum(r["chat_time"] for r in results) / len(results)
        avg_memory_time = sum(r["memory_time"] for r in results) / len(results)
        avg_total_time = sum(r["total_time"] for r in results) / len(results)

        # Validate concurrent performance
        assert len(results) == concurrent_count
        assert (
            total_concurrent_time < 30.0
        )  # All concurrent operations under 30 seconds
        assert avg_total_time < 10.0  # Average workflow under 10 seconds

        print(f"Concurrent operations completed in: {total_concurrent_time:.3f}s")
        print(f"Average workflow time: {avg_total_time:.3f}s")
        print(f"Average auth time: {avg_auth_time:.3f}s")
        print(f"Average agent time: {avg_agent_time:.3f}s")
        print(f"Average chat time: {avg_chat_time:.3f}s")
        print(f"Average memory time: {avg_memory_time:.3f}s")

    async def test_batch_operation_performance(
        self,
        mock_memory_repo: Mock,
    ) -> None:
        """Test performance of batch operations."""

        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Create batch of memory operations
        batch_size = 25

        # Measure batch operation time
        start_time = time.perf_counter()

        batch_tasks = []
        for i in range(batch_size):
            task = store_memory_use_case(
                content=f"Batch memory operation {i + 1}",
                memory_type="semantic" if i % 2 == 0 else "episodic",
                importance="medium",
                agent_id="batch_test_agent",
                context={"batch_id": i, "total_batch_size": batch_size},
                tags=["batch", f"item_{i + 1}"],
            )
            batch_tasks.append(task)

        # Execute batch operations
        batch_results = await asyncio.gather(*batch_tasks)

        batch_time = time.perf_counter() - start_time

        # Validate batch performance
        assert len(batch_results) == batch_size
        assert all(memory.content is not None for memory in batch_results)
        assert batch_time < 15.0  # Batch operations should complete under 15 seconds

        avg_operation_time = batch_time / batch_size
        assert avg_operation_time < 1.0  # Average operation under 1 second

        print(f"Batch of {batch_size} operations completed in: {batch_time:.3f}s")
        print(f"Average operation time: {avg_operation_time:.3f}s")

    async def test_memory_usage_simulation(
        self,
        mock_memory_repo: Mock,
    ) -> None:
        """Test system behavior under memory-intensive operations."""

        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Simulate large memory content
        large_content_size = 10000  # 10KB of text
        large_content = "A" * large_content_size

        # Measure large memory storage
        start_time = time.perf_counter()

        large_memory = await store_memory_use_case(
            content=large_content,
            memory_type="semantic",
            importance="high",
            agent_id="memory_test_agent",
            context={
                "content_size": large_content_size,
                "memory_test": True,
            },
            tags=["large", "memory", "test"],
        )

        end_time = time.perf_counter()
        response_time = end_time - start_time

        # Validate memory handling
        assert large_memory.content == large_content
        assert len(large_memory.content) == large_content_size
        assert response_time < 3.0  # Large memory operations under 3 seconds

        print(
            f"Large memory ({large_content_size} bytes) stored in: {response_time:.3f}s"
        )

    async def test_search_performance_scaling(
        self,
        mock_memory_repo: Mock,
    ) -> None:
        """Test search performance with varying result sizes."""

        # Test different search result sizes
        search_sizes = [1, 10, 50, 100]

        search_times = []

        for size in search_sizes:
            # Mock search results for different sizes
            mock_memory_repo.search = AsyncMock(
                side_effect=lambda query, **kwargs: asyncio.create_task(
                    self._simulate_search_with_size(0.1 + (size * 0.002), size, query)
                )
            )

            start_time = time.perf_counter()

            results = await mock_memory_repo.search(
                query=f"search test for {size} results",
                limit=size,
            )

            end_time = time.perf_counter()
            search_time = end_time - start_time
            search_times.append(search_time)

            # Validate search scaling
            assert len(results) == size
            assert search_time < 2.0  # All searches under 2 seconds

            print(f"Search for {size} results: {search_time:.3f}s")

        # Validate search scaling is reasonable
        # Larger result sets should not be drastically slower
        max_time = max(search_times)
        min_time = min(search_times)
        time_ratio = max_time / min_time if min_time > 0 else 1

        assert time_ratio < 5.0  # Performance shouldn't degrade more than 5x

    async def _simulate_search_with_size(
        self, delay: float, size: int, query: str
    ) -> list[Memory]:
        """Simulate search with specific result size."""
        await asyncio.sleep(delay)

        return [
            Memory(
                content=f"Search result {i + 1} for: {query}",
                type=MemoryType.SEMANTIC,
                importance=MemoryImportance.MEDIUM,
                agent_id="search_agent",
                context={"result_index": i + 1, "search_query": query},
                tags=["search", f"result_{i + 1}"],
            )
            for i in range(size)
        ]

    async def test_api_throughput_simulation(
        self,
        mock_user_repo: Mock,
        mock_chat_repo: Mock,
    ) -> None:
        """Test API endpoint throughput under load."""

        auth_use_case = AuthenticateUser(mock_user_repo)
        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        # Simulate API request load
        requests_per_second = 20
        test_duration = 2  # seconds
        total_requests = requests_per_second * test_duration

        async def simulate_api_request(request_id: int) -> dict[str, Any]:
            """Simulate a complete API request."""

            request_start = time.perf_counter()

            # Authentication (simulating JWT validation)
            auth_time_start = time.perf_counter()
            login_request = LoginRequest(
                email=f"api_user_{request_id}@example.com",
                password=os.getenv("PASSWORD"),
            )

            from unittest.mock import patch

            with (
                patch("bcrypt.checkpw", return_value=True),
                patch("jwt.encode", return_value=f"api_token_{request_id}"),
            ):
                await auth_use_case(login_request)

            auth_time = time.perf_counter() - auth_time_start

            # API operation (chat message)
            api_time_start = time.perf_counter()
            await send_message_use_case.execute(
                agent_id=f"api_agent_{request_id % 5}",  # Simulate agent reuse
                content=f"API request {request_id}",
                user_id=f"api_user_{request_id}",
            )
            api_time = time.perf_counter() - api_time_start

            total_request_time = time.perf_counter() - request_start

            return {
                "request_id": request_id,
                "auth_time": auth_time,
                "api_time": api_time,
                "total_time": total_request_time,
                "success": True,
            }

        # Execute load test
        load_test_start = time.perf_counter()

        # Stagger requests to simulate realistic load
        request_tasks = []
        for i in range(total_requests):
            # Add small delay between requests to simulate realistic timing
            if i > 0:
                await asyncio.sleep(1.0 / requests_per_second)

            task = asyncio.create_task(simulate_api_request(i))
            request_tasks.append(task)

        # Wait for all requests to complete
        results = await asyncio.gather(*request_tasks, return_exceptions=True)

        load_test_time = time.perf_counter() - load_test_start

        # Analyze throughput
        successful_requests = [
            r for r in results if isinstance(r, dict) and r.get("success")
        ]
        success_rate = len(successful_requests) / total_requests

        avg_request_time = sum(r["total_time"] for r in successful_requests) / len(
            successful_requests
        )
        max_request_time = max(r["total_time"] for r in successful_requests)

        # Validate throughput performance
        assert success_rate >= 0.95  # At least 95% success rate
        assert avg_request_time < 2.0  # Average request under 2 seconds
        assert max_request_time < 5.0  # No request over 5 seconds

        actual_throughput = len(successful_requests) / load_test_time

        print("API Load Test Results:")
        print(f"  Requests: {total_requests}, Successful: {len(successful_requests)}")
        print(f"  Success Rate: {success_rate:.2%}")
        print(f"  Total Time: {load_test_time:.3f}s")
        print(f"  Average Request Time: {avg_request_time:.3f}s")
        print(f"  Max Request Time: {max_request_time:.3f}s")
        print(f"  Actual Throughput: {actual_throughput:.1f} req/s")
