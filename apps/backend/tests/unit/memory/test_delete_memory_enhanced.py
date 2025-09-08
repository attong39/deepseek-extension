from __future__ import annotations

import os
from unittest.mock import Mock

import pytest

from apps.backend.core.use_cases.memory.delete_memory_simple import (
    DeleteMemory,
    DeleteMemoryEnhanced,
    DeletionMode,
    DeletionResult,
)

"""
Tests for Enhanced Memory Deletion Use Case - ZETA AI SERVER
=========================================================

Comprehensive test coverage for DeleteMemoryEnhanced functionality:
- Single memory deletion with different modes
- Batch deletion operations
- Error handling and edge cases
- Backward compatibility
"""
    DeleteMemoryEnhanced,
    DeletionMode,
    DeletionResult,
)

class TestDeletionResult:
    """Test DeletionResult data class."""

    def test_deletion_result_creation_defaults(self) -> None:
        """Test creating DeletionResult with default values."""
        result = DeletionResult()

        assert result.deleted_count == 0
        assert result.failed_ids == []
        assert result.archive_location is None
        assert result.can_restore is False
        assert result.restore_token is None
        assert result.error_message is None

    def test_deletion_result_creation_with_values(self) -> None:
        """Test creating DeletionResult with specific values."""
        failed_ids = ["id1", "id2"]
        result = DeletionResult(
            deleted_count=5,
            failed_ids=failed_ids,
            archive_location="archive://test",
            can_restore=True,
            restore_token = os.getenv("TOKEN"),
            error_message="Test error",
        )

        assert result.deleted_count == 5
        assert result.failed_ids == failed_ids
        assert result.archive_location == "archive://test"
        assert result.can_restore is True
        assert result.restore_token == "token123"
        assert result.error_message == "Test error"

    def test_deletion_result_to_dict(self) -> None:
        """Test converting DeletionResult to dictionary."""
        result = DeletionResult(
            deleted_count=3, failed_ids=["id1"], can_restore=True, restore_token = os.getenv("TOKEN")
        )

        result_dict = result.to_dict()

        assert result_dict["deleted_count"] == 3
        assert result_dict["failed_ids"] == ["id1"]
        assert result_dict["can_restore"] is True
        assert result_dict["restore_token"] == "token123"
        assert result_dict["success"] is False  # Has failed_ids

class TestDeleteMemoryEnhanced:
    """Test enhanced memory deletion use case."""

    @pytest.fixture
    def mock_memory_service(self) -> Mock:
        """Create mock memory service."""
        mock = Mock()
        mock.delete.return_value = {"status": "success", "deleted_count": 1}
        return mock

    @pytest.fixture
    def delete_use_case(self, mock_memory_service: Mock) -> DeleteMemoryEnhanced:
        """Create DeleteMemoryEnhanced instance with mock service."""
        return DeleteMemoryEnhanced(memory=mock_memory_service)

    def test_delete_single_hard_mode_success(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test successful single memory deletion in hard mode."""
        memory_id = "test_memory_123"
        namespace = "test_namespace"

        _ = delete_use_case.delete_single(
            memory_id=memory_id, namespace=namespace, mode=DeletionMode.HARD, reason="Test deletion"
        )

        assert result.deleted_count == 1
        assert result.failed_ids == []
        assert result.can_restore is False

        mock_memory_service.delete.assert_called_once_with(
            namespace=namespace, ids=[memory_id], hard=True
        )

    def test_delete_single_soft_mode_fallback(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test soft mode falls back to hard delete."""
        memory_id = "test_memory_123"
        namespace = "test_namespace"

        _ = delete_use_case.delete_single(
            memory_id=memory_id,
            namespace=namespace,
            mode=DeletionMode.SOFT,
            reason="Test soft deletion",
        )

        assert result.deleted_count == 1
        assert result.failed_ids == []
        # Currently falls back to hard delete
        assert result.can_restore is False

        mock_memory_service.delete.assert_called_once_with(
            namespace=namespace, ids=[memory_id], hard=True
        )

    def test_delete_single_archive_mode_fallback(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test archive mode falls back to hard delete."""
        memory_id = "test_memory_123"
        namespace = "test_namespace"

        _ = delete_use_case.delete_single(
            memory_id=memory_id,
            namespace=namespace,
            mode=DeletionMode.ARCHIVE,
            reason="Test archive deletion",
        )

        assert result.deleted_count == 1
        assert result.failed_ids == []
        # Currently falls back to hard delete
        assert result.can_restore is False

    def test_delete_single_exception_handling(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test exception handling in single deletion."""
        mock_memory_service.delete.side_effect = Exception("Service error")

        memory_id = "test_memory_123"
        namespace = "test_namespace"

        _ = delete_use_case.delete_single(
            memory_id=memory_id, namespace=namespace, mode=DeletionMode.HARD
        )

        assert result.deleted_count == 0
        assert memory_id in result.failed_ids
        assert "Deletion failed" in result.error_message

    def test_delete_batch_success(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test successful batch deletion."""
        memory_ids = ["id1", "id2", "id3"]
        namespace = "test_namespace"

        _ = delete_use_case.delete_batch(
            memory_ids=memory_ids,
            namespace=namespace,
            mode=DeletionMode.HARD,
            reason="Batch deletion test",
        )

        assert result.deleted_count == 3
        assert result.failed_ids == []
        assert result.can_restore is False

        # Should call delete for each memory_id
        assert mock_memory_service.delete.call_count == 3

    def test_delete_batch_empty_list(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test batch deletion with empty memory_ids list."""
        _ = delete_use_case.delete_batch(
            memory_ids=[], namespace="test_namespace", mode=DeletionMode.HARD
        )

        assert result.deleted_count == 0
        assert result.failed_ids == []

        # Should not call delete service
        mock_memory_service.delete.assert_not_called()

    def test_delete_batch_partial_failure(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test batch deletion with partial failures."""
        memory_ids = ["id1", "id2", "id3"]
        namespace = "test_namespace"

        # Make second call fail
        mock_memory_service.delete.side_effect = [
            {"status": "success"},
            Exception("Service error"),
            {"status": "success"},
        ]

        _ = delete_use_case.delete_batch(
            memory_ids=memory_ids, namespace=namespace, mode=DeletionMode.HARD
        )

        assert result.deleted_count == 2  # 2 successful
        assert len(result.failed_ids) == 1  # 1 failed
        assert "id2" in result.failed_ids

    def test_delete_by_filter_hard_mode(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test deletion by filter in hard mode."""
        namespace = "test_namespace"
        filters = {"tag": "old_memories"}

        mock_memory_service.delete.return_value = {"deleted_count": 5}

        _ = delete_use_case.delete_by_filter(
            namespace=namespace, filters=filters, mode=DeletionMode.HARD, max_count=1000
        )

        assert result.deleted_count == 5
        assert result.can_restore is False

        mock_memory_service.delete.assert_called_once_with(
            namespace=namespace, flt=filters, hard=True
        )

    def test_delete_by_filter_soft_mode_fallback(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test soft mode filter deletion falls back to hard."""
        namespace = "test_namespace"
        filters = {"tag": "old_memories"}

        mock_memory_service.delete.return_value = {"deleted_count": 3}

        _ = delete_use_case.delete_by_filter(
            namespace=namespace, filters=filters, mode=DeletionMode.SOFT, max_count=1000
        )

        # Should fall back to hard delete
        assert result.deleted_count == 3
        assert result.can_restore is False

    def test_delete_by_filter_exception_handling(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test exception handling in filter deletion."""
        mock_memory_service.delete.side_effect = Exception("Filter error")

        _ = delete_use_case.delete_by_filter(
            namespace="test_namespace", filters={"tag": "test"}, mode=DeletionMode.HARD
        )

        assert result.deleted_count == 0
        assert "Filter deletion failed" in result.error_message

class TestDeleteMemoryBackwardCompatibility:
    """Test backward compatibility of original DeleteMemory class."""

    @pytest.fixture
    def mock_memory_service(self) -> Mock:
        """Create mock memory service."""
        mock = Mock()
        mock.delete.return_value = {"status": "success"}
        return mock

    @pytest.fixture
    def delete_use_case(self, mock_memory_service: Mock) -> DeleteMemory:
        """Create original DeleteMemory instance."""
        return DeleteMemory(memory=mock_memory_service)

    def test_original_delete_memory_interface(
        self, delete_use_case: DeleteMemory, mock_memory_service: Mock
    ) -> None:
        """Test original DeleteMemory interface still works."""
        input_data = {"namespace": "test_namespace", "ids": ["memory1", "memory2"], "hard": True}

        _ = delete_use_case(input_data)

        assert result == {"status": "success"}

        mock_memory_service.delete.assert_called_once_with(
            namespace="test_namespace", ids=["memory1", "memory2"], flt=None, hard=True
        )

    def test_original_delete_memory_with_filter(
        self, delete_use_case: DeleteMemory, mock_memory_service: Mock
    ) -> None:
        """Test original DeleteMemory with filter."""
        input_data = {"namespace": "test_namespace", "filter": {"tag": "old"}, "hard": False}

        _ = delete_use_case(input_data)

        assert result == {"status": "success"}

        mock_memory_service.delete.assert_called_once_with(
            namespace="test_namespace", ids=None, flt={"tag": "old"}, hard=False
        )

    def test_original_delete_memory_with_context(
        self, delete_use_case: DeleteMemory, mock_memory_service: Mock
    ) -> None:
        """Test original DeleteMemory ignores context parameter."""
        input_data = {
            "namespace": "test_namespace",
            "ids": ["memory1"],
        }
        context = {"user_id": "test_user"}

        _ = delete_use_case(input_data, ctx=context)

        assert result == {"status": "success"}
        # Context should be ignored but not cause errors

class TestDeletionModeEnum:
    """Test DeletionMode enum functionality."""

    def test_deletion_mode_values(self) -> None:
        """Test DeletionMode enum values."""
        assert DeletionMode.SOFT.value == "soft"
        assert DeletionMode.HARD.value == "hard"
        assert DeletionMode.ARCHIVE.value == "archive"

    def test_deletion_mode_from_string(self) -> None:
        """Test creating DeletionMode from string values."""
        assert DeletionMode("soft") == DeletionMode.SOFT
        assert DeletionMode("hard") == DeletionMode.HARD
        assert DeletionMode("archive") == DeletionMode.ARCHIVE

    def test_deletion_mode_invalid_value(self) -> None:
        """Test DeletionMode with invalid value raises error."""
        with pytest.raises(ValueError):
            DeletionMode("invalid_mode")

class TestIntegrationScenarios:
    """Integration test scenarios for enhanced deletion."""

    @pytest.fixture
    def mock_memory_service(self) -> Mock:
        """Create realistic mock memory service."""
        mock = Mock()
        mock.delete.return_value = {"status": "success", "deleted_count": 1}
        return mock

    @pytest.fixture
    def delete_use_case(self, mock_memory_service: Mock) -> DeleteMemoryEnhanced:
        """Create DeleteMemoryEnhanced instance."""
        return DeleteMemoryEnhanced(memory=mock_memory_service)

    def test_cleanup_old_memories_scenario(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test realistic cleanup scenario."""
        # Simulate cleaning up old memories by filter
        namespace = "user_123_memories"
        old_memory_filter = {"created_before": "2024-01-01", "importance": "low"}

        mock_memory_service.delete.return_value = {"deleted_count": 25}

        _ = delete_use_case.delete_by_filter(
            namespace=namespace,
            filters=old_memory_filter,
            mode=DeletionMode.HARD,
            reason="Automatic cleanup of old low-importance memories",
            max_count=100,
        )

        assert result.deleted_count == 25
        assert result.failed_ids == []
        assert result.can_restore is False

        mock_memory_service.delete.assert_called_once_with(
            namespace=namespace, flt=old_memory_filter, hard=True
        )

    def test_user_initiated_deletion_scenario(
        self, delete_use_case: DeleteMemoryEnhanced, mock_memory_service: Mock
    ) -> None:
        """Test user-initiated deletion with restore capability."""
        # User deletes specific memories but wants restore option
        memory_ids = ["memory_1", "memory_2", "memory_3"]
        namespace = "user_456_memories"

        _ = delete_use_case.delete_batch(
            memory_ids=memory_ids,
            namespace=namespace,
            mode=DeletionMode.SOFT,  # Soft delete for restore
            reason="User requested deletion via UI",
        )

        assert result.deleted_count == 3
        assert result.failed_ids == []
        # Note: Currently falls back to hard delete, but in future soft delete
        # implementation this would be True

        assert mock_memory_service.delete.call_count == 3
