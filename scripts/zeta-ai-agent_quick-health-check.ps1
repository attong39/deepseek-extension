#!/usr/bin/env powershell

# Comprehensive Health Check Script for Zeta Agent
# Works with or without Kubernetes/Docker

param(
    [int]$Port = 8000,
    [string]$HostName = "localhost",
    [switch]$Detailed,
    [switch]$Continuous,
    [int]$Interval = 5
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Test-PortOpen {
    param([string]$HostName, [int]$Port, [int]$TimeoutMs = 1000)
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $asyncResult = $tcpClient.BeginConnect($HostName, $Port, $null, $null)
        $wait = $asyncResult.AsyncWaitHandle.WaitOne($TimeoutMs)
        if ($wait) {
            $tcpClient.EndConnect($asyncResult)
            $tcpClient.Close()
            return $true
        } else {
            $tcpClient.Close()
            return $false
        }
    } catch {
        return $false
    }
}

function Test-ApplicationEndpoints {
    param([string]$BaseUrl)
    
    $Results = @()
    $Endpoints = @(
        @{ Path = "/health"; Description = "Health Check"; ExpectedStatus = 200; Timeout = 5 },
        @{ Path = "/ready"; Description = "Readiness Check"; ExpectedStatus = 200; Timeout = 5 },
        @{ Path = "/api/v1/status"; Description = "API Status"; ExpectedStatus = 200; Timeout = 5 },
        @{ Path = "/docs"; Description = "API Documentation"; ExpectedStatus = 200; Timeout = 5 },
        @{ Path = "/metrics"; Description = "Prometheus Metrics"; ExpectedStatus = 200; Timeout = 5 }
    )
    
    foreach ($Endpoint in $Endpoints) {
        $Url = "$BaseUrl$($Endpoint.Path)"
        try {
            Write-Host "Testing $($Endpoint.Description) at $Url..." -ForegroundColor Gray
            
            $Response = Invoke-WebRequest -Uri $Url -TimeoutSec $Endpoint.Timeout -UseBasicParsing -ErrorAction Stop
            
            $Results += @{
                Endpoint = $Endpoint.Path
                Description = $Endpoint.Description
                Status = "✅ PASS"
                StatusCode = $Response.StatusCode
                ResponseTime = "< $($Endpoint.Timeout)s"
                ContentLength = $Response.Content.Length
                Details = $Response.Content.Substring(0, [Math]::Min(100, $Response.Content.Length))
            }
            Write-Status "$($Endpoint.Description): ✅ OK ($($Response.StatusCode))" "Success"
            
        } catch {
            $Results += @{
                Endpoint = $Endpoint.Path
                Description = $Endpoint.Description
                Status = "❌ FAIL"
                StatusCode = $_.Exception.Response.StatusCode.value__ -or "N/A"
                ResponseTime = "> $($Endpoint.Timeout)s"
                ContentLength = 0
                Details = $_.Exception.Message
            }
            Write-Status "$($Endpoint.Description): ❌ FAIL" "Error"
        }
    }
    
    return $Results
}

function Test-ProcessHealth {
    Write-Status "🔍 Checking application processes..." "Info"
    
    # Check Python processes
    $PythonProcesses = Get-Process python* -ErrorAction SilentlyContinue
    if ($PythonProcesses) {
        Write-Status "✅ Found $($PythonProcesses.Count) Python process(es)" "Success"
        foreach ($Process in $PythonProcesses) {
            $MemoryMB = [math]::Round($Process.WorkingSet / 1MB, 2)
            $CpuTime = $Process.TotalProcessorTime
            Write-Host "   PID $($Process.Id): Memory ${MemoryMB}MB, CPU Time $CpuTime" -ForegroundColor White
        }
    } else {
        Write-Status "⚠️  No Python processes found" "Warning"
    }
    
    # Check Node processes (for VS Code extension)
    $NodeProcesses = Get-Process node* -ErrorAction SilentlyContinue
    if ($NodeProcesses) {
        Write-Status "✅ Found $($NodeProcesses.Count) Node.js process(es)" "Success"
    }
    
    # Check port usage
    $PortInfo = netstat -ano | Select-String ":$Port"
    if ($PortInfo) {
        Write-Status "✅ Port $Port is in use" "Success"
        $PortInfo | ForEach-Object { Write-Host "   $_" -ForegroundColor White }
    } else {
        Write-Status "⚠️  Port $Port is not in use" "Warning"
    }
}

function Show-HealthSummary {
    param([array]$Results)
    
    Write-Host "`n📊 Health Check Summary:" -ForegroundColor Cyan
    Write-Host "========================" -ForegroundColor Cyan
    
    $PassCount = ($Results | Where-Object { $_.Status -like "*✅*" }).Count
    $FailCount = ($Results | Where-Object { $_.Status -like "*❌*" }).Count
    $TotalCount = $Results.Count
    
    Write-Host "Total Endpoints: $TotalCount" -ForegroundColor White
    Write-Host "Passed: $PassCount" -ForegroundColor Green
    Write-Host "Failed: $FailCount" -ForegroundColor Red
    Write-Host "Success Rate: $(if($TotalCount -gt 0) { [math]::Round(($PassCount / $TotalCount) * 100, 1) } else { 0 })%" -ForegroundColor $(if($PassCount -eq $TotalCount) { "Green" } else { "Yellow" })
    
    if ($Detailed) {
        Write-Host "`n📋 Detailed Results:" -ForegroundColor Cyan
        foreach ($Result in $Results) {
            Write-Host "`n$($Result.Description) ($($Result.Endpoint)):" -ForegroundColor Yellow
            Write-Host "   Status: $($Result.Status)" -ForegroundColor $(if($Result.Status -like "*✅*") { "Green" } else { "Red" })
            Write-Host "   HTTP Status: $($Result.StatusCode)" -ForegroundColor White
            Write-Host "   Response Time: $($Result.ResponseTime)" -ForegroundColor White
            Write-Host "   Content Length: $($Result.ContentLength) bytes" -ForegroundColor White
            if ($Result.Details -and $Result.Details.Length -gt 0) {
                Write-Host "   Preview: $($Result.Details)" -ForegroundColor Gray
            }
        }
    }
}

function Show-QuickCommands {
    Write-Host "`n🎯 Quick Diagnostic Commands:" -ForegroundColor Cyan
    Write-Host "==============================" -ForegroundColor Cyan
    
    Write-Host "`n🔍 Application Status:" -ForegroundColor Yellow
    Write-Host "   Get-Process python* | Select-Object Name, Id, CPU, WorkingSet" -ForegroundColor White
    Write-Host "   netstat -ano | findstr :$Port" -ForegroundColor White
    Write-Host "   curl http://${HostName}:${Port}/health" -ForegroundColor White
    
    Write-Host "`n🌐 API Testing:" -ForegroundColor Yellow
    Write-Host "   Invoke-RestMethod -Uri 'http://${HostName}:${Port}/health'" -ForegroundColor White
    Write-Host "   Invoke-RestMethod -Uri 'http://${HostName}:${Port}/api/v1/status'" -ForegroundColor White
    Write-Host "   start http://${HostName}:${Port}/docs" -ForegroundColor White
    
    Write-Host "`n📊 Performance:" -ForegroundColor Yellow
    Write-Host "   # Simple load test" -ForegroundColor White
    Write-Host "   for (\$i=1; \$i -le 10; \$i++) { Invoke-RestMethod -Uri 'http://${HostName}:${Port}/health' }" -ForegroundColor White
    
    Write-Host "`n🔧 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   # Check logs (if running with Python)" -ForegroundColor White
    Write-Host "   python -m app.main" -ForegroundColor White
    Write-Host "   # Check port conflicts" -ForegroundColor White
    Write-Host "   Get-NetTCPConnection -LocalPort $Port" -ForegroundColor White
}

function Start-ContinuousMonitoring {
    Write-Status "🔄 Starting continuous monitoring (Ctrl+C to stop)..." "Info"
    
    while ($true) {
        Clear-Host
        Write-Host "🔍 Zeta Agent Health Monitor - $(Get-Date)" -ForegroundColor Cyan
        Write-Host "============================================" -ForegroundColor Cyan
        
        # Test port connectivity
        $PortOpen = Test-PortOpen -HostName $HostName -Port $Port
        if ($PortOpen) {
            Write-Status "✅ Port $Port is accessible" "Success"
            
            # Test endpoints
            $Results = Test-ApplicationEndpoints -BaseUrl "http://${HostName}:${Port}"
            Show-HealthSummary -Results $Results
        } else {
            Write-Status "❌ Port $Port is not accessible" "Error"
        }
        
        Test-ProcessHealth
        
        Write-Host "`nNext check in $Interval seconds..." -ForegroundColor Gray
        Start-Sleep $Interval
    }
}

# Main execution
Write-Status "🚀 Zeta Agent Health Check Starting..." "Info"
Write-Status "Target: http://${HostName}:${Port}" "Info"

try {
    if ($Continuous) {
        Start-ContinuousMonitoring
    } else {
        # Single check
        Write-Status "Testing port connectivity..." "Info"
        $PortOpen = Test-PortOpen -HostName $HostName -Port $Port
        
        if ($PortOpen) {
            Write-Status "✅ Port $Port is accessible" "Success"
            
            # Test all endpoints
            $Results = Test-ApplicationEndpoints -BaseUrl "http://${HostName}:${Port}"
            Show-HealthSummary -Results $Results
            
        } else {
            Write-Status "❌ Port $Port is not accessible on $HostName" "Error"
            Write-Status "Is the application running? Try: python -m app.main" "Info"
        }
        
        Test-ProcessHealth
        Show-QuickCommands
    }
    
    Write-Status "✅ Health check completed!" "Success"
    
} catch {
    Write-Status "❌ Error during health check: $($_.Exception.Message)" "Error"
    exit 1
}
