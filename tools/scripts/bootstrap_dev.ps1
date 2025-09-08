# ZETA_VN AI Self-Management Bootstrap - Windows PowerShell
# Run with: .\scripts\bootstrap_dev.ps1

param(
    [switch]$SkipDocker = $false,
    [switch]$SkipDesktop = $false
)

Write-Host "🚀 ZETA_VN AI Self-Management Bootstrap (Windows)" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# 1. Install uv if not present
Write-Host "📦 Installing uv package manager..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv..."
    iwr https://astral.sh/uv/install.ps1 -UseB -OutFile uv.ps1
    .\uv.ps1
    Remove-Item uv.ps1

    # Refresh PATH
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
}

# 2. Python setup
Write-Host "🐍 Setting up Python environment..." -ForegroundColor Yellow
uv python install 3.11
uv sync

# 3. Database setup (optional)
if (-not $SkipDocker) {
    Write-Host "🗄️ Setting up database..." -ForegroundColor Yellow
    try {
        docker --version | Out-Null
        $dockerRunning = (docker ps 2>$null)
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Starting PostgreSQL with pgvector..."
            docker run --rm -d --name zeta-pg `
                -e POSTGRES_PASSWORD=pass `
                -e POSTGRES_DB=zeta `
                -p 5432:5432 `
                pgvector/pgvector:pg16
            if ($LASTEXITCODE -ne 0) {
                Write-Host "⚠️  Database container already running or failed to start" -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "⚠️  Docker is not running" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "⚠️  Docker not available. Please set up PostgreSQL manually." -ForegroundColor Yellow
    }
}

# 4. Environment file
Write-Host "⚙️ Creating .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    @"
# Database
DATABASE_URL=postgresql+asyncpg://postgres:pass@localhost:5432/zeta

# Outbox Pattern
OUTBOX_WORKERS=2
OUTBOX_BATCH_SIZE=200

# AI Self-Management (DEVELOPMENT ONLY)
ZETA_ALLOW_RUNTIME_INSTALL=1
ZETA_ALLOW_SELF_UPDATE=0
ZETA_SELF_SECURITY_AUTO_PATCH=0

# Security allowlist for auto-patching
ZETA_PATCH_ALLOW=requests,aiohttp,psutil

# Monitoring
ENABLE_METRICS=true
HEALTH_CHECK_INTERVAL=30

# Development
ZETA_DEV_MODE=1
LOG_LEVEL=DEBUG
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Created .env file with development settings" -ForegroundColor Green
}
else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# 5. Database migration
Write-Host "🔄 Running database migrations..." -ForegroundColor Yellow
Start-Sleep 3  # Wait for DB container to be ready
try {
    uv run alembic upgrade head
    Write-Host "✅ Database migrations completed" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Migration failed. Check database connection." -ForegroundColor Yellow
}

# 6. Desktop app setup
if (-not $SkipDesktop -and (Test-Path "desktop_ai_zeta")) {
    Write-Host "🖥️ Setting up apps/desktop application..." -ForegroundColor Yellow
    Push-Location desktop_ai_zeta

    # Check Node version
    try {
        $nodeVersion = node --version
        if (-not ($nodeVersion -match "v20")) {
            Write-Host "⚠️  Please install Node.js 20+ manually" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "⚠️  Node.js not found. Please install Node.js 20+" -ForegroundColor Yellow
        Pop-Location
        return
    }

    # Install dependencies
    Write-Host "📦 Installing Node dependencies..." -ForegroundColor Yellow
    npm ci

    # Generate API types
    Write-Host "🔄 Generating API types..." -ForegroundColor Yellow
    try {
        npm run codegen:api
    }
    catch {
        try {
            npm run api:gen
        }
        catch {
            Write-Host "⚠️  API type generation failed" -ForegroundColor Yellow
        }
    }

    Pop-Location
}
elseif (-not (Test-Path "desktop_ai_zeta")) {
    Write-Host "⚠️  desktop_ai_zeta directory not found" -ForegroundColor Yellow
}

# 7. Git hooks setup
Write-Host "🪝 Setting up Git hooks..." -ForegroundColor Yellow
git config core.hooksPath .githooks

# 8. Verify installation
Write-Host "✅ Verifying installation..." -ForegroundColor Yellow

# Test Python environment
uv run python -c @"
import sys
print(f'Python version: {sys.version}')

# Test AI Self-Management imports
try:
    from zeta_vn.core.self_improvement import AutoOptimizer, PerformanceKnobs
    from zeta_vn.core.security import security_sweep
    from zeta_vn.core.self_awareness import HealthMonitor
    from zeta_vn.core.utils import get_runtime_install_status
    print('✅ AI Self-Management modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')

# Test database connection (optional)
try:
    import asyncio
    import os
    from zeta_vn.data.database import test_connection
    if os.getenv('DATABASE_URL'):
        asyncio.run(test_connection())
        print('✅ Database connection successful')
except Exception as e:
    print(f'⚠️  Database test failed: {e}')
"@

Write-Host ""
Write-Host "🎉 Bootstrap complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Open VS Code: code ."
Write-Host "2. Run quality check: uv run python tools/master_quality_check.py"
Write-Host "3. Start development server: uv run uvicorn zeta_vn.app.main_production:app --reload"
Write-Host "4. Start apps/desktop app: cd desktop_ai_zeta; npm run dev"
Write-Host ""
Write-Host "📚 Useful VS Code tasks:" -ForegroundColor Cyan
Write-Host "- Ctrl+Shift+P > 'Tasks: Run Task' > 'QA: Master Quality Check'"
Write-Host "- Ctrl+Shift+P > 'Tasks: Run Task' > 'FastAPI: Uvicorn Dev'"
Write-Host "- Ctrl+Shift+P > 'Tasks: Run Task' > 'Desktop: Contract Sync'"
Write-Host ""
Write-Host "🤖 AI Self-Management features are ready!" -ForegroundColor Magenta
Write-Host "Check status: Invoke-RestMethod http://localhost:8000/admin/health/detailed"
