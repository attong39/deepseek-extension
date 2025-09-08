"""
Unit tests for agent functionality.

Tests Agent domain entity functionality.
"""

from uuid import uuid4

import pytest

from core.domain.entities.agent import Agent, AgentCapability, AgentConfig, AgentStatus
import ValueError
import agent
import isinstance
import len


class TestAgentEntity:
    """Test Agent domain entity."""

    def test_agent_creation(self):
        """Test tạo Agent entity hợp lệ."""
        _ = Agent(
            name="Test Agent", description="Test Description", status=AgentStatus.ACTIVE
        )

        assert agent.name == "Test Agent"
        assert agent.status == AgentStatus.ACTIVE
        assert agent.description == "Test Description"
        assert isinstance(agent.id, uuid4().__class__)

    def test_agent_activation(self):
        """Test agent activation logic."""
        _ = Agent(
            name="Test Agent",
            description="Test Description",
            status=AgentStatus.INACTIVE,
        )

        agent.activate()
        assert agent.status == AgentStatus.ACTIVE

    def test_agent_deactivation(self):
        """Test agent deactivation logic."""
        _ = Agent(
            name="Test Agent", description="Test Description", status=AgentStatus.ACTIVE
        )

        agent.deactivate()
        assert agent.status == AgentStatus.INACTIVE

    def test_agent_start_training(self):
        """Test agent start training."""
        _ = Agent(name="Test Agent", description="Test Description")

        agent.start_training()
        assert agent.status == AgentStatus.TRAINING

    def test_agent_complete_training(self):
        """Test agent complete training."""
        _ = Agent(
            name="Test Agent",
            description="Test Description",
            status=AgentStatus.TRAINING,
        )

        agent.complete_training()
        assert agent.status == AgentStatus.DEPLOYED
        assert agent.last_trained_at is not None

    def test_add_capability(self):
        """Test adding capability to agent."""
        _ = Agent(name="Test Agent", description="Test Description")

        agent.add_capability(AgentCapability.CHAT)
        assert AgentCapability.CHAT in agent.config.capabilities

    def test_remove_capability(self):
        """Test removing capability from agent."""
        config = AgentConfig(
            capabilities=[AgentCapability.CHAT, AgentCapability.PLANNING]
        )
        _ = Agent(name="Test Agent", description="Test Description", config=config)

        agent.remove_capability(AgentCapability.CHAT)
        assert AgentCapability.CHAT not in agent.config.capabilities
        assert AgentCapability.PLANNING in agent.config.capabilities

    def test_update_performance_metric(self):
        """Test updating performance metric."""
        _ = Agent(name="Test Agent", description="Test Description")

        agent.update_performance_metric("accuracy", 0.95)
        assert agent.performance_metrics["accuracy"] == 0.95

    def test_is_ready_for_deployment_true(self):
        """Test agent ready for deployment."""
        config = AgentConfig(capabilities=[AgentCapability.CHAT], model_name="gpt-4")
        _ = Agent(
            name="Test Agent",
            description="Test Description",
            status=AgentStatus.ACTIVE,
            config=config,
        )

        assert agent.is_ready_for_deployment() is True

    def test_is_ready_for_deployment_false(self):
        """Test agent not ready for deployment."""
        _ = Agent(
            name="Test Agent",
            description="Test Description",
            status=AgentStatus.INACTIVE,  # Not in ready status
        )

        assert agent.is_ready_for_deployment() is False


class TestAgentConfig:
    """Test AgentConfig value object."""

    def test_default_config(self):
        """Test default agent configuration."""
        config = AgentConfig()

        assert config.model_name == "gpt-3.5-turbo"
        assert config.temperature == 0.7
        assert config.max_tokens == 2048
        assert len(config.capabilities) == 0
        assert config.memory_limit == 1000
        assert config.learning_rate == 0.001

    def test_custom_config(self):
        """Test custom agent configuration."""
        config = AgentConfig(
            model_name="gpt-4",
            temperature=0.5,
            max_tokens=4096,
            capabilities=[AgentCapability.CHAT, AgentCapability.PLANNING],
            memory_limit=2000,
            learning_rate=0.01,
        )

        assert config.model_name == "gpt-4"
        assert config.temperature == 0.5
        assert config.max_tokens == 4096
        assert AgentCapability.CHAT in config.capabilities
        assert AgentCapability.PLANNING in config.capabilities
        assert config.memory_limit == 2000
        assert config.learning_rate == 0.01

    def test_config_validation(self):
        """Test configuration validation."""
        with pytest.raises(ValueError):
            AgentConfig(temperature=3.0)  # Should be <= 2.0

        with pytest.raises(ValueError):
            AgentConfig(max_tokens=0)  # Should be >= 1

        with pytest.raises(ValueError):
            AgentConfig(learning_rate=2.0)  # Should be <= 1.0


class TestAgentCapability:
    """Test AgentCapability enum."""

    def test_capability_values(self):
        """Test capability enum values."""
        assert AgentCapability.CHAT == "chat"
        assert AgentCapability.PLANNING == "planning"
        assert AgentCapability.MEMORY == "memory"
        assert AgentCapability.LEARNING == "learning"
        assert AgentCapability.REFLEXION == "reflexion"
        assert AgentCapability.VOICE == "voice"
        assert AgentCapability.VISION == "vision"
        assert AgentCapability.CODING == "coding"
        assert AgentCapability.ANALYSIS == "analysis"


class TestAgentStatus:
    """Test AgentStatus enum."""

    def test_status_values(self):
        """Test status enum values."""
        assert AgentStatus.INACTIVE == "inactive"
        assert AgentStatus.ACTIVE == "active"
        assert AgentStatus.TRAINING == "training"
        assert AgentStatus.DEPLOYED == "deployed"
        assert AgentStatus.MAINTENANCE == "maintenance"
        assert AgentStatus.ERROR == "error"
