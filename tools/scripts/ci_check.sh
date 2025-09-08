#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> 1/8 Python QA (ruff/mypy/pytest/bandit/pip-audit/vulture)"
bash "$ROOT_DIR/scripts/check_python.sh"

echo "==> 2/8 Export OpenAPI từ server → contracts/openapi.json"
python "$ROOT_DIR/scripts/export_openapi.py"

echo "==> 3/8 Gen TS types client từ OpenAPI"
bash "$ROOT_DIR/scripts/gen_ts_client.sh"

echo "==> 4/8 Validate JSON Schemas (actions/ws/errors) với AJV"
node "$ROOT_DIR/scripts/validate_schemas.mjs"

echo "==> 5/8 So khớp ENV giữa shared/server/apps/desktop"
python "$ROOT_DIR/scripts/check_env_sync.py"

echo "==> 6/8 So khớp i18n keys (vi/en)"
node "$ROOT_DIR/scripts/check_i18n.mjs"

echo "==> 7/8 Phát hiện trùng lặp mã nguồn (jscpd)"
bash "$ROOT_DIR/scripts/check_duplication.sh"

echo "==> 8/8 Type-check & build apps/desktop (tùy chọn nếu có)"
if [ -f "$ROOT_DIR/desktop_ai_zeta/tsconfig.json" ]; then
  pushd "$ROOT_DIR/desktop_ai_zeta" >/dev/null
  # Sử dụng npm để đồng bộ với Makefile và CI cache
  npm ci
  npm run ts:check
  # npm run build # bật nếu muốn build thật
  popd >/dev/null
fi

echo "✅ Tất cả bài kiểm tra đã PASSED."
