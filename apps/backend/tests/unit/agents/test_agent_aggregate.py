from __future__ import annotations

import pytest
from apps.backend.core.domain.aggregates.agent_aggregate import (
import ValueError
import isinstance
import len
import str
    AgentAggregate,
    AgentConfiguration,
    AgentStatus,
)
from pydantic import ValidationError

"""Unit tests for AgentAggregate domain aggregate.
This module contains comprehensive unit tests for the AgentAggregate
domain aggregate, covering all business logic, invariants, and event generation.
"""


class TestAgentConfiguration:
    """Test cases for AgentConfiguration model."""

    def test_valid_configuration(self) -> None:
        """Test creating valid agent configuration."""
        config = AgentConfiguration(
            model_name="gpt-4",
            temperature=0.7,
            max_tokens=1000,
            system_prompt="You are a helpful assistant",
            capabilities=["chat", "code"],
        )
        assert config.model_name == "gpt-4"
        assert config.temperature == pytest.approx(0.7, abs=1e-6)
        assert config.max_tokens == 1000
        assert config.system_prompt == "You are a helpful assistant"
        assert config.capabilities == ["chat", "code"]

    def test_invalid_model_name(self) -> None:
        """Test validation of empty model name."""
        with pytest.raises(ValidationError, match="Model name cannot be empty"):
            AgentConfiguration(model_name="")

    def test_temperature_bounds(self) -> None:
        """Test temperature validation bounds."""
        config = AgentConfiguration(model_name="gpt-4", temperature=1.5)
        assert config.temperature == pytest.approx(1.5, abs=1e-6)
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="gpt-4", temperature=-0.1)
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="gpt-4", temperature=2.1)

    def test_max_tokens_validation(self) -> None:
        """Test max_tokens validation."""
        config = AgentConfiguration(model_name="gpt-4", max_tokens=500)
        assert config.max_tokens == 500
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="gpt-4", max_tokens=0)
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="gpt-4", max_tokens=-1)


class TestAgentAggregateCreation:
    """Test cases for AgentAggregate creation and validation."""

    def test_create_valid_agent(self) -> None:
        """Test creating a valid agent aggregate."""
        agent = AgentAggregate.create(
            id="agent-123", name="Test Agent", description="A test agent"
        )
        assert agent.id == "agent-123"
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert agent.status == AgentStatus.INACTIVE
        assert agent.configuration.model_name == "gpt-4"
        assert agent.capabilities == []
        assert agent.training_sessions == []

    def test_create_agent_minimal(self) -> None:
        """Test creating agent with minimal required fields."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        assert agent.id == "agent-123"
        assert agent.name == "Test Agent"
        assert agent.status == AgentStatus.INACTIVE
        assert isinstance(agent.configuration, AgentConfiguration)

    def test_create_agent_empty_name(self) -> None:
        """Test creating agent with empty name fails."""
        with pytest.raises(ValidationError, match="Agent name cannot be empty"):
            AgentAggregate.create(id="agent-123", name="")

    def test_create_agent_whitespace_name(self) -> None:
        """Test creating agent with whitespace-only name fails."""
        with pytest.raises(ValidationError, match="Agent name cannot be empty"):
            AgentAggregate.create(id="agent-123", name="   ")

    def test_validate_invariants_unique_capabilities(self) -> None:
        """Test that duplicate capabilities are rejected."""
        agent = AgentAggregate(
            id="agent-123",
            name="Test Agent",
            capabilities=["chat", "chat"],  # Duplicate
        )
        with pytest.raises(ValueError, match="Agent capabilities must be unique"):
            agent.validate_invariants()


class TestAgentAggregateActivation:
    """Test cases for agent activation/deactivation."""

    @pytest.fixture
    def inactive_agent(self) -> AgentAggregate:
        """Create an inactive agent for testing."""
        return AgentAggregate.create(id="agent-123", name="Test Agent")

    @pytest.fixture
    def active_agent(self) -> AgentAggregate:
        """Create an active agent for testing."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        return agent.activate()

    def test_activate_inactive_agent(self, inactive_agent: AgentAggregate) -> None:
        """Test activating an inactive agent."""
        assert inactive_agent.status == AgentStatus.INACTIVE
        activated = inactive_agent.activate()
        assert activated.status == AgentStatus.ACTIVE
        assert activated.id == inactive_agent.id
        assert activated.version > inactive_agent.version
        events = activated.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentActivated"
        assert events[0].aggregate_id == "agent-123"

    def test_activate_already_active_agent(self, active_agent: AgentAggregate) -> None:
        """Test activating an already active agent fails."""
        with pytest.raises(ValueError, match="Agent must be active to deactivate"):
            active_agent.activate()

    def test_deactivate_active_agent(self, active_agent: AgentAggregate) -> None:
        """Test deactivating an active agent."""
        assert active_agent.status == AgentStatus.ACTIVE
        deactivated = active_agent.deactivate()
        assert deactivated.status == AgentStatus.INACTIVE
        assert deactivated.id == active_agent.id
        events = deactivated.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentDeactivated"

    def test_deactivate_inactive_agent(self, inactive_agent: AgentAggregate) -> None:
        """Test deactivating an inactive agent fails."""
        with pytest.raises(ValueError, match="Agent must be active to deactivate"):
            inactive_agent.deactivate()


class TestAgentAggregateTraining:
    """Test cases for agent training functionality."""

    @pytest.fixture
    def agent(self) -> AgentAggregate:
        """Create an agent for training tests."""
        return AgentAggregate.create(id="agent-123", name="Test Agent")

    def test_start_training_valid(self, agent: AgentAggregate) -> None:
        """Test starting training with valid parameters."""
        training_params = {"epochs": 10, "learning_rate": 0.001}
        training_agent = agent.start_training(
            dataset_id="dataset-456", params=training_params
        )
        assert training_agent.status == AgentStatus.TRAINING
        assert len(training_agent.training_sessions) == 1
        session = training_agent.training_sessions[0]
        assert session["dataset_id"] == "dataset-456"
        assert session["params"] == training_params
        assert session["status"] == "STARTED"
        assert "started_at" in session
        events = training_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentTrainingStarted"
        assert events[0].data["dataset_id"] == "dataset-456"

    def test_start_training_empty_dataset_id(self, agent: AgentAggregate) -> None:
        """Test starting training with empty dataset ID fails."""
        with pytest.raises(ValueError, match="Dataset ID cannot be empty"):
            agent.start_training(dataset_id="")

    def test_start_training_already_training(self, agent: AgentAggregate) -> None:
        """Test starting training when already training fails."""
        training_agent = agent.start_training(dataset_id="dataset-456")
        with pytest.raises(ValueError, match="Agent is already training"):
            training_agent.start_training(dataset_id="dataset-789")

    def test_complete_training_success(self, agent: AgentAggregate) -> None:
        """Test completing training successfully."""
        training_agent = agent.start_training(dataset_id="dataset-456")
        training_agent.pull_events()  # Clear events
        metrics = {"accuracy": 0.95, "loss": 0.05}
        completed_agent = training_agent.complete_training(metrics=metrics)
        assert completed_agent.status == AgentStatus.ACTIVE
        assert len(completed_agent.training_sessions) == 1
        session = completed_agent.training_sessions[0]
        assert session["status"] == "COMPLETED"
        assert session["metrics"] == metrics
        assert "completed_at" in session
        events = completed_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentTrainingCompleted"

    def test_complete_training_not_training(self, agent: AgentAggregate) -> None:
        """Test completing training when not training fails."""
        with pytest.raises(
            ValueError, match="Agent must be training to complete training"
        ):
            agent.complete_training()


class TestAgentAggregateConfiguration:
    """Test cases for agent configuration management."""

    @pytest.fixture
    def agent(self) -> AgentAggregate:
        """Create an agent for configuration tests."""
        config = AgentConfiguration(
            model_name="gpt-3.5", temperature=0.5, max_tokens=500
        )
        return AgentAggregate.create(
            id="agent-123", name="Test Agent", configuration=config
        )

    def test_update_config_valid(self, agent: AgentAggregate) -> None:
        """Test updating configuration with valid changes."""
        updates = {"model_name": "gpt-4", "temperature": 0.8, "max_tokens": 2000}
        updated_agent = agent.update_config(updates)
        assert updated_agent.configuration.model_name == "gpt-4"
        assert updated_agent.configuration.temperature == pytest.approx(0.8, abs=1e-6)
        assert updated_agent.configuration.max_tokens == 2000
        events = updated_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentConfigUpdated"
        assert "model_name" in events[0].data["keys"]

    def test_update_config_empty(self, agent: AgentAggregate) -> None:
        """Test updating configuration with empty changes fails."""
        with pytest.raises(ValueError, match="Configuration updates cannot be empty"):
            agent.update_config({})

    def test_update_config_invalid(self, agent: AgentAggregate) -> None:
        """Test updating configuration with invalid values fails."""
        invalid_updates = {"temperature": 3.0}  # Invalid temperature
        with pytest.raises(ValueError, match="Invalid configuration update"):
            agent.update_config(invalid_updates)


class TestAgentAggregateCapabilities:
    """Test cases for agent capability management."""

    @pytest.fixture
    def agent(self) -> AgentAggregate:
        """Create an agent for capability tests."""
        return AgentAggregate.create(
            id="agent-123", name="Test Agent", capabilities=["chat"]
        )

    def test_add_capability_valid(self, agent: AgentAggregate) -> None:
        """Test adding a valid capability."""
        updated_agent = agent.add_capability("planning")
        assert "planning" in updated_agent.capabilities
        assert "chat" in updated_agent.capabilities  # Original should remain
        assert len(updated_agent.capabilities) == 2
        events = updated_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentCapabilityAdded"
        assert events[0].data["capability"] == "planning"

    def test_add_capability_empty(self, agent: AgentAggregate) -> None:
        """Test adding empty capability fails."""
        with pytest.raises(ValueError, match="Capability cannot be empty"):
            agent.add_capability("")

    def test_add_capability_duplicate(self, agent: AgentAggregate) -> None:
        """Test adding duplicate capability fails."""
        with pytest.raises(ValueError, match="Capability 'chat' already exists"):
            agent.add_capability("chat")

    def test_remove_capability_valid(self, agent: AgentAggregate) -> None:
        """Test removing an existing capability."""
        updated_agent = agent.remove_capability("chat")
        assert "chat" not in updated_agent.capabilities
        assert len(updated_agent.capabilities) == 0
        events = updated_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentCapabilityRemoved"
        assert events[0].data["capability"] == "chat"

    def test_remove_capability_not_exists(self, agent: AgentAggregate) -> None:
        """Test removing non-existent capability fails."""
        with pytest.raises(ValueError, match="Capability 'nonexistent' not found"):
            agent.remove_capability("nonexistent")


class TestAgentAggregateErrorHandling:
    """Test cases for agent error handling."""

    @pytest.fixture
    def agent(self) -> AgentAggregate:
        """Create an agent for error handling tests."""
        return AgentAggregate.create(id="agent-123", name="Test Agent")

    def test_mark_error_valid(self, agent: AgentAggregate) -> None:
        """Test marking agent with error."""
        error_agent = agent.mark_error("Connection timeout")
        assert error_agent.status == AgentStatus.ERROR
        events = error_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentErrored"
        assert events[0].data["reason"] == "Connection timeout"

    def test_mark_error_empty_reason(self, agent: AgentAggregate) -> None:
        """Test marking error with empty reason fails."""
        with pytest.raises(ValueError, match="Error reason cannot be empty"):
            agent.mark_error("")


class TestAgentAggregateImmutability:
    """Test cases for aggregate immutability."""

    def test_aggregate_immutability(self) -> None:
        """Test that aggregates are immutable."""
        agent1 = AgentAggregate.create(id="agent-123", name="Test Agent")
        agent2 = agent1.activate()
        assert agent1.status == AgentStatus.INACTIVE
        assert agent2.status == AgentStatus.ACTIVE
        assert agent1.version == 0
        assert agent2.version == 1

    def test_event_collection_isolation(self) -> None:
        """Test that events are properly isolated between instances."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        agent1 = agent.activate()
        events1 = agent1.pull_events()
        assert len(events1) == 1
        agent2 = agent.activate()
        events2 = agent2.pull_events()
        assert len(events2) == 1
        assert events1[0].event_id != events2[0].event_id


class TestAgentAggregateEventGeneration:
    """Test cases for domain event generation."""

    def test_event_structure(self) -> None:
        """Test that generated events have correct structure."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        activated = agent.activate()
        events = activated.pull_events()
        assert len(events) == 1
        event = events[0]
        assert event.aggregate_type == "agent"
        assert event.aggregate_id == "agent-123"
        assert event.event_type == "AgentActivated"
        assert isinstance(event.timestamp, str)
        assert event.data == {}
        assert event.metadata["version"] == 1

    def test_multiple_events(self) -> None:
        """Test generating multiple events in sequence."""
        agent = AgentAggregate.create(id="agent-123", name="Test Agent")
        agent = agent.activate()
        agent = agent.add_capability("planning")
        agent = agent.update_config({"temperature": 0.8})
        events = agent.pull_events()
        assert len(events) == 3
        event_types = [e.event_type for e in events]
        assert "AgentActivated" in event_types
        assert "AgentCapabilityAdded" in event_types
        assert "AgentConfigUpdated" in event_types


class TestAgentAggregateWorkflow:
    """Integration tests for complete agent workflows."""

    def test_complete_agent_lifecycle(self) -> None:
        """Test complete agent lifecycle from creation to training completion."""
        agent = AgentAggregate.create(
            id="agent-123",
            name="ML Agent",
            configuration=AgentConfiguration(model_name="gpt-4"),
        )
        agent = agent.activate()
        assert agent.status == AgentStatus.ACTIVE
        agent = agent.add_capability("ml_training")
        agent = agent.add_capability("data_analysis")
        assert len(agent.capabilities) == 2
        agent = agent.start_training(
            dataset_id="ml-dataset-456", params={"epochs": 100, "batch_size": 32}
        )
        assert agent.status == AgentStatus.TRAINING
        assert len(agent.training_sessions) == 1
        agent = agent.complete_training(metrics={"accuracy": 0.92})
        assert agent.status == AgentStatus.ACTIVE
        assert agent.training_sessions[0]["status"] == "COMPLETED"
        all_events = []
        for op in [
            agent.activate(),
            agent.add_capability("test"),
            agent.start_training("test"),
            agent.complete_training(),
        ]:
            all_events.extend(op.pull_events())
        event_types = {e.event_type for e in all_events}
        expected_events = {
            "AgentActivated",
            "AgentCapabilityAdded",
            "AgentTrainingStarted",
            "AgentTrainingCompleted",
        }
        assert expected_events.issubset(event_types)


@pytest.fixture
def value_error():
    """Fixture for ValueError"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def e():
    """Fixture for e"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def isinstance_fixture():
    """Fixture for isinstance"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def op():
    """Fixture for op"""
    return None  # TODO: Define appropriate fixture


__all__ = [
    "TestAgentAggregateActivation",
    "TestAgentAggregateCapabilities",
    "TestAgentAggregateConfiguration",
    "TestAgentAggregateCreation",
    "TestAgentAggregateErrorHandling",
    "TestAgentAggregateEventGeneration",
    "TestAgentAggregateImmutability",
    "TestAgentAggregateTraining",
    "TestAgentAggregateWorkflow",
    "TestAgentConfiguration",
]
