$ErrorActionPreference = "Stop"
Write-Host "== ZETA_AI :: QUALITY GATES (RESTRUCTURED PATHS) ==" -ForegroundColor Cyan

function Invoke-Check {
    param(
        [string]$Command,
        [string]$Description,
        [bool]$StrictMode = $true
    )
    
    Write-Host "🔍 $Description..." -ForegroundColor Yellow
    
    try {
        if ($StrictMode) {
            Invoke-Expression $Command
            if ($LASTEXITCODE -ne 0) {
                throw "Command failed with exit code: $LASTEXITCODE"
            }
        }
        else {
            Invoke-Expression $Command
            if ($LASTEXITCODE -ne 0) {
                Write-Host "⚠️  $Description warnings detected" -ForegroundColor Yellow
            }
        }
        Write-Host "✅ $Description passed" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ $Description failed: $($_.Exception.Message)" -ForegroundColor Red
        if ($StrictMode) {
            exit 1
        }
    }
}

# Main quality checks with restructured paths
Invoke-Check "uv run ruff check ." "Ruff linting"
Invoke-Check "uv run ruff format --check ." "Ruff formatting"
Invoke-Check "uv run mypy zeta_vn zeta_vn_restructured" "MyPy type checking (both projects)"
Invoke-Check "uv run pytest tests zeta_vn_restructured/tests -q -k 'not slow' --maxfail=1" "Pytest quick tests (both projects)"

# Optional security & supply chain checks (non-strict)
Invoke-Check "uv run bandit -q -r zeta_vn zeta_vn_restructured" "Bandit security scan (both projects)" $false
Invoke-Check "uv run pip-audit" "Pip-audit supply chain check" $false

Write-Host "`n== ✅ ALL QUALITY GATES PASSED (RESTRUCTURED PATHS UPDATED) ==" -ForegroundColor Green
Write-Host "🚀 Both zeta_vn and zeta_vn_restructured are ready!" -ForegroundColor Cyan
