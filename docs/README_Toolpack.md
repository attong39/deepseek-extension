# 🔧 Python Toolpack - Bộ công cụ tối ưu toàn diện

Bộ công cụ "quét – sửa – dọn – tối ưu" cho Python project với backup + rollback tự động, chỉ commit khi test pass.

## 🚀 Quick Start

### 1. Cài đặt công cụ

```bash
# Cài tất cả tool cần thiết
make tooling

# Hoặc manual
uv pip install ruff isort autoflake pycln mypy pytest coverage vulture deptry bandit pip-audit pre-commit
pre-commit install
```

### 2. Chạy dry-run để kiểm tra

```bash
# Xem tool sẽ làm gì (không thay đổi file)
make safe-dryrun

# Hoặc direct
python tools/fix_repo_safe.py --root zeta_vn
```

### 3. Apply thay đổi (có backup + rollback)

```bash
# Apply toàn bộ project
make safe-apply

# Hoặc theo từng thư mục
make safe-apply-core    # Chỉ core/
make safe-apply-app     # Chỉ app/
make safe-apply-data    # Chỉ data/
```

## 🛠️ Công cụ chính

### Safe Repository Fixer (`tools/fix_repo_safe.py`)

**Mục đích:** Tối ưu code Python mà không phá vỡ hành vi hiện tại.

**Quy trình:**
1. **Backup** toàn bộ package trước khi thay đổi
2. **Ensure `__init__.py`** - Tạo file thiếu
3. **Generate `__all__`** - Export API (conservative)
4. **Ruff --fix** - Sửa lỗi lint tự động
5. **isort** - Sắp xếp import
6. **autoflake** - Xóa import/variable thừa
7. **Ruff format** - Format code theo PEP8
8. **MyPy check** - Kiểm tra type hints
9. **PyTest** - Chạy test suite
10. **Auto rollback** nếu mypy/pytest fail

**Flags quan trọng:**
```bash
--root zeta_vn          # Package root (required)
--apply                 # Apply changes (default: dry-run)
--path core/            # Chỉ fix thư mục cụ thể
--no-auto-all           # Skip __all__ generation
--force-all             # Force regenerate __all__
--include "*.py"        # Include pattern
--exclude "__pycache__" # Exclude pattern
```

### Makefile Targets

```bash
# Setup
make tooling            # Cài đặt tất cả tool
make help              # Hiển thị help

# Quick fixes
make fix               # Ruff format + isort + autoflake
make lint              # Ruff check
make type              # MyPy
make test              # PyTest
make coverage          # PyTest với coverage

# Safe comprehensive fixes
make safe-dryrun       # Dry-run safe fixer
make safe-apply        # Apply safe fixer
make safe-apply-core   # Chỉ core/
make safe-apply-app    # Chỉ app/
make safe-apply-data   # Chỉ data/

# Security & dependencies
make security          # Bandit + pip-audit
make deps             # Deptry dependency check
make vulture          # Dead code detection

# Cleanup
make clean            # Xóa cache files
```

## 🔒 Bảo mật & Quality

### Pre-commit Hooks

Tự động chạy khi commit:
- **Ruff** (lint + format)
- **isort** (import sorting)
- **autoflake** (remove unused)
- **MyPy** (type checking)
- **Bandit** (security - report only)
- **PyTest** (unit tests only)

```bash
# Setup
pre-commit install

# Manual run
pre-commit run --all-files
```

### CI/CD Pipeline (`.github/workflows/ci_safe.yml`)

**Jobs:**
1. **Lint** - Ruff check + format
2. **Type Check** - MyPy strict mode
3. **Tests** - PyTest với coverage
4. **Security** - Bandit + pip-audit + safety
5. **Dependencies** - Deptry + vulture
6. **Safe Fixer Dry-run** - Kiểm tra tool hoạt động

**Artifacts:** Reports được upload tự động.

## 📊 Báo cáo

Tất cả báo cáo được lưu trong `reports/`:

```
reports/
├── fix_report.json          # Safe fixer results (JSON)
├── fix_report.md            # Safe fixer results (Markdown)
├── bandit_report.json       # Security issues
├── pip_audit_report.json    # Vulnerability scan
├── deptry_report.json       # Dependency issues
└── vulture_report.txt       # Dead code
```

## 🚨 Rollback Guide

### Tự động Rollback

Safe fixer tự động rollback khi:
- MyPy check fail
- PyTest fail
- Unexpected error

### Manual Rollback

```bash
# Backup được lưu trong .safe_fix_backups/
ls .safe_fix_backups/

# Restore manual (nếu cần)
rm -rf zeta_vn/
cp -r .safe_fix_backups/backup_20240829_143022/ zeta_vn/
```

### Git Rollback

```bash
# Nếu đã commit nhưng có vấn đề
git log --oneline -5                    # Xem recent commits
git reset --hard HEAD~1                # Quay lại commit trước
git reset --soft HEAD~1                # Giữ changes, unstage commit
```

## 🎯 Best Practices

### 1. Quy trình khuyến nghị

```bash
# 1. Backup current state
git add . && git commit -m "chore: backup before tooling"

# 2. Dry-run để xem thay đổi
make safe-dryrun

# 3. Apply từng phần (an toàn hơn)
make safe-apply-core        # Test
make safe-apply-app         # Test
make safe-apply-data        # Test

# 4. Kiểm tra kết quả
make test
make lint
make type

# 5. Commit nếu OK
git add .
git commit -m "chore(tooling): apply safe fix (ruff/isort/autoflake/mypy/pytest)"
```

### 2. Flags hữu ích

```bash
# Chỉ fix imports, không đụng __all__
python tools/fix_repo_safe.py --root zeta_vn --no-auto-all --apply

# Force regenerate __all__ (nguy hiểm)
python tools/fix_repo_safe.py --root zeta_vn --force-all --apply

# Chỉ fix một file cụ thể
python tools/fix_repo_safe.py --root zeta_vn --path core/domain/ --apply
```

### 3. Guardrails

- ✅ **Luôn dry-run trước**
- ✅ **Commit trạng thái hiện tại trước khi apply**
- ✅ **Test từng phần thay vì toàn bộ**
- ✅ **Đọc reports trước khi commit**
- ❌ **KHÔNG push ngay sau khi apply**
- ❌ **KHÔNG skip testing sau optimization**

## 🐛 Troubleshooting

### Issue: MyPy check fail

```bash
# Xem chi tiết error
uv run mypy zeta_vn/

# Fix common issues
# 1. Missing type hints
# 2. Import issues
# 3. Configuration problems
```

### Issue: PyTest fail

```bash
# Chạy tests với verbose
uv run pytest -v tests/

# Chạy specific test
uv run pytest tests/test_specific.py -v
```

### Issue: Rollback không tự động

```bash
# Kiểm tra backup
ls -la .safe_fix_backups/

# Manual restore
python tools/fix_repo_safe.py --root zeta_vn --restore-from backup_20240829_143022
```

### Issue: Pre-commit quá chậm

```bash
# Skip specific hooks
SKIP=mypy,vulture git commit -m "temp commit"

# Update pre-commit
pre-commit autoupdate
```

## 📈 Metrics & Monitoring

### Tracking Quality Improvements

```bash
# Before optimization
make qa-full > reports/before.txt

# Apply fixes
make safe-apply

# After optimization  
make qa-full > reports/after.txt

# Compare
diff reports/before.txt reports/after.txt
```

### CI Monitoring

Check GitHub Actions for:
- Build times
- Test coverage trends
- Security issue trends
- Dependency health

## 🔄 Maintenance

### Weekly Tasks

```bash
# Update pre-commit hooks
pre-commit autoupdate

# Update tooling
uv pip install --upgrade ruff mypy pytest

# Run full quality assessment
make qa-full

# Clean accumulated cache
make clean
```

### Monthly Tasks

```bash
# Review security reports
cat reports/bandit_report.json
cat reports/pip_audit_report.json

# Review dependency health
cat reports/deptry_report.json

# Update this README if needed
```

---

## 🎉 Kết quả mong đợi

Sau khi áp dụng toolpack:

- ✅ **Code quality:** PEP8 compliant, type-safe
- ✅ **Security:** Không có known vulnerabilities
- ✅ **Performance:** Không dead code, optimal imports
- ✅ **Maintainability:** Clear structure, documented APIs
- ✅ **CI/CD:** Fast, reliable pipelines
- ✅ **Developer Experience:** Pre-commit guards, clear feedback

**Happy coding! 🚀**
