$ErrorActionPreference = "Stop"
Write-Host "[pre-commit] Update OpenAPI hash..."
uv run python tools/consistency/openapi_hash.py --write
git add apps/desktop/src/constants/OPENAPI_HASH.ts | Out-Null

Write-Host "[pre-commit] Consistency Guard..."
uv run python tools/consistency/run_all.py
Write-Host "[pre-commit] OK"
