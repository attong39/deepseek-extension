# 🤖 AI Project Optimization Report
Generated at: 2025-09-08 19:31:09

**Total optimization time:** 7.26 seconds

## 📊 Summary
- **Success rate:** 1/4 (25.0%)

## 🔍 Detailed Results
### Imports_Exports
- ✅ `python fix_imports_exports.py` (2.00s)

### Ruff
- ❌ `N/A` (0.00s)
  ```
  Unknown error...
  ```

### Mypy
- ❌ `mypy apps/backend/app/ apps/backend/core/ --ignore-missing-imports --no-error-summary` (5.26s)
  ```
  Unknown error...
  ```

### Pytest
- ❌ `pytest collection` (0.00s)
  ```
  ImportError while loading conftest 'E:\zeta-monorepo\apps\backend\tests\conftest.py'.
tests\conftest.py:40: in <module>
    from config.settings import Settings
config\settings\__init__.py:9: in <modu...
  ```
