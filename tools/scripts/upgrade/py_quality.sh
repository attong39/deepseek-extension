#!/usr/bin/env bash
set -euo pipefail
COVERAGE_MIN="${1:-80}"

echo "— PY Quality — ruff/mypy/pytest/bandit/pip-audit/pycln"

# Format & lint & import order
uv run ruff check . --fix
uv run ruff format .

# Safe remove unused imports (skip __init__.py to giữ API surface)
# pycln with explicit exclusion for init files
find . -type f -name "*.py" ! -name "__init__.py" -print0 | xargs -0 -I{} sh -c 'uvx pycln "{}" --silence || true' || true

# Type check (không chặn pipeline)
uv run mypy zeta_vn --pretty --no-error-summary || true

# Security
uv run bandit -q -r zeta_vn || true
if [ -f "requirements.txt" ]; then
  uv run pip-audit -r requirements.txt || true
else
  uvx pip-audit || true
fi

# Tests + coverage
if [ -d "tests" ]; then
  uv run pytest -q --maxfail=1 --disable-warnings --cov=zeta_vn --cov-report=term-missing --cov-fail-under="${COVERAGE_MIN}" || true
fi

echo "— Done PY Quality —"
