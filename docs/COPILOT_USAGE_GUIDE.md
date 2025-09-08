# Hướng Dẫn Sử Dụng Copilot Quality System

## 🚀 Cài Đặt Nhanh

### 1. Bật Git Hooks
```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

### 2. Kiểm Tra Setup
```bash
# Test copilot guard
uv run python tools/copilot_guard.py

# Test full quality check
uv run pytest -q
uv run ruff check .
uv run mypy .
```

## 📋 Workflow Chuẩn

### Với Copilot Chat

1. **Bắt đầu tác vụ:**
   ```
   Đọc GUIDE.md + copilot-instructions.md + PROJECT_MAP.md
   /map zeta_vn/core/domain/entities/agent.py
   ```

2. **Lập kế hoạch:**
   ```
   /plan thêm trường metadata vào Agent entity
   ```

3. **Implement:**
   ```
   /patch zeta_vn/core/domain/entities/agent.py
   /tests Agent entity với metadata field
   ```

4. **Quality check:**
   ```
   /qa
   ```

5. **Tạo PR:**
   ```
   /pr
   ```

### Với VS Code Tasks

- **Ctrl+Shift+P** → "Tasks: Run Task"
- Chọn task phù hợp:
  - `QA: Full Quality Check` - kiểm tra toàn bộ
  - `Guard: Check Consistency` - kiểm tra tính nhất quán
  - `QA: Pre-commit Check` - chạy pre-commit hooks

### Với Terminal

```bash
# Kiểm tra consistency trước khi code
uv run python tools/copilot_guard.py

# Full quality check
uv run ruff format . && \
uv run ruff check . && \
uv run mypy . && \
uv run pytest -q

# Security checks (non-blocking)
uv run bandit -q -r zeta_vn
uv run pip-audit -q
uv run vulture zeta_vn
```

## 🔧 Quy Trình Sửa Lỗi

### Khi Copilot Guard Fail

```
❌ copilot_guard: phát hiện vi phạm tính nhất quán

1. Khi chạm 'domain/entities', cần có thay đổi ở '^tests/'
   File trigger: ['zeta_vn/core/domain/entities/agent.py']
   Gợi ý: Thêm/cập nhật tests trong tests/unit/domain/
```

**Cách khắc phục:**
1. Thêm/cập nhật tests tương ứng
2. Hoặc stage thêm file test đã có sẵn nếu chưa thay đổi

### Khi Ruff Fail
```bash
# Auto-fix hầu hết issues
uv run ruff check --fix .
uv run ruff format .
```

### Khi MyPy Fail
```bash
# Xem chi tiết lỗi type checking
uv run mypy . --show-error-codes
```

### Khi Tests Fail
```bash
# Chạy test cụ thể để debug
uv run pytest -xvs tests/unit/domain/test_agent.py::test_agent_creation
```

## 📁 Cấu Trúc File Rules

### Khi Chạm Domain
- **Trigger:** `zeta_vn/core/domain/*`
- **Required:** `tests/*`
- **Gợi ý:** Thêm/cập nhật unit tests

### Khi Chạm API
- **Trigger:** `zeta_vn/app/api/v1/*`
- **Required:** `tests/*` hoặc `desktop_ai_zeta/scripts/contract_guard.mjs`
- **Gợi ý:** Cập nhật API tests hoặc apps/desktop contracts

### Khi Chạm Database
- **Trigger:** `zeta_vn/data/models/*`
- **Required:** `zeta_vn/data/migrations/*`
- **Gợi ý:** Tạo Alembic migration

### Khi Chạm Interfaces
- **Trigger:** `zeta_vn/core/interfaces/*`
- **Required:** `zeta_vn/core/services/*` hoặc `zeta_vn/data/*`
- **Gợi ý:** Cập nhật implementations

## 🔍 Debug Common Issues

### "No staged files" Error
```bash
# Stage một số files trước
git add zeta_vn/core/domain/entities/agent.py
git add tests/unit/domain/test_agent.py
```

### Import Errors
```bash
# Kiểm tra PYTHONPATH
export PYTHONPATH="${PWD}/zeta_vn:${PWD}/zeta_vn/app:${PWD}/zeta_vn/core:${PWD}/zeta_vn/data"
```

### Type Errors với Pydantic v2
```python
from __future__ import annotations
from pydantic import BaseModel, Field

# Sử dụng ConfigDict thay vì class Config
class MyModel(BaseModel):
    model_config = {"frozen": True}
```

## 🎯 Best Practices

### 1. Luôn Map Trước Khi Code
```
/map path/to/file.py  # hiểu impact
/plan feature_name    # lập kế hoạch
/patch file.py        # implement
```

### 2. Test-Driven Development
- Viết test trước hoặc cùng lúc với implementation
- Coverage tối thiểu 75%, domain layer 90%

### 3. Atomic Commits
```bash
# Commit theo lớp
git add zeta_vn/core/domain/
git commit -m "feat(domain): add metadata field to Agent entity"

git add tests/unit/domain/
git commit -m "test(domain): add tests for Agent metadata field"
```

### 4. API Changes
```bash
# Sau khi thay đổi API, luôn regen contracts
cd desktop_ai_zeta
node scripts/generate_openapi_types.mjs
git add src/api/generated/
git commit -m "chore(contracts): sync API types"
```

## 📊 CI/CD Integration

### GitHub Actions sẽ tự động:
- Chạy `copilot_guard.py`
- Lint với ruff
- Type check với mypy
- Run tests với coverage
- Security scan với bandit
- Contract guard cho apps/desktop (nếu API thay đổi)

### Để Pass CI:
1. ✅ Tất cả quality gates local pass
2. ✅ Coverage ≥ 75%
3. ✅ Không có type errors
4. ✅ Architectural consistency OK
5. ✅ Desktop contracts đồng bộ (nếu có)

## 💡 Tips & Tricks

### Nhanh chóng fix style issues:
```bash
# One-liner để fix hầu hết style issues
uv run ruff check --fix . && uv run ruff format .
```

### Debug test failures:
```bash
# Chạy test với output chi tiết
uv run pytest -xvs --tb=short

# Chỉ chạy failed tests
uv run pytest --lf
```

### Check specific rule violations:
```bash
# Xem rules copilot_guard đang check
grep -A 5 "RULES = " tools/copilot_guard.py
```

### Override pre-commit tạm thời (không khuyến nghị):
```bash
git commit --no-verify -m "WIP: temporary commit"
```

## 🆘 Khi Gặp Vấn Đề

1. **Đọc error message** từ copilot_guard - thường có gợi ý cụ thể
2. **Kiểm tra PROJECT_MAP.md** để hiểu dependencies
3. **Chạy từng tool riêng biệt** để isolate issue
4. **Hỏi Copilot** với context đầy đủ về lỗi
