#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

if [ ! -x ".venv/bin/python" ]; then
  echo "Creating virtualenv .venv..."
  python3 -m venv .venv
else
  echo "Using existing .venv"
fi

if [ -f requirements-dev.txt ]; then
  echo "Installing requirements-dev.txt..."
  .venv/bin/pip install -r requirements-dev.txt
else
  echo "No requirements-dev.txt found, skipping pip install"
fi

echo "Enabling git hooks..."
./scripts/setup_hooks.sh

echo "Running duplicate checks once..."
.venv/bin/python scripts/check_duplicates.py --report-dir reports/duplicates || true
