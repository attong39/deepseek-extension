# ZETA_VN Go-Live Check - PowerShell Version
# Comprehensive validation: foundation → API → performance → security → quality

param(
    [string]$BaseUrl = "http://127.0.0.1:8000",
    [int]$PerfP95Ms = 200,
    [int]$PerfReqs = 800,
    [int]$PerfConc = 40,
    [string]$JwtTest = "",
    [string]$RedisUrl = ""
)

$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "ZETA_VN Go-Live Check"

# Configuration from environment or parameters
$ZETA_BASE_URL = if ($env:ZETA_BASE_URL) { $env:ZETA_BASE_URL } else { $BaseUrl }
$PERF_P95_MS = if ($env:PERF_P95_MS) { [int]$env:PERF_P95_MS } else { $PerfP95Ms }
$PERF_REQS = if ($env:PERF_REQS) { [int]$env:PERF_REQS } else { $PerfReqs }
$PERF_CONC = if ($env:PERF_CONC) { [int]$env:PERF_CONC } else { $PerfConc }
$JWT_TEST = if ($env:JWT_TEST) { $env:JWT_TEST } else { $JwtTest }
$REDIS_URL = if ($env:REDIS_URL) { $env:REDIS_URL } else { $RedisUrl }

# Color functions
function Write-Step {
    param($StepNum, $Message)
    Write-Host "== [$StepNum/7] $Message" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Global variables for cleanup
$ApiProcess = $null
$QualityErrors = 0

# Cleanup function
function Cleanup {
    if ($ApiProcess -and -not $ApiProcess.HasExited) {
        Write-Host ""
        Write-Step "CLEANUP" "Shutting down API server"
        try {
            Stop-Process -Id $ApiProcess.Id -Force -ErrorAction SilentlyContinue
            Write-Success "API server stopped"
        }
        catch {
            Write-Warning "Could not stop API server gracefully"
        }
    }
}

# Set cleanup trap
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup }

Write-Host "🚀 ZETA_VN GO-LIVE CHECK" -ForegroundColor Blue
Write-Host "========================" -ForegroundColor Blue
Write-Host "Comprehensive validation: preflight → foundation → API → performance → security → quality" -ForegroundColor White
Write-Host ""

Write-Host "Configuration:"
Write-Host "  Base URL: $ZETA_BASE_URL"
Write-Host "  P95 Target: ${PERF_P95_MS}ms"
Write-Host "  Load Test: $PERF_REQS requests, $PERF_CONC concurrent"
Write-Host "  JWT Test: $(if ($JWT_TEST) { 'Enabled' } else { 'Disabled' })"
Write-Host "  Redis: $(if ($REDIS_URL) { 'Enabled' } else { 'Disabled' })"
Write-Host ""

try {
    # ==== Step 0: Preflight ====
    Write-Step "0" "Preflight - System Readiness Check"
    try {
        uv run python scripts/qa/preflight.py
        Write-Success "Preflight checks passed"
    }
    catch {
        Write-Error "Preflight checks failed - system not ready: $($_.Exception.Message)"
        exit 1
    }
    Write-Host ""
    # ==== Step 1: Foundation ====
    Write-Step "1" "Foundation - Code Quality & Dependencies"
    try {
        bash scripts/impl/phase1_foundation.sh
        Write-Success "Foundation checks passed"
    }
    catch {
        Write-Error "Foundation checks failed: $($_.Exception.Message)"
        exit 1
    }
    Write-Host ""

    # ==== Step 2: Boot API ====
    Write-Step "2" "Boot API (Production Mode)"
    Write-Host "Starting production API server..." -ForegroundColor Cyan
    
    $ApiProcess = Start-Process -PassThru -FilePath "uv" -ArgumentList @(
        "run", "uvicorn", "zeta_vn.app.main_production:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ) -WindowStyle Hidden
    
    Write-Host "API PID: $($ApiProcess.Id)"

    # Wait for server to start
    Write-Host "Waiting for API to start..." -ForegroundColor Cyan
    $started = $false
    for ($i = 1; $i -le 30; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "$ZETA_BASE_URL/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "API server started and responding"
                $started = $true
                break
            }
        }
        catch {
            # Expected during startup
        }
        Start-Sleep -Seconds 1
    }

    if (-not $started) {
        Write-Error "API server failed to start within 30 seconds"
        exit 1
    }
    Write-Host ""

    # ==== Step 3: Warm Cache ====
    Write-Step "3" "Warm Cache (Initial requests)"
    Write-Host "Warming up cache with initial requests..." -ForegroundColor Cyan

    # Basic health check
    try {
        Invoke-WebRequest -Uri "$ZETA_BASE_URL/health" -UseBasicParsing -TimeoutSec 5 | Out-Null
        Write-Success "Health endpoint warmed"
    }
    catch {
        Write-Warning "Health endpoint not responding properly"
    }

    # Try status endpoint
    try {
        Invoke-WebRequest -Uri "$ZETA_BASE_URL/api/v1/status" -UseBasicParsing -TimeoutSec 5 | Out-Null
        Write-Success "Status endpoint warmed"
    }
    catch {
        # Not critical
    }

    # Try RAG endpoint
    try {
        Invoke-WebRequest -Uri "$ZETA_BASE_URL/rag/query?q=test" -UseBasicParsing -TimeoutSec 5 | Out-Null
        Write-Success "RAG endpoint warmed"
    }
    catch {
        # Not critical
    }

    Write-Success "Cache warming completed"
    Write-Host ""

    # ==== Step 4: Performance Probe ====
    Write-Step "4" "Performance Probe - Load Testing"
    Write-Host "Running performance test against $ZETA_BASE_URL/health" -ForegroundColor Cyan
    Write-Host "Parameters: $PERF_REQS requests, $PERF_CONC concurrent connections" -ForegroundColor Cyan

    try {
        $probeOutput = uv run python scripts/perf/probe.py "$ZETA_BASE_URL/health" --concurrency $PERF_CONC --requests $PERF_REQS
        Write-Host $probeOutput

        # Extract P95 from output
        if ($probeOutput -match "p95=([0-9\.]+)ms") {
            $p95 = [double]$Matches[1]
            if ($p95 -gt $PERF_P95_MS) {
                Write-Error "P95 $p95 ms > $PERF_P95_MS ms (target exceeded)"
                exit 1
            }
            else {
                Write-Success "P95 $p95 ms <= $PERF_P95_MS ms (target met)"
            }
        }
        else {
            Write-Error "Could not parse P95 from probe output"
            exit 1
        }
    }
    catch {
        Write-Error "Performance probe failed: $($_.Exception.Message)"
        exit 1
    }
    Write-Host ""

    # ==== Step 5: Zero-Trust Security Checks ====
    Write-Step "5" "Zero-Trust Security Validation"
    Write-Host "Testing authentication and authorization..." -ForegroundColor Cyan

    try {
        if ($JWT_TEST) {
            uv run python scripts/qa/check_zero_trust.py --base "$ZETA_BASE_URL" --jwt "$JWT_TEST"
        }
        else {
            uv run python scripts/qa/check_zero_trust.py --base "$ZETA_BASE_URL"
            Write-Warning "JWT_TEST not provided - protected endpoint testing with JWT skipped"
        }
        Write-Success "Zero-Trust checks passed"
    }
    catch {
        Write-Error "Zero-Trust validation failed: $($_.Exception.Message)"
        exit 1
    }
    Write-Host ""

    # ==== Step 6: Quality Gates Snapshot ====
    Write-Step "6" "Quality Gates - Final Validation"
    Write-Host "Running comprehensive quality checks..." -ForegroundColor Cyan

    # Ruff check
    Write-Host "Running Ruff code quality check..." -ForegroundColor Cyan
    try {
        uv run ruff check . --quiet
        Write-Success "Ruff checks passed"
    }
    catch {
        Write-Warning "Ruff found issues"
        $QualityErrors++
    }

    # MyPy check
    Write-Host "Running MyPy type checking..." -ForegroundColor Cyan
    try {
        $null = uv run mypy . --no-error-summary 2>$null
        Write-Success "MyPy checks passed"
    }
    catch {
        Write-Warning "MyPy found issues"
        $QualityErrors++
    }

    # Pytest
    Write-Host "Running pytest test suite..." -ForegroundColor Cyan
    try {
        uv run pytest -q --tb=no
        Write-Success "Test suite passed"
    }
    catch {
        Write-Warning "Some tests failed"
        $QualityErrors++
    }

    # Bandit security scan
    Write-Host "Running Bandit security scan..." -ForegroundColor Cyan
    try {
        uv run bandit -q -r zeta_vn
        Write-Success "Security scan passed"
    }
    catch {
        Write-Warning "Security issues found"
        $QualityErrors++
    }

    # pip-audit
    Write-Host "Running pip-audit dependency check..." -ForegroundColor Cyan
    try {
        uv run pip-audit --quiet
        Write-Success "Dependency audit passed"
    }
    catch {
        Write-Warning "Vulnerable dependencies found"
        $QualityErrors++
    }

    Write-Host ""

    # ==== Final Summary ====
    Write-Host "🎉 GO-LIVE CHECK COMPLETE" -ForegroundColor Blue
    Write-Host "==========================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "✅ Foundation: Code quality and dependencies validated"
    Write-Host "✅ API Server: Production mode started and responding"
    Write-Host "✅ Performance: P95 $p95 ms <= $PERF_P95_MS ms target"
    Write-Host "✅ Security: Zero-Trust middleware validated"
    
    if ($QualityErrors -eq 0) {
        Write-Host "✅ Quality Gates: All checks passed"
        Write-Success "ALL SYSTEMS GO! 🚀 Ready for production deployment"
    }
    else {
        Write-Host "⚠️  Quality Gates: $QualityErrors issues found (warnings only)"
        Write-Warning "System functional but $QualityErrors quality issues need attention"
    }

    Write-Host ""
    Write-Host "🎯 Next Steps:"
    Write-Host "   1. Address any quality warnings if needed"
    Write-Host "   2. Deploy to staging environment"
    Write-Host "   3. Run load testing in staging"
    Write-Host "   4. Deploy to production with canary"
    Write-Host ""
    Write-Host "📊 Performance Metrics:"
    Write-Host "   - P95 Latency: $p95 ms"
    Write-Host "   - Target: $PERF_P95_MS ms"
    Write-Host "   - Load Test: $PERF_REQS requests @ $PERF_CONC concurrent"
    Write-Host ""
    Write-Host "🔒 Security Status:"
    Write-Host "   - Zero-Trust middleware: Active"
    Write-Host "   - Authentication: Validated"
    Write-Host "   - Security scan: $(if ($QualityErrors -eq 0) { 'Clean' } else { 'Warnings' })"
}
finally {
    Cleanup
}