#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"/../.. && pwd)"
OUT="$ROOT/.artifacts/jscpd-report"
mkdir -p "$OUT"

echo "— Clone Code Detection with jscpd —"

# Install jscpd if not available
if ! command -v npx >/dev/null 2>&1; then
  echo "❌ npx not found. Install Node.js first."
  exit 1
fi

# Run jscpd với config tối ưu cho ZETA_AI
npx jscpd --reporters html --output "$OUT" \
  --threshold 2 \
  --min-tokens 40 \
  --ignore "node_modules/**,dist/**,build/**,.artifacts/**,.venv/**,**/__pycache__/**,*.min.js,*.bundle.*" \
  --pattern "**/*.{ts,tsx,js,jsx,py}" \
  --format "typescript,javascript,python" \
  . || true

echo "📊 jscpd report → $OUT/jscpd-report.html"

# Generate summary
if [ -f "$OUT/jscpd-report.html" ]; then
  # Extract clone percentage if available (basic grep)
  CLONE_RATE=$(grep -o "Clone rate: [0-9.]*%" "$OUT/jscpd-report.html" || echo "unknown")
  echo "🔍 Code duplication: $CLONE_RATE"
  
  if [[ "$CLONE_RATE" == *%* ]]; then
    RATE_NUM=$(echo "$CLONE_RATE" | grep -o "[0-9.]*")
    if (( $(echo "$RATE_NUM > 2.0" | bc -l) )); then
      echo "⚠️  High duplication rate detected. Review report for refactoring opportunities."
    else
      echo "✅ Duplication rate within acceptable limits (<2%)"
    fi
  fi
else
  echo "⚠️  No jscpd report generated"
fi
