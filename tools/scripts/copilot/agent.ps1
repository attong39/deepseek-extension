# PowerShell wrapper cho Copilot Coding Agent
param(
    [switch]$Force,
    [string]$LogLevel = "INFO"
)

Write-Host "🤖 COPILOT CODING AGENT - PowerShell Edition" -ForegroundColor Cyan

# Check dependencies
function Test-Command($cmd) {
    $null = Get-Command $cmd -ErrorAction SilentlyContinue
    return $?
}

if (-not (Test-Command "uv")) {
    Write-Host "❌ uv not found. Install from: https://docs.astral.sh/uv/" -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "node")) {
    Write-Host "❌ Node.js not found. Install from: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host "⚠️  Continuing without frontend checks..." -ForegroundColor Yellow
}

# Setup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = ".artifacts/copilot_agent_$timestamp.log"

if (-not (Test-Path ".artifacts")) {
    New-Item -ItemType Directory -Path ".artifacts" -Force | Out-Null
}

# Logging function
function Write-Log($message, $color = "White") {
    $timestamped = "[$(Get-Date -Format 'HH:mm:ss')] $message"
    Write-Host $timestamped -ForegroundColor $color
    Add-Content -Path $logFile -Value $timestamped
}

Write-Log "▶ Copilot Coding Agent started @ $timestamp" "Cyan"

try {
    # 1) Build Copilot context
    Write-Log "📖 Building Copilot context..." "Yellow"
    & uv run python scripts/copilot/build_context.py 2>&1 | Add-Content -Path $logFile
    
    # 2) Backend quality
    Write-Log "🐍 Running Python quality checks..." "Green"
    & uv sync 2>&1 | Add-Content -Path $logFile
    & uv run ruff check . --fix 2>&1 | Add-Content -Path $logFile
    & uv run ruff format . 2>&1 | Add-Content -Path $logFile
    & uv run mypy zeta_vn --pretty --no-error-summary 2>&1 | Add-Content -Path $logFile
    & uv run pytest -q --maxfail=1 --disable-warnings --cov=zeta_vn --cov-report=term-missing --cov-fail-under=80 2>&1 | Add-Content -Path $logFile
    & uv run bandit -q -r zeta_vn 2>&1 | Add-Content -Path $logFile
    & uv run pip-audit 2>&1 | Add-Content -Path $logFile
    
    # 3) Frontend quality (if exists)
    if (Test-Path "desktop_ai_zeta") {
        Write-Log "📘 Running TypeScript quality checks..." "Blue"
        Push-Location "desktop_ai_zeta"
        try {
            if (Test-Command "npm") {
                & npm ci 2>&1 | Add-Content -Path "../$logFile"
                & npx prettier "src/**/*.{ts,tsx,css,md}" --write 2>&1 | Add-Content -Path "../$logFile"
                & npx eslint "src/**/*.{ts,tsx}" --fix 2>&1 | Add-Content -Path "../$logFile"
                & npx tsc --noEmit 2>&1 | Add-Content -Path "../$logFile"
                
                if (Test-Path "vitest.config.ts") {
                    & npx vitest run --coverage 2>&1 | Add-Content -Path "../$logFile"
                }
                
                & npx depcheck 2>&1 | Add-Content -Path "../$logFile"
                
                if (-not (Test-Path "../.artifacts/deadcode")) {
                    New-Item -ItemType Directory -Path "../.artifacts/deadcode" -Force | Out-Null
                }
                & npx ts-prune > "../.artifacts/deadcode/ts-prune.txt" 2>&1
            }
        }
        finally {
            Pop-Location
        }
    }
    
    # 4) Code analysis
    Write-Log "🔍 Running code duplication analysis..." "Magenta"
    if (-not (Test-Path ".artifacts/jscpd-report")) {
        New-Item -ItemType Directory -Path ".artifacts/jscpd-report" -Force | Out-Null
    }
    
    if (Test-Command "npx") {
        & npx jscpd --reporters html --output .artifacts/jscpd-report --threshold 2 --pattern "**/*.{ts,tsx,js,py}" . 2>&1 | Add-Content -Path $logFile
    }
    
    Write-Log "💀 Running dead code analysis..." "DarkRed"
    if (-not (Test-Path ".artifacts/deadcode")) {
        New-Item -ItemType Directory -Path ".artifacts/deadcode" -Force | Out-Null
    }
    & uvx vulture zeta_vn --min-confidence 80 > ".artifacts/deadcode/vulture.txt" 2>&1
    
    # 5) Performance gate
    Write-Log "⚡ Running performance gate..." "Yellow"
    & uv run python scripts/perf/perf_gate.py --startup-budget 3.0 --ram-budget-mb 300 2>&1 | Add-Content -Path $logFile
    
    # 6) Summary
    Write-Log "" 
    Write-Log "=== SUMMARY ARTIFACTS ===" "Cyan"
    
    $artifacts = @(
        ".artifacts/jscpd-report/jscpd-report.html",
        ".artifacts/deadcode/vulture.txt", 
        ".artifacts/deadcode/ts-prune.txt",
        "COPILOT_CONTEXT.md"
    )
    
    foreach ($artifact in $artifacts) {
        $status = if (Test-Path $artifact) { "(OK)" } else { "(missing)" }
        $color = if (Test-Path $artifact) { "Green" } else { "Red" }
        Write-Log "• $artifact $status" $color
        Add-Content -Path $logFile -Value "• $artifact $status"
    }
    
    Write-Log "" 
    Write-Log "✔ Done. Log: $logFile" "Green"
    Write-Log "👉 Gợi ý commit: git add -A && git commit -m 'chore: copilot agent – format, imports, dedupe, deadcode, perf-gate'" "Yellow"
    
    # Open key artifacts if available
    if ($Force -and (Test-Path ".artifacts/jscpd-report/jscpd-report.html")) {
        Write-Log "🌐 Opening duplication report..." "Cyan"
        Start-Process ".artifacts/jscpd-report/jscpd-report.html"
    }
    
}
catch {
    Write-Log "❌ Error occurred: $($_.Exception.Message)" "Red"
    exit 1
}
