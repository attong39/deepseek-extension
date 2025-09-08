from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from apps.backend.core.domain.aggregates.agent_aggregate import (
import ValueError
import abs
import len
import mock_get_logger
import str
    AgentAggregate,
    AgentConfiguration,
    AgentError,
    AgentStatus,
)

"""Unit tests for agent aggregate.
This module contains comprehensive unit tests for the AgentAggregate
class, covering all lifecycle operations, validation, error handling,
and async functionality.
"""


class TestAgentConfiguration:
    """Test cases for AgentConfiguration model."""

    def test_valid_configuration_creation(self):
        """Test creating a valid agent configuration."""
        config = AgentConfiguration(
            model_name="gpt-4",
            temperature=0.8,
            max_tokens=2000,
            timeout_seconds=60,
            retry_attempts=5,
            rate_limit_per_minute=100,
        )
        assert abs(config.temperature - 0.8) < 1e-6
        assert config.max_tokens == 2000
        assert config.timeout_seconds == 60
        assert config.retry_attempts == 5
        assert config.rate_limit_per_minute == 100

    def test_default_configuration_values(self):
        """Test default values for agent configuration."""
        config = AgentConfiguration(model_name="gpt-3.5-turbo")
        assert config.model_name == "gpt-3.5-turbo"
        assert abs(config.temperature - 0.7) < 1e-6
        assert config.max_tokens == 1000
        assert config.timeout_seconds == 30
        assert config.retry_attempts == 3
        assert config.rate_limit_per_minute == 60

    def test_invalid_model_name_validation(self):
        """Test that empty model name raises ValueError."""
        with pytest.raises(ValueError, match="Model name cannot be empty"):
            AgentConfiguration(model_name="")

    def test_temperature_validation(self):
        """Test temperature field validation."""
        AgentConfiguration(model_name="gpt-4", temperature=0.0)
        AgentConfiguration(model_name="gpt-4", temperature=1.5)
        AgentConfiguration(model_name="gpt-4", temperature=2.0)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", temperature=-0.1)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", temperature=2.1)

    def test_max_tokens_validation(self):
        """Test max_tokens field validation."""
        AgentConfiguration(model_name="gpt-4", max_tokens=1)
        AgentConfiguration(model_name="gpt-4", max_tokens=4000)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", max_tokens=0)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", max_tokens=4001)

    def test_timeout_seconds_validation(self):
        """Test timeout_seconds field validation."""
        AgentConfiguration(model_name="gpt-4", timeout_seconds=1)
        AgentConfiguration(model_name="gpt-4", timeout_seconds=300)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", timeout_seconds=0)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", timeout_seconds=301)

    def test_retry_attempts_validation(self):
        """Test retry_attempts field validation."""
        AgentConfiguration(model_name="gpt-4", retry_attempts=0)
        AgentConfiguration(model_name="gpt-4", retry_attempts=10)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", retry_attempts=-1)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", retry_attempts=11)

    def test_rate_limit_validation(self):
        """Test rate_limit_per_minute field validation."""
        AgentConfiguration(model_name="gpt-4", rate_limit_per_minute=1)
        AgentConfiguration(model_name="gpt-4", rate_limit_per_minute=1000)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", rate_limit_per_minute=0)
        with pytest.raises(ValueError):
            AgentConfiguration(model_name="gpt-4", rate_limit_per_minute=1001)


class TestAgentError:
    """Test cases for AgentError exception."""

    def test_agent_error_creation(self):
        """Test creating AgentError with basic parameters."""
        error = AgentError("Test error", "agent-123")
        assert str(error) == "Test error"
        assert error.agent_id == "agent-123"
        assert error.details == {}

    def test_agent_error_with_details(self):
        """Test creating AgentError with details."""
        details = {"operation": "activate", "reason": "invalid_status"}
        error = AgentError("Cannot activate", "agent-123", details)
        assert str(error) == "Cannot activate"
        assert error.agent_id == "agent-123"
        assert error.details == details


class TestAgentAggregate:
    """Test cases for AgentAggregate class."""

    def test_create_agent_success(self):
        """Test successful agent creation."""
        agent = AgentAggregate.create(
            id="agent-123",
            name="Test Agent",
            configuration=AgentConfiguration(model_name="gpt-4"),
            description="Test description",
            capabilities=["chat", "code"],
        )
        assert agent.id == "agent-123"
        assert agent.name == "Test Agent"
        assert agent.description == "Test description"
        assert agent.status == AgentStatus.INACTIVE
        assert agent.capabilities == ["chat", "code"]
        assert len(agent.training_sessions) == 0
        assert agent.version == 0

    def test_create_agent_minimal(self):
        """Test creating agent with minimal parameters."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        assert agent.id == "agent-123"
        assert agent.name == "Test Agent"
        assert agent.status == AgentStatus.INACTIVE
        assert agent.capabilities == []
        assert agent.configuration.model_name == "gpt-4"

    def test_create_agent_missing_id(self):
        """Test creating agent without required id."""
        with pytest.raises(AgentError, match="Agent id and name are required"):
            AgentAggregate.create(name="Test Agent")

    def test_create_agent_missing_name(self):
        """Test creating agent without required name."""
        with pytest.raises(AgentError, match="Agent id and name are required"):
            AgentAggregate.create(id="agent-123")

    def test_create_agent_empty_name(self):
        """Test creating agent with empty name."""
        with pytest.raises(AgentError, match="Agent id and name are required"):
            AgentAggregate.create(id="agent-123", name="")

    def test_validate_invariants_valid(self):
        """Test validating invariants on valid agent."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        agent.validate_invariants()

    def test_validate_invariants_empty_name(self):
        """Test validating invariants with empty name."""
        agent = AgentAggregate(
            id="agent-123",
            name="",
            status=AgentStatus.INACTIVE,
            capabilities=[],
            training_sessions=[],
        )
        with pytest.raises(ValueError, match="Agent name cannot be empty"):
            agent.validate_invariants()

    def test_validate_invariants_invalid_status(self):
        """Test validating invariants with invalid status."""
        agent = AgentAggregate(
            id="agent-123",
            name="Test Agent",
            status="INVALID_STATUS",
            capabilities=[],
            training_sessions=[],
        )
        with pytest.raises(ValueError, match="Invalid status"):
            agent.validate_invariants()

    def test_validate_invariants_duplicate_capabilities(self):
        """Test validating invariants with duplicate capabilities."""
        agent = AgentAggregate(
            id="agent-123",
            name="Test Agent",
            status=AgentStatus.INACTIVE,
            capabilities=["chat", "code", "chat"],
            training_sessions=[],
        )
        with pytest.raises(ValueError, match="Agent capabilities must be unique"):
            agent.validate_invariants()

    def test_activate_success(self):
        """Test successful agent activation."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        activated = agent.activate()
        assert activated.status == AgentStatus.ACTIVE
        assert activated.id == agent.id
        assert activated != agent  # Should be a new instance
        assert activated.version == agent.version  # Version should be preserved

    def test_activate_already_active(self):
        """Test activating already active agent."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        with pytest.raises(AgentError, match="Agent must be inactive to activate"):
            active_agent.activate()

    def test_deactivate_success(self):
        """Test successful agent deactivation."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        deactivated = active_agent.deactivate()
        assert deactivated.status == AgentStatus.INACTIVE
        assert deactivated.id == agent.id
        assert deactivated != active_agent

    def test_deactivate_not_active(self):
        """Test deactivating inactive agent."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        with pytest.raises(AgentError, match="Agent must be active to deactivate"):
            agent.deactivate()

    def test_start_training_success(self):
        """Test successful training start."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_config = {"dataset": "test-dataset", "epochs": 10}
        training_agent = active_agent.start_training(training_config)
        assert training_agent.status == AgentStatus.TRAINING
        assert len(training_agent.training_sessions) == 1
        assert training_agent.training_sessions[0]["status"] == "STARTED"
        assert training_agent.training_sessions[0]["config"] == training_config

    def test_start_training_not_active(self):
        """Test starting training on inactive agent."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        with pytest.raises(AgentError, match="Agent must be active to start training"):
            agent.start_training({})

    def test_start_training_already_training(self):
        """Test starting training on already training agent."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_agent = active_agent.start_training({})
        with pytest.raises(AgentError, match="Agent is already in training"):
            training_agent.start_training({})

    def test_complete_training_success(self):
        """Test successful training completion."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_agent = active_agent.start_training({})
        results = {"accuracy": 0.95, "loss": 0.05}
        completed_agent = training_agent.complete_training(results)
        assert completed_agent.status == AgentStatus.ACTIVE
        assert len(completed_agent.training_sessions) == 1
        assert completed_agent.training_sessions[0]["status"] == "COMPLETED"
        assert completed_agent.training_sessions[0]["results"] == results

    def test_complete_training_not_training(self):
        """Test completing training on non-training agent."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        with pytest.raises(AgentError, match="Agent must be training to complete"):
            agent.complete_training({})

    def test_fail_training_success(self):
        """Test successful training failure."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_agent = active_agent.start_training({})
        error_msg = "GPU out of memory"
        failed_agent = training_agent.fail_training(error_msg)
        assert failed_agent.status == AgentStatus.ERROR
        assert len(failed_agent.training_sessions) == 1
        assert failed_agent.training_sessions[0]["status"] == "FAILED"
        assert failed_agent.training_sessions[0]["error"] == error_msg

    def test_update_configuration_success(self):
        """Test successful configuration update."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        updates = {"temperature": 0.9, "max_tokens": 1500}
        updated_agent = agent.update_configuration(updates)
        assert abs(updated_agent.configuration.temperature - 0.9) < 1e-6
        assert updated_agent.configuration.max_tokens == 1500
        assert updated_agent.configuration.model_name == "gpt-4"  # Unchanged

    def test_update_configuration_invalid(self):
        """Test configuration update with invalid values."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        with pytest.raises(AgentError, match="Invalid configuration"):
            agent.update_configuration({"temperature": 3.0})

    def test_add_capability_success(self):
        """Test successful capability addition."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        updated_agent = agent.add_capability("chat")
        assert "chat" in updated_agent.capabilities
        assert len(updated_agent.capabilities) == 1

    def test_add_capability_duplicate(self):
        """Test adding duplicate capability."""
        agent = AgentAggregate.create(
            id="agent-123", name="Test Agent", capabilities=["chat"]
        )
        with pytest.raises(AgentError, match="Capability 'chat' already exists"):
            agent.add_capability("chat")

    def test_add_capability_case_insensitive_duplicate(self):
        """Test adding duplicate capability with different case."""
        agent = AgentAggregate.create(
            id="agent-123", name="Test Agent", capabilities=["CHAT"]
        )
        with pytest.raises(AgentError, match="Capability 'chat' already exists"):
            agent.add_capability("chat")

    def test_remove_capability_success(self):
        """Test successful capability removal."""
        agent = AgentAggregate.create(
            id="agent-123", name="Test Agent", capabilities=["chat", "code"]
        )
        updated_agent = agent.remove_capability("chat")
        assert "chat" not in updated_agent.capabilities
        assert "code" in updated_agent.capabilities
        assert len(updated_agent.capabilities) == 1

    def test_remove_capability_not_found(self):
        """Test removing non-existent capability."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        with pytest.raises(AgentError, match="Capability 'nonexistent' not found"):
            agent.remove_capability("nonexistent")

    def test_remove_capability_case_insensitive(self):
        """Test removing capability with different case."""
        agent = AgentAggregate.create(
            id="agent-123", name="Test Agent", capabilities=["CHAT"]
        )
        updated_agent = agent.remove_capability("chat")
        assert "CHAT" not in updated_agent.capabilities
        assert len(updated_agent.capabilities) == 0

    def test_get_training_history(self):
        """Test getting training history."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_agent = active_agent.start_training({"dataset": "test"})
        completed_agent = training_agent.complete_training({"accuracy": 0.9})
        history = completed_agent.get_training_history()
        assert len(history) == 1
        assert history[0]["status"] == "COMPLETED"
        assert history[0]["config"] == {"dataset": "test"}
        assert history[0]["results"] == {"accuracy": 0.9}

    def test_immutability(self):
        """Test that all operations return new instances."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        activated = agent.activate()
        assert activated is not agent
        with_capability = agent.add_capability("test")
        assert with_capability is not agent
        assert agent.status == AgentStatus.INACTIVE
        assert len(agent.capabilities) == 0

    @pytest.mark.asyncio
    async def test_start_training_async(self):
        """Test async training start."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_config = {"dataset": "async-test"}
        training_agent = await active_agent.start_training_async(training_config)
        assert training_agent.status == AgentStatus.TRAINING
        assert len(training_agent.training_sessions) == 1

    @pytest.mark.asyncio
    async def test_complete_training_async(self):
        """Test async training completion."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_agent = active_agent.start_training({})
        results = {"accuracy": 0.95}
        completed_agent = await training_agent.complete_training_async(results)
        assert completed_agent.status == AgentStatus.ACTIVE
        assert completed_agent.training_sessions[0]["status"] == "COMPLETED"

    def test_event_generation(self):
        """Test that operations generate appropriate domain events."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        activated = agent.activate()
        events = activated.pull_events()
        assert len(events) >= 1  # At least activation event
        with_capability = activated.add_capability("test")
        events = with_capability.pull_events()
        assert len(events) >= 1  # At least capability added event

    def test_timestamp_updates(self):
        """Test that operations update timestamps appropriately."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        original_updated_at = agent.updated_at
        activated = agent.activate()
        assert activated.updated_at > original_updated_at

    def test_version_preservation(self):
        """Test that version is preserved across operations."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        activated = agent.activate()
        assert activated.version == agent.version
        with_capability = activated.add_capability("test")
        assert with_capability.version == agent.version


class TestAgentAggregateIntegration:
    """Integration tests for AgentAggregate with external dependencies."""

    @patch("zeta_vn.core.domain.aggregates.agent_aggregate.get_logger")
    def test_logging_integration(self, mock_get_logger):
        """Test that logging is properly integrated."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        agent.activate()
        mock_logger.info.assert_called()

    def test_configuration_persistence(self):
        """Test that configuration changes are properly persisted."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        updated = agent.update_configuration(
            {"model_name": "gpt-4-turbo", "temperature": 0.5, "max_tokens": 3000}
        )
        assert updated.configuration.model_name == "gpt-4-turbo"
        assert abs(updated.configuration.temperature - 0.5) < 1e-6
        assert updated.configuration.max_tokens == 3000

    def test_error_context_propagation(self):
        """Test that errors include proper context."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        try:
            agent.start_training({})  # Should fail - not active
        except AgentError as e:
            assert e.agent_id == "agent-123"
            assert "active" in str(e).lower()

    def test_training_session_isolation(self):
        """Test that training sessions are properly isolated."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        active_agent = agent.activate()
        training_agent = active_agent.start_training({"session": 1})
        with pytest.raises(AgentError):
            training_agent.start_training({"session": 2})
        completed = training_agent.complete_training({"result": "success"})
        assert completed.status == AgentStatus.ACTIVE
        new_training = completed.start_training({"session": 2})
        assert len(new_training.training_sessions) == 2


@pytest.fixture
def value_error():
    """Fixture for ValueError"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def abs_fixture():
    """Fixture for abs"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def e():
    """Fixture for e"""
    return None  # TODO: Define appropriate fixture


__all__ = [
    "TestAgentAggregate",
    "TestAgentAggregateIntegration",
    "TestAgentConfiguration",
    "TestAgentError",
]
