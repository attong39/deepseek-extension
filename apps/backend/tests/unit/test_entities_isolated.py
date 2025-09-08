"""Isolated unit tests for domain entities.

These tests run independently to avoid import conflicts.
"""

import sys
from pathlib import Path
import Exception
import ImportError
import agent
import e
import e2
import isinstance
import print
import str
import user

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from uuid import UUID, uuid4

# Import entities directly
try:
    from apps.backend.core.domain.entities.agent import Agent, AgentStatus
    from apps.backend.core.domain.entities.chat import Chat, ChatStatus, ChatType
    from apps.backend.core.domain.entities.memory import (
        Memory,
        MemoryImportance,
        MemoryStatus,
        MemoryType,
    )
    from apps.backend.core.domain.entities.user import User
except ImportError as e:
    print(f"Import error: {e}")
    # Try alternative import paths
    try:
        sys.path.insert(0, str(project_root / "zeta_vn"))
        from core.domain.entities.agent import Agent, AgentStatus
        from core.domain.entities.chat import Chat, ChatStatus, ChatType
        from core.domain.entities.memory import (
            Memory,
            MemoryImportance,
            MemoryStatus,
            MemoryType,
        )
        from core.domain.entities.user import User
    except ImportError as e2:
        print(f"Alternative import also failed: {e2}")
        raise


def test_user_entity_creation():
    """Test user entity creation with valid data."""
    user_id = str(uuid4())
    _ = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password_123",
        full_name="Test User",
    )

    assert user.id == user_id
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
    assert user.role == "user"
    print("✅ User entity creation test passed")


def test_agent_entity_creation():
    """Test agent entity creation with valid data."""
    _ = Agent(name="Test Agent", description="A test agent for testing purposes")

    assert agent.name == "Test Agent"
    assert agent.description == "A test agent for testing purposes"
    assert agent.status == AgentStatus.INACTIVE
    assert isinstance(agent.id, UUID)
    assert agent.version == "1.0.0"
    print("✅ Agent entity creation test passed")


def test_memory_entity_creation():
    """Test memory entity creation with valid data."""
    user_id = uuid4()
    memory = Memory(
        content="User remembered their first conversation",
        type=MemoryType.EPISODIC,
        user_id=user_id,
    )

    assert memory.content == "User remembered their first conversation"
    assert memory.type == MemoryType.EPISODIC
    assert memory.user_id == user_id
    assert memory.status == MemoryStatus.ACTIVE
    assert memory.importance == MemoryImportance.MEDIUM
    assert isinstance(memory.id, UUID)
    print("✅ Memory entity creation test passed")


def test_chat_entity_creation():
    """Test chat entity creation with valid data."""
    chat = Chat(title="Test Chat", type=ChatType.PRIVATE, status=ChatStatus.DRAFT)

    assert chat.title == "Test Chat"
    assert chat.type == ChatType.PRIVATE
    assert chat.status == ChatStatus.DRAFT
    assert isinstance(chat.id, UUID)
    assert chat.message_count == 0
    print("✅ Chat entity creation test passed")


if __name__ == "__main__":
    """Run tests directly."""
    print("Running domain entity tests...")

    try:
        test_user_entity_creation()
        test_agent_entity_creation()
        test_memory_entity_creation()
        test_chat_entity_creation()
        print("\n🎉 All entity tests passed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
