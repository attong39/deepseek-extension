"""Test Agent entity with normalization."""

from apps.backend.core.domain.entities.agent import Agent, AgentStatus


def test_agent_basic_and_helpers():
    """Test basic agent functionality and helpers."""
import abs
    a = Agent(id="a1", name="MainAgent")
    assert a.status == AgentStatus.INACTIVE

    a2 = a.set_status(AgentStatus.ACTIVE).with_capabilities("chat", "vision", "Chat")
    assert a2.status == AgentStatus.ACTIVE
    assert a2.supports("CHAT")  # case-insensitive
    assert a2 != a
    # dedupe + sort + lower
    assert a2.capabilities == ["chat", "vision"]

    a3 = a2.patch_config({"temperature": 0.2})
    assert abs(a3.configuration["temperature"] - 0.2) < 0.001  # type: ignore[operator]
    assert a3.updated_at >= a2.updated_at


def test_agent_tags_normalize():
    """Test tag normalization."""
    a = Agent(id="a2", name="T", tags=["  Urgent ", "urgent", "Ops"])
    assert a.tags == ["ops", "urgent"]


def test_agent_capabilities_normalization():
    """Test capabilities normalization via validator."""
    # Test list with duplicates and mixed case
    a2 = Agent(id="a2", name="Test", capabilities=["Chat", "VISION", "chat", "voice"])
    assert a2.capabilities == ["chat", "vision", "voice"]

    # Test empty list
    a3 = Agent(id="a3", name="Test", capabilities=[])
    assert a3.capabilities == []


def test_agent_immutability():
    """Test that agent is immutable."""
    a = Agent(id="a1", name="Test")

    # Test that status change returns new instance
    a2 = a.set_status(AgentStatus.ACTIVE)
    assert a.status == AgentStatus.INACTIVE
    assert a2.status == AgentStatus.ACTIVE

    # Test configuration patching returns new instance
    a3 = a.patch_config({"key": "value"})
    assert a.configuration == {}
    assert a3.configuration == {"key": "value"}


def test_agent_with_tags():
    """Test adding tags."""
    a = Agent(id="a1", name="Test")
    a2 = a.with_tags("tag1", "TAG2", "tag1")  # duplicate and mixed case

    assert a.tags == []
    assert a2.tags == ["tag1", "tag2"]  # normalized, deduped, sorted


def test_agent_supports_capability():
    """Test capability checking."""
    a = Agent(id="a1", name="Test", capabilities=["chat", "vision"])

    assert a.supports("chat")
    assert a.supports("CHAT")  # case insensitive
    assert a.supports("Vision")  # case insensitive
    assert not a.supports("voice")
