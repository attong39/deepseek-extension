$ErrorActionPreference = "Continue"

Write-Host "[pre-push] Quick consistency check..."

# Non-blocking hash check
Write-Host "[pre-push] Checking OpenAPI hash..."
try {
    uv run python tools/consistency/openapi_hash.py --check
} catch {
    Write-Host "[pre-push] ⚠️  Hash mismatch - consider running 'make guard-fix'" -ForegroundColor Yellow
}

# Non-blocking Guard check  
Write-Host "[pre-push] Running Consistency Guard..."
try {
    uv run python tools/consistency/run_all.py
} catch {
    Write-Host "[pre-push] ⚠️  Contract issues detected - check 'make guard' for details" -ForegroundColor Yellow
}

Write-Host "[pre-push] ✅ Quick check completed (non-blocking)" -ForegroundColor Green
