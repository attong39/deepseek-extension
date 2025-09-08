# Missing Code Audit System

Hệ thống audit toàn diện để phát hiện code thiếu chức năng và kiểm tra conformance giữa Protocols và Adapters trong dự án ZETA.

## 🎯 Mục tiêu

- **Static Scan**: Phát hiện stub patterns, code chưa implement trong Python và TypeScript
- **Conformance Check**: Kiểm tra tính tuân thủ giữa Adapters và Protocols (Clean Architecture)
- **CI/CD Integration**: Fail build khi có HIGH severity issues
- **Automated Fixes**: Tools để tự động sửa một số pattern phổ biến

## 📋 Phát hiện các vấn đề

### Python Issues
- **HIGH Severity**:
  - `pass` trong function bodies
  - `...` (ellipsis) trong function bodies  
  - `raise NotImplementedError` chưa implement
  - Syntax errors

- **MEDIUM Severity**:
  - `TODO`/`FIXME`/`HACK` comments
  - Functions return `None` nhưng annotation non-Optional

- **LOW Severity**:
  - Empty classes (chỉ có `pass`)

### TypeScript Issues  
- **HIGH Severity**:
  - `throw new Error('Not implemented')`

- **MEDIUM Severity**:
  - `TODO`/`FIXME`/`HACK` comments
  - Empty function bodies

- **LOW Severity**:  
  - Usage of `any` type
  - `as any` casts

### Conformance Issues
- **HIGH Severity**:
  - Missing methods in Protocol implementations
  - Wrong method signatures (parameter mismatches)

- **MEDIUM Severity**:
  - Wrong return type annotations

## 🚀 Quick Start

### 1. Cài đặt dependencies
```bash
uv sync
```

### 2. Chạy full audit
```bash
# Audit missing code patterns
uv run python scripts/missing_code_audit.py

# Check Protocol conformance  
uv run python scripts/check_conformance.py

# Chạy demo system
uv run python scripts/demo_missing_code_system.py
```

### 3. Xem báo cáo
```bash
# Báo cáo được lưu trong .artifacts/
cat .artifacts/missing_code_report.json
cat .artifacts/conformance_report.json
```

### 4. Quick fix các vấn đề phổ biến
```bash
# Tự động sửa stubs và tạo TODO list
uv run python scripts/quick_fix_stubs.py
```

## 🔧 Sử dụng @implements decorator

### 1. Đánh dấu implementations

```python
from zeta_vn.tools.implements import implements
from typing import Protocol

# Define Protocol
class CacheBackend(Protocol):
    async def get(self, key: str) -> Any | None: ...
    async def set(self, key: str, value: Any) -> None: ...

# Mark implementation với decorator
@implements(CacheBackend)
class RedisCacheAdapter:
    async def get(self, key: str) -> Any | None:
        return await self.redis.get(key)
    
    async def set(self, key: str, value: Any) -> None:
        await self.redis.set(key, value)
```

### 2. Conformance checking sẽ tự động phát hiện:
- Missing methods
- Wrong parameter names  
- Wrong return types
- Extra methods not in Protocol

## 📊 Báo cáo mẫu

### Missing Code Report
```json
{
  \"summary\": {
    \"total\": 1801,
    \"high\": 301,
    \"medium\": 1279, 
    \"low\": 221
  },
  \"by_kind\": {
    \"stub-function\": 299,
    \"none-return-mismatch\": 1133,
    \"any-type\": 202,
    \"todo-marker\": 146
  }
}
```

### Conformance Report
```json
{
  \"summary\": {
    \"total_problems\": 5,
    \"high_severity\": 2,
    \"medium_severity\": 2,
    \"low_severity\": 1
  },
  \"by_category\": {
    \"missing_method\": 2,
    \"signature_mismatch\": 2,
    \"extra_methods\": 1
  }
}
```

## 🔄 CI/CD Integration

### GitHub Actions Workflow
File `.github/workflows/missing-code.yml` đã được tạo sẵn với:

- Chạy missing code audit
- Chạy conformance check  
- Fail build nếu có HIGH severity issues
- Upload artifacts
- Comment trên PR với kết quả

### Enable workflow:
```bash
# Workflow sẽ tự động chạy trên push/PR
# Không cần setup gì thêm
```

## 📝 Tests

```bash
# Chạy tests cho audit tools
uv run pytest zeta_vn/tests/tools/ -v

# Test specific modules
uv run pytest zeta_vn/tests/tools/test_missing_code_audit.py
uv run pytest zeta_vn/tests/tools/test_conformance.py
```

## 🛠️ Scripts Overview

| Script                                | Mục đích                   | Exit Code            |
| ------------------------------------- | -------------------------- | -------------------- |
| `scripts/missing_code_audit.py`       | Scan missing code patterns | 1 nếu có HIGH issues |
| `scripts/check_conformance.py`        | Check Protocol conformance | 1 nếu có HIGH issues |
| `scripts/quick_fix_stubs.py`          | Auto-fix common patterns   | 0 (always)           |
| `scripts/demo_missing_code_system.py` | Demo full system           | 1 nếu có HIGH issues |

## 📁 File Structure

```
zeta_vn/
├── tools/
│   └── implements.py              # @implements decorator
├── tests/tools/                   # Tests cho audit tools
├── scripts/
│   ├── missing_code_audit.py      # Main audit script  
│   ├── check_conformance.py       # Conformance checker
│   ├── quick_fix_stubs.py         # Auto-fix tools
│   └── demo_missing_code_system.py # Demo script
├── examples/
│   └── implements_usage_example.py # Usage examples
├── .artifacts/                    # Generated reports
├── .github/workflows/
│   └── missing-code.yml          # CI workflow
└── TODO.md                       # Generated TODO list
```

## ⚙️ Configuration

### Scan Roots (scripts/missing_code_audit.py)
```python
SCAN_ROOTS = [
    Path(\"zeta_vn\"),           # Python apps/backend
    Path(\"desktop_ai_zeta/src\"), # TypeScript frontend  
]
```

### Quality Gates
- **HIGH severity**: Build fails, must fix before merge
- **MEDIUM severity**: Warning, should fix eventually  
- **LOW severity**: Information, optional fixes

## 🎯 Best Practices

1. **Add @implements decorator** cho mọi adapter implementations
2. **Chạy audit trước commit**: `uv run python scripts/missing_code_audit.py`
3. **Fix HIGH severity first**: Ưu tiên NotImplementedError và missing methods
4. **Review generated TODO.md**: Plan implementation tasks
5. **Enable CI workflow**: Prevent regression

## 🚨 Common Issues & Fixes

### Issue: \"301 HIGH severity issues found\"
```bash
# Quick fix automatic patterns
uv run python scripts/quick_fix_stubs.py

# Manual review TODO.md cho remaining issues
cat TODO.md
```

### Issue: \"Missing method in Protocol implementation\"
```python
# Add missing method to implementation class
@implements(MyProtocol)
class MyImplementation:
    def missing_method(self, param: str) -> bool:
        raise NotImplementedError(\"TODO: Implement missing_method\")
```

### Issue: \"Parameter mismatch\" 
```python
# Fix parameter names to match Protocol
# Protocol định nghĩa:
def process(self, data: str, options: dict) -> str: ...

# Implementation phải match exactly:
def process(self, data: str, options: dict) -> str:
    return f\"processed: {data}\"
```

## 📈 Success Metrics

- **Zero HIGH severity issues** trong main branch
- **All @implements decorators** properly registered
- **CI green** cho mọi PRs
- **Decreasing trend** trong MEDIUM/LOW issues

## 🔮 Future Enhancements

1. **Coverage Integration**: Include coverage data trong audit
2. **React Component Patterns**: Detect incomplete React components  
3. **API Contract Validation**: Check FastAPI ↔ Frontend schema sync
4. **Performance Rules**: Flag expensive patterns
5. **Documentation Coverage**: Ensure public APIs have docstrings

---

> 💡 **Tip**: Bắt đầu với `uv run python scripts/demo_missing_code_system.py` để xem overview system và current status của repo.
