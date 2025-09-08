#!/usr/bin/env bash
set -euo pipefail
echo "— TS Quality — prettier/eslint/tsc/vitest/depcheck/ts-prune"

# deps (idempotent)
npm ci --ignore-scripts || npm i --include=dev

# format & lint
npx prettier "src/**/*.{ts,tsx,css,md}" --write
npx eslint "src/**/*.{ts,tsx}" --fix || true

# type
npx tsc --noEmit

# tests
if [ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ]; then
  npx vitest run --coverage || true
fi

# unused deps & symbols
npx depcheck || true
npx ts-prune > ../.artifacts/deadcode/ts-prune.txt || true

echo "— Done TS Quality —"
