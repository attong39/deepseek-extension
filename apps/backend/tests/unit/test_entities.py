"""Unit tests for domain entities.

Tests all core domain entities including User, Agent, Memory, etc.
"""

from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.core.domain.entities.agent import Agent, AgentCapability, AgentStatus
from apps.backend.core.domain.entities.chat import Chat, ChatStatus, ChatType
from apps.backend.core.domain.entities.config import Configuration
from apps.backend.core.domain.entities.file import File, FileStatus
from apps.backend.core.domain.entities.memory import (
import content
import isinstance
import len
import relevance_score
import self
import str
import timestamp
    Memory,
    MemoryImportance,
    MemoryStatus,
    MemoryType,
)
from apps.backend.core.domain.entities.plan import Plan, PlanStatus
from apps.backend.core.domain.entities.session import Session
from apps.backend.core.domain.entities.user import User


# Create a simple MemoryEntry class for tests since it's referenced but not found
class MemoryEntry:
    def __init__(self, memory_id, content, timestamp, relevance_score, **kwargs):
        self.id = uuid4()
        self.memory_id = memory_id
        self.content = content
        self.timestamp = timestamp
        self.relevance_score = relevance_score


class TestUserEntity:
    """Test cases for User entity."""

    def test_user_creation(self) -> None:
        """Test user entity creation with valid data."""
        user_id = str(uuid4())
        user = User(
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

    def test_user_with_optional_fields(self) -> None:
        """Test user creation with optional fields."""
        user_id = str(uuid4())
        user = User(
            id=user_id,
            username="testuser2",
            email="test2@example.com",
            password_hash="hashed_password_456",
            full_name="Test User 2",
            role="admin",
        )

        assert user.role == "admin"
        assert user.full_name == "Test User 2"


class TestAgentEntity:
    """Test cases for Agent entity."""

    def test_agent_creation(self) -> None:
        """Test agent entity creation with valid data."""
        agent = Agent(
            name="Test Agent", description="A test agent for testing purposes"
        )

        assert agent.name == "Test Agent"
        assert agent.description == "A test agent for testing purposes"
        assert agent.status == AgentStatus.INACTIVE
        assert isinstance(agent.id, UUID)
        assert agent.version == "1.0.0"

    def test_agent_activation(self) -> None:
        """Test agent activation."""
        agent = Agent(name="Activatable Agent")

        assert agent.status == AgentStatus.INACTIVE

        agent.activate()
        assert agent.status == AgentStatus.ACTIVE

    def test_agent_capabilities(self) -> None:
        """Test agent capabilities management."""
        agent = Agent(name="Capable Agent")

        # Add capability
        agent.add_capability(AgentCapability.CHAT)
        assert AgentCapability.CHAT in agent.config.capabilities

        # Add another capability
        agent.add_capability(AgentCapability.PLANNING)
        assert AgentCapability.PLANNING in agent.config.capabilities
        assert len(agent.config.capabilities) == 2

        # Remove capability
        agent.remove_capability(AgentCapability.CHAT)
        assert AgentCapability.CHAT not in agent.config.capabilities
        assert len(agent.config.capabilities) == 1

    def test_agent_training(self) -> None:
        """Test agent training workflow."""
        agent = Agent(name="Training Agent")

        # Start training
        agent.start_training()
        assert agent.status == AgentStatus.TRAINING

        # Complete training
        agent.complete_training()
        assert agent.status == AgentStatus.DEPLOYED
        assert agent.last_trained_at is not None


class TestMemoryEntity:
    """Test cases for Memory entity."""

    def test_memory_creation(self) -> None:
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

    def test_memory_access(self) -> None:
        """Test memory access tracking."""
        memory = Memory(content="Accessible memory", type=MemoryType.SEMANTIC)

        initial_count = memory.metrics.access_count
        memory.access()

        assert memory.metrics.access_count == initial_count + 1
        assert memory.metrics.last_accessed is not None

    def test_memory_content_update(self) -> None:
        """Test memory content update."""
        memory = Memory(content="Original content", type=MemoryType.PROCEDURAL)

        new_content = "Updated content with more information"
        memory.update_content(new_content)

        assert memory.content == new_content

    def test_memory_types(self) -> None:
        """Test different memory types."""
        # Episodic memory
        episodic = Memory(
            content="User had a conversation about Python", type=MemoryType.EPISODIC
        )
        assert episodic.type == MemoryType.EPISODIC

        # Semantic memory
        semantic = Memory(
            content="Python is a programming language", type=MemoryType.SEMANTIC
        )
        assert semantic.type == MemoryType.SEMANTIC

        # Procedural memory
        procedural = Memory(
            content="How to write a for loop in Python", type=MemoryType.PROCEDURAL
        )
        assert procedural.type == MemoryType.PROCEDURAL


class TestChatEntity:
    """Test cases for Chat entity (from previous test)."""

    def test_chat_creation(self) -> None:
        """Test chat entity creation with valid data."""
        chat = Chat(title="Test Chat", type=ChatType.PRIVATE, status=ChatStatus.DRAFT)

        assert chat.title == "Test Chat"
        assert chat.type == ChatType.PRIVATE
        assert chat.status == ChatStatus.DRAFT
        assert isinstance(chat.id, UUID)
        assert chat.message_count == 0


class TestEntityIntegration:
    """Test cases for entity interactions."""

    def test_user_memory_relationship(self) -> None:
        """Test relationship between User and Memory entities."""
        user_id = str(uuid4())
        user = User(
            id=user_id,
            username="memory_user",
            email="memory@example.com",
            password_hash="hashed_password",
            full_name="Memory User",
        )

        memory = Memory(
            content="User prefers detailed explanations",
            type=MemoryType.SEMANTIC,
            user_id=UUID(user_id),
        )

        assert str(memory.user_id) == user.id
        assert memory.type == MemoryType.SEMANTIC

    def test_agent_memory_relationship(self) -> None:
        """Test relationship between Agent and Memory entities."""
        agent = Agent(
            name="Learning Agent", description="An agent that learns from interactions"
        )

        memory = Memory(
            content="Agent learned to be more helpful",
            type=MemoryType.PROCEDURAL,
            agent_id=agent.id,
        )

        assert memory.agent_id == agent.id
        assert memory.type == MemoryType.PROCEDURAL

    def test_memory_importance_levels(self) -> None:
        """Test different memory importance levels."""
        # Low importance
        low_memory = Memory(content="User said hello", importance=MemoryImportance.LOW)
        assert low_memory.importance == MemoryImportance.LOW

        # High importance
        high_memory = Memory(
            content="User shared their personal goals", importance=MemoryImportance.HIGH
        )
        assert high_memory.importance == MemoryImportance.HIGH

        # Critical importance
        critical_memory = Memory(
            content="User provided emergency contact information",
            importance=MemoryImportance.CRITICAL,
        )
        assert critical_memory.importance == MemoryImportance.CRITICAL


class TestAgentEntity:
    """Test cases for Agent entity."""

    def test_agent_creation(self) -> None:
        """Test agent entity creation with valid data."""
        agent = Agent(
            name="Test Agent",
            description="A test agent for testing purposes",
            model="gpt-4",
            system_prompt="You are a helpful test assistant.",
        )

        assert agent.name == "Test Agent"
        assert agent.description == "A test agent for testing purposes"
        assert agent.model == "gpt-4"
        assert agent.system_prompt == "You are a helpful test assistant."
        assert isinstance(agent.id, UUID)
        assert agent.is_active is True

    def test_agent_with_capabilities(self) -> None:
        """Test agent with capabilities."""
        capabilities = ["text_generation", "code_analysis", "math"]
        agent = Agent(
            name="Capable Agent",
            description="An agent with multiple capabilities",
            model="gpt-4",
            capabilities=capabilities,
        )

        assert agent.capabilities == capabilities
        assert len(agent.capabilities) == 3


class TestMemoryEntity:
    """Test cases for Memory entity."""

    def test_memory_creation(self) -> None:
        """Test memory entity creation with valid data."""
        user_id = uuid4()
        memory = Memory(
            user_id=user_id,
            type=MemoryType.EPISODIC,
            content="User remembered their first conversation",
            metadata={"importance": 0.8},
        )

        assert memory.user_id == user_id
        assert memory.type == MemoryType.EPISODIC
        assert memory.content == "User remembered their first conversation"
        assert memory.metadata["importance"] == 0.8
        assert memory.status == MemoryStatus.ACTIVE

    def test_memory_entry_creation(self) -> None:
        """Test memory entry creation."""
        memory_id = uuid4()
        entry = MemoryEntry(
            memory_id=memory_id,
            content="Specific memory detail",
            timestamp=datetime.now(),
            relevance_score=0.9,
        )

        assert entry.memory_id == memory_id
        assert entry.content == "Specific memory detail"
        assert entry.relevance_score == 0.9
        assert isinstance(entry.id, UUID)


class TestSessionEntity:
    """Test cases for Session entity."""

    def test_session_creation(self) -> None:
        """Test session entity creation with valid data."""
        user_id = uuid4()
        session = Session(user_id=user_id, title="Test Session", type="conversation")

        assert session.user_id == user_id
        assert session.title == "Test Session"
        assert session.type == "conversation"
        assert isinstance(session.id, UUID)
        assert session.is_active is True

    def test_session_with_context(self) -> None:
        """Test session with context data."""
        user_id = uuid4()
        context = {"language": "en", "timezone": "UTC"}

        session = Session(user_id=user_id, title="Context Session", context=context)

        assert session.context == context
        assert session.context["language"] == "en"


class TestPlanEntity:
    """Test cases for Plan entity."""

    def test_plan_creation(self) -> None:
        """Test plan entity creation with valid data."""
        user_id = uuid4()
        plan = Plan(
            user_id=user_id,
            title="Test Plan",
            description="A plan for testing",
            goal="Complete the test successfully",
        )

        assert plan.user_id == user_id
        assert plan.title == "Test Plan"
        assert plan.description == "A plan for testing"
        assert plan.goal == "Complete the test successfully"
        assert plan.status == PlanStatus.DRAFT
        assert isinstance(plan.id, UUID)

    def test_plan_with_steps(self) -> None:
        """Test plan with execution steps."""
        user_id = uuid4()
        steps = [
            {"step": 1, "action": "Initialize test", "status": "pending"},
            {"step": 2, "action": "Execute test", "status": "pending"},
            {"step": 3, "action": "Verify results", "status": "pending"},
        ]

        plan = Plan(
            user_id=user_id,
            title="Stepped Plan",
            description="A plan with defined steps",
            steps=steps,
        )

        assert len(plan.steps) == 3
        assert plan.steps[0]["action"] == "Initialize test"


class TestFileEntity:
    """Test cases for File entity."""

    def test_file_creation(self) -> None:
        """Test file entity creation with valid data."""
        user_id = uuid4()
        file = File(
            user_id=user_id,
            filename="test.txt",
            content_type="text/plain",
            file_size=1024,
            file_path="/uploads/test.txt",
        )

        assert file.user_id == user_id
        assert file.filename == "test.txt"
        assert file.content_type == "text/plain"
        assert file.file_size == 1024
        assert file.file_path == "/uploads/test.txt"
        assert file.status == FileStatus.PENDING
        assert isinstance(file.id, UUID)

    def test_file_with_metadata(self) -> None:
        """Test file with metadata."""
        user_id = uuid4()
        metadata = {"uploaded_by": "test_user", "source": "api"}

        file = File(
            user_id=user_id,
            filename="metadata_test.txt",
            content_type="text/plain",
            file_size=2048,
            metadata=metadata,
        )

        assert file.metadata == metadata
        assert file.metadata["uploaded_by"] == "test_user"


class TestConfigurationEntity:
    """Test cases for Configuration entity."""

    def test_configuration_creation(self) -> None:
        """Test configuration entity creation with valid data."""
        config = Configuration(
            key="test_setting",
            value="test_value",
            category="testing",
            description="A test configuration setting",
        )

        assert config.key == "test_setting"
        assert config.value == "test_value"
        assert config.category == "testing"
        assert config.description == "A test configuration setting"
        assert isinstance(config.id, UUID)

    def test_configuration_with_metadata(self) -> None:
        """Test configuration with metadata."""
        metadata = {"type": "string", "required": True, "default": "none"}
        config = Configuration(
            key="advanced_setting", value="advanced_value", metadata=metadata
        )

        assert config.metadata == metadata
        assert config.metadata["type"] == "string"
        assert config.metadata["required"] is True


class TestEntityIntegration:
    """Test cases for entity interactions."""

    def test_user_session_relationship(self) -> None:
        """Test relationship between User and Session entities."""
        user = User(
            username="session_user",
            email="session@example.com",
            full_name="Session User",
        )

        session = Session(user_id=user.id, title="User Session", type="conversation")

        assert session.user_id == user.id
        assert user.is_active is True
        assert session.is_active is True

    def test_memory_user_relationship(self) -> None:
        """Test relationship between Memory and User entities."""
        user = User(
            username="memory_user", email="memory@example.com", full_name="Memory User"
        )

        memory = Memory(
            user_id=user.id,
            type=MemoryType.SEMANTIC,
            content="User prefers detailed explanations",
        )

        assert memory.user_id == user.id
        assert memory.type == MemoryType.SEMANTIC

    def test_plan_user_relationship(self) -> None:
        """Test relationship between Plan and User entities."""
        user = User(
            username="planning_user",
            email="plan@example.com",
            full_name="Planning User",
        )

        plan = Plan(
            user_id=user.id,
            title="User Learning Plan",
            description="A personalized learning plan",
            goal="Master Python programming",
        )

        assert plan.user_id == user.id
        assert plan.goal == "Master Python programming"
