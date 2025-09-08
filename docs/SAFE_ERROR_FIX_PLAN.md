# 🛠️ PLAN SỬA LỖI AN TOÀN CHO ZETA_VN

## 📊 Tình Trạng Hiện Tại

- **Tổng lỗi mypy**: ~21,986 (chủ yếu type checking)
- **Lỗi ruff**: ~200+ (import, style, security)
- **Trạng thái**: Cần sửa theo độ ưu tiên để giữ project an toàn

## 🎯 Chiến Lược Sửa Lỗi (4 Phases)

### PHASE 1: Critical & Security Issues (Ưu tiên cao) 🚨

#### 1.1 Security Fixes
- [ ] **Hardcoded password**: `zeta_vn/trainer/evaluators/gpt5_verifier.py:31`
  ```python
  # Thay đổi từ:
  PASS = "PASS"  # S105: Possible hardcoded password
  # Thành:
  EVALUATION_PASS = "PASS"  # Rõ ràng đây là constant cho evaluation
  ```

- [ ] **Exception handling**: Thêm logging thay vì `try-except-pass`
  ```python
  # Thay vì:
  try:
      dangerous_operation()
  except:
      pass
  
  # Dùng:
  try:
      dangerous_operation()
  except SpecificException as e:
      logger.warning(f"Operation failed: {e}")
  ```

#### 1.2 Import & Module Issues
- [ ] **Invalid module names**: Đổi tên PascalCase → snake_case
  - `Agent.py` → `agent.py`  
  - `Chat.py` → `chat.py`
  - `Memory.py` → `memory.py`
  - `Plan.py` → `plan.py`
  - `User.py` → `user.py`

- [ ] **Import ordering**: Auto-fix với ruff
  ```bash
  uv run ruff check . --fix --select I
  ```

### PHASE 2: Type Safety Issues (Ưu tiên trung) 🔍

#### 2.1 Missing Type Annotations
- [ ] **ScoredChunk import**: Sửa lỗi trong `context_planner.py`
  ```python
  # Kiểm tra và fix import path
  try:
      from zeta_vn.core.domain.entities.chunk import ScoredChunk
  except ImportError:
      # Tạo temporary stub hoặc fix import path
  ```

- [ ] **Retrieval service**: Thêm return statements
  ```python
  def upsert_chunks(...) -> int:
      """Thêm/cập nhật nhiều chunk. Trả về số chunk đã upsert."""
      # Implementation here
      return count  # Thêm return thay vì ...
  ```

#### 2.2 Complex Functions Refactoring
- [ ] **Chunking service complexity**: Tách các hàm quá phức tạp
  - `_split_text_recursive` (35 → 15 complexity)
  - `_chunk_by_paragraphs` (28 → 15 complexity)  
  - `_chunk_by_sentences` (18 → 15 complexity)

### PHASE 3: Code Quality Issues (Ưu tiên thấp) 🧹

#### 3.1 Unused Variables & Arguments
- [ ] **Loop variables**: Rename với prefix `_`
  ```python
  # Từ:
  for name in items:  # B007: unused
  
  # Thành:
  for _name in items:
  ```

- [ ] **Function arguments**: Thêm `# noqa: ARG001` hoặc sử dụng
  ```python
  def func(used_arg, unused_arg):  # ARG001
      # Option 1: Use it
      _ = unused_arg
      # Option 2: Add noqa comment
  ```

#### 3.2 Line Length & Formatting
- [ ] **Auto-format**: 
  ```bash
  uv run ruff format .
  uv run ruff check . --fix --select E501
  ```

### PHASE 4: Enhancement & Prevention (Tương lai) 🚀

#### 4.1 CI/CD Quality Gates
- [ ] **Pre-commit hooks**: Setup tự động format
- [ ] **GitHub Actions**: Chặn merge nếu có lỗi critical
- [ ] **Type checking**: Tăng cường mypy strict mode

#### 4.2 Development Guidelines  
- [ ] **Type annotation standards**
- [ ] **Error handling patterns**
- [ ] **Security review checklist**

## 🔧 Script Tự Động Sửa Lỗi

### 1. Quick Wins (Auto-fixable)
```bash
# Format code
uv run ruff format .

# Fix imports
uv run ruff check . --fix --select I,E402

# Fix simple issues
uv run ruff check . --fix --select F,E,W
```

### 2. Rename Files (Semi-manual)
```python
# Script đổi tên file an toàn
import os
from pathlib import Path

def rename_entity_files():
    """Đổi tên các entity file từ PascalCase → snake_case"""
    base_path = Path("zeta_vn/core/domain/entities")
    
    renames = {
        "Agent.py": "agent.py",
        "Chat.py": "chat.py", 
        "Memory.py": "memory.py",
        "Plan.py": "plan.py",
        "User.py": "user.py"
    }
    
    for old_name, new_name in renames.items():
        old_path = base_path / old_name
        new_path = base_path / new_name
        
        if old_path.exists() and not new_path.exists():
            print(f"Renaming {old_path} → {new_path}")
            # Backup first
            backup_path = old_path.with_suffix(".py.backup")
            old_path.rename(backup_path)
            # Then rename
            backup_path.rename(new_path)
```

### 3. Security Fixes
```python
def fix_security_issues():
    """Sửa các lỗi security cơ bản"""
    # Replace hardcoded passwords with constants
    # Add proper exception logging
    # Validate inputs
```

## 📈 Success Metrics

### Immediate Goals (1-2 days)
- [ ] Giảm lỗi security từ ~20 → 0
- [ ] Giảm lỗi import từ ~50 → 0  
- [ ] Pass basic quality checks

### Short-term (1 week)
- [ ] Giảm mypy errors từ 21,986 → <5,000
- [ ] Tất cả critical functions có type hints
- [ ] CI/CD pipeline hoạt động stable

### Long-term (1 month)
- [ ] Mypy strict mode pass
- [ ] 100% test coverage cho core modules
- [ ] Zero security warnings

## 🚀 Getting Started

1. **Backup current state**: 
   ```bash
   git checkout -b fix/safe-error-resolution
   ```

2. **Run Phase 1 fixes**:
   ```bash
   uv run ruff format .
   uv run ruff check . --fix --select I,F401,F841
   ```

3. **Test after each phase**:
   ```bash
   uv run pytest -x --lf
   ```

4. **Monitor progress**:
   ```bash
   uv run ruff check . | wc -l  # Count remaining issues
   uv run mypy . | grep error | wc -l  # Count type errors
   ```

---
**⚠️ LƯU Ý AN TOÀN**: 
- Luôn backup trước khi sửa
- Test từng phase trước khi chuyển phase tiếp theo
- Commit nhỏ, thường xuyên
- Rollback ngay nếu có regression