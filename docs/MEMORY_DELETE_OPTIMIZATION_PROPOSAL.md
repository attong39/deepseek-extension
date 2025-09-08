# Đề xuất tối ưu Memory Deletion Use Case

## Phân tích & Chiến lược

### 🎯 Mục tiêu

1. **Thống nhất** logic xóa memory trong hệ thống
2. **Nâng cấp** `delete_memory_simple.py` thành implementation hiện đại
3. **Đảm bảo tương thích ngược** với API và service hiện tại
4. **Tối ưu performance** với async patterns và batch operations

### 🔍 Hiện trạng

- `delete_memory_simple.py`: Logic cơ bản, thiếu tính năng
- `delete_memory.py`: Đầy đủ tính năng nhưng phức tạp
- `MemoryManagerService`: Có logic riêng
- `DeleteMemory` use case: Trong `store_memory.py`, logic đơn giản
- API endpoints: Logic phân tán

### ⚡ Đề xuất Implementation

#### 1. Enhanced Delete Memory Use Case (thay thế `delete_memory_simple.py`)

```python
"""
Enhanced Memory Deletion Use Case - ZETA AI SERVER
================================================

Thống nhất và tối ưu logic xóa memory với:
- Async patterns hiện đại
- Validation đầy đủ
- Soft/hard delete options  
- Batch operations
- Audit logging
- Recovery capabilities
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol
from uuid import UUID

from core.domain.entities.memory import Memory, MemoryStatus
from core.interfaces.repositories import MemoryRepository
from core.utils.async_utils import _maybe_await


class DeletionMode(Enum):
    """Chế độ xóa memory."""
    SOFT = "soft"      # Mark as deleted, keep data
    HARD = "hard"      # Permanently remove
    ARCHIVE = "archive" # Move to archive storage


class DeletionCriteria:
    """Tiêu chí xóa memory."""
    
    def __init__(
        self,
        memory_ids: list[UUID] | None = None,
        agent_id: UUID | None = None,
        older_than_days: int | None = None,
        importance_below: str | None = None,
        memory_types: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> None:
        self.memory_ids = memory_ids or []
        self.agent_id = agent_id
        self.older_than_days = older_than_days
        self.importance_below = importance_below
        self.memory_types = memory_types or []
        self.tags = tags or []


class DeletionResult:
    """Kết quả quá trình xóa."""
    
    def __init__(
        self,
        deleted_count: int = 0,
        failed_ids: list[UUID] | None = None,
        archive_location: str | None = None,
        can_restore: bool = False,
        restore_token: str | None = None,
    ) -> None:
        self.deleted_count = deleted_count
        self.failed_ids = failed_ids or []
        self.archive_location = archive_location
        self.can_restore = can_restore
        self.restore_token = restore_token


class DeleteMemoryEnhanced:
    """Enhanced memory deletion use case with comprehensive features."""

    def __init__(self, memory_repo: MemoryRepository) -> None:
        self.memory_repo = memory_repo

    async def delete_single(
        self,
        memory_id: UUID,
        mode: DeletionMode = DeletionMode.SOFT,
        reason: str | None = None,
    ) -> DeletionResult:
        """Xóa một memory đơn lẻ.
        
        Args:
            memory_id: ID của memory cần xóa
            mode: Chế độ xóa (soft/hard/archive)
            reason: Lý do xóa (cho audit log)
            
        Returns:
            Kết quả xóa với thông tin chi tiết
        """
        # Validate memory exists
        memory = await _maybe_await(self.memory_repo.get_by_id(memory_id))
        if not memory:
            return DeletionResult(failed_ids=[memory_id])

        # Execute deletion based on mode
        if mode == DeletionMode.SOFT:
            return await self._soft_delete(memory, reason)
        elif mode == DeletionMode.HARD:
            return await self._hard_delete(memory, reason)
        elif mode == DeletionMode.ARCHIVE:
            return await self._archive_delete(memory, reason)
        
        return DeletionResult(failed_ids=[memory_id])

    async def delete_batch(
        self,
        criteria: DeletionCriteria,
        mode: DeletionMode = DeletionMode.SOFT,
        batch_size: int = 100,
        reason: str | None = None,
    ) -> DeletionResult:
        """Xóa hàng loạt memory theo tiêu chí.
        
        Args:
            criteria: Tiêu chí lọc memory cần xóa
            mode: Chế độ xóa
            batch_size: Kích thước batch
            reason: Lý do xóa
            
        Returns:
            Kết quả xóa tổng hợp
        """
        # Find memories matching criteria
        target_memories = await self._find_by_criteria(criteria)
        if not target_memories:
            return DeletionResult()

        # Process in batches
        total_deleted = 0
        failed_ids: list[UUID] = []
        
        for i in range(0, len(target_memories), batch_size):
            batch = target_memories[i:i + batch_size]
            batch_result = await self._delete_batch_memories(batch, mode, reason)
            total_deleted += batch_result.deleted_count
            failed_ids.extend(batch_result.failed_ids)

        return DeletionResult(
            deleted_count=total_deleted,
            failed_ids=failed_ids,
            can_restore=(mode == DeletionMode.SOFT),
        )

    async def restore_deleted(self, restore_token: str) -> DeletionResult:
        """Khôi phục memory đã xóa soft."""
        # Implementation for restore functionality
        # This would query soft-deleted memories and restore them
        pass

    # Private implementation methods
    async def _soft_delete(self, memory: Memory, reason: str | None) -> DeletionResult:
        """Soft delete: mark as deleted but keep data."""
        memory.status = MemoryStatus.DELETED
        memory.updated_at = datetime.now(UTC)
        if reason:
            memory.context["deletion_reason"] = reason
            memory.context["deleted_at"] = datetime.now(UTC).isoformat()
        
        updated = await _maybe_await(self.memory_repo.update(memory))
        if updated:
            return DeletionResult(
                deleted_count=1,
                can_restore=True,
                restore_token=f"restore_{memory.id}_{int(datetime.now(UTC).timestamp())}"
            )
        return DeletionResult(failed_ids=[memory.id])

    async def _hard_delete(self, memory: Memory, reason: str | None) -> DeletionResult:
        """Hard delete: permanently remove from storage."""
        success = await _maybe_await(self.memory_repo.delete(memory.id))
        if success:
            return DeletionResult(deleted_count=1, can_restore=False)
        return DeletionResult(failed_ids=[memory.id])

    async def _archive_delete(self, memory: Memory, reason: str | None) -> DeletionResult:
        """Archive delete: move to long-term archive storage."""
        # Archive logic would go here
        # For now, similar to soft delete but with archive status
        memory.status = MemoryStatus.ARCHIVED
        memory.updated_at = datetime.now(UTC)
        if reason:
            memory.context["archive_reason"] = reason
            memory.context["archived_at"] = datetime.now(UTC).isoformat()
        
        updated = await _maybe_await(self.memory_repo.update(memory))
        if updated:
            return DeletionResult(
                deleted_count=1,
                archive_location=f"archive://{memory.agent_id}/{memory.id}",
                can_restore=True
            )
        return DeletionResult(failed_ids=[memory.id])

    async def _find_by_criteria(self, criteria: DeletionCriteria) -> list[Memory]:
        """Find memories matching deletion criteria."""
        if criteria.memory_ids:
            # Direct ID lookup
            memories = []
            for mem_id in criteria.memory_ids:
                memory = await _maybe_await(self.memory_repo.get_by_id(mem_id))
                if memory:
                    memories.append(memory)
            return memories
        
        # Criteria-based search (would need repository methods)
        # For now, fallback to agent-based lookup
        if criteria.agent_id:
            repo_any = cast("Any", self.memory_repo)
            if hasattr(repo_any, "get_by_agent"):
                return await _maybe_await(repo_any.get_by_agent(criteria.agent_id))
        
        return []

    async def _delete_batch_memories(
        self, 
        memories: list[Memory], 
        mode: DeletionMode, 
        reason: str | None
    ) -> DeletionResult:
        """Delete a batch of memories."""
        deleted_count = 0
        failed_ids: list[UUID] = []
        
        for memory in memories:
            result = await self.delete_single(memory.id, mode, reason)
            deleted_count += result.deleted_count
            failed_ids.extend(result.failed_ids)
        
        return DeletionResult(
            deleted_count=deleted_count,
            failed_ids=failed_ids,
            can_restore=(mode == DeletionMode.SOFT)
        )


# Backward compatibility alias
DeleteMemorySimple = DeleteMemoryEnhanced


# Export cho barrel
__all__ = [
    "DeleteMemoryEnhanced",
    "DeleteMemorySimple", 
    "DeletionMode",
    "DeletionCriteria", 
    "DeletionResult"
]
```

#### 2. Service Layer Integration

```python
# Trong core/services/memory_manager_service.py - method mới

async def delete_memory_enhanced(
    self,
    memory_id: str,
    mode: str = "soft",
    reason: str | None = None,
) -> dict[str, Any]:
    """Enhanced memory deletion with multiple modes."""
    from core.use_cases.memory.delete_memory_simple import (
        DeleteMemoryEnhanced, 
        DeletionMode
    )
    
    delete_use_case = DeleteMemoryEnhanced(self._memory_repository)
    deletion_mode = DeletionMode(mode)
    
    result = await delete_use_case.delete_single(
        UUID(memory_id), 
        deletion_mode, 
        reason
    )
    
    return {
        "success": result.deleted_count > 0,
        "deleted_count": result.deleted_count,
        "can_restore": result.can_restore,
        "restore_token": result.restore_token,
        "failed_ids": [str(id) for id in result.failed_ids],
    }
```

#### 3. API Enhancement

```python
# Trong app/api/v1/memory/router.py - endpoints mới

@router.delete("/{memory_id}/enhanced")
async def delete_memory_enhanced(
    memory_id: UUID,
    mode: str = "soft",
    reason: str | None = None,
    current_user: User = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service),
) -> dict[str, Any]:
    """Enhanced memory deletion with multiple modes."""
    result = await memory_service.delete_memory_enhanced(
        str(memory_id), mode, reason
    )
    return result

@router.post("/batch-delete")
async def batch_delete_memories(
    deletion_request: BatchDeletionRequest,
    current_user: User = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service),
) -> dict[str, Any]:
    """Batch delete memories with criteria."""
    # Implementation for batch deletion
    pass
```

### 📊 Lợi ích của đề xuất

#### Performance
- **Async patterns**: Tối ưu I/O operations
- **Batch processing**: Xử lý hàng loạt hiệu quả
- **Lazy loading**: Chỉ load data khi cần

#### Reliability  
- **Soft delete**: Cho phép khôi phục
- **Audit trail**: Ghi nhận lý do và thời gian xóa
- **Error handling**: Xử lý lỗi chi tiết

#### Maintainability
- **Single responsibility**: Mỗi method có nhiệm vụ rõ ràng
- **Extensible**: Dễ thêm tính năng mới
- **Testable**: Interface rõ ràng cho testing

#### Backward Compatibility
- **Alias**: `DeleteMemorySimple = DeleteMemoryEnhanced`
- **API versioning**: Giữ endpoint cũ, thêm endpoint mới
- **Gradual migration**: Có thể migrate từng phần

### 🔄 Migration Plan

#### Phase 1: Core Implementation
1. Implement `DeleteMemoryEnhanced` 
2. Add backward compatibility alias
3. Update unit tests

#### Phase 2: Service Integration  
1. Add enhanced methods to `MemoryManagerService`
2. Update integration tests
3. Add API documentation

#### Phase 3: API Enhancement
1. Add enhanced endpoints
2. Update OpenAPI schema  
3. Update apps/desktop app types

#### Phase 4: Migration & Cleanup
1. Migrate existing usages
2. Deprecate old methods
3. Remove deprecated code

### 🧪 Testing Strategy

#### Unit Tests
```python
# Test coverage for new functionality
- test_delete_single_soft()
- test_delete_single_hard() 
- test_delete_batch_by_criteria()
- test_restore_deleted()
- test_backward_compatibility()
```

#### Integration Tests
```python
# End-to-end testing
- test_api_enhanced_delete()
- test_service_integration()
- test_repository_operations()
```

### 📈 Performance Impact

#### Before (Simple)
- Single memory deletion only
- No batch operations
- Synchronous patterns
- Limited error handling

#### After (Enhanced)
- Single + batch operations  
- Async processing
- Multiple deletion modes
- Comprehensive error handling
- Recovery capabilities

### ✅ Success Metrics

1. **Code Quality**: Ruff + MyPy pass 100%
2. **Test Coverage**: >95% for new code
3. **Performance**: <100ms for single delete, <5s for batch
4. **Compatibility**: Zero breaking changes
5. **Documentation**: Complete API docs + examples

### 🚀 Implementation Priority

**High Priority:**
- Core `DeleteMemoryEnhanced` implementation
- Backward compatibility 
- Basic testing

**Medium Priority:**
- Service layer integration
- Enhanced API endpoints
- Batch operations

**Low Priority:**
- Advanced restore features
- Archive storage integration
- Performance optimizations

---

## 📋 Next Steps

1. **Review & Approve** đề xuất này
2. **Implement Phase 1** - Core functionality
3. **Run quality gates** - ruff, mypy, pytest
4. **Update project map** và documentation
5. **Plan migration** từ implementation cũ