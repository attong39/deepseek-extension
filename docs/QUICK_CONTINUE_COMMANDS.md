🎯 QUICK COMMANDS TO CONTINUE OPTIMIZATION
==========================================

Đây là các commands để tiếp tục mà không cần Copilot:

## 🚀 1. AUTO-CONTINUE SCRIPT

```powershell
# Chạy script tự động
python continue_optimization.py
```

## 🛠️ 2. MANUAL COMMANDS (nếu cần control từng bước)

```powershell
# App modules còn lại
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/infrastructure/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/monitoring/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/observability/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/utils/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/common/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/startup/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/status/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/ai/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path app/realtime/ --apply

# Data modules còn lại
python tools/fix_repo_safe_v2.py --root zeta_vn --path data/shared/ --apply
python tools/fix_repo_safe_v2.py --root zeta_vn --path data/utils/ --apply
```

## 📊 3. CHECK PROGRESS

```powershell
# Đếm lỗi còn lại
uv run ruff check . --quiet | Measure-Object -Line

# Check specific error types
uv run ruff check --select E402,E722 .

# Overall quality check
uv run ruff check .
uv run mypy .
uv run pytest -q
```

## 🎉 4. CURRENT STATUS

✅ **COMPLETED:**
- Core: 7/9 modules
- App: 6/10+ modules (websockets, handlers, middleware, auth, security, schemas)
- Data: 2/3 modules (models, services)

⚠️ **REMAINING:**
- App: ~4 modules (infrastructure, monitoring, observability, utils...)
- Data: 1 module (shared/utils)

🚫 **INTENTIONALLY SKIPPED (autobarrel wildcard imports):**
- app/controllers, app/serializers, app/validators, app/exceptions
- core/use_cases, core/interfaces
- config/settings, data/repositories, data/external

## 🏆 EXPECTED FINAL RESULT

- From ~498 initial lint errors → <50 final errors
- Only F403 wildcard imports from autobarrel (intentional)
- All tests passing
- Production-ready code quality

## ⚡ ONE-LINER UNTUK SEMUA

```powershell
python continue_optimization.py && echo "🎉 OPTIMIZATION COMPLETED!"
```
