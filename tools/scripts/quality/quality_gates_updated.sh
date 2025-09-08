#!/usr/bin/env bash
set -euo pipefail
echo "== ZETA_AI :: QUALITY GATES =="
echo "🔍 Running quality checks for zeta_vn_restructured..."

# Core quality checks
echo "📝 Checking code formatting and linting..."
uv run ruff check .
uv run ruff format --check .

echo "🔍 Running type checking..."
uv run mypy zeta_vn_restructured --show-column-numbers --hide-error-context

echo "🧪 Running quick tests..."
uv run pytest -q -k 'not slow' --maxfail=1

# Security checks (warnings only in dev mode)
echo "🔒 Running security checks..."
uv run bandit -q -r zeta_vn_restructured || echo "⚠️ Bandit warnings detected"

echo "📦 Checking dependencies for vulnerabilities..."
uv run pip-audit || echo "⚠️ Pip-audit warnings detected"

echo "== ✅ Quality gates passed (dev mode) =="