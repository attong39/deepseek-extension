#!/usr/bin/env bash
set -euo pipefail

echo "🏗️ [Phase1] Foundation - Dọn nợ kỹ thuật và chuẩn hóa codebase"
echo "=========================================================="

echo "📦 [Phase1] Sync dependencies..."
uv sync --all-extras --dev || {
    echo "⚠️ uv sync failed, continuing..."
}

echo "🧹 [Phase1] Ruff auto-fix (safe fixes only)..."
uv run ruff check . --fix || {
    echo "⚠️ Some ruff errors remain, continuing..."
}

echo "✨ [Phase1] Format code with ruff..."
uv run ruff format .

echo "🔍 [Phase1] Type checking with mypy (strict mode)..."
uv run mypy . --strict || {
    echo "⚠️ MyPy type errors found, continuing..."
}

echo "🧪 [Phase1] Running tests..."
uv run pytest -q --maxfail=5 || {
    echo "⚠️ Some tests failed, continuing..."
}

echo "🔒 [Phase1] Security scan (bandit)..."
uv run bandit -q -r zeta_vn || {
    echo "⚠️ Security issues found, continuing..."
}

echo "📋 [Phase1] Audit dependencies..."
uv run pip-audit || {
    echo "⚠️ Dependency vulnerabilities found, continuing..."
}

echo "✅ [Phase1] Foundation phase completed!"
echo "Next: Run 'bash scripts/impl/phase2_perf.sh' for performance testing"