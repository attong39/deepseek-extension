# Quick setup aliases for ZETA_VN development - PowerShell
# Source this file: . .\scripts\dev_aliases.ps1

function zeta-bootstrap { .\scripts\bootstrap_dev.ps1 }
function zeta-server { uv run uvicorn zeta_vn.app.main_production:app --reload --host 0.0.0.0 --port 8000 }
function zeta-worker { uv run celery -A zeta_vn.app.worker.celery_app worker -l info }
function zeta-beat { uv run celery -A zeta_vn.app.worker.celery_app beat -l info }
function zeta-desktop { Set-Location desktop_ai_zeta; npm run dev }
function zeta-test { uv run pytest -v }
function zeta-lint { uv run ruff check . }
function zeta-format { uv run ruff format . }
function zeta-typecheck { uv run mypy . }
function zeta-quality { uv run python tools/master_quality_check.py }
function zeta-security { uv run python -m zeta_vn.cli.maintenance security sweep }
function zeta-health { uv run python -m zeta_vn.cli.maintenance health check --detailed }
function zeta-optimize { uv run python -m zeta_vn.cli.maintenance optimize status }
function zeta-info { uv run python -m zeta_vn.cli.maintenance system info }
function zeta-codegen { Set-Location desktop_ai_zeta; npm run codegen:api; Set-Location .. }
function zeta-migration { uv run alembic upgrade head }
function zeta-db {
    docker run --rm -d --name zeta-pg `
        -e POSTGRES_PASSWORD=pass `
        -e POSTGRES_DB=zeta `
        -p 5432:5432 `
        pgvector/pgvector:pg16
}

Write-Host "🚀 ZETA_VN development aliases loaded!" -ForegroundColor Green
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  zeta-bootstrap    # Quick bootstrap development environment"
Write-Host "  zeta-server       # Start FastAPI development server"
Write-Host "  zeta-desktop      # Start apps/desktop app"
Write-Host "  zeta-quality      # Run full quality checks"
Write-Host "  zeta-health       # Check system health"
Write-Host "  zeta-security     # Run security sweep"
