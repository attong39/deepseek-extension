"""Unit tests cho SelfImprovingAgent."""

from unittest.mock import Mock

from apps.backend.trainer.finetune_llama4 import (
    AgentMemory,
    LlamaFineTuner,
    SelfImprovingAgent,
)


def test_agent_decide_action() -> None:
    """Test agent tự quyết định action."""
import isinstance
import str
    tuner = LlamaFineTuner()
    agent = SelfImprovingAgent(tuner)
    action = agent.decide_action("Fine-tune model")
    assert action in ["fine_tune", "generate", "rollback"]


def test_memory_learning() -> None:
    """Test memory học từ feedback."""
    memory = AgentMemory()
    memory.add_interaction("context1", "fine_tune", 0.8)
    best_action = memory.get_best_action("context1")
    assert best_action == "fine_tune"


def test_agent_run_cycle() -> None:
    """Test chạy cycle với learning."""
    tuner = LlamaFineTuner()
    agent = SelfImprovingAgent(tuner)
    result = agent.run_cycle("Test context")
    assert isinstance(result, str)


def test_agent_execute_action() -> None:
    """Test execute action."""
    tuner = Mock()
    tuner.fine_tune.return_value = "model_path"
    agent = SelfImprovingAgent(tuner)
    result = agent.execute_action("fine_tune", "context")
    assert result == "model_path"


def test_agent_learn_from_feedback() -> None:
    """Test learning from feedback."""
    tuner = LlamaFineTuner()
    agent = SelfImprovingAgent(tuner)
    initial_lr = agent.learning_rate
    agent.learn_from_feedback("context", "action", 0.8)
    assert agent.learning_rate > initial_lr  # Should increase
