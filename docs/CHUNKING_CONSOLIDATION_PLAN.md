# CHUNKING CODE CONSOLIDATION PLAN

## 🎯 Mục tiêu
Hợp nhất và loại bỏ code trùng lặp trong các service chunking, giữ kiến trúc Clean Architecture.

## 📊 Hiện tại (Trùng lặp)

### Files có logic chunking:
1. `core/services/rag_chunker.py` ⭐ (Simple, lightweight)
2. `core/services/chunking.py` (Token-aware với tiktoken)
3. `core/adapters/vector/chunking_service.py` (Enhanced với nhiều strategy)
4. `core/adapters/vector/semantic_chunking.py` (Semantic chunking)
5. `core/services/retrieval_service.py` (Chỉ có class Chunk)

### Chunk models trùng lặp:
- `Chunk` (rag_chunker.py) - Simple
- `Chunk` (retrieval_service.py) - Với meta
- `TextChunk` (chunking_service.py) - Với position
- `DocumentChunk` (semantic_chunking.py) - Với full metadata

## 🎯 Kế hoạch consolidation

### Phase 1: Chuẩn hóa Domain Model
**Target**: `core/domain/entities/Chunk.py`
```python
@dataclass(frozen=True, slots=True)
class Chunk:
    """Unified chunk entity."""
    text: str
    start: int
    end: int
    index: int
    metadata: dict[str, Any] = field(default_factory=dict)
    
@dataclass(frozen=True, slots=True) 
class ChunkWithScore:
    chunk: Chunk
    score: float
```

### Phase 2: Consolidate Interfaces
**Target**: `core/domain/ports/chunking_port.py`
```python
class ChunkingPort(Protocol):
    def chunk(self, text: str, strategy: str = "sentence") -> list[Chunk]: ...
    def estimate_chunks(self, text: str) -> int: ...
```

### Phase 3: Single Implementation
**Target**: `core/services/chunking_service.py` (rename từ chunking.py)
```python
class ChunkingService:
    """Unified chunking service với all strategies."""
    def __init__(self, strategy: ChunkStrategy = "sentence"): ...
    def chunk(self, text: str, **opts) -> list[Chunk]: ...
    
    # Private methods
    def _chunk_simple(self, text: str, size: int, overlap: int) -> list[Chunk]: ...
    def _chunk_sentence(self, text: str, size: int, overlap: int) -> list[Chunk]: ...
    def _chunk_semantic(self, text: str, size: int, overlap: int) -> list[Chunk]: ...
    def _chunk_token_aware(self, text: str, max_tokens: int, overlap: int) -> list[Chunk]: ...
```

### Phase 4: Adapter Layer
**Target**: `core/adapters/vector/chunking_adapter.py`
```python
class VectorChunkingAdapter:
    """Adapter cho vector store chunking needs."""
    def __init__(self, chunking_service: ChunkingService): ...
    def chunk_for_embedding(self, text: str) -> list[DocumentChunk]: ...
```

## 🗑️ Files to DELETE

### Immediate deletion:
1. ✅ `core/services/rag_chunker.py` - Logic merge vào chunking_service
2. ✅ `core/adapters/vector/chunking_service.py` - Logic merge vào core
3. ❓ `core/adapters/vector/semantic_chunking.py` - Keep semantic strategies only

### Keep and refactor:
1. ✅ `core/services/chunking.py` → rename to `chunking_service.py` + enhance
2. ✅ `core/services/retrieval_service.py` - Remove Chunk class, use domain

## 🔄 Migration Steps

### Step 1: Create Domain Entity
```bash
# Create unified chunk entity
touch core/domain/entities/Chunk.py
```

### Step 2: Update Port Interface
```bash
# Update chunking port
edit core/domain/ports/chunking_port.py
```

### Step 3: Consolidate Service
```bash
# Merge all chunking logic into one service
cp core/services/chunking.py core/services/chunking_service.py
# Merge logic from other files
# Update imports throughout codebase
```

### Step 4: Update Usage
```bash
# Find all imports and usage
grep -r "from.*rag_chunker import" .
grep -r "RagChunker" .
# Replace with new unified service
```

### Step 5: Delete Duplicates
```bash
rm core/services/rag_chunker.py
rm core/adapters/vector/chunking_service.py
# Update __init__.py files
```

### Step 6: Update Tests
```bash
# Consolidate tests
mv tests/unit/test_rag_chunker_sentences.py tests/unit/test_chunking_service.py
# Update test imports and assertions
```

## 🧪 Testing Strategy

### Before migration:
```bash
# Run existing tests to establish baseline
uv run pytest tests/unit/test_rag_chunker_sentences.py -v
uv run pytest tests/unit/test_rag_services.py -v
```

### After migration:
```bash
# Verify new unified service
uv run pytest tests/unit/test_chunking_service.py -v
# Integration tests
uv run pytest tests/integration/test_rag_integration.py -v
```

## 🎯 Expected Benefits

### Code reduction:
- **-3 duplicate files** (rag_chunker.py, chunking_service.py từ adapters, duplicate logic)
- **-200+ lines** of duplicate code
- **1 unified API** thay vì 4-5 different interfaces

### Maintenance:
- **Single source of truth** cho chunking logic
- **Easier testing** với 1 service thay vì nhiều
- **Consistent behavior** across toàn system

### Performance:
- **Better caching** với unified implementation
- **Reduced memory** usage (không có duplicate instances)
- **Faster imports** (ít modules hơn)

## ⚠️ Risks & Mitigation

### Risk 1: Breaking changes
**Mitigation**: Alias imports trong __init__.py cho backward compatibility

### Risk 2: Test failures
**Mitigation**: Comprehensive test migration và regression testing

### Risk 3: Performance regression  
**Mitigation**: Benchmark before/after migration

## 📋 Success Criteria

- [ ] All existing tests pass với new unified service
- [ ] No duplicate chunking logic remaining
- [ ] Backward compatibility maintained qua aliases
- [ ] Documentation updated
- [ ] Performance maintained or improved

---

**Timeline**: 2-3 hours work
**Priority**: HIGH (code hygiene + maintenance burden)
**Risk Level**: MEDIUM (many touchpoints but straightforward refactor)