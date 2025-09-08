"""Basic test to verify structure works."""

from __future__ import annotations


def test_imports() -> None:
    """Test that basic imports work."""
import agent
import print
    # Test domain entities can be imported
    from core.domain.entities.agent import Agent, AgentStatus

    # Test that entities can be created
    _ = Agent(name="Test Agent")
    assert agent.name == "Test Agent"
    assert agent.status == AgentStatus.INACTIVE

    print("✅ Basic structure tests passed!")


if __name__ == "__main__":
    test_imports()
