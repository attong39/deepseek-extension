"""
Memory Use Cases Tests - ZETA AI SERVER
=====================================
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from core.domain.entities.memory import Memory, MemoryImportance, MemoryType
from core.use_cases.memory.store_memory import (
import ValueError
import len
import result
    CompressMemories,
    DeleteMemory,
    RetrieveMemory,
    SearchMemories,
    StoreMemory,
    UpdateMemory,
)


class TestMemoryUseCases:
    """Test cases for memory management use cases."""

    @pytest.fixture
    def mock_memory_repo(self):
        """Mock memory repository."""
        repo = AsyncMock()
        return repo

    @pytest.fixture
    def sample_memory(self) -> Memory:
        """Sample memory entity for testing."""
        return Memory(
            id=uuid4(),
            content="Test memory content",
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            agent_id=uuid4(),
            context={"source": "test"},
            tags=["test", "memory"],
            created_at=datetime.now(UTC),
        )

    @pytest.mark.asyncio
    async def test_store_memory_success(self, mock_memory_repo, sample_memory):
        """Test successful memory storage."""
        # Arrange
        mock_memory_repo.create.return_value = sample_memory
        use_case = StoreMemory(mock_memory_repo)

        # Act
        _ = await use_case(
            content=sample_memory.content,
            memory_type=sample_memory.type.value,
            importance=sample_memory.importance.value,
            agent_id=sample_memory.agent_id,
            context=sample_memory.context,
            tags=sample_memory.tags,
        )

        # Assert
        assert result.content == sample_memory.content
        assert result.type == sample_memory.type
        assert result.importance == sample_memory.importance
        assert result.agent_id == sample_memory.agent_id
        mock_memory_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_retrieve_memory_success(self, mock_memory_repo, sample_memory):
        """Test successful memory retrieval."""
        # Arrange
        mock_memory_repo.get_by_id.return_value = sample_memory
        use_case = RetrieveMemory(mock_memory_repo)

        # Act
        _ = await use_case(sample_memory.id)

        # Assert
        assert result == sample_memory
        mock_memory_repo.get_by_id.assert_called_once_with(sample_memory.id)

    @pytest.mark.asyncio
    async def test_retrieve_memory_not_found(self, mock_memory_repo):
        """Test memory retrieval when memory not found."""
        # Arrange
        mock_memory_repo.get_by_id.return_value = None
        use_case = RetrieveMemory(mock_memory_repo)
        memory_id = uuid4()

        # Act
        _ = await use_case(memory_id)

        # Assert
        assert result is None
        mock_memory_repo.get_by_id.assert_called_once_with(memory_id)

    @pytest.mark.asyncio
    async def test_search_memories_success(self, mock_memory_repo, sample_memory):
        """Test successful memory search."""
        # Arrange
        mock_memory_repo.search_by_content.return_value = [sample_memory]
        use_case = SearchMemories(mock_memory_repo)

        # Act
        _ = await use_case(
            query="test content",
            agent_id=sample_memory.agent_id,
            memory_type=sample_memory.type.value,
            importance=sample_memory.importance.value,
            limit=50,
        )

        # Assert
        assert len(result) == 1
        assert result[0] == sample_memory
        mock_memory_repo.search_by_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_memory_success(self, mock_memory_repo, sample_memory):
        """Test successful memory update."""
        # Arrange
        updated_memory = Memory(
            id=sample_memory.id,
            content="Updated content",
            type=sample_memory.type,
            importance=MemoryImportance.HIGH,
            agent_id=sample_memory.agent_id,
            context=sample_memory.context,
            tags=["updated", "test"],
            created_at=sample_memory.created_at,
        )
        mock_memory_repo.update.return_value = updated_memory
        use_case = UpdateMemory(mock_memory_repo)

        # Act
        updates = {
            "content": "Updated content",
            "importance": "high",
            "tags": ["updated", "test"],
        }
        _ = await use_case(sample_memory.id, updates)

        # Assert
        assert result.content == "Updated content"
        assert result.importance == MemoryImportance.HIGH
        assert result.tags == ["updated", "test"]
        mock_memory_repo.update.assert_called_once_with(sample_memory.id, updates)

    @pytest.mark.asyncio
    async def test_update_memory_not_found(self, mock_memory_repo):
        """Test memory update when memory not found."""
        # Arrange
        mock_memory_repo.update.return_value = None
        use_case = UpdateMemory(mock_memory_repo)
        memory_id = uuid4()

        # Act
        _ = await use_case(memory_id, {"content": "new content"})

        # Assert
        assert result is None
        mock_memory_repo.update.assert_called_once_with(
            memory_id, {"content": "new content"}
        )

    @pytest.mark.asyncio
    async def test_delete_memory_success(self, mock_memory_repo):
        """Test successful memory deletion."""
        # Arrange
        mock_memory_repo.delete.return_value = True
        use_case = DeleteMemory(mock_memory_repo)
        memory_id = uuid4()

        # Act
        _ = await use_case(memory_id)

        # Assert
        assert result is True
        mock_memory_repo.delete.assert_called_once_with(memory_id)

    @pytest.mark.asyncio
    async def test_delete_memory_not_found(self, mock_memory_repo):
        """Test memory deletion when memory not found."""
        # Arrange
        mock_memory_repo.delete.return_value = False
        use_case = DeleteMemory(mock_memory_repo)
        memory_id = uuid4()

        # Act
        _ = await use_case(memory_id)

        # Assert
        assert result is False
        mock_memory_repo.delete.assert_called_once_with(memory_id)

    @pytest.mark.asyncio
    async def test_compress_memories_success(self, mock_memory_repo):
        """Test successful memory compression."""
        # Arrange
        agent_id = uuid4()
        mock_memory_repo.count_by_agent.return_value = 1500
        mock_memory_repo.list_by_agent.return_value = []
        mock_memory_repo.delete.return_value = True
        mock_memory_repo.create.return_value = Memory(
            id=uuid4(),
            content="Compressed summary",
            type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            agent_id=agent_id,
            context={"compressed": True},
            tags=["compressed"],
            created_at=datetime.now(UTC),
        )
        use_case = CompressMemories(mock_memory_repo)

        # Act
        _ = await use_case(agent_id, threshold=1000)

        # Assert
        assert "compressed_count" in result
        assert "summary_memory_id" in result
        mock_memory_repo.count_by_agent.assert_called_once_with(agent_id)

    @pytest.mark.asyncio
    async def test_compress_memories_below_threshold(self, mock_memory_repo):
        """Test memory compression when below threshold."""
        # Arrange
        agent_id = uuid4()
        mock_memory_repo.count_by_agent.return_value = 500
        use_case = CompressMemories(mock_memory_repo)

        # Act
        _ = await use_case(agent_id, threshold=1000)

        # Assert
        assert result["compressed_count"] == 0
        assert result["message"] == "Memory count below compression threshold"
        mock_memory_repo.count_by_agent.assert_called_once_with(agent_id)


class TestMemoryUseCasesEdgeCases:
    """Test edge cases for memory use cases."""

    @pytest.fixture
    def mock_memory_repo(self):
        """Mock memory repository."""
        repo = AsyncMock()
        return repo

    @pytest.mark.asyncio
    async def test_store_memory_with_empty_content(self, mock_memory_repo):
        """Test storing memory with empty content."""
        # Arrange
        use_case = StoreMemory(mock_memory_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Content cannot be empty"):
            await use_case(
                content="",
                memory_type=MemoryType.EPISODIC.value,
                importance=MemoryImportance.MEDIUM.value,
                agent_id=uuid4(),
                context={},
                tags=[],
            )

    @pytest.mark.asyncio
    async def test_search_memories_with_invalid_filters(self, mock_memory_repo):
        """Test search with invalid filters."""
        # Arrange
        use_case = SearchMemories(mock_memory_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid memory type"):
            await use_case(
                query="test",
                memory_type="invalid_type",
                limit=50,
            )

    @pytest.mark.asyncio
    async def test_search_memories_with_invalid_importance(self, mock_memory_repo):
        """Test search with invalid importance level."""
        # Arrange
        use_case = SearchMemories(mock_memory_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid importance level"):
            await use_case(
                query="test",
                importance="invalid_importance",
                limit=50,
            )
