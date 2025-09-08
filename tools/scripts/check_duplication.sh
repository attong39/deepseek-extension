#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Đảm bảo jscpd sẵn qua npx (sử dụng cache npm actions hoặc npm ci apps/desktop)
if [ -f "$ROOT_DIR/desktop_ai_zeta/package.json" ]; then
	pushd "$ROOT_DIR/desktop_ai_zeta" >/dev/null
	npm ci
	popd >/dev/null
fi

# Quét trùng lặp trên các thư mục source chính (không quét .venv / site-packages)
# Giới hạn target thay vì quét toàn repo để tránh quét các package cài trong .venv
TARGETS=("$ROOT_DIR/zeta_vn" "$ROOT_DIR/desktop_ai_zeta/src")

# Tăng bộ nhớ heap cho Node để tránh OOM khi quét code lớn
export NODE_OPTIONS="--max-old-space-size=4096"

npx jscpd \
	--min-lines 20 \
	--threshold 0 \
	--reporters console \
	--ignore "**/node_modules/**" \
	--ignore "**/.venv/**" \
	--ignore "**/.pytest_cache/**" \
	--ignore "**/__pycache__/**" \
	--ignore "**/build/**" \
	--ignore "**/dist/**" \
	--ignore "**/desktop_ai_zeta/src/api/generated/**" \
	"${TARGETS[@]}"
