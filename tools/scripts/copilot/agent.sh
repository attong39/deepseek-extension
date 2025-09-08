#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"/../.. && pwd)"
ART=".artifacts"
TS_DIR="desktop_ai_zeta"
BACKENDS=("zeta_vn")
STARTUP_BUDGET="3.0"
RAM_BUDGET_MB="300"
COV_MIN="80"

mkdir -p "$ROOT/$ART"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG_RAW="$ROOT/$ART/copilot_agent_$STAMP.raw.log"
LOG="$ROOT/$ART/copilot_agent_$STAMP.log"

# — redact helper: mask emails, bearer/jwt-like tokens, AWS-style keys — #
redact() {
  sed -E \
    -e 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/<redacted@email>/g' \
    -e 's/(Bearer|JWT|Token)[[:space:]]+[A-Za-z0-9\-\._]+/\1 <redacted>/gi' \
    -e 's/(AKIA|ASIA)[A-Z0-9]{16}/<redacted_key>/g'
}

run() {
  echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_RAW"
  eval "$@" 2>&1 | tee -a "$LOG_RAW"
}

echo "▶ Copilot Coding Agent started @ $STAMP" | tee -a "$LOG_RAW"

# 1) Build Copilot context
run "uv run python scripts/copilot/build_context.py"

# 2) BACKEND quality (first apps/backend found)
for B in "${BACKENDS[@]}"; do
  if [ -d "$ROOT/$B" ]; then
    echo "→ Backend: $B" | tee -a "$LOG_RAW"
    ( cd "$ROOT" && \
      uv sync && \
      bash "$ROOT/scripts/upgrade/py_quality.sh" "$COV_MIN" && \
      uv run python "$ROOT/scripts/perf/perf_gate.py" --startup-budget "$STARTUP_BUDGET" --ram-budget-mb "$RAM_BUDGET_MB" \
    )
    break
  fi
done

# 3) FRONTEND quality
if [ -d "$ROOT/$TS_DIR" ]; then
  echo "→ Frontend: $TS_DIR" | tee -a "$LOG_RAW"
  ( cd "$ROOT/$TS_DIR" && bash "$ROOT/scripts/upgrade/ts_quality.sh" )
fi

# 4) Clone-code & dead-code guards
bash "$ROOT/scripts/upgrade/dedupe_guard.sh" | tee -a "$LOG_RAW"
bash "$ROOT/scripts/upgrade/dead_code_guard.sh" | tee -a "$LOG_RAW"

# 5) Summarize
python - << 'PY' | tee -a "$LOG_RAW"
from pathlib import Path
art = Path(".artifacts")
rep = [
  art / "jscpd-report" / "jscpd-report.html",
  art / "deadcode" / "vulture.txt",
  art / "deadcode" / "ts-prune.txt",
  Path("COPILOT_CONTEXT.md"),
]
print("\n=== SUMMARY ARTIFACTS ===")
for p in rep:
  print(f"• {p} {'(OK)' if p.exists() else '(missing)'}")
PY

# 6) Redact and finalize log
redact < "$LOG_RAW" > "$LOG"
rm -f "$LOG_RAW"
echo "✔ Done. Log: $LOG"
echo "👉 Gợi ý commit: git add -A && git commit -m 'chore: copilot agent – format, imports, dedupe, deadcode, perf-gate'"
