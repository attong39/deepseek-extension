# 🎯 Environment Status & Quick Setup

## 📊 Current Environment Assessment

✅ **Available:**
- PowerShell ✅
- WSL (Windows Subsystem for Linux) ✅
- Git ✅
- Node.js development environment ✅

❌ **Missing:**
- Docker Desktop
- kubectl (Kubernetes CLI)
- Helm
- k6 (Load testing)

## 🚀 Quick Development Setup (No Admin Rights Required)

### Option 1: Local Development (Recommended)
```powershell
# Navigate to the project
cd E:\zeta\zeta-monorepo\apps/zeta-ai-agent

# Install dependencies
npm install

# Start in development mode
npm run dev

# Or start with PM2 for production-like
npm install -g pm2
pm2 start ecosystem.config.js
```

### Option 2: Portable Tools Setup
```powershell
# Create tools directory
mkdir .\tools
cd .\tools

# Download portable kubectl
Invoke-WebRequest -Uri "https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe" -OutFile "kubectl.exe"

# Download portable helm
Invoke-WebRequest -Uri "https://get.helm.sh/helm-v3.12.0-windows-amd64.zip" -OutFile "helm.zip"
Expand-Archive -Path "helm.zip" -DestinationPath "."

# Add to current session PATH
$env:PATH += ";$(Get-Location)"
```

### Option 3: WSL Development
```powershell
# Use WSL for containerized development
wsl --install Ubuntu-22.04

# In WSL terminal:
sudo apt update
sudo apt install -y docker.io kubectl helm
sudo systemctl start docker
sudo usermod -aG docker $USER
```

## 🔍 Quick Health Checks (Current Environment)

### 1. Application Health Check
```powershell
# If application is running locally
curl http://localhost:3000/health
curl http://localhost:3000/api/v1/status
curl http://localhost:3000/metrics

# Alternative with PowerShell
Invoke-RestMethod -Uri "http://localhost:3000/health"
Invoke-RestMethod -Uri "http://localhost:3000/api/v1/status"
```

### 2. Process Monitoring
```powershell
# Check if Node.js app is running
Get-Process node -ErrorAction SilentlyContinue

# Check port usage
netstat -ano | findstr :3000
netstat -ano | findstr :9090
netstat -ano | findstr :9093
```

### 3. Performance Monitoring (Basic)
```powershell
# Monitor resource usage
Get-Process node | Select-Object Name, CPU, WorkingSet, PagedMemorySize

# Monitor network connections
Get-NetTCPConnection -LocalPort 3000
```

## 🎯 Quick Mock Verification Commands

Since we don't have Kubernetes running yet, here are equivalent checks:

### Instead of `kubectl get hpa -n zeta-agent`:
```powershell
# Check if application supports auto-scaling config
$Response = Invoke-RestMethod -Uri "http://localhost:3000/api/v1/status" -ErrorAction SilentlyContinue
if ($Response) {
    Write-Host "✅ Application is responsive" -ForegroundColor Green
    $Response | ConvertTo-Json -Depth 3
} else {
    Write-Host "❌ Application not responding" -ForegroundColor Red
}
```

### Instead of `kubectl top pods -n zeta-agent`:
```powershell
# Monitor local process resources
$Process = Get-Process node -ErrorAction SilentlyContinue
if ($Process) {
    Write-Host "✅ Node.js Process Status:" -ForegroundColor Green
    $Process | Select-Object Name, Id, CPU, WorkingSet, PagedMemorySize | Format-Table
    Write-Host "Memory Usage: $(($Process.WorkingSet / 1MB).ToString('N2')) MB" -ForegroundColor Cyan
    Write-Host "CPU Time: $($Process.TotalProcessorTime)" -ForegroundColor Cyan
} else {
    Write-Host "❌ Node.js process not found" -ForegroundColor Red
}
```

### Instead of Prometheus metrics scraping:
```powershell
# Get application metrics directly
try {
    $Metrics = Invoke-WebRequest -Uri "http://localhost:3000/metrics" -UseBasicParsing
    Write-Host "✅ Metrics endpoint accessible" -ForegroundColor Green
    Write-Host "Metrics size: $($Metrics.Content.Length) bytes" -ForegroundColor Cyan
    
    # Parse key metrics
    $MetricsLines = $Metrics.Content -split "`n"
    $RequestCount = $MetricsLines | Where-Object { $_ -like "*http_requests_total*" } | Select-Object -First 1
    $ResponseTime = $MetricsLines | Where-Object { $_ -like "*http_request_duration*" } | Select-Object -First 1
    
    if ($RequestCount) { Write-Host "Request metrics: $RequestCount" -ForegroundColor White }
    if ($ResponseTime) { Write-Host "Response time metrics: $ResponseTime" -ForegroundColor White }
    
} catch {
    Write-Host "❌ Cannot access metrics endpoint" -ForegroundColor Red
}
```

### Instead of Alertmanager checks:
```powershell
# Simple health monitoring script
function Test-ApplicationHealth {
    $HealthChecks = @()
    
    # Health endpoint
    try {
        $Health = Invoke-RestMethod -Uri "http://localhost:3000/health" -TimeoutSec 5
        $HealthChecks += @{ Check = "Health Endpoint"; Status = "✅ PASS"; Response = $Health }
    } catch {
        $HealthChecks += @{ Check = "Health Endpoint"; Status = "❌ FAIL"; Response = $_.Exception.Message }
    }
    
    # API endpoint
    try {
        $Status = Invoke-RestMethod -Uri "http://localhost:3000/api/v1/status" -TimeoutSec 5
        $HealthChecks += @{ Check = "API Endpoint"; Status = "✅ PASS"; Response = $Status }
    } catch {
        $HealthChecks += @{ Check = "API Endpoint"; Status = "❌ FAIL"; Response = $_.Exception.Message }
    }
    
    # Process check
    $Process = Get-Process node -ErrorAction SilentlyContinue
    if ($Process) {
        $HealthChecks += @{ Check = "Process Running"; Status = "✅ PASS"; Response = "PID: $($Process.Id)" }
    } else {
        $HealthChecks += @{ Check = "Process Running"; Status = "❌ FAIL"; Response = "No Node.js process found" }
    }
    
    # Display results
    Write-Host "`n🔍 Application Health Check Results:" -ForegroundColor Cyan
    $HealthChecks | ForEach-Object {
        Write-Host "$($_.Check): $($_.Status)" -ForegroundColor $(if ($_.Status -like "*✅*") { "Green" } else { "Red" })
        if ($_.Response) {
            Write-Host "   Response: $($_.Response)" -ForegroundColor Gray
        }
    }
}

# Run the health check
Test-ApplicationHealth
```

## 🚀 Immediate Actions

### 1. Start Application Locally (Right Now)
```powershell
# Quick start command
cd E:\zeta\zeta-monorepo\apps/zeta-ai-agent
npm install
npm start

# In another terminal, run health checks
.\scripts\env-check.ps1 -ShowCommands
```

### 2. Performance Testing (Without k6)
```powershell
# Simple PowerShell load test
$StartTime = Get-Date
$Requests = 0
$Errors = 0

for ($i = 1; $i -le 100; $i++) {
    try {
        $Response = Invoke-RestMethod -Uri "http://localhost:3000/health" -TimeoutSec 2
        $Requests++
    } catch {
        $Errors++
    }
    Write-Progress -Activity "Load Testing" -Status "Request $i/100" -PercentComplete $i
}

$Duration = (Get-Date) - $StartTime
$RPS = $Requests / $Duration.TotalSeconds

Write-Host "`n📊 Simple Load Test Results:" -ForegroundColor Cyan
Write-Host "Total Requests: $Requests" -ForegroundColor White
Write-Host "Errors: $Errors" -ForegroundColor $(if ($Errors -gt 0) { "Red" } else { "Green" })
Write-Host "Duration: $($Duration.TotalSeconds.ToString('N2')) seconds" -ForegroundColor White
Write-Host "RPS: $($RPS.ToString('N2'))" -ForegroundColor White
Write-Host "Error Rate: $(($Errors / 100 * 100).ToString('N2'))%" -ForegroundColor $(if ($Errors -gt 5) { "Red" } else { "Green" })
```

## 📋 Next Steps Priority

1. **Immediate** (5 minutes): Start application locally and run health checks
2. **Short-term** (30 minutes): Install Docker Desktop for containerization
3. **Medium-term** (1 hour): Set up local Kubernetes with Docker Desktop
4. **Long-term** (2 hours): Deploy full monitoring stack

---
💡 **Start Here**: Run `npm start` and then use the health check commands above!
