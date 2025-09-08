# SAFE CHUNKING CONSOLIDATION STRATEGY

## 🛡️ Nguyên tắc an toàn

### KHÔNG được phá vỡ:
1. ✅ Existing APIs và public interfaces
2. ✅ Test suite hiện tại
3. ✅ Production functionality
4. ✅ Import paths đang được sử dụng

### PHẢI đảm bảo:
1. ✅ Backward compatibility 100%
2. ✅ Zero downtime migration
3. ✅ Rollback capability
4. ✅ Comprehensive testing

## 📋 PHASE 1: SAFE DISCOVERY & ANALYSIS

### Step 1.1: Map all dependencies
```bash
# Tìm tất cả files import chunking modules
grep -r "from.*rag_chunker" zeta_vn/ --include="*.py"
grep -r "from.*chunking" zeta_vn/ --include="*.py" 
grep -r "RagChunker\|TokenChunker\|ChunkingService" zeta_vn/ --include="*.py"
grep -r "class.*Chunk" zeta_vn/ --include="*.py"
```

### Step 1.2: Test current state
```bash
# Establish baseline
uv run pytest tests/unit/test_rag_chunker_sentences.py -v
uv run pytest tests/unit/test_rag_services.py -v  
uv run pytest tests/unit/ -k "chunk" -v
uv run ruff check zeta_vn/core/services/
uv run mypy zeta_vn/core/services/
```

### Step 1.3: Create comprehensive backup
```bash
# Backup entire affected structure
cp -r zeta_vn/core/services/ _backup_services_$(date +%Y%m%d_%H%M%S)/
cp -r zeta_vn/core/adapters/vector/ _backup_vector_$(date +%Y%m%d_%H%M%S)/
cp -r zeta_vn/tests/unit/ _backup_tests_$(date +%Y%m%d_%H%M%S)/
```

## 📋 PHASE 2: GRADUAL SAFE MIGRATION

### Step 2.1: Create NEW unified service (không xóa cũ)
```bash
# Tạo service mới song song với cũ
touch zeta_vn/core/services/unified_chunking_service.py
# Implement tất cả functionality trong file mới
```

### Step 2.2: Create domain entity (non-breaking)
```bash
# Tạo domain entity mới
touch zeta_vn/core/domain/entities/chunk.py
# Implement unified Chunk class
```

### Step 2.3: Add compatibility layer
```python
# Trong mỗi file cũ, thêm import alias:
# rag_chunker.py
from zeta_vn.core.services.unified_chunking_service import UnifiedChunkingService as RagChunker

# chunking.py  
from zeta_vn.core.services.unified_chunking_service import UnifiedChunkingService as TokenChunker
```

### Step 2.4: Test new service extensively
```bash
# Test new service với existing test cases
uv run pytest tests/unit/test_unified_chunking_service.py -v
# Integration tests
uv run pytest tests/integration/ -k "chunk" -v
```

## 📋 PHASE 3: SAFE CUTOVER

### Step 3.1: Update imports gradually (file by file)
```python
# Update imports one file at a time, test after each change
# Old:
from zeta_vn.core.services.rag_chunker import RagChunker
# New:
from zeta_vn.core.services.unified_chunking_service import UnifiedChunkingService as RagChunker
```

### Step 3.2: Verify each change
```bash
# After each file update:
uv run pytest tests/unit/ -k "chunk" -v
uv run ruff check .
uv run mypy .
```

### Step 3.3: Only delete old files AFTER everything works
```bash
# Chỉ xóa sau khi 100% confident
# rm zeta_vn/core/services/rag_chunker.py  # CUỐI CÙNG
```

## 🚨 SAFETY CHECKPOINTS

### Before each step:
- [ ] All tests passing
- [ ] No lint/type errors  
- [ ] Backup created
- [ ] Rollback plan ready

### After each step:
- [ ] All tests still passing
- [ ] No new lint/type errors
- [ ] Functionality unchanged
- [ ] Performance maintained

## 🛟 ROLLBACK PLAN

### If anything goes wrong:
```bash
# Immediate rollback
git checkout HEAD -- zeta_vn/core/services/
git checkout HEAD -- zeta_vn/core/adapters/vector/
git checkout HEAD -- zeta_vn/tests/unit/

# Or restore from backup
cp -r _backup_services_*/ zeta_vn/core/services/
cp -r _backup_vector_*/ zeta_vn/core/adapters/vector/
cp -r _backup_tests_*/ zeta_vn/tests/unit/
```

## 🎯 SPECIFIC SAFE ACTIONS FOR CONTEXT_PLANNER

### Current risk:
`context_planner.py` imports `ScoredChunk` from `retrieval_service.py`

### Safe solution:
1. **KHÔNG** thay đổi `retrieval_service.py` import structure
2. **Thêm** domain entity mới song song
3. **Gradual migration** sau khi unified service ổn định

### Immediate safe action:
```python
# context_planner.py - add fallback import
try:
    from zeta_vn.core.domain.entities.chunk import ScoredChunk
except ImportError:
    from zeta_vn.core.services.retrieval_service import ScoredChunk
```

## ⏱️ TIMELINE ESTIMATE

### Phase 1 (Discovery): 30 minutes
- Map dependencies
- Create backups  
- Test baseline

### Phase 2 (Migration): 2 hours
- Create new service
- Add compatibility
- Extensive testing

### Phase 3 (Cutover): 1 hour  
- Gradual import updates
- Final verification
- Cleanup

### Total: ~3.5 hours (với plenty safety margin)

## 🎯 SUCCESS CRITERIA

- [ ] Zero breaking changes
- [ ] All existing tests pass
- [ ] No new lint/type errors
- [ ] Performance maintained/improved
- [ ] Backward compatibility preserved
- [ ] Clean, consolidated codebase