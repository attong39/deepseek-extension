#!/usr/bin/env bash
# Auto-fix: deps & virtualenv (Bash)
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"/../.. && pwd)"
echo "▶ Auto-fix: deps & virtualenv"

# 1) Sửa _virtualenv.pth + tạo venv bằng uv
uv run python "$ROOT/scripts/fix/repair_env.py" --apply

# 2) Đồng bộ apps/backend (nếu có)
for B in "zeta_vn_restructured" "zeta_vn"; do
  if [ -d "$ROOT/$B" ]; then
    (cd "$ROOT/$B" && uv sync)
    break
  fi
done

# 3) Cài tối thiểu cho Deepseek Agent (an toàn, idempotent)
uv add typer==0.12.5 rich requests --dev || true

# 4) Desktop deps (nếu có)
if [ -d "$ROOT/apps/desktop" ]; then
  (cd "$ROOT/apps/desktop" && (npm ci || npm i --include=dev))
fi

# 5) Kiểm tra nhanh
uv run python "$ROOT/scripts/fix/verify_stack.py"

echo "✔ Done. Gợi ý: uv run python -m deepseek agent --apply"
