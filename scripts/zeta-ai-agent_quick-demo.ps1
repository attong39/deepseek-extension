# =============================================================================
# 🚀 Zeta AI Agent - Quick Deployment Demo
# Script để demo nhanh deployment và kiểm tra tất cả các tính năng
# =============================================================================

Write-Host "🚀 Zeta AI Agent - Quick Deployment Demo" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  Running as regular user (some Docker commands may require admin)" -ForegroundColor Yellow
}

# Function to check if command exists
function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Function to run command with error handling
function Invoke-SafeCommand {
    param(
        [string]$Command,
        [string]$Description,
        [switch]$IgnoreError
    )
    
    Write-Host "`n🔧 $Description" -ForegroundColor Cyan
    Write-Host "Command: $Command" -ForegroundColor Gray
    
    try {
        Invoke-Expression $Command
        Write-Host "✅ Success" -ForegroundColor Green
        return $true
    }
    catch {
        if ($IgnoreError) {
            Write-Host "⚠️  Warning: $($_.Exception.Message)" -ForegroundColor Yellow
            return $false
        } else {
            Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    }
}

Write-Host "`n📋 Checking Prerequisites..." -ForegroundColor Yellow

# Check Node.js
if (Test-Command "node") {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check Python
if (Test-Command "python") {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check Docker (optional)
if (Test-Command "docker") {
    $dockerVersion = docker --version
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
    $hasDocker = $true
} else {
    Write-Host "⚠️  Docker not found (optional for container demo)" -ForegroundColor Yellow
    $hasDocker = $false
}

# Check VS Code (optional)
if (Test-Command "code") {
    Write-Host "✅ VS Code: Available" -ForegroundColor Green
    $hasVSCode = $true
} else {
    Write-Host "⚠️  VS Code not found (optional for extension demo)" -ForegroundColor Yellow
    $hasVSCode = $false
}

Write-Host "`n🏗️  Building Zeta AI Agent..." -ForegroundColor Yellow

# Install Node.js dependencies
Invoke-SafeCommand "npm install" "Installing Node.js dependencies"

# Install Python dependencies
Invoke-SafeCommand "pip install -r requirements.txt" "Installing Python dependencies"

# Build the extension
Invoke-SafeCommand "npm run build" "Building TypeScript code"
Invoke-SafeCommand "npm run compile" "Compiling extension"

Write-Host "`n🚀 Starting Services..." -ForegroundColor Yellow

# Start metrics server in background
Write-Host "`n🔧 Starting Metrics Server" -ForegroundColor Cyan
$metricsProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "metrics_server:app", "--host", "127.0.0.1", "--port", "9100" -PassThru -WindowStyle Hidden

Start-Sleep -Seconds 3

# Check if metrics server is running
try {
    Invoke-WebRequest -Uri "http://localhost:9100/health" -UseBasicParsing | Out-Null
    Write-Host "✅ Metrics server running on http://localhost:9100" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start metrics server" -ForegroundColor Red
    exit 1
}

Write-Host "`n🧪 Running Demo Tests..." -ForegroundColor Yellow

# Test 1: Health Check
Write-Host "`n1. Testing Health Endpoints" -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:9100/health"
    Write-Host "   Health: $($health.status)" -ForegroundColor Green
    
    $ready = Invoke-RestMethod -Uri "http://localhost:9100/ready"
    Write-Host "   Ready: $($ready.status)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Health check failed" -ForegroundColor Red
}

# Test 2: Submit Sample Feedback
Write-Host "`n2. Testing Feedback Submission" -ForegroundColor Cyan
$sampleFeedback = @{
    model_name = "demo-model"
    prompt = "Viết code Python tính fibonacci"
    response = "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
    rating = 9
    latency = 1.2
    vietnamese_quality = 8
    session_id = "demo-session-$(Get-Random)"
} | ConvertTo-Json

try {
    $feedbackResponse = Invoke-RestMethod -Uri "http://localhost:9100/feedback" -Method Post -Body $sampleFeedback -ContentType "application/json"
    Write-Host "   ✅ Feedback submitted successfully" -ForegroundColor Green
    Write-Host "   Message: $($feedbackResponse.message)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Feedback submission failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Check Metrics
Write-Host "`n3. Testing Prometheus Metrics" -ForegroundColor Cyan
try {
    $metrics = Invoke-WebRequest -Uri "http://localhost:9100/metrics" -UseBasicParsing
    $metricsLines = $metrics.Content -split "`n" | Where-Object { $_ -match "zeta_" -and $_ -notmatch "^#" }
    
    Write-Host "   ✅ Metrics available:" -ForegroundColor Green
    $metricsLines | Select-Object -First 5 | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
    
    if ($metricsLines.Count -gt 5) {
        Write-Host "     ... and $($metricsLines.Count - 5) more metrics" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Metrics check failed" -ForegroundColor Red
}

# Test 4: Statistics
Write-Host "`n4. Testing Statistics Endpoint" -ForegroundColor Cyan
try {
    $stats = Invoke-RestMethod -Uri "http://localhost:9100/stats"
    Write-Host "   ✅ Statistics retrieved:" -ForegroundColor Green
    Write-Host "     Total feedback: $($stats.total_feedback)" -ForegroundColor Gray
    Write-Host "     Feedback 24h: $($stats.feedback_24h)" -ForegroundColor Gray
    Write-Host "     Active models: $($stats.metrics.active_models)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Statistics check failed" -ForegroundColor Red
}

# Docker Demo (if available)
if ($hasDocker) {
    Write-Host "`n🐳 Docker Demo..." -ForegroundColor Yellow
    
    Write-Host "`n🔧 Building Docker Image" -ForegroundColor Cyan
    if (Invoke-SafeCommand "docker build -t apps/zeta-ai-agent:demo ." "Building Docker image" -IgnoreError) {
        Write-Host "`n🔧 Running Docker Container" -ForegroundColor Cyan
        
        # Stop existing container if running
        docker stop zeta-demo 2>$null | Out-Null
        docker rm zeta-demo 2>$null | Out-Null
        
        $dockerCommand = "docker run -d --name zeta-demo -p 9101:9100 -e ALLOWED_ORIGINS=http://localhost:* apps/zeta-ai-agent:demo"
        
        if (Invoke-SafeCommand $dockerCommand "Starting Docker container on port 9101" -IgnoreError) {
            Start-Sleep -Seconds 5
            
            try {
                $dockerHealth = Invoke-RestMethod -Uri "http://localhost:9101/health"
                Write-Host "   ✅ Docker container running: $($dockerHealth.status)" -ForegroundColor Green
                Write-Host "   🌐 Access at: http://localhost:9101" -ForegroundColor Cyan
            } catch {
                Write-Host "   ⚠️  Docker container may still be starting" -ForegroundColor Yellow
            }
        }
    }
}

# VS Code Extension Demo (if available)
if ($hasVSCode) {
    Write-Host "`n🔧 VS Code Extension Demo" -ForegroundColor Yellow
    
    # Package extension
    if (Test-Command "npx") {
        Write-Host "`n🔧 Packaging Extension" -ForegroundColor Cyan
        if (Invoke-SafeCommand "npx vsce package --out zeta-ai-agent-demo.vsix" "Creating VSIX package" -IgnoreError) {
            Write-Host "   📦 Extension packaged: zeta-ai-agent-demo.vsix" -ForegroundColor Green
            Write-Host "   💡 To install: code --install-extension zeta-ai-agent-demo.vsix" -ForegroundColor Cyan
        }
    }
}

Write-Host "`n📊 Production Configuration Check..." -ForegroundColor Yellow

# Run the production config checker
if (Test-Path ".\scripts\check-production-config.ps1") {
    Write-Host "`n🔧 Running Production Config Checker" -ForegroundColor Cyan
    try {
        & ".\scripts\check-production-config.ps1" -Host "localhost" -Port 9100
    } catch {
        Write-Host "⚠️  Could not run production config checker" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Production config checker script not found" -ForegroundColor Yellow
}

Write-Host "`n🎉 Demo Complete!" -ForegroundColor Blue
Write-Host "================" -ForegroundColor Blue

Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "✅ Metrics Server: http://localhost:9100" -ForegroundColor Green
Write-Host "   - Health: http://localhost:9100/health"
Write-Host "   - Metrics: http://localhost:9100/metrics"
Write-Host "   - Stats: http://localhost:9100/stats"

if ($hasDocker) {
    Write-Host "✅ Docker Container: http://localhost:9101" -ForegroundColor Green
}

if ($hasVSCode -and (Test-Path "zeta-ai-agent-demo.vsix")) {
    Write-Host "✅ VS Code Extension: zeta-ai-agent-demo.vsix" -ForegroundColor Green
}

Write-Host "`n🔧 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open VS Code and install the extension (if packaged)"
Write-Host "2. Set up Prometheus to scrape http://localhost:9100/metrics"
Write-Host "3. Configure Alertmanager with provided rules"
Write-Host "4. Set up Grafana dashboard"
Write-Host "5. Deploy to production with proper CORS settings"

Write-Host "`n🛑 Cleanup:" -ForegroundColor Yellow
Write-Host "To stop services:"
Write-Host "  • Metrics server: Stop-Process -Id $($metricsProcess.Id)"
if ($hasDocker) {
    Write-Host "  • Docker: docker stop zeta-demo && docker rm zeta-demo"
}

Write-Host "`n📚 Documentation:" -ForegroundColor Cyan
Write-Host "• Production Guide: PRODUCTION_DEPLOYMENT_GUIDE.md"
Write-Host "• Configuration: config/"
Write-Host "• Helm Chart: helm/apps/zeta-ai-agent/"

# Keep console open
Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
