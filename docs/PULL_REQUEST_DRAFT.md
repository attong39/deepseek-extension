# Draft PR: chore/fix-barrels-absolute

Tóm tắt thay đổi
- Chuẩn hoá các `__init__.py` (barrel files) sang absolute imports `zeta_vn...` bằng scripts trong `tools/`.
- Thêm/điều chỉnh vài helper scripts: `tools/fix_barrels_absolute.py`, `tools/fix_minimal_imports_blocks.py`, `tools/convert_remaining_barrels.py`.
- Sửa một vài file nhỏ gây lỗi runtime/lint (ví dụ `zeta_vn/infrastructure/__init__.py`, `zeta_vn/data/repositories/__init__.py`, `zeta_vn/app/middleware/security/zero_trust.py`, `zeta_vn/config/settings/__init__.py`).

Files changed (high level)
- many auto-generated `zeta_vn/**/__init__.py` barrels (converted to absolute imports).
- `tools/*` (3 scripts created/updated)
- small manual fixes in: `zeta_vn/infrastructure/__init__.py`, `zeta_vn/data/repositories/__init__.py`, `zeta_vn/app/middleware/security/zero_trust.py`, `zeta_vn/config/settings/__init__.py`, `zeta_vn/app/deps_proposed/services.py`, `zeta_vn/app/__init__.py`, `zeta_vn/core/domain/__init__.py`, `zeta_vn/data/services/__init__.py`

Why
- Project style mandates absolute imports for barrels. This PR normalizes barrels to avoid linter errors (TID252 / ruff) and to simplify imports across the codebase.

Validation performed (local)
- `ruff --fix` then `ruff check` — All checks passed locally.
- `mypy --strict zeta_vn` — many typing issues surfaced (2147 errors) — see summary below.
- `pytest -q zeta_vn/tests/unit -k "not slow"` — ran unit tests; result: 101 failed, 289 passed, 26 warnings, 15 errors. Key failures/notes below.

Quick reproduction (Windows PowerShell)
```powershell
& .\.venv\Scripts\Activate.ps1
.
E:\zeta\.venv\Scripts\python.exe -m mypy --strict zeta_vn
E:\zeta\.venv\Scripts\python.exe -m pytest -q zeta_vn/tests/unit
```

Key findings (short)
- `mypy` failures: large number of pre-existing typing issues (missing type args for `dict`, many `no-untyped-def`, `no-any-return`). These are mostly broad and existed before barrel changes — but mypy now checks the whole package and surfaced them.
- `pytest` failures: two classes of problems observed:
  1. Import-time / syntax/runtime blockers fixed during the run (fixed: stray extra dot; handled `factory_simple` deprecation by fallback).
  2. Test failures during execution: many failures are due to async event-loop issues ("There is no current event loop in thread 'MainThread'"), some domain-level assertion changes (entity defaults, VO validation), and a handful of environment/missing optional deps (e.g. `openai` not installed) and authentication/zero-trust related test assertions (422 vs 200). These need targeted fixes.

Suggested next steps (prioritized)
1. Push branch and open a PR draft using this file as the PR body so reviewers can see scope.
2. Triage failing unit tests — focus on highest-impact categories:
   - Async event loop issues: ensure `conftest.py` event_loop fixture and `pytest-asyncio` setup are compatible on Windows; consider adding `asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())` early in test setup if needed.
   - Domain regressions: run a subset of failing tests and inspect diffs in the related modules (entities & value objects) — many failures look like behavioral mismatches (e.g., default attributes, constructors changed by import reorder).
   - Optional deps: document optional extras or add test-time mocks; skip tests that require external services where appropriate.
3. Fix high-severity mypy errors incrementally (start from top-level modules used by tests). Use `mypy --strict --exclude build` and iterate.

Checklist for PR
- [ ] Branch created: `chore/fix-barrels-absolute` (local) ✅
- [ ] All modified files staged & committed ✅
- [ ] `ruff --fix` + `ruff check` passed ✅
- [ ] `mypy --strict` run (errors listed in PR) ❌
- [ ] Unit tests run (summary in PR) ❌
- [ ] Plan to address failing tests & mypy errors in follow-ups (this PR keeps changes minimal) ✅

Notes for reviewers
- Many barrels were auto-changed by scripts; focus review on files marked `# === manual exports below ===` to ensure manual exports were preserved.
- I avoided changing domain/business logic; only fixed small issues that blocked linting/tests.

If you want, I can continue: either (A) start fixing the async event-loop related test failures, or (B) prepare PR and then fix failures incrementally in follow-ups. Indicate preferred next action.

---
Generated on: 2025-08-21
