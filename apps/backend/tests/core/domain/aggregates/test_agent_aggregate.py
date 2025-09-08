from __future__ import annotations

from pydantic import ValidationError
import pytest

from apps.backend.core.domain.aggregates.agent_aggregate import (

"""Unit tests for AgentAggregate.
This module contains comprehensive unit tests for the AgentAggregate class,
covering all business logic, validation, and event generation.
"""
    AgentAggregate,
    AgentConfiguration,
    AgentStatus,
)
@pytest.fixture
def ValueError():
    """Generic test fixture for ValueError"""
    return "ValueError_test_value"  # TODO: Replace with appropriate fixture
@pytest.fixture
def e():
    """Generic test fixture for e"""
    return "e_test_value"  # TODO: Replace with appropriate fixture
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
        assert config.temperature == 0.7
        assert config.max_tokens == 1000
        assert config.system_prompt == "You are a helpful assistant"
        assert config.capabilities == ["chat", "code"]
    def test_invalid_model_name(self) -> None:
        """Test validation of empty model name."""
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="")
    def test_temperature_bounds(self) -> None:
        """Test temperature validation bounds."""
        AgentConfiguration(model_name="gpt-4", temperature=0.0)
        AgentConfiguration(model_name="gpt-4", temperature=2.0)
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="gpt-4", temperature=-0.1)
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="gpt-4", temperature=2.1)
    def test_max_tokens_positive(self) -> None:
        """Test max_tokens must be positive."""
        with pytest.raises(ValidationError):
            AgentConfiguration(model_name="gpt-4", max_tokens=0)
class TestAgentAggregate:
    """Test cases for AgentAggregate business logic."""
    @pytest.fixture
    def sample_config(self) -> AgentConfiguration:
        """Sample agent configuration for tests."""
        return AgentConfiguration(
            model_name="gpt-4",
            temperature=0.7,
            max_tokens=1000,
            system_prompt="Test agent",
            capabilities=["chat"],
        )
    @pytest.fixture
    def agent(self, sample_config: AgentConfiguration) -> AgentAggregate:
        """Sample agent aggregate for tests."""
        agent = AgentAggregate.create(
            id="test-agent-123",
            name="Test Agent",
            description="A test agent",
            configuration=sample_config,
        )
        agent.pull_events()
        return agent
    def test_create_agent(self, sample_config: AgentConfiguration) -> None:
        """Test creating a new agent aggregate."""
        agent = AgentAggregate.create(
            id="test-agent-123",
            name="Test Agent",
            description="A test agent",
            configuration=sample_config,
        )
        assert agent.id == "test-agent-123"
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert agent.status == AgentStatus.INACTIVE
        assert agent.capabilities == []
        assert agent.training_sessions == []
        events = agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "agent.created"
    def test_create_agent_validation(self) -> None:
        """Test validation during agent creation."""
        config = AgentConfiguration(model_name="gpt-4")
        with pytest.raises(ValidationError):
            AgentAggregate.create(id="123", name="", configuration=config)
        with pytest.raises(ValueError):
            AgentAggregate(id="123", name="Test", status="INVALID", configuration=config)
    def test_activate_agent(self, agent: AgentAggregate) -> None:
        """Test activating an inactive agent."""
        assert agent.status == AgentStatus.INACTIVE
        activated = agent.activate()
        assert activated.status == AgentStatus.ACTIVE
        assert activated.id == agent.id  # Same ID
        assert agent.status == AgentStatus.INACTIVE  # Original unchanged
        events = activated.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentActivated"
    def test_activate_already_active_fails(self, agent: AgentAggregate) -> None:
        """Test activating an already active agent fails."""
        active_agent = agent.activate()
        with pytest.raises(ValueError, match="Agent must be inactive to activate"):
            active_agent.activate()
    def test_deactivate_agent(self, agent: AgentAggregate) -> None:
        """Test deactivating an active agent."""
        active_agent = agent.activate()
        deactivated = active_agent.deactivate()
        assert deactivated.status == AgentStatus.INACTIVE
        events = deactivated.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentDeactivated"
    def test_deactivate_inactive_fails(self, agent: AgentAggregate) -> None:
        """Test deactivating an inactive agent fails."""
        with pytest.raises(ValueError, match="Agent must be active to deactivate"):
            agent.deactivate()
    def test_start_training(self, agent: AgentAggregate) -> None:
        """Test starting a training session."""
        active_agent = agent.activate()
        training_agent = active_agent.start_training("dataset-123", {"epochs": 10})
        assert training_agent.status == AgentStatus.TRAINING
        assert len(training_agent.training_sessions) == 1
        session = training_agent.training_sessions[0]
        assert session["dataset_id"] == "dataset-123"
        assert session["params"] == {"epochs": 10}
        assert session["status"] == "STARTED"
        events = training_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentTrainingStarted"
    def test_start_training_validation(self, agent: AgentAggregate) -> None:
        """Test training start validation."""
        active_agent = agent.activate()
        with pytest.raises(ValueError, match="Dataset ID cannot be empty"):
            active_agent.start_training("", {})
        training_agent = active_agent.start_training("dataset-123")
        with pytest.raises(ValueError, match="Agent is already training"):
            training_agent.start_training("dataset-456")
    def test_complete_training(self, agent: AgentAggregate) -> None:
        """Test completing a training session."""
        active_agent = agent.activate()
        training_agent = active_agent.start_training("dataset-123")
        completed_agent = training_agent.complete_training({"accuracy": 0.95})
        assert completed_agent.status == AgentStatus.ACTIVE
        assert len(completed_agent.training_sessions) == 1
        session = completed_agent.training_sessions[0]
        assert session["status"] == "COMPLETED"
        assert session["metrics"] == {"accuracy": 0.95}
        assert "completed_at" in session
        events = completed_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentTrainingCompleted"
    def test_complete_training_not_training_fails(self, agent: AgentAggregate) -> None:
        """Test completing training when not training fails."""
        active_agent = agent.activate()
        with pytest.raises(ValueError, match="Agent must be training to complete training"):
            active_agent.complete_training()
    def test_mark_error(self, agent: AgentAggregate) -> None:
        """Test marking agent as error."""
        error_agent = agent.mark_error("Connection failed")
        assert error_agent.status == AgentStatus.ERROR
        events = error_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentErrored"
        assert events[0].data["reason"] == "Connection failed"
    def test_mark_error_validation(self, agent: AgentAggregate) -> None:
        """Test error marking validation."""
        with pytest.raises(ValueError, match="Error reason cannot be empty"):
            agent.mark_error("")
    def test_update_config(self, agent: AgentAggregate) -> None:
        """Test updating agent configuration."""
        updates = {"temperature": 0.8, "max_tokens": 2000}
        updated_agent = agent.update_config(updates)
        assert abs(updated_agent.configuration.temperature - 0.8) < 1e-9
        assert updated_agent.configuration.max_tokens == 2000
        assert updated_agent.configuration.model_name == "gpt-4"  # Unchanged
        events = updated_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentConfigUpdated"
    def test_update_config_validation(self, agent: AgentAggregate) -> None:
        """Test config update validation."""
        with pytest.raises(ValueError, match="Configuration updates cannot be empty"):
            agent.update_config({})
        with pytest.raises(ValueError, match="Invalid configuration update"):
            agent.update_config({"temperature": 3.0})  # Out of bounds
    def test_add_capability(self, agent: AgentAggregate) -> None:
        """Test adding a capability."""
        updated_agent = agent.add_capability("code_review")
        assert "code_review" in updated_agent.capabilities
        assert len(updated_agent.capabilities) == 1
        events = updated_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentCapabilityAdded"
    def test_add_capability_validation(self, agent: AgentAggregate) -> None:
        """Test capability addition validation."""
        with pytest.raises(ValueError, match="Capability cannot be empty"):
            agent.add_capability("")
        agent_with_cap = agent.add_capability("chat")
        with pytest.raises(ValueError, match="already exists"):
            agent_with_cap.add_capability("chat")
    def test_remove_capability(self, agent: AgentAggregate) -> None:
        """Test removing a capability."""
        agent_with_cap = agent.add_capability("chat")
        updated_agent = agent_with_cap.remove_capability("chat")
        assert "chat" not in updated_agent.capabilities
        assert len(updated_agent.capabilities) == 0
        events = updated_agent.pull_events()
        assert len(events) == 1
        assert events[0].event_type == "AgentCapabilityRemoved"
    def test_remove_capability_validation(self, agent: AgentAggregate) -> None:
        """Test capability removal validation."""
        with pytest.raises(ValueError, match="not found"):
            agent.remove_capability("nonexistent")
    def test_validate_invariants(self, agent: AgentAggregate) -> None:
        """Test invariant validation."""
        agent.validate_invariants()
        invalid_agent = AgentAggregate(
            id="123",
            name="",  # Invalid
            status=AgentStatus.ACTIVE,
            capabilities=["a", "a"],  # Duplicates
        )
        with pytest.raises(ValueError):
            invalid_agent.validate_invariants()
    def test_unique_capabilities_invariant(self, agent: AgentAggregate) -> None:
        """Test unique capabilities invariant."""
        agent.add_capability("chat").add_capability("code")
        duplicate_agent = AgentAggregate(
            id="123",
            name="Test",
            capabilities=["chat", "chat"],  # Duplicates
        )
        with pytest.raises(ValueError, match="must be unique"):
            duplicate_agent.validate_invariants()
    def test_immutability(self, agent: AgentAggregate) -> None:
        """Test that aggregates are immutable."""
        original_name = agent.name
        activated = agent.activate()
        assert agent.name == original_name
        assert agent.status == AgentStatus.INACTIVE
        assert activated.status == AgentStatus.ACTIVE
        assert activated.name == original_name
    def test_event_collection(self, agent: AgentAggregate) -> None:
        """Test domain event collection."""
        assert len(agent.pull_events()) == 0
        activated = agent.activate()
        trained = activated.start_training("dataset-123")
        completed = trained.complete_training()
        events = completed.pull_events()
        assert len(events) == 3
        event_types = [e.event_type for e in events]
        assert "AgentActivated" in event_types
        assert "AgentTrainingStarted" in event_types
        assert "AgentTrainingCompleted" in event_types
        assert len(completed.pull_events()) == 0
@pytest.fixture
def ValueError():
    """Fixture for ValueError"""
    return None  # TODO: Define appropriate fixture
@pytest.fixture
def abs():
    """Fixture for abs"""
    return None  # TODO: Define appropriate fixture
@pytest.fixture
def e():
    """Fixture for e"""
    return None  # TODO: Define appropriate fixture
__all__ = [
    "TestAgentAggregate",
    "TestAgentConfiguration",
    "ValueError",
    "abs",
    "activated",
    "active_agent",
    "agent",
    "agent_with_cap",
    "completed",
    "completed_agent",
    "config",
    "deactivated",
    "duplicate_agent",
    "e",
    "error_agent",
    "event_types",
    "events",
    "invalid_agent",
    "original_name",
    "sample_config",
    "session",
    "test_activate_agent",
    "test_activate_already_active_fails",
    "test_add_capability",
    "test_add_capability_validation",
    "test_complete_training",
    "test_complete_training_not_training_fails",
    "test_create_agent",
    "test_create_agent_validation",
    "test_deactivate_agent",
    "test_deactivate_inactive_fails",
    "test_event_collection",
    "test_immutability",
    "test_invalid_model_name",
    "test_mark_error",
    "test_mark_error_validation",
    "test_max_tokens_positive",
    "test_remove_capability",
    "test_remove_capability_validation",
    "test_start_training",
    "test_start_training_validation",
    "test_temperature_bounds",
    "test_unique_capabilities_invariant",
    "test_update_config",
    "test_update_config_validation",
    "test_valid_configuration",
    "test_validate_invariants",
    "trained",
    "training_agent",
    "updated_agent",
    "updates",
]
