$ErrorActionPreference = "Stop"
Write-Host "== ZETA_AI :: QUALITY GATES ==" -ForegroundColor Green
Write-Host "🔍 Running quality checks for zeta_vn_restructured..." -ForegroundColor Blue

# Core quality checks
Write-Host "📝 Checking code formatting and linting..." -ForegroundColor Yellow
uv run ruff check .
if ($LASTEXITCODE -ne 0) { throw "Ruff check failed" }

uv run ruff format --check .
if ($LASTEXITCODE -ne 0) { throw "Ruff format check failed" }

Write-Host "🔍 Running type checking..." -ForegroundColor Yellow
uv run mypy zeta_vn_restructured --show-column-numbers --hide-error-context
if ($LASTEXITCODE -ne 0) { throw "MyPy type checking failed" }

Write-Host "🧪 Running quick tests..." -ForegroundColor Yellow
uv run pytest -q -k "not slow" --maxfail=1
if ($LASTEXITCODE -ne 0) { throw "Pytest failed" }

# Security checks (warnings only in dev mode)
Write-Host "🔒 Running security checks..." -ForegroundColor Yellow
uv run bandit -q -r zeta_vn_restructured
if ($LASTEXITCODE -ne 0) { 
    Write-Host "⚠️ Bandit warnings detected" -ForegroundColor Yellow
}

Write-Host "📦 Checking dependencies for vulnerabilities..." -ForegroundColor Yellow
uv run pip-audit
if ($LASTEXITCODE -ne 0) { 
    Write-Host "⚠️ Pip-audit warnings detected" -ForegroundColor Yellow
}

Write-Host "== ✅ Quality gates passed (dev mode) ==" -ForegroundColor Green