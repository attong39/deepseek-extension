import os
import Exception
import TimeoutError
import agent
import auth_result
import base_delay
import chat_result
import dict
import e
import email
import float
import hasattr
import i
import int
import isinstance
import kwargs
import len
import max
import mem_id
import memory_id
import memory_result
import msg_id
import op_id
import print
import r
import range
import request_id
import result
import self
import set
import str
import sum
import user
import workflow_id

"""
💥 Stress Tests - ZETA AI SERVER
===============================

Stress tests for system resilience under extreme conditions:
- High-load scenarios and resource exhaustion
- System recovery and graceful degradation
- Memory leak detection and cleanup
- Error handling under pressure
- Database connection pooling limits
- Concurrent user limit testing

These tests validate system stability and recovery
capabilities under extreme stress conditions.
"""

import asyncio
import time
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from core.domain.entities.agent import Agent
from core.domain.entities.chat import ChatMessage
from core.domain.entities.user import User
from core.domain.value_objects.auth import LoginRequest
from core.use_cases.agent.create_agent import CreateAgent
from core.use_cases.auth.authenticate_user import AuthenticateUser
from core.use_cases.chat.send_message import SendMessageUseCase
from core.use_cases.memory.store_memory import StoreMemory


@pytest.mark.stress
@pytest.mark.asyncio
class TestStressConditions:
    """Stress tests for system resilience."""

    @pytest.fixture
    def mock_user_repo(self) -> Mock:
        """Create mock user repository with stress simulation."""
        repo = Mock()
        repo.get_by_email = AsyncMock(
            side_effect=lambda email: asyncio.create_task(
                self._simulate_stressed_db_operation(0.1, self._create_test_user(email))
            )
        )
        return repo

    @pytest.fixture
    def mock_agent_repo(self) -> Mock:
        """Create mock agent repository with stress simulation."""
        repo = Mock()
        repo.create = AsyncMock(
            side_effect=lambda agent: asyncio.create_task(
                self._simulate_stressed_db_operation(0.2, agent)
            )
        )
        return repo

    @pytest.fixture
    def mock_chat_repo(self) -> Mock:
        """Create mock chat repository with stress simulation."""
        repo = Mock()
        repo.send_message = AsyncMock(
            side_effect=lambda **kwargs: asyncio.create_task(
                self._simulate_stressed_ai_operation(
                    0.5, self._create_mock_response(**kwargs)
                )
            )
        )
        return repo

    @pytest.fixture
    def mock_memory_repo(self) -> Mock:
        """Create mock memory repository with stress simulation."""
        repo = Mock()
        repo.create = AsyncMock(
            side_effect=lambda memory: asyncio.create_task(
                self._simulate_stressed_db_operation(0.3, memory)
            )
        )
        return repo

    async def _simulate_stressed_db_operation(
        self, base_delay: float, result: Any
    ) -> Any:
        """Simulate database operation under stress with variable latency."""
        # Add random stress-induced delays
        import random

        stress_factor = random.uniform(1.0, 3.0)
        actual_delay = base_delay * stress_factor
        await asyncio.sleep(actual_delay)
        return result

    async def _simulate_stressed_ai_operation(
        self, base_delay: float, result: Any
    ) -> Any:
        """Simulate AI operation under stress with potential timeouts."""
        import random

        # Sometimes simulate timeout conditions
        if random.random() < 0.05:  # 5% timeout rate
            await asyncio.sleep(base_delay * 10)  # Very slow response
        else:
            stress_factor = random.uniform(1.0, 4.0)
            actual_delay = base_delay * stress_factor
            await asyncio.sleep(actual_delay)
        return result

    def _create_test_user(self, email: str) -> User:
        """Create a test user for stress testing."""
        username = email.split("@")[0]
        return User(
            id=f"stress_user_{username}",
            email=email,
            username=username,
            full_name=f"Stress Test User {username.title()}",
            password_hash="$2b$12$hashed_password",
            is_active=True,
        )

    def _create_mock_response(self, **kwargs: Any) -> ChatMessage:
        """Create a mock chat response."""
        return ChatMessage(
            id="stress_response",
            content=f"Stress test response to: {kwargs.get('content', 'message')}",
            sender_type="agent",
            sender_id=kwargs.get("agent_id", "stress_agent"),
            agent_id=kwargs.get("agent_id", "stress_agent"),
            timestamp=datetime.now(UTC),
        )

    async def test_high_concurrent_user_load(
        self,
        mock_user_repo: Mock,
        mock_agent_repo: Mock,
        mock_chat_repo: Mock,
        mock_memory_repo: Mock,
    ) -> None:
        """Test system under high concurrent user load."""

        # Setup use cases
        auth_use_case = AuthenticateUser(mock_user_repo)
        create_agent_use_case = CreateAgent(mock_agent_repo)
        send_message_use_case = SendMessageUseCase(mock_chat_repo)
        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Stress test with high concurrent users
        concurrent_users = 100

        async def stress_user_workflow(user_id: int) -> dict[str, Any]:
            """Execute a complete user workflow under stress."""

            try:
                # Authentication
                login_request = LoginRequest(
                    email=f"stress_user_{user_id}@example.com",
                    password=os.getenv("PASSWORD"),
                )

                from unittest.mock import patch

                with (
                    patch("bcrypt.checkpw", return_value=True),
                    patch("jwt.encode", return_value=f"stress_token_{user_id}"),
                ):
                    _ = await asyncio.wait_for(
                        auth_use_case(login_request), timeout=10.0
                    )

                # Agent creation under stress
                _ = await asyncio.wait_for(
                    create_agent_use_case(
                        name=f"StressAgent{user_id}",
                        description=f"Stress test agent {user_id}",
                        capabilities=["chat", "memory"],
                        config_data={"temperature": 0.5},
                    ),
                    timeout=15.0,
                )

                # Multiple chat operations per user (stress factor)
                chat_results = []
                for msg_id in range(3):  # 3 messages per user
                    _ = await asyncio.wait_for(
                        send_message_use_case.execute(
                            agent_id=str(agent.id),
                            content=f"Stress message {msg_id} from user {user_id}",
                            user_id=f"stress_user_{user_id}",
                        ),
                        timeout=20.0,
                    )
                    chat_results.append(chat_result)

                # Memory operations under stress
                memory_results = []
                for mem_id in range(2):  # 2 memories per user
                    _ = await asyncio.wait_for(
                        store_memory_use_case(
                            content=f"Stress memory {mem_id} for user {user_id}",
                            memory_type="episodic",
                            importance="medium",
                            agent_id=agent.id,
                            context={"user_id": user_id, "stress_test": True},
                            tags=[f"stress_{user_id}", f"memory_{mem_id}"],
                        ),
                        timeout=10.0,
                    )
                    memory_results.append(memory_result)

                return {
                    "user_id": user_id,
                    "success": True,
                    "auth": auth_result,
                    "agent": agent,
                    "chat_count": len(chat_results),
                    "memory_count": len(memory_results),
                    "error": None,
                }

            except TimeoutError:
                return {
                    "user_id": user_id,
                    "success": False,
                    "error": "timeout",
                }
            except Exception as e:
                return {
                    "user_id": user_id,
                    "success": False,
                    "error": str(e),
                }

        # Execute stress test
        stress_start = time.perf_counter()

        stress_tasks = [stress_user_workflow(i) for i in range(concurrent_users)]

        results = await asyncio.gather(*stress_tasks, return_exceptions=True)

        stress_duration = time.perf_counter() - stress_start

        # Analyze stress test results
        successful_workflows = [
            r for r in results if isinstance(r, dict) and r.get("success")
        ]
        timeout_errors = [
            r for r in results if isinstance(r, dict) and r.get("error") == "timeout"
        ]
        other_errors = [
            r
            for r in results
            if isinstance(r, dict) and r.get("error") and r.get("error") != "timeout"
        ]

        success_rate = len(successful_workflows) / concurrent_users
        timeout_rate = len(timeout_errors) / concurrent_users
        error_rate = len(other_errors) / concurrent_users

        # Validate stress test results
        assert success_rate >= 0.80  # At least 80% success under stress
        assert timeout_rate <= 0.15  # No more than 15% timeouts
        assert error_rate <= 0.10  # No more than 10% other errors

        print(f"High Load Stress Test (n={concurrent_users}):")
        print(f"  Duration: {stress_duration:.2f}s")
        print(f"  Success Rate: {success_rate:.2%}")
        print(f"  Timeout Rate: {timeout_rate:.2%}")
        print(f"  Error Rate: {error_rate:.2%}")

    async def test_memory_exhaustion_simulation(
        self,
        mock_memory_repo: Mock,
    ) -> None:
        """Test system behavior under simulated memory pressure."""

        store_memory_use_case = StoreMemory(mock_memory_repo)

        # Simulate memory exhaustion with large objects
        large_memory_operations = 50
        large_content_size = 50000  # 50KB per memory

        async def create_large_memory(memory_id: int) -> dict[str, Any]:
            """Create a large memory object."""

            try:
                large_content = "X" * large_content_size

                start_time = time.perf_counter()

                memory = await asyncio.wait_for(
                    store_memory_use_case(
                        content=large_content,
                        memory_type="semantic",
                        importance="high",
                        agent_id=uuid4(),
                        context={
                            "memory_id": memory_id,
                            "size": large_content_size,
                            "stress_test": True,
                        },
                        tags=["large", "stress", f"memory_{memory_id}"],
                    ),
                    timeout=30.0,
                )

                operation_time = time.perf_counter() - start_time

                return {
                    "memory_id": memory_id,
                    "success": True,
                    "operation_time": operation_time,
                    "content_size": len(memory.content) if memory.content else 0,
                }

            except TimeoutError:
                return {
                    "memory_id": memory_id,
                    "success": False,
                    "error": "timeout",
                }
            except Exception as e:
                return {
                    "memory_id": memory_id,
                    "success": False,
                    "error": str(e),
                }

        # Execute memory stress test
        memory_stress_start = time.perf_counter()

        memory_tasks = [create_large_memory(i) for i in range(large_memory_operations)]

        memory_results = await asyncio.gather(*memory_tasks)

        memory_stress_duration = time.perf_counter() - memory_stress_start

        # Analyze memory stress results
        successful_operations = [r for r in memory_results if r.get("success")]
        [r for r in memory_results if not r.get("success")]

        success_rate = len(successful_operations) / large_memory_operations
        avg_operation_time = (
            sum(r["operation_time"] for r in successful_operations)
            / len(successful_operations)
            if successful_operations
            else 0
        )
        total_memory_processed = sum(r["content_size"] for r in successful_operations)

        # Validate memory stress test
        assert success_rate >= 0.85  # At least 85% success under memory pressure
        assert avg_operation_time < 10.0  # Average operation under 10 seconds

        print("Memory Exhaustion Stress Test:")
        print(f"  Operations: {large_memory_operations}")
        print(f"  Duration: {memory_stress_duration:.2f}s")
        print(f"  Success Rate: {success_rate:.2%}")
        print(f"  Average Operation Time: {avg_operation_time:.3f}s")
        print(
            f"  Total Memory Processed: {total_memory_processed / 1024 / 1024:.1f} MB"
        )

    async def test_rapid_fire_requests(
        self,
        mock_chat_repo: Mock,
    ) -> None:
        """Test system under rapid-fire request conditions."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        # Rapid-fire configuration
        burst_count = 200

        async def rapid_request(request_id: int) -> dict[str, Any]:
            """Execute a rapid-fire request."""

            try:
                start_time = time.perf_counter()

                await asyncio.wait_for(
                    send_message_use_case.execute(
                        agent_id=str(uuid4()),
                        content=f"Rapid request #{request_id}",
                        user_id=f"rapid_user_{request_id % 10}",  # Simulate 10 concurrent users
                    ),
                    timeout=15.0,
                )

                response_time = time.perf_counter() - start_time

                return {
                    "request_id": request_id,
                    "success": True,
                    "response_time": response_time,
                }

            except TimeoutError:
                return {
                    "request_id": request_id,
                    "success": False,
                    "error": "timeout",
                }
            except Exception as e:
                return {
                    "request_id": request_id,
                    "success": False,
                    "error": str(e),
                }

        # Execute rapid-fire test
        rapid_start = time.perf_counter()

        # Create requests with minimal delay between them
        rapid_tasks = []
        for i in range(burst_count):
            task = asyncio.create_task(rapid_request(i))
            rapid_tasks.append(task)

            # Minimal stagger to create burst effect
            if i % 20 == 0:  # Small pause every 20 requests
                await asyncio.sleep(0.01)

        rapid_results = await asyncio.gather(*rapid_tasks)

        rapid_duration = time.perf_counter() - rapid_start

        # Analyze rapid-fire results
        successful_requests = [r for r in rapid_results if r.get("success")]
        [r for r in rapid_results if not r.get("success")]

        success_rate = len(successful_requests) / burst_count
        avg_response_time = (
            sum(r["response_time"] for r in successful_requests)
            / len(successful_requests)
            if successful_requests
            else 0
        )
        max_response_time = max(
            (r["response_time"] for r in successful_requests), default=0
        )

        actual_throughput = len(successful_requests) / rapid_duration

        # Validate rapid-fire test
        assert success_rate >= 0.90  # At least 90% success under rapid-fire
        assert avg_response_time < 3.0  # Average response under 3 seconds
        assert max_response_time < 20.0  # No response over 20 seconds

        print("Rapid-Fire Stress Test:")
        print(f"  Requests: {burst_count} in {rapid_duration:.2f}s")
        print(f"  Success Rate: {success_rate:.2%}")
        print(f"  Throughput: {actual_throughput:.1f} req/s")
        print(f"  Avg Response Time: {avg_response_time:.3f}s")
        print(f"  Max Response Time: {max_response_time:.3f}s")

    async def test_error_cascade_resilience(
        self,
        mock_user_repo: Mock,
        mock_agent_repo: Mock,
        mock_chat_repo: Mock,
    ) -> None:
        """Test system resilience to cascading errors."""

        auth_use_case = AuthenticateUser(mock_user_repo)
        create_agent_use_case = CreateAgent(mock_agent_repo)
        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        # Configure repositories to simulate intermittent failures
        failure_rate = 0.3  # 30% failure rate

        def failing_auth_side_effect(email: str) -> Any:
            import random

            if random.random() < failure_rate:
                raise Exception("Simulated auth service failure")
            return self._create_test_user(email)

        def failing_agent_side_effect(agent: Agent) -> Any:
            import random

            if random.random() < failure_rate:
                raise Exception("Simulated agent creation failure")
            return agent

        def failing_chat_side_effect(**kwargs: Any) -> Any:
            import random

            if random.random() < failure_rate:
                raise Exception("Simulated chat service failure")
            return self._create_mock_response(**kwargs)

        mock_user_repo.get_by_email = AsyncMock(side_effect=failing_auth_side_effect)
        mock_agent_repo.create = AsyncMock(side_effect=failing_agent_side_effect)
        mock_chat_repo.send_message = AsyncMock(side_effect=failing_chat_side_effect)

        # Test error resilience
        cascade_operations = 50

        async def resilience_workflow(workflow_id: int) -> dict[str, Any]:
            """Execute workflow with error handling."""

            errors = []
            partial_success = {}

            try:
                # Step 1: Authentication
                login_request = LoginRequest(
                    email=f"resilience_user_{workflow_id}@example.com",
                    password=os.getenv("PASSWORD"),
                )

                from unittest.mock import patch

                with (
                    patch("bcrypt.checkpw", return_value=True),
                    patch("jwt.encode", return_value=f"resilience_token_{workflow_id}"),
                ):
                    await auth_use_case(login_request)
                    partial_success["auth"] = True

            except Exception as e:
                errors.append(f"auth_error: {e}")

            try:
                # Step 2: Agent Creation
                if "auth" in partial_success:
                    await create_agent_use_case(
                        name=f"ResilienceAgent{workflow_id}",
                        description=f"Resilience test agent {workflow_id}",
                        capabilities=["chat"],
                        config_data={"temperature": 0.5},
                    )
                    partial_success["agent"] = True

            except Exception as e:
                errors.append(f"agent_error: {e}")

            try:
                # Step 3: Chat Operation
                if "agent" in partial_success:
                    await send_message_use_case.execute(
                        agent_id=str(uuid4()),
                        content=f"Resilience test message {workflow_id}",
                        user_id=f"resilience_user_{workflow_id}",
                    )
                    partial_success["chat"] = True

            except Exception as e:
                errors.append(f"chat_error: {e}")

            return {
                "workflow_id": workflow_id,
                "partial_success": partial_success,
                "errors": errors,
                "success_count": len(partial_success),
                "error_count": len(errors),
            }

        # Execute resilience test
        resilience_start = time.perf_counter()

        resilience_tasks = [resilience_workflow(i) for i in range(cascade_operations)]

        resilience_results = await asyncio.gather(*resilience_tasks)

        resilience_duration = time.perf_counter() - resilience_start

        # Analyze resilience results
        total_auth_attempts = cascade_operations
        total_agent_attempts = sum(
            1 for r in resilience_results if "auth" in r["partial_success"]
        )
        total_chat_attempts = sum(
            1 for r in resilience_results if "agent" in r["partial_success"]
        )

        auth_successes = sum(
            1 for r in resilience_results if "auth" in r["partial_success"]
        )
        agent_successes = sum(
            1 for r in resilience_results if "agent" in r["partial_success"]
        )
        chat_successes = sum(
            1 for r in resilience_results if "chat" in r["partial_success"]
        )

        # Calculate success rates for each step
        auth_success_rate = (
            auth_successes / total_auth_attempts if total_auth_attempts > 0 else 0
        )
        agent_success_rate = (
            agent_successes / total_agent_attempts if total_agent_attempts > 0 else 0
        )
        chat_success_rate = (
            chat_successes / total_chat_attempts if total_chat_attempts > 0 else 0
        )

        # Validate error resilience
        assert (
            auth_success_rate >= 0.60
        )  # Expected success rate considering 30% failure rate
        assert agent_success_rate >= 0.60
        assert chat_success_rate >= 0.60

        # Ensure system didn't completely fail
        workflows_with_some_success = sum(
            1 for r in resilience_results if r["success_count"] > 0
        )
        partial_success_rate = workflows_with_some_success / cascade_operations

        assert partial_success_rate >= 0.80  # Most workflows should have some success

        print("Error Cascade Resilience Test:")
        print(f"  Operations: {cascade_operations} in {resilience_duration:.2f}s")
        print(f"  Auth Success Rate: {auth_success_rate:.2%}")
        print(f"  Agent Success Rate: {agent_success_rate:.2%}")
        print(f"  Chat Success Rate: {chat_success_rate:.2%}")
        print(f"  Partial Success Rate: {partial_success_rate:.2%}")

    async def test_resource_cleanup_under_stress(
        self,
        mock_user_repo: Mock,
        mock_agent_repo: Mock,
    ) -> None:
        """Test proper resource cleanup under stress conditions."""

        auth_use_case = AuthenticateUser(mock_user_repo)
        create_agent_use_case = CreateAgent(mock_agent_repo)

        # Simulate resource tracking
        active_resources = {
            "sessions": set(),
            "agents": set(),
            "connections": set(),
        }

        # Modified repositories to track resources
        async def tracking_auth_side_effect(email: str) -> User:
            _ = self._create_test_user(email)
            active_resources["sessions"].add(user.id)
            await asyncio.sleep(0.1)  # Simulate processing
            return user

        async def tracking_agent_side_effect(agent: Agent) -> Agent:
            active_resources["agents"].add(str(agent.id))
            active_resources["connections"].add(f"conn_{agent.id}")
            await asyncio.sleep(0.2)  # Simulate processing
            return agent

        mock_user_repo.get_by_email = AsyncMock(side_effect=tracking_auth_side_effect)
        mock_agent_repo.create = AsyncMock(side_effect=tracking_agent_side_effect)

        # Stress test with resource creation
        resource_operations = 30

        async def resource_workflow(workflow_id: int) -> dict[str, Any]:
            """Create resources and simulate cleanup."""

            try:
                # Create session
                login_request = LoginRequest(
                    email=f"resource_user_{workflow_id}@example.com",
                    password=os.getenv("PASSWORD"),
                )

                from unittest.mock import patch

                with (
                    patch("bcrypt.checkpw", return_value=True),
                    patch("jwt.encode", return_value=f"resource_token_{workflow_id}"),
                ):
                    _ = await auth_use_case(login_request)

                # Create agent
                _ = await create_agent_use_case(
                    name=f"ResourceAgent{workflow_id}",
                    description=f"Resource test agent {workflow_id}",
                    capabilities=["chat"],
                    config_data={"temperature": 0.5},
                )

                # Simulate resource usage
                await asyncio.sleep(0.1)

                # Simulate cleanup (remove from tracking)
                user_id = (
                    user.access_token.split("_")[-1]
                    if hasattr(user, "access_token")
                    else f"resource_user_{workflow_id}"
                )
                active_resources["sessions"].discard(user_id)
                active_resources["agents"].discard(str(agent.id))
                active_resources["connections"].discard(f"conn_{agent.id}")

                return {
                    "workflow_id": workflow_id,
                    "success": True,
                    "user_id": user_id,
                    "agent_id": str(agent.id),
                }

            except Exception as e:
                return {
                    "workflow_id": workflow_id,
                    "success": False,
                    "error": str(e),
                }

        # Execute resource stress test
        cleanup_start = time.perf_counter()

        cleanup_tasks = [resource_workflow(i) for i in range(resource_operations)]

        cleanup_results = await asyncio.gather(*cleanup_tasks)

        cleanup_duration = time.perf_counter() - cleanup_start

        # Analyze resource cleanup
        successful_workflows = [r for r in cleanup_results if r.get("success")]
        success_rate = len(successful_workflows) / resource_operations

        # Check for resource leaks
        remaining_sessions = len(active_resources["sessions"])
        remaining_agents = len(active_resources["agents"])
        remaining_connections = len(active_resources["connections"])

        total_remaining_resources = (
            remaining_sessions + remaining_agents + remaining_connections
        )

        # Validate resource cleanup
        assert success_rate >= 0.90  # At least 90% successful workflows
        assert total_remaining_resources <= (
            resource_operations * 0.1
        )  # Max 10% resource leakage

        print("Resource Cleanup Stress Test:")
        print(f"  Operations: {resource_operations} in {cleanup_duration:.2f}s")
        print(f"  Success Rate: {success_rate:.2%}")
        print(f"  Remaining Sessions: {remaining_sessions}")
        print(f"  Remaining Agents: {remaining_agents}")
        print(f"  Remaining Connections: {remaining_connections}")
        print(
            f"  Total Resource Leakage: {total_remaining_resources}/{resource_operations * 3}"
        )

    async def test_system_recovery_after_failure(
        self,
        mock_chat_repo: Mock,
    ) -> None:
        """Test system recovery capabilities after simulated failures."""

        send_message_use_case = SendMessageUseCase(mock_chat_repo)

        # Phase 1: Normal operation
        normal_operations = 20

        async def normal_operation(op_id: int) -> dict[str, Any]:
            """Normal system operation."""
            try:
                await send_message_use_case.execute(
                    agent_id=str(uuid4()),
                    content=f"Normal operation {op_id}",
                    user_id=f"normal_user_{op_id}",
                )
                return {"phase": "normal", "op_id": op_id, "success": True}
            except Exception as e:
                return {
                    "phase": "normal",
                    "op_id": op_id,
                    "success": False,
                    "error": str(e),
                }

        # Execute normal phase
        normal_tasks = [normal_operation(i) for i in range(normal_operations)]
        normal_results = await asyncio.gather(*normal_tasks)

        normal_success_rate = (
            sum(1 for r in normal_results if r["success"]) / normal_operations
        )

        # Phase 2: Simulated system failure
        def failing_side_effect(**kwargs: Any) -> Any:
            raise Exception("Simulated system failure")

        mock_chat_repo.send_message = AsyncMock(side_effect=failing_side_effect)

        failure_operations = 10

        async def failure_operation(op_id: int) -> dict[str, Any]:
            """Operation during system failure."""
            try:
                await send_message_use_case.execute(
                    agent_id=str(uuid4()),
                    content=f"Failure operation {op_id}",
                    user_id=f"failure_user_{op_id}",
                )
                return {"phase": "failure", "op_id": op_id, "success": True}
            except Exception as e:
                return {
                    "phase": "failure",
                    "op_id": op_id,
                    "success": False,
                    "error": str(e),
                }

        # Execute failure phase
        failure_tasks = [failure_operation(i) for i in range(failure_operations)]
        failure_results = await asyncio.gather(*failure_tasks)

        failure_success_rate = (
            sum(1 for r in failure_results if r["success"]) / failure_operations
        )

        # Phase 3: System recovery
        def recovering_side_effect(**kwargs: Any) -> Any:
            import random

            # Gradual recovery - 80% success rate
            if random.random() < 0.8:
                return self._create_mock_response(**kwargs)
            else:
                raise Exception("Recovery in progress")

        mock_chat_repo.send_message = AsyncMock(side_effect=recovering_side_effect)

        recovery_operations = 25

        async def recovery_operation(op_id: int) -> dict[str, Any]:
            """Operation during system recovery."""
            try:
                await send_message_use_case.execute(
                    agent_id=str(uuid4()),
                    content=f"Recovery operation {op_id}",
                    user_id=f"recovery_user_{op_id}",
                )
                return {"phase": "recovery", "op_id": op_id, "success": True}
            except Exception as e:
                return {
                    "phase": "recovery",
                    "op_id": op_id,
                    "success": False,
                    "error": str(e),
                }

        # Execute recovery phase
        recovery_tasks = [recovery_operation(i) for i in range(recovery_operations)]
        recovery_results = await asyncio.gather(*recovery_tasks)

        recovery_success_rate = (
            sum(1 for r in recovery_results if r["success"]) / recovery_operations
        )

        # Validate system recovery
        assert (
            normal_success_rate >= 0.95
        )  # Normal operation should be highly successful
        assert failure_success_rate <= 0.05  # Failure phase should mostly fail
        assert (
            recovery_success_rate >= 0.70
        )  # Recovery should show improving success rate

        print("System Recovery Test:")
        print(f"  Normal Phase Success Rate: {normal_success_rate:.2%}")
        print(f"  Failure Phase Success Rate: {failure_success_rate:.2%}")
        print(f"  Recovery Phase Success Rate: {recovery_success_rate:.2%}")
        print(
            f"  Recovery Improvement: {(recovery_success_rate - failure_success_rate) * 100:.1f} percentage points"
        )
