import asyncio
import time
from uuid import uuid4

import pytest
from app.api.graphql.core.middleware import (
import Exception
import a
import agent_data
import any
import e
import error
import i
import key
import kwargs
import len
import limit
import range
import self
import setattr
import skip
import str
import update_data
import value
    create_optimized_schema,
    get_performance_summary,
    performance_metrics,
)
from app.api.graphql.optimized_schema import schema
from strawberry.test import GraphQLTestClient

"""Comprehensive test suite cho optimized GraphQL API.
Tests để ensure sub-100ms performance, type safety, và correctness.
"""


@pytest.fixture
def graphql_client():
    """GraphQL test client với performance extensions."""
    optimized_schema = create_optimized_schema(schema, enable_caching=True)
    return GraphQLTestClient(optimized_schema)


@pytest.fixture
def mock_context():
    """Mock GraphQL context for testing."""
    return {
        "container": MockContainer(),
        "current_user": MockUser(),
        "security_context": MockSecurityContext(),
    }


class MockUser:
    """Mock user for testing."""

    def __init__(self):
        self.id = "test-user-123"
        self.username = "testuser"
        self.email = "test@example.com"
        self.is_admin = False
        self.created_at = "2024-01-01T00:00:00Z"


class MockSecurityContext:
    """Mock security context."""

    def __init__(self):
        self.user_id = "test-user-123"
        self.tenant_id = "test-tenant"


class MockContainer:
    """Mock dependency container."""

    async def get_agent_repository(self):
        return MockAgentRepository()


class MockAgentRepository:
    """Mock agent repository for testing."""

    def __init__(self):
        self.agents = []

    async def get_all(self, skip=0, limit=10, filters=None):
        """Mock get_all method."""
        return self.agents[skip : skip + limit]

    async def get_by_id(self, agent_id):
        """Mock get_by_id method."""
        for agent in self.agents:
            if str(agent.id) == str(agent_id):
                return agent
        return None

    async def create(self, agent_data):
        """Mock create method."""
        agent = MockAgent(**agent_data)
        self.agents.append(agent)
        return agent

    async def update(self, agent_id, update_data):
        """Mock update method."""
        agent = await self.get_by_id(agent_id)
        if agent:
            for key, value in update_data.items():
                setattr(agent, key, value)
        return agent

    async def delete(self, agent_id):
        """Mock delete method."""
        self.agents = [a for a in self.agents if str(a.id) != str(agent_id)]


class MockAgent:
    """Mock agent entity."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", uuid4())
        self.name = kwargs.get("name", "Test Agent")
        self.description = kwargs.get("description", "Test Description")
        self.model_type = kwargs.get("model_type", "gpt-4")
        self.capabilities = kwargs.get("capabilities", ["chat", "analysis"])
        self.status = kwargs.get("status", "active")
        self.owner_id = kwargs.get("owner_id", "test-user-123")
        self.created_at = kwargs.get("created_at", "2024-01-01T00:00:00Z")
        self.updated_at = kwargs.get("updated_at", "2024-01-01T00:00:00Z")


class TestPerformance:
    """Performance tests để ensure sub-100ms targets."""

    @pytest.mark.asyncio
    async def test_query_performance_under_100ms(self, graphql_client, mock_context):
        """Test that queries execute under 100ms."""
        query = """
        query {
            agents(limit: 10) {
                id
                name
                description
                status
            }
        }
        """
        start_time = time.time()
        result = graphql_client.query(query, context_value=mock_context)
        execution_time = (time.time() - start_time) * 1000  # Convert to ms
        assert (
            execution_time < 100
        ), f"Query took {execution_time:.2f}ms, exceeds 100ms target"
        assert result.errors is None

    @pytest.mark.asyncio
    async def test_mutation_performance_under_200ms(self, graphql_client, mock_context):
        """Test that mutations execute under 200ms."""
        mutation = """
        mutation {
            createAgent(input: {
                name: "Performance Test Agent"
                description: "Testing performance"
                modelType: "gpt-4"
                capabilities: ["chat"]
            }) {
                agent {
                    id
                    name
                }
                success
                errors {
                    message
                }
            }
        }
        """
        start_time = time.time()
        result = graphql_client.query(mutation, context_value=mock_context)
        execution_time = (time.time() - start_time) * 1000
        assert (
            execution_time < 200
        ), f"Mutation took {execution_time:.2f}ms, exceeds 200ms target"
        assert result.errors is None

    @pytest.mark.asyncio
    async def test_concurrent_queries_performance(self, graphql_client, mock_context):
        """Test performance under concurrent load."""
        query = """
        query {
            agents(limit: 5) {
                id
                name
            }
        }
        """

        async def execute_query():
            start_time = time.time()
            result = graphql_client.query(query, context_value=mock_context)
            execution_time = (time.time() - start_time) * 1000
            return execution_time, result

        tasks = [execute_query() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        for execution_time, result in results:
            assert execution_time < 150, f"Concurrent query took {execution_time:.2f}ms"
            assert result.errors is None


class TestCaching:
    """Test caching functionality."""

    @pytest.mark.asyncio
    async def test_query_caching_improves_performance(
        self, graphql_client, mock_context
    ):
        """Test that repeated queries are cached và faster."""
        query = """
        query {
            agents(limit: 5) {
                id
                name
                description
            }
        }
        """
        start_time = time.time()
        result1 = graphql_client.query(query, context_value=mock_context)
        first_execution_time = (time.time() - start_time) * 1000
        start_time = time.time()
        result2 = graphql_client.query(query, context_value=mock_context)
        second_execution_time = (time.time() - start_time) * 1000
        assert second_execution_time < first_execution_time * 0.5
        assert result1.data == result2.data

    @pytest.mark.asyncio
    async def test_cache_invalidation_on_mutation(self, graphql_client, mock_context):
        """Test that mutations properly invalidate cache."""
        query = """
        query {
            agents {
                id
                name
            }
        }
        """
        result1 = graphql_client.query(query, context_value=mock_context)
        mutation = """
        mutation {
            createAgent(input: {
                name: "Cache Test Agent"
                modelType: "gpt-4"
            }) {
                success
            }
        }
        """
        graphql_client.query(mutation, context_value=mock_context)
        result2 = graphql_client.query(query, context_value=mock_context)
        assert result1.data != result2.data or len(result2.data["agents"]) > len(
            result1.data["agents"]
        )


class TestValidation:
    """Test input validation và error handling."""

    @pytest.mark.asyncio
    async def test_invalid_agent_creation_input(self, graphql_client, mock_context):
        """Test validation of invalid input data."""
        mutation = """
        mutation {
            createAgent(input: {
                name: "X"  # Too short
                modelType: "invalid-model"  # Invalid model
            }) {
                agent {
                    id
                }
                success
                errors {
                    message
                    code
                }
            }
        }
        """
        result = graphql_client.query(mutation, context_value=mock_context)
        assert not result.data["createAgent"]["success"]
        assert len(result.data["createAgent"]["errors"]) > 0
        assert any(
            "name" in error["message"].lower()
            for error in result.data["createAgent"]["errors"]
        )

    @pytest.mark.asyncio
    async def test_authentication_required(self, graphql_client):
        """Test that authentication is required for protected operations."""
        mutation = """
        mutation {
            createAgent(input: {
                name: "Test Agent"
                modelType: "gpt-4"
            }) {
                success
                errors {
                    message
                }
            }
        }
        """
        result = graphql_client.query(mutation, context_value={})
        assert result.errors is not None or not result.data["createAgent"]["success"]


class TestDataLoader:
    """Test DataLoader functionality để prevent N+1 queries."""

    @pytest.mark.asyncio
    async def test_no_n_plus_one_queries(self, graphql_client, mock_context):
        """Test that DataLoader prevents N+1 query problems."""
        query = """
        query {
            agents(limit: 5) {
                id
                name
                owner {
                    id
                    username
                }
            }
        }
        """
        container = mock_context["container"]
        repo = await container.get_agent_repository()
        for i in range(5):
            await repo.create(
                {
                    "name": f"Agent {i}",
                    "model_type": "gpt-4",
                    "owner_id": f"user-{i}",
                }
            )
        start_time = time.time()
        result = graphql_client.query(query, context_value=mock_context)
        execution_time = (time.time() - start_time) * 1000
        assert execution_time < 100
        assert result.errors is None
        assert len(result.data["agents"]) == 5


class TestMetrics:
    """Test performance metrics collection."""

    def test_performance_metrics_collection(self):
        """Test that performance metrics are properly collected."""
        performance_metrics.reset()
        performance_metrics.record_query(0.05, had_errors=False)  # 50ms
        performance_metrics.record_query(0.15, had_errors=False)  # 150ms (slow)
        performance_metrics.record_query(0.03, had_errors=True)  # 30ms with error
        summary = performance_metrics.get_summary()
        assert summary["query_count"] == 3
        assert summary["slow_queries"] == 1
        assert summary["error_count"] == 1
        assert summary["avg_execution_time"] == pytest.approx(0.077, rel=0.01)

    def test_performance_summary_includes_all_metrics(self):
        """Test that performance summary includes all expected metrics."""
        summary = get_performance_summary()
        required_keys = ["performance", "dataloader", "uptime"]
        for key in required_keys:
            assert key in summary
        perf_metrics = summary["performance"]
        required_perf_keys = [
            "query_count",
            "total_execution_time",
            "avg_execution_time",
            "slow_queries",
            "error_count",
            "timing_breakdown",
        ]
        for key in required_perf_keys:
            assert key in perf_metrics


@pytest.mark.integration
class TestEndToEndFlow:
    """End-to-end integration tests."""

    @pytest.mark.asyncio
    async def test_complete_agent_crud_flow(self, graphql_client, mock_context):
        """Test complete CRUD flow performs within targets."""
        agent_id = None
        try:
            create_mutation = """
            mutation {
                createAgent(input: {
                    name: "E2E Test Agent"
                    description: "End-to-end testing"
                    modelType: "gpt-4"
                    capabilities: ["chat", "analysis"]
                }) {
                    agent {
                        id
                        name
                    }
                    success
                }
            }
            """
            start_time = time.time()
            create_result = graphql_client.query(
                create_mutation, context_value=mock_context
            )
            create_time = (time.time() - start_time) * 1000
            assert create_time < 200  # Create under 200ms
            assert create_result.data["createAgent"]["success"]
            agent_id = create_result.data["createAgent"]["agent"]["id"]
            read_query = f"""
            query {{
                agent(id: "{agent_id}") {{
                    id
                    name
                    description
                    status
                }}
            }}
            """
            start_time = time.time()
            read_result = graphql_client.query(read_query, context_value=mock_context)
            read_time = (time.time() - start_time) * 1000
            assert read_time < 100  # Read under 100ms
            assert read_result.data["agent"]["name"] == "E2E Test Agent"
            update_mutation = f"""
            mutation {{
                updateAgent(id: "{agent_id}", input: {{
                    name: "Updated E2E Agent"
                    status: "inactive"
                }}) {{
                    agent {{
                        name
                        status
                    }}
                    success
                }}
            }}
            """
            start_time = time.time()
            update_result = graphql_client.query(
                update_mutation, context_value=mock_context
            )
            update_time = (time.time() - start_time) * 1000
            assert update_time < 150  # Update under 150ms
            assert update_result.data["updateAgent"]["success"]
            assert (
                update_result.data["updateAgent"]["agent"]["name"]
                == "Updated E2E Agent"
            )
            delete_mutation = f"""
            mutation {{
                deleteAgent(id: "{agent_id}")
            }}
            """
            start_time = time.time()
            delete_result = graphql_client.query(
                delete_mutation, context_value=mock_context
            )
            delete_time = (time.time() - start_time) * 1000
            assert delete_time < 100  # Delete under 100ms
            assert delete_result.data["deleteAgent"]
        except Exception as e:
            pytest.fail(f"E2E test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
__all__ = [
    "MockAgent",
    "MockAgentRepository",
    "MockContainer",
    "MockSecurityContext",
    "MockUser",
    "TestCaching",
    "TestDataLoader",
    "TestEndToEndFlow",
    "TestMetrics",
    "TestPerformance",
    "TestValidation",
    "agent",
    "agent_id",
    "container",
    "create_mutation",
    "create_result",
    "create_time",
    "delete_mutation",
    "delete_result",
    "delete_time",
    "execution_time",
    "first_execution_time",
    "graphql_client",
    "mock_context",
    "mutation",
    "optimized_schema",
    "perf_metrics",
    "query",
    "read_query",
    "read_result",
    "read_time",
    "repo",
    "required_keys",
    "required_perf_keys",
    "result",
    "result1",
    "result2",
    "results",
    "second_execution_time",
    "start_time",
    "summary",
    "tasks",
    "test_performance_metrics_collection",
    "test_performance_summary_includes_all_metrics",
    "update_mutation",
    "update_result",
    "update_time",
]
