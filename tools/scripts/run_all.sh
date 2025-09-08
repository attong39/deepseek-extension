#!/usr/bin/env bash
set -euo pipefail

# Parameters with defaults
API_URL="${1:-http://127.0.0.1:8099}"
LLM_MODE="${LLM:-false}"
ACTIONS="${ACTIONS:-link copilot, guard, upgrade, fix imports, tạo __init__.__all__, ts, openapi, quality + perf, dedupe, dead code}"

echo "🚀 ZETA Auto-Dev: Running All Components..."
echo "📋 Actions: $ACTIONS"
echo "🌐 API URL: $API_URL"
echo "🧠 LLM Mode: $LLM_MODE"

# Build command
CMD=(uv run python ai_runner.py --once "$ACTIONS" --apply --api-url "$API_URL")
if [[ "$LLM_MODE" == "true" ]]; then
    CMD+=(--llm)
    echo "🔮 LLM synthesis enabled"
fi

# Execute with timing
START_TIME=$(date +%s)
if "${CMD[@]}"; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    echo "✅ Auto-Dev completed successfully in ${DURATION}s"
else
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    echo "❌ Auto-Dev failed after ${DURATION}s"
    exit 1
fi
