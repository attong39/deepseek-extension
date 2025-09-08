"""
Unit tests for memory functionality.

Tests Memory domain entity và related functionality.
"""

from datetime import datetime
from uuid import UUID, uuid4

from core.domain.entities.memory import (
import i
import isinstance
import len
import range
import str
    Memory,
    MemoryEmbedding,
    MemoryImportance,
    MemoryMetrics,
    MemoryStatus,
    MemoryType,
)


class TestMemoryEntity:
    """Test Memory domain entity."""

    def test_memory_creation_default(self):
        """Test tạo Memory entity với default values."""
        memory = Memory()

        assert isinstance(memory.id, UUID)
        assert memory.content == ""
        assert memory.type == MemoryType.EPISODIC
        assert memory.status == MemoryStatus.ACTIVE
        assert memory.importance == MemoryImportance.MEDIUM
        assert memory.embedding is None
        assert isinstance(memory.metrics, MemoryMetrics)
        assert isinstance(memory.created_at, datetime)

    def test_memory_creation_with_content(self):
        """Test tạo Memory entity với content."""
        content = "This is a test memory content"
        memory = Memory(
            content=content, type=MemoryType.SEMANTIC, importance=MemoryImportance.HIGH
        )

        assert memory.content == content
        assert memory.type == MemoryType.SEMANTIC
        assert memory.importance == MemoryImportance.HIGH
        assert memory.summary == content  # Content is short enough

    def test_memory_with_long_content_summary(self):
        """Test memory summary creation from long content."""
        long_content = " ".join([f"word{i}" for i in range(25)])  # 25 words
        memory = Memory(content=long_content)

        # Summary should be first 20 words + "..."
        expected_summary = " ".join([f"word{i}" for i in range(20)]) + "..."
        assert memory.summary == expected_summary

    def test_memory_with_embedding(self):
        """Test memory với embedding vector."""
        embedding = MemoryEmbedding(
            vector=[0.1, 0.2, 0.3, 0.4, 0.5],
            model="text-embedding-ada-002",
            dimension=5,
        )
        memory = Memory(
            content="Memory with embedding",
            type=MemoryType.SEMANTIC,
            embedding=embedding,
        )

        assert memory.embedding is not None
        assert memory.embedding.vector == [0.1, 0.2, 0.3, 0.4, 0.5]
        assert memory.embedding.model == "text-embedding-ada-002"
        assert memory.embedding.dimension == 5

    def test_memory_with_context(self):
        """Test memory với context metadata."""
        context = {
            "source": "chat",
            "conversation_id": str(uuid4()),
            "user_id": str(uuid4()),
        }
        memory = Memory(
            content="Memory with context", type=MemoryType.WORKING, context=context
        )

        assert memory.context == context
        assert memory.context["source"] == "chat"

    def test_memory_access_tracking(self):
        """Test memory access tracking."""
        memory = Memory(content="Test memory for access tracking")

        # Initial state
        assert memory.metrics.access_count == 0
        assert memory.metrics.last_accessed is None

        # After first access
        memory.access()
        assert memory.metrics.access_count == 1
        assert memory.metrics.last_accessed is not None

    def test_memory_content_update(self):
        """Test memory content update."""
        memory = Memory(content="Original content")
        original_summary = memory.summary

        new_content = "Updated content"
        memory.update_content(new_content)

        assert memory.content == new_content
        assert memory.summary == new_content
        assert memory.summary != original_summary

    def test_memory_embedding_update(self):
        """Test memory embedding update."""
        memory = Memory(content="Test memory")
        assert memory.embedding is None

        new_embedding = MemoryEmbedding(
            vector=[0.1, 0.2, 0.3], model="test-model", dimension=3
        )
        memory.update_embedding(new_embedding)

        assert memory.embedding is not None
        assert memory.embedding.vector == [0.1, 0.2, 0.3]

    def test_memory_tag_management(self):
        """Test memory tag add/remove functionality."""
        memory = Memory(content="Test memory for tags")

        # Add tags
        memory.add_tag("important")
        memory.add_tag("ai")
        assert "important" in memory.tags
        assert "ai" in memory.tags
        assert len(memory.tags) == 2

        # Add duplicate tag (should not duplicate)
        memory.add_tag("important")
        assert len(memory.tags) == 2

        # Remove tag
        memory.remove_tag("ai")
        assert "ai" not in memory.tags
        assert "important" in memory.tags
        assert len(memory.tags) == 1

    def test_memory_agent_association(self):
        """Test memory association với agent."""
        agent_id = uuid4()
        memory = Memory(content="Agent-associated memory", agent_id=agent_id)

        assert memory.agent_id == agent_id

    def test_memory_user_association(self):
        """Test memory association với user."""
        user_id = uuid4()
        memory = Memory(content="User-associated memory", user_id=user_id)

        assert memory.user_id == user_id

    def test_memory_linked_memories(self):
        """Test memory linking functionality."""
        memory1 = Memory(content="First memory")
        memory2 = Memory(content="Second memory")

        # Link memories
        memory1.linked_memories.append(memory2.id)

        assert memory2.id in memory1.linked_memories
        assert len(memory1.linked_memories) == 1


class TestMemoryType:
    """Test MemoryType enum."""

    def test_memory_type_values(self):
        """Test memory type enum values."""
        assert MemoryType.EPISODIC == "episodic"
        assert MemoryType.SEMANTIC == "semantic"
        assert MemoryType.WORKING == "working"
        assert MemoryType.PROCEDURAL == "procedural"
        assert MemoryType.LONG_TERM == "long_term"


class TestMemoryStatus:
    """Test MemoryStatus enum."""

    def test_memory_status_values(self):
        """Test memory status enum values."""
        assert MemoryStatus.ACTIVE == "active"
        assert MemoryStatus.ARCHIVED == "archived"
        assert MemoryStatus.COMPRESSED == "compressed"
        assert MemoryStatus.DELETED == "deleted"


class TestMemoryImportance:
    """Test MemoryImportance enum."""

    def test_memory_importance_values(self):
        """Test memory importance enum values."""
        assert MemoryImportance.LOW == "low"
        assert MemoryImportance.MEDIUM == "medium"
        assert MemoryImportance.HIGH == "high"
        assert MemoryImportance.CRITICAL == "critical"


class TestMemoryEmbedding:
    """Test MemoryEmbedding value object."""

    def test_embedding_creation(self):
        """Test embedding creation."""
        vector = [0.1, 0.2, 0.3, 0.4]
        embedding = MemoryEmbedding(
            vector=vector, model="text-embedding-ada-002", dimension=4
        )

        assert embedding.vector == vector
        assert embedding.model == "text-embedding-ada-002"
        assert embedding.dimension == 4
        assert isinstance(embedding.created_at, datetime)


class TestMemoryMetrics:
    """Test MemoryMetrics value object."""

    def test_metrics_creation_default(self):
        """Test metrics creation với default values."""
        metrics = MemoryMetrics()

        assert metrics.access_count == 0
        assert metrics.last_accessed is None
        assert metrics.relevance_score == 0.0
        assert metrics.decay_factor == 1.0
        assert metrics.compression_ratio == 1.0
        assert metrics.retrieval_latency_ms == 0.0

    def test_metrics_creation_custom(self):
        """Test metrics creation với custom values."""
        metrics = MemoryMetrics(access_count=5, relevance_score=0.85, decay_factor=0.9)

        assert metrics.access_count == 5
        assert metrics.relevance_score == 0.85
        assert metrics.decay_factor == 0.9


class TestMemoryUseCases:
    """Test Memory use case scenarios."""

    def test_conversation_memory_scenario(self):
        """Test creating memory from conversation."""
        agent_id = uuid4()
        user_id = uuid4()

        conversation_memory = Memory(
            content="User asked about weather in Paris",
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            agent_id=agent_id,
            user_id=user_id,
            context={
                "source": "conversation",
                "user_query": "weather in Paris",
                "response_type": "weather_info",
            },
        )

        conversation_memory.add_tag("weather")
        conversation_memory.add_tag("geography")

        assert conversation_memory.context["source"] == "conversation"
        assert "weather" in conversation_memory.tags
        assert conversation_memory.agent_id == agent_id
        assert conversation_memory.user_id == user_id

    def test_knowledge_memory_scenario(self):
        """Test creating knowledge-based memory."""
        knowledge_memory = Memory(
            content="Python is a high-level programming language",
            type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            context={
                "source": "knowledge_base",
                "domain": "programming",
                "verified": True,
            },
        )

        knowledge_memory.add_tag("programming")
        knowledge_memory.add_tag("python")

        assert knowledge_memory.type == MemoryType.SEMANTIC
        assert knowledge_memory.importance == MemoryImportance.HIGH
        assert knowledge_memory.context["domain"] == "programming"

    def test_working_memory_scenario(self):
        """Test working memory for ongoing tasks."""
        task_memory = Memory(
            content="Currently processing file upload request",
            type=MemoryType.WORKING,
            importance=MemoryImportance.CRITICAL,
            context={"task_id": str(uuid4()), "status": "in_progress"},
        )

        task_memory.add_tag("task")
        task_memory.add_tag("file_upload")

        assert task_memory.type == MemoryType.WORKING
        assert task_memory.importance == MemoryImportance.CRITICAL
        assert task_memory.context["status"] == "in_progress"

    def test_procedural_memory_scenario(self):
        """Test procedural memory for learned skills."""
        skill_memory = Memory(
            content="Steps to analyze data: 1) Load data 2) Clean data 3) Analyze patterns",
            type=MemoryType.PROCEDURAL,
            importance=MemoryImportance.HIGH,
            context={"skill_type": "data_analysis", "steps": 3, "complexity": "medium"},
        )

        skill_memory.add_tag("data_analysis")
        skill_memory.add_tag("procedure")

        assert skill_memory.type == MemoryType.PROCEDURAL
        assert "Steps to analyze" in skill_memory.content
        assert skill_memory.context["skill_type"] == "data_analysis"
