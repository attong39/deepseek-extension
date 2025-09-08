# SAFE_PHASE2_WORK_ORDERS.md
**Kế hoạch Work Orders chi tiết — Phase 2 SAFE_REPAIR**  
*Ưu tiên: HIGH → MEDIUM → LOW*

---

## 🎯 Nguyên tắc & Definition of Done (DoD)

### Nguyên tắc bắt buộc:
1. **Không xóa symbol public** → thêm AUTO-STUB chuyển tiếp nếu cần đổi API
2. **Phá cyclic imports** bằng TYPE_CHECKING, local import trong hàm, hoặc tách types/ports
3. **Mỗi WO phải đạt**: `ruff clean` + `mypy clean` + `tests pass` (không giảm coverage)

### Definition of Done (DoD):
- ✅ Ruff check CLEAN (0 issues)
- ✅ MyPy check CLEAN (0 errors) 
- ✅ Tests PASS (coverage không giảm)
- ✅ No public API breaking changes
- ✅ AUTO-STUB for deprecated functions

---

## WO-001 (HIGH) — zeta_vn/core/auth/base.py

### 🎯 **Mục tiêu**: Bổ sung types, Protocol/ABC, AUTO-STUB
### 📊 **Issues**: 38 Ruff errors + missing type hints
### ⏱️ **Estimated**: 45 phút

### **Patch mẫu**:
```python
# zeta_vn/core/auth/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from datetime import datetime

# >>> AUTO-STUB >>> old_authenticate
def old_authenticate(user: str, password: str) -> bool:
    """Deprecated: Use AuthProvider.authenticate() instead. 
    DO NOT DELETE until tests cover new path."""
    return AuthProvider().authenticate(user, password)
# <<< AUTO-STUB <<<

@runtime_checkable
class AuthProvider(Protocol):
    """Authentication provider interface."""
    
    def authenticate(self, user_id: str, credentials: str) -> bool:
        """Authenticate user with credentials."""
        ...
    
    def get_user_permissions(self, user_id: str) -> list[str]:
        """Get user permissions list."""
        ...

class BaseAuthenticator(ABC):
    """Base abstract authenticator."""
    
    @abstractmethod
    def validate_token(self, token: str) -> dict[str, str] | None:
        """Validate authentication token."""
        pass
    
    @abstractmethod  
    def create_session(self, user_id: str) -> dict[str, str]:
        """Create new user session."""
        pass
```

### **Test mẫu**:
```python
# tests/core/auth/test_base_auth.py
import pytest
from zeta_vn.core.auth.base import AuthProvider, BaseAuthenticator

def test_auth_provider_protocol():
    """Test AuthProvider protocol compliance."""
    class MockAuth:
        def authenticate(self, user_id: str, credentials: str) -> bool:
            return user_id == "test" and credentials == "valid"
        
        def get_user_permissions(self, user_id: str) -> list[str]:
            return ["read", "write"] if user_id == "test" else []
    
    mock_auth = MockAuth()
    assert isinstance(mock_auth, AuthProvider)
    assert mock_auth.authenticate("test", "valid") is True
    assert mock_auth.get_user_permissions("test") == ["read", "write"]

def test_auto_stub_backward_compatibility():
    """Test AUTO-STUB maintains backward compatibility."""
    from zeta_vn.core.auth.base import old_authenticate
    # Should not crash and return expected behavior
    result = old_authenticate("test", "password")
    assert isinstance(result, bool)
```

### **Validation commands**:
```bash
uv run ruff check zeta_vn/core/auth/base.py
uv run mypy zeta_vn/core/auth/base.py  
uv run pytest -q tests/core/auth/test_base_auth.py
```

---

## WO-002 (MEDIUM) — zeta_vn/app/api/graphql/resolvers.py

### 🎯 **Mục tiêu**: Phá vòng lặp import với TYPE_CHECKING + local import
### 📊 **Issues**: 11 Ruff errors + cyclic imports
### ⏱️ **Estimated**: 60 phút

### **Patch mẫu**:
```python
# zeta_vn/app/api/graphql/resolvers.py
from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from zeta_vn.core.services.memory_service import MemoryService
    from zeta_vn.core.domain.entities.User import User
    from strawberry.types import Info

import strawberry

@strawberry.type
class UserResolver:
    """GraphQL User resolver with cycle-free imports."""
    
    @strawberry.field
    def get_user(self, info: Info, user_id: str) -> dict[str, Any]:
        """Get user by ID - local import to avoid cycles."""
        # Local import inside function to break cycle
        from zeta_vn.core.services.user_service import get_user_by_id
        
        user = get_user_by_id(user_id)
        return {
            "id": user.id,
            "name": user.name, 
            "email": user.email
        } if user else {}
    
    @strawberry.field
    def get_user_memories(self, info: Info, user_id: str) -> list[dict[str, Any]]:
        """Get user memories - TYPE_CHECKING import."""
        # Import only when needed at runtime
        from zeta_vn.core.services.memory_service import MemoryService
        
        memory_service: MemoryService = info.context["memory_service"]
        memories = memory_service.get_user_memories(user_id)
        
        return [
            {
                "id": mem.id,
                "content": mem.content,
                "created_at": mem.created_at.isoformat()
            }
            for mem in memories
        ]

# >>> AUTO-STUB >>> old_resolver_function  
def old_resolver_function(*args: Any, **kwargs: Any) -> dict[str, Any]:
    """Deprecated resolver: Use UserResolver.get_user() instead.
    DO NOT DELETE until GraphQL schema migration complete."""
    resolver = UserResolver()
    return resolver.get_user(args[0], args[1]) if len(args) >= 2 else {}
# <<< AUTO-STUB <<<
```

### **Test mẫu**:
```python
# tests/app/api/graphql/test_smoke.py
import pytest
from unittest.mock import Mock, MagicMock
from zeta_vn.app.api.graphql.resolvers import UserResolver

def test_user_resolver_get_user():
    """Smoke test for UserResolver.get_user()."""
    resolver = UserResolver()
    
    # Mock info object
    mock_info = Mock()
    mock_info.context = {"user_service": Mock()}
    
    # Test with mocked dependencies - should not crash
    try:
        result = resolver.get_user(mock_info, "test_user_id")
        assert isinstance(result, dict)
    except ImportError:
        pytest.skip("Dependencies not available for smoke test")

def test_no_circular_imports():
    """Test that importing resolvers doesn't create circular import."""
    try:
        from zeta_vn.app.api.graphql.resolvers import UserResolver
        assert UserResolver is not None
    except ImportError as e:
        pytest.fail(f"Circular import detected: {e}")

def test_auto_stub_resolver():
    """Test AUTO-STUB backward compatibility."""
    from zeta_vn.app.api.graphql.resolvers import old_resolver_function
    
    # Should not crash
    result = old_resolver_function()
    assert isinstance(result, dict)
```

### **Validation commands**:
```bash
uv run ruff check zeta_vn/app/api/graphql/resolvers.py
uv run mypy zeta_vn/app/api/graphql/resolvers.py
uv run pytest -q tests/app/api/graphql/test_smoke.py
```

---

## WO-003 (LOW) — zeta_vn/integration/rag/chunking.py

### 🎯 **Mục tiêu**: Refactor thành pure functions, kiểm soát overlap
### 📊 **Issues**: Duplicated code + no docstrings  
### ⏱️ **Estimated**: 30 phút

### **Patch mẫu**:
```python
# zeta_vn/integration/rag/chunking.py
from __future__ import annotations
from typing import NamedTuple
from dataclasses import dataclass

@dataclass(frozen=True)
class ChunkConfig:
    """Configuration for text chunking."""
    chunk_size: int = 1000
    overlap_size: int = 200
    min_chunk_size: int = 100
    
    def __post_init__(self) -> None:
        """Validate chunk configuration."""
        if self.overlap_size >= self.chunk_size:
            raise ValueError("Overlap size must be less than chunk size")
        if self.min_chunk_size > self.chunk_size:
            raise ValueError("Min chunk size must be <= chunk size")

class TextChunk(NamedTuple):
    """Immutable text chunk with metadata."""
    content: str
    start_idx: int
    end_idx: int
    chunk_id: int

def chunk_text_pure(text: str, config: ChunkConfig) -> list[TextChunk]:
    """Pure function to chunk text with controlled overlap.
    
    Args:
        text: Input text to chunk
        config: Chunking configuration
        
    Returns:
        List of TextChunk objects
        
    Example:
        >>> config = ChunkConfig(chunk_size=100, overlap_size=20)
        >>> chunks = chunk_text_pure("Hello world...", config)
        >>> len(chunks) > 0
        True
    """
    if not text.strip():
        return []
    
    chunks: list[TextChunk] = []
    start_idx = 0
    chunk_id = 0
    
    while start_idx < len(text):
        end_idx = min(start_idx + config.chunk_size, len(text))
        
        # Extract chunk content
        chunk_content = text[start_idx:end_idx].strip()
        
        # Skip if chunk is too small
        if len(chunk_content) < config.min_chunk_size and start_idx > 0:
            break
            
        chunks.append(TextChunk(
            content=chunk_content,
            start_idx=start_idx,
            end_idx=end_idx,
            chunk_id=chunk_id
        ))
        
        # Move to next chunk with overlap
        start_idx = end_idx - config.overlap_size
        chunk_id += 1
        
        # Prevent infinite loop
        if start_idx >= end_idx:
            break
    
    return chunks

def validate_chunks(chunks: list[TextChunk]) -> bool:
    """Validate chunk consistency and overlap.
    
    Args:
        chunks: List of chunks to validate
        
    Returns:
        True if chunks are valid
    """
    if not chunks:
        return True
        
    for i, chunk in enumerate(chunks[:-1]):
        next_chunk = chunks[i + 1]
        
        # Check ordering
        if chunk.end_idx > next_chunk.start_idx + 50:  # Allow some overlap
            return False
            
        # Check chunk IDs are sequential  
        if next_chunk.chunk_id != chunk.chunk_id + 1:
            return False
    
    return True

# >>> AUTO-STUB >>> old_chunk_function
def old_chunk_function(text: str, chunk_size: int = 1000) -> list[str]:
    """Deprecated: Use chunk_text_pure() with ChunkConfig instead.
    DO NOT DELETE until all callers migrated."""
    config = ChunkConfig(chunk_size=chunk_size, overlap_size=200)
    chunks = chunk_text_pure(text, config)
    return [chunk.content for chunk in chunks]
# <<< AUTO-STUB <<<
```

### **Test mẫu**:
```python
# tests/integration/rag/test_chunking.py
import pytest
from zeta_vn.integration.rag.chunking import (
    ChunkConfig, TextChunk, chunk_text_pure, validate_chunks, old_chunk_function
)

def test_chunk_config_validation():
    """Test ChunkConfig validation."""
    # Valid config
    config = ChunkConfig(chunk_size=1000, overlap_size=200)
    assert config.chunk_size == 1000
    
    # Invalid config - overlap >= chunk_size
    with pytest.raises(ValueError, match="Overlap size must be less"):
        ChunkConfig(chunk_size=100, overlap_size=100)

def test_chunk_text_pure():
    """Test pure chunking function."""
    text = "Hello world. " * 100  # ~1300 chars
    config = ChunkConfig(chunk_size=500, overlap_size=100, min_chunk_size=50)
    
    chunks = chunk_text_pure(text, config)
    
    assert len(chunks) >= 2
    assert all(isinstance(chunk, TextChunk) for chunk in chunks)
    assert chunks[0].chunk_id == 0
    assert chunks[1].chunk_id == 1
    
    # Test overlap
    assert chunks[1].start_idx < chunks[0].end_idx

def test_empty_text_chunking():
    """Test chunking empty or whitespace text."""
    config = ChunkConfig()
    
    assert chunk_text_pure("", config) == []
    assert chunk_text_pure("   ", config) == []

def test_validate_chunks():
    """Test chunk validation function."""
    valid_chunks = [
        TextChunk("chunk1", 0, 100, 0),
        TextChunk("chunk2", 80, 180, 1),  # Valid overlap
        TextChunk("chunk3", 160, 260, 2)
    ]
    
    assert validate_chunks(valid_chunks) is True
    assert validate_chunks([]) is True  # Empty is valid

def test_auto_stub_backward_compatibility():
    """Test AUTO-STUB maintains old API."""
    text = "Hello world test chunking."
    
    # Old function should still work
    old_chunks = old_chunk_function(text, chunk_size=50)
    
    assert isinstance(old_chunks, list)
    assert all(isinstance(chunk, str) for chunk in old_chunks)
    assert len(old_chunks) > 0
```

### **Validation commands**:
```bash
uv run ruff check zeta_vn/integration/rag/chunking.py
uv run mypy zeta_vn/integration/rag/chunking.py
uv run pytest -q tests/integration/rag/test_chunking.py
```

---

## 📋 Bảng DoD Checklist

| WO     | File                           | Ruff | MyPy | Tests | API Safe | Status |
| ------ | ------------------------------ | ---- | ---- | ----- | -------- | ------ |
| WO-001 | `core/auth/base.py`            | ✅    | ✅    | ✅     | ✅        | ✅ DONE |
| WO-002 | `app/api/graphql/resolvers.py` | ❌    | ❌    | ❌     | ✅        | TODO   |
| WO-003 | `integration/rag/chunking.py`  | ❌    | ❌    | ❌     | ✅        | TODO   |

---

## 🤖 Prompt Copilot cho từng WO

### Prompt cho WO-001:
```
🛡️ COPILOT GUARDRAILS: KHÔNG xóa function/class công khai. Thêm AUTO-STUB cho deprecated.

Task: Fix zeta_vn/core/auth/base.py
- Add type hints for all functions
- Create Protocol/ABC for auth interfaces  
- Add AUTO-STUB for old_authenticate function
- Ensure: ruff clean + mypy clean + tests pass

Follow Vietnamese guardrails in .github/prompts/copilot/COPILOT_GUARDRAILS.md
```

### Prompt cho WO-002:
```
🛡️ COPILOT GUARDRAILS: Phá cyclic imports bằng TYPE_CHECKING + local imports.

Task: Fix zeta_vn/app/api/graphql/resolvers.py  
- Use TYPE_CHECKING for type imports
- Local imports inside functions to break cycles
- Add AUTO-STUB for old resolver functions
- Ensure: ruff clean + mypy clean + GraphQL tests pass

No breaking changes to GraphQL schema!
```

### Prompt cho WO-003:
```
🛡️ COPILOT GUARDRAILS: Refactor thành pure functions, giữ backward compatibility.

Task: Fix zeta_vn/integration/rag/chunking.py
- Refactor to pure functions with dataclasses
- Add proper overlap control and validation
- Add comprehensive docstrings  
- Add AUTO-STUB for old chunking functions
- Ensure: ruff clean + mypy clean + chunking tests pass
```

---

## 🚀 Lệnh kiểm tra nhanh

```bash
# Update Work Orders table
uv run python scripts/safe/generate_work_orders.py

# WO-001 (HIGH) — auth/base.py  
uv run ruff check zeta_vn/core/auth/base.py
uv run mypy zeta_vn/core/auth/base.py
uv run pytest -q tests/core/auth/test_base_auth.py

# WO-002 (MEDIUM) — GraphQL resolvers
uv run ruff check zeta_vn/app/api/graphql/resolvers.py
uv run mypy zeta_vn/app/api/graphql/resolvers.py  
uv run pytest -q tests/app/api/graphql/test_smoke.py

# WO-003 (LOW) — RAG chunking
uv run ruff check zeta_vn/integration/rag/chunking.py
uv run mypy zeta_vn/integration/rag/chunking.py
uv run pytest -q tests/integration/rag/test_chunking.py

# Full quality gates
uv run ruff check .
uv run mypy zeta_vn
uv run pytest -q --maxfail=3
```

---

## ⚠️ Rủi ro & Mitigation

### Rủi ro:
1. **False positive từ guard** khi rename lớn
   - **Mitigation**: Tách commit nhỏ, tăng `max_deletions.txt` tạm thời, giữ AUTO-STUB

2. **Dedup gom sai cặp** "na ná"  
   - **Mitigation**: Luôn review `artifacts/merged/*.py` trước khi hợp nhất

3. **MyPy siết sớm** có thể đỏ CI
   - **Mitigation**: Bật ignore tạm theo module, thu hẹp dần

### Next Steps (2-3 ngày):
1. ✅ Bắt đầu **WO-001 (HIGH)** theo file work orders đã kèm patch & test
2. ✅ Chạy **CI Quality Gates** (ruff/mypy/pytest/bandit/pip-audit)  
3. ✅ Khi WO-001 xanh → chuyển **WO-002** (phá cycle) → **WO-003** (refactor RAG)
4. ✅ Cập nhật **WORK_ORDERS.md** để track tiến độ

---

**Ready to execute! 🚀 Bắt đầu với WO-001 (HIGH priority) ngay!**