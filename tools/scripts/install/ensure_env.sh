#!/usr/bin/env bash
set -euo pipefail

echo "==> Ensuring Python tools via uv..."
if command -v uv >/dev/null 2>&1; then
    uv pip install \
        "ruff>=0.4,<1" \
        "mypy>=1.10,<2" \
        "bandit>=1.7,<2" \
        "pytest>=8,<9" \
        "coverage>=7.5,<8" \
        "requests>=2.31,<3" \
        "httpx>=0.27,<0.28" \
        "pydantic>=2.6,<3" \
        "watchdog>=3,<5" \
        "autoflake>=2.2,<3" \
        "pycln>=2.4,<3" \
        "psutil>=5.9,<6" \
        "uvicorn>=0.30,<1" --quiet
    echo "✔ Python toolchain OK"
else
    echo "❌ uv not found. Please install uv first: https://github.com/astral-sh/uv"
    exit 1
fi

if command -v node >/dev/null 2>&1; then
    echo "==> Ensuring Node tools (dev deps)"
    npm install --no-audit --no-fund -D \
        typescript@^5.4 \
        eslint@^9 \
        prettier@^3 \
        vitest@^1 \
        ts-node@^10 \
        ts-prune@^0.10 \
        jscpd@^3.5 \
        openapi-typescript@^6.7 >/dev/null
    echo "✔ Node dev deps OK"
else
    echo "⚠ Node chưa có — các bước TS sẽ được bỏ qua. Cài Node rồi chạy lại script này."
fi
