#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"/../.. && pwd)"

# —— Config —— #
BACKENDS=("zeta_vn")
FRONTEND="desktop_ai_zeta"
PY_SRC_DIRS=("zeta_vn")
COVERAGE_MIN=80

echo "▶ ZETA_AI UPGRADE START"

# — Backend — #
for b in "${BACKENDS[@]}"; do
  if [ -d "$ROOT_DIR/$b" ]; then
    echo "→ Backend: $b"
    (cd "$ROOT_DIR" && \
      uv sync && \
      bash "$ROOT_DIR/scripts/upgrade/py_quality.sh" "$COVERAGE_MIN")
    # perf gate (khởi động <3s, RAM <300MB)
    (cd "$ROOT_DIR" && uv run python "$ROOT_DIR/scripts/perf/perf_gate.py" --host 127.0.0.1 --port 8099 --startup-budget 3.0 --ram-budget-mb 300)
    break
  fi
done

# — Frontend — #
if [ -d "$ROOT_DIR/$FRONTEND" ]; then
  echo "→ Frontend: $FRONTEND"
  (cd "$ROOT_DIR/$FRONTEND" && bash "$ROOT_DIR/scripts/upgrade/ts_quality.sh")
else
  echo "⚠ Không tìm thấy thư mục desktop_ai_zeta/, bỏ qua bước frontend."
fi

echo "✔ Hoàn tất nâng cấp. Gợi ý: git add -A && git commit -m 'chore: upgrade & quality gates'"
