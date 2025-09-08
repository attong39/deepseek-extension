# GO-LIVE CHECK LITE - PowerShell Version
# Simplified testing without server startup

param(
    [string]$BaseUrl = "http://127.0.0.1:8000",
    [int]$PerfP95Ms = 200
)

$ErrorActionPreference = "Stop"

# Create artifacts directory
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ArtifactsDir = "artifacts\go-live-lite-$Timestamp"
New-Item -ItemType Directory -Path $ArtifactsDir -Force | Out-Null

Write-Host "🚀 GO-LIVE CHECK LITE (PowerShell)" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Testing: Preflight + Code Quality + Configuration"
Write-Host "Artifacts: $ArtifactsDir"
Write-Host ""

$RuffErrors = 0
$MypyErrors = 0
$TestFailures = 0
$ConfigIssues = 0

try {
    # Step 0: Preflight
    Write-Host "== [0] PREFLIGHT - System Readiness" -ForegroundColor Yellow
    Write-Host "Checking: uv, ports, RAM, Redis, packages, disk..."
    
    $PreflightOutput = & uv run python scripts/qa/preflight.py 2>&1
    $PreflightOutput | Out-File -FilePath "$ArtifactsDir\preflight.txt" -Encoding UTF8
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ PREFLIGHT FAILED - System not ready" -ForegroundColor Red
        Write-Host "Check: $ArtifactsDir\preflight.txt"
        exit 1
    }
    
    Write-Host "✅ Preflight passed" -ForegroundColor Green
    Write-Host ""

    # Step 1: Code Quality
    Write-Host "== [1] CODE QUALITY - Static Analysis" -ForegroundColor Yellow
    Write-Host "Running: ruff check, mypy..."

    # Ruff check
    Write-Host "  → Running ruff check..."
    $RuffOutput = & uv run ruff check . 2>&1
    $RuffOutput | Out-File -FilePath "$ArtifactsDir\ruff_check.txt" -Encoding UTF8
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ruff check failed" -ForegroundColor Red
        $RuffErrors = ($RuffOutput | Measure-Object -Line).Lines
    }
    else {
        Write-Host "✅ Ruff check passed" -ForegroundColor Green
        $RuffErrors = 0
    }

    # MyPy check  
    Write-Host "  → Running mypy..."
    $MypyOutput = & uv run mypy . 2>&1
    $MypyOutput | Out-File -FilePath "$ArtifactsDir\mypy_check.txt" -Encoding UTF8
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ MyPy check failed" -ForegroundColor Red
        $MypyErrors = ($MypyOutput | Select-String "error:" | Measure-Object).Count
    }
    else {
        Write-Host "✅ MyPy check passed" -ForegroundColor Green
        $MypyErrors = 0
    }

    Write-Host ""

    # Step 2: Unit Tests
    Write-Host "== [2] UNIT TESTS - Fast Tests Only" -ForegroundColor Yellow
    Write-Host "Running: pytest with fast tests..."

    $PytestOutput = & uv run pytest -x --tb=short -q 2>&1
    $PytestOutput | Out-File -FilePath "$ArtifactsDir\pytest.txt" -Encoding UTF8
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Unit tests failed" -ForegroundColor Red
        $TestFailures = ($PytestOutput | Select-String "FAILED" | Measure-Object).Count
    }
    else {
        Write-Host "✅ Unit tests passed" -ForegroundColor Green
        $TestFailures = 0
    }

    Write-Host ""

    # Step 3: Configuration
    Write-Host "== [3] CONFIGURATION - Environment Check" -ForegroundColor Yellow
    Write-Host "Validating: environment variables, config files..."

    $ConfigIssues = 0

    if (-not (Test-Path "pyproject.toml")) {
        Write-Host "❌ pyproject.toml missing" -ForegroundColor Red
        $ConfigIssues++
    }
    else {
        Write-Host "✅ pyproject.toml found" -ForegroundColor Green
    }

    if (-not (Test-Path ".env.example")) {
        Write-Host "❌ .env.example missing" -ForegroundColor Red  
        $ConfigIssues++
    }
    else {
        Write-Host "✅ .env.example found" -ForegroundColor Green
    }

    Write-Host ""

    # Step JUDGE: Analysis
    Write-Host "== [JUDGE] LITE ANALYSIS - Code Quality Assessment" -ForegroundColor Yellow

    $CodeQualityPass = ($RuffErrors -eq 0) -and ($MypyErrors -eq 0)
    $TestsPass = ($TestFailures -eq 0)
    $ConfigPass = ($ConfigIssues -eq 0)
    $OverallPass = $CodeQualityPass -and $TestsPass -and $ConfigPass

    # Create summary
    $Summary = @{
        timestamp       = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"
        test_type       = "lite"
        results         = @{
            preflight     = "passed"
            ruff_errors   = $RuffErrors
            mypy_errors   = $MypyErrors
            test_failures = $TestFailures
            config_issues = $ConfigIssues
        }
        criteria        = @{
            code_quality_pass = $CodeQualityPass
            tests_pass        = $TestsPass
            config_pass       = $ConfigPass
        }
        overall_pass    = $OverallPass
        recommendations = @()
    }

    $Summary | ConvertTo-Json -Depth 3 | Out-File -FilePath "$ArtifactsDir\lite_summary.json" -Encoding UTF8

    Write-Host ""
    Write-Host "📁 ARTIFACTS SAVED TO: $ArtifactsDir" -ForegroundColor Cyan
    Write-Host "   - preflight.txt     (system readiness)"
    Write-Host "   - ruff_check.txt    (code style)"
    Write-Host "   - mypy_check.txt    (type checking)"
    Write-Host "   - pytest.txt        (unit tests)"
    Write-Host "   - lite_summary.json (final results)"
    Write-Host ""

    if ($OverallPass) {
        Write-Host "🎉 GO-LIVE CHECK LITE: PASS" -ForegroundColor Green
        Write-Host "✅ Code quality ready for production" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 Next steps:" -ForegroundColor Cyan
        Write-Host "   1. Start server manually: uv run uvicorn zeta_vn.app.main_production:app --host 0.0.0.0 --port 8000"
        Write-Host "   2. Test endpoints with: uv run python scripts/qa/warm_and_probe_rag.py"
        Write-Host "   3. Run full go-live when server is stable"
        exit 0
    }
    else {
        Write-Host "💥 GO-LIVE CHECK LITE: FAIL" -ForegroundColor Red
        Write-Host "❌ Code quality issues detected:" -ForegroundColor Red
        if ($RuffErrors -gt 0) { Write-Host "   - $RuffErrors ruff errors" }
        if ($MypyErrors -gt 0) { Write-Host "   - $MypyErrors mypy errors" }
        if ($TestFailures -gt 0) { Write-Host "   - $TestFailures test failures" }
        if ($ConfigIssues -gt 0) { Write-Host "   - $ConfigIssues config issues" }
        Write-Host ""
        Write-Host "🔧 Fix issues above before proceeding" -ForegroundColor Yellow
        exit 2
    }

}
catch {
    Write-Host "💥 GO-LIVE CHECK LITE FAILED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}