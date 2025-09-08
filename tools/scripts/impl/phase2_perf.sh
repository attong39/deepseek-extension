#!/usr/bin/env bash
set -euo pipefail

API_URL=${API_URL:-"http://127.0.0.1:8000/health"}

echo "⚡ [Phase2] Performance Testing - Tối ưu và đo hiệu năng"
echo "======================================================="

echo "🔍 [Phase2] Quick P95 performance probe -> $API_URL"

# Check if server is running
if ! curl -fsS "$API_URL" >/dev/null 2>&1; then
    echo "⚠️ Server not running at $API_URL"
    echo "💡 Start server first: uv run uvicorn zeta_vn.app.main_production:app --host 0.0.0.0 --port 8000"
    echo "🚀 Or use minimal: uv run uvicorn zeta_vn.app.main_minimal:app --host 0.0.0.0 --port 8000"
    exit 1
fi

echo "🚀 Running performance probe..."
uv run python scripts/perf/probe.py "$API_URL" --concurrency 50 --requests 1000

echo "✅ [Phase2] Performance testing completed!"
echo "Next: Run 'bash scripts/impl/phase3_security.sh' for security hardening"