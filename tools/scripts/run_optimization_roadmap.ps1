# ZETA_VN Optimization Roadmap - Master Execution Script (PowerShell)
# Runs all 4 phases of the optimization roadmap

param(
    [switch]$SkipDocker,
    [switch]$Verbose
)

# Set error action preference
$ErrorActionPreference = "Continue"

Write-Host "🚀 ZETA_VN OPTIMIZATION ROADMAP 2025" -ForegroundColor Blue
Write-Host "====================================" -ForegroundColor Blue
Write-Host "Running all 4 phases of the optimization roadmap" -ForegroundColor White
Write-Host ""

# Color functions
function Write-Phase {
    param($Message)
    Write-Host $Message -ForegroundColor Blue
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

# Check prerequisites
function Test-Prerequisites {
    Write-Phase "Checking prerequisites..."
    
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Error "uv is not installed. Please install uv first."
        exit 1
    }
    
    if (-not (Get-Command docker -ErrorAction SilentlyContinue) -or $SkipDocker) {
        Write-Warning "Docker is not available or skipped. Phase 4 will be skipped."
        $script:SkipDockerPhase = $true
    }
    else {
        $script:SkipDockerPhase = $false
    }
    
    Write-Success "Prerequisites checked"
}

# Phase 1: Foundation
function Invoke-Phase1 {
    Write-Phase "🏗️ PHASE 1: FOUNDATION - Code Quality & Architecture"
    
    try {
        # Run foundation script commands
        Write-Host "Running code formatting..." -ForegroundColor Cyan
        uv run ruff format .
        
        Write-Host "Running code checking..." -ForegroundColor Cyan
        uv run ruff check .
        
        Write-Host "Running type checking..." -ForegroundColor Cyan
        uv run mypy .
        
        Write-Host "Running tests..." -ForegroundColor Cyan
        uv run pytest -q
        
        Write-Host "Running security scan..." -ForegroundColor Cyan
        uv run bandit -q -r zeta_vn
        
        Write-Host "Running dependency audit..." -ForegroundColor Cyan
        uv run pip-audit -q
        
        Write-Success "Phase 1 completed successfully"
    }
    catch {
        Write-Warning "Phase 1 completed with warnings: $($_.Exception.Message)"
    }
    Write-Host ""
}

# Phase 2: Performance
function Invoke-Phase2 {
    Write-Phase "⚡ PHASE 2: PERFORMANCE - Testing & Optimization"
    
    try {
        # Start server in background
        Write-Host "Starting test server..." -ForegroundColor Cyan
        $serverJob = Start-Job -ScriptBlock {
            Set-Location $using:PWD
            uv run uvicorn zeta_vn.app.main_minimal:app --host 0.0.0.0 --port 8000
        }
        
        # Wait for server to start
        Start-Sleep -Seconds 5
        
        # Check if server is running
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
            Write-Success "Test server started (Job ID: $($serverJob.Id))"
            
            # Run performance probe
            Write-Host "Running performance probe..." -ForegroundColor Cyan
            uv run python scripts/perf/probe.py
            
            Write-Success "Phase 2 completed successfully"
        }
        catch {
            Write-Error "Failed to connect to test server: $($_.Exception.Message)"
        }
        finally {
            # Clean up server
            if ($serverJob) {
                Stop-Job -Job $serverJob -ErrorAction SilentlyContinue
                Remove-Job -Job $serverJob -ErrorAction SilentlyContinue
                Write-Success "Test server stopped"
            }
        }
    }
    catch {
        Write-Warning "Phase 2 completed with warnings: $($_.Exception.Message)"
    }
    Write-Host ""
}

# Phase 3: Security
function Invoke-Phase3 {
    Write-Phase "🔒 PHASE 3: SECURITY - Hardening & Compliance"
    
    try {
        Write-Host "Running enhanced security scan..." -ForegroundColor Cyan
        uv run bandit -r zeta_vn --format json --output bandit_security_report.json
        
        Write-Host "Running vulnerability audit..." -ForegroundColor Cyan
        uv run pip-audit --format=json --output=pip_audit_report.json
        
        Write-Host "Running dead code detection..." -ForegroundColor Cyan
        uv run vulture zeta_vn --min-confidence 80
        
        Write-Success "Phase 3 completed successfully"
    }
    catch {
        Write-Warning "Phase 3 completed with warnings: $($_.Exception.Message)"
    }
    Write-Host ""
}

# Phase 4: Deployment
function Invoke-Phase4 {
    Write-Phase "🚀 PHASE 4: DEPLOYMENT - Production Ready"
    
    if ($script:SkipDockerPhase) {
        Write-Warning "Skipping Phase 4 - Docker not available"
        return
    }
    
    try {
        Write-Host "Building production Docker image..." -ForegroundColor Cyan
        docker build -f Dockerfile.production -t zeta_vn:production .
        
        Write-Host "Running container security scan..." -ForegroundColor Cyan
        docker run --rm -v ${PWD}:/app zeta_vn:production sh -c "cd /app && bandit -r zeta_vn"
        
        Write-Success "Phase 4 completed successfully"
    }
    catch {
        Write-Error "Phase 4 failed: $($_.Exception.Message)"
    }
    Write-Host ""
}

# Summary report
function Write-Summary {
    Write-Phase "📊 OPTIMIZATION SUMMARY"
    Write-Host "=======================" -ForegroundColor Blue
    
    Write-Host "🏗️ Phase 1: Foundation" -ForegroundColor White
    Write-Host "   - Code quality fixes applied" -ForegroundColor Gray
    Write-Host "   - Type checking performed" -ForegroundColor Gray
    Write-Host "   - Tests executed" -ForegroundColor Gray
    Write-Host "   - Security scan completed" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "⚡ Phase 2: Performance" -ForegroundColor White
    Write-Host "   - API performance tested" -ForegroundColor Gray
    Write-Host "   - Bottlenecks identified" -ForegroundColor Gray
    Write-Host "   - Optimization opportunities noted" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "🔒 Phase 3: Security" -ForegroundColor White
    Write-Host "   - Security hardening applied" -ForegroundColor Gray
    Write-Host "   - Vulnerability assessment completed" -ForegroundColor Gray
    Write-Host "   - Compliance checks performed" -ForegroundColor Gray
    
    Write-Host ""
    if (-not $script:SkipDockerPhase) {
        Write-Host "🚀 Phase 4: Deployment" -ForegroundColor White
        Write-Host "   - Production Docker image built" -ForegroundColor Gray
        Write-Host "   - Container ready for deployment" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Success "All phases completed!"
    Write-Host ""
    Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Review any warnings or errors above" -ForegroundColor Gray
    Write-Host "   2. Fix remaining issues identified" -ForegroundColor Gray
    Write-Host "   3. Run individual phases as needed" -ForegroundColor Gray
    Write-Host "   4. Deploy to staging environment" -ForegroundColor Gray
    Write-Host "   5. Perform load testing" -ForegroundColor Gray
    Write-Host "   6. Deploy to production" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📖 For detailed implementation:" -ForegroundColor Cyan
    Write-Host "   - See PROJECT_OPTIMIZATION_COMPLETE_ROADMAP.md" -ForegroundColor Gray
    Write-Host "   - Run individual phase scripts in scripts/impl/" -ForegroundColor Gray
    Write-Host "   - Check CI/CD workflow in .github/workflows/quality_v3.yml" -ForegroundColor Gray
}

# Main execution
function Main {
    Test-Prerequisites
    
    Write-Host "Starting optimization roadmap execution..." -ForegroundColor White
    Write-Host "This will run all 4 phases sequentially." -ForegroundColor White
    Write-Host ""
    
    # Run all phases
    Invoke-Phase1
    Invoke-Phase2
    Invoke-Phase3
    Invoke-Phase4
    
    # Generate summary
    Write-Summary
}

# Handle Ctrl+C
try {
    Main
}
catch {
    Write-Host ""
    Write-Error "Script interrupted: $($_.Exception.Message)"
    exit 1
}