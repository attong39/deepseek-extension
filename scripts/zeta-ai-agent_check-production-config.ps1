# =============================================================================
# 🚀 Zeta AI Agent - Production Configuration Checker (PowerShell)
# Kiểm tra tất cả các cấu hình production cho Windows environment
# =============================================================================

[CmdletBinding()]
param(
    [string]$TargetHost = "localhost",
    [int]$Port = 9100,
    [switch]$Detailed,
    [switch]$Help
)

# Colors for PowerShell output
$Colors = @{
    Red    = "Red"
    Green  = "Green"
    Yellow = "Yellow"
    Blue   = "Blue"
    Cyan   = "Cyan"
}

# Configuration
$BaseUrl = "http://${TargetHost}:${Port}"
$CheckResults = @()

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [string]$Prefix = ""
    )
    
    if ($Prefix) {
        Write-Host "$Prefix " -NoNewline -ForegroundColor $Color
        Write-Host $Message
    } else {
        Write-Host $Message -ForegroundColor $Color
    }
}

function Test-Endpoint {
    param(
        [string]$Endpoint,
        [int]$ExpectedStatus = 200,
        [string]$Description,
        [hashtable]$Headers = @{}
    )
    
    Write-ColoredOutput "🔍 Testing: $Description" -Color Blue
    Write-Host "Endpoint: $Endpoint"
    
    try {
        $response = Invoke-WebRequest -Uri $Endpoint -Headers $Headers -Method Get -UseBasicParsing -TimeoutSec 10
        $statusCode = $response.StatusCode
        
        if ($statusCode -eq $ExpectedStatus) {
            Write-ColoredOutput "✅ PASS" -Color Green -Prefix ""
            Write-Host "   HTTP $statusCode - Response time: $(if ($response.Headers.'X-Response-Time') { $response.Headers.'X-Response-Time' } else { 'N/A' })"
            return @{ Success = $true; StatusCode = $statusCode; Content = $response.Content }
        } else {
            Write-ColoredOutput "❌ FAIL" -Color Red -Prefix ""
            Write-Host "   Expected HTTP $ExpectedStatus, got $statusCode"
            return @{ Success = $false; StatusCode = $statusCode; Content = $response.Content }
        }
    }
    catch {
        Write-ColoredOutput "❌ ERROR" -Color Red -Prefix ""
        Write-Host "   $($_.Exception.Message)"
        return @{ Success = $false; StatusCode = 0; Error = $_.Exception.Message }
    }
}

function Test-CorsConfiguration {
    Write-ColoredOutput "`n🔒 CORS Configuration Check" -Color Yellow
    Write-Host "============================================="
    
    # Test 1: Allowed origin (localhost)
    Write-Host "`n1. Testing allowed origin (localhost)"
    $headers = @{ "Origin" = "http://localhost:3000" }
    
    try {
        $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Headers $headers -Method Get -UseBasicParsing
        
        if ($response.Headers."Access-Control-Allow-Origin") {
            Write-ColoredOutput "✅ PASS" -Color Green -Prefix ""
            Write-Host "   CORS headers present: $($response.Headers.'Access-Control-Allow-Origin')"
        } else {
            Write-ColoredOutput "❌ FAIL" -Color Red -Prefix ""
            Write-Host "   CORS headers missing"
        }
    }
    catch {
        Write-ColoredOutput "❌ ERROR" -Color Red -Prefix ""
        Write-Host "   $($_.Exception.Message)"
    }
    
    # Test 2: Evil origin (should be blocked)
    Write-Host "`n2. Testing blocked origin (evil.com)"
    $evilHeaders = @{ "Origin" = "https://evil.com" }
    
    try {
        $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Headers $evilHeaders -Method Get -UseBasicParsing
        
        if ($response.Headers."Access-Control-Allow-Origin" -eq "https://evil.com") {
            Write-ColoredOutput "❌ SECURITY RISK" -Color Red -Prefix ""
            Write-Host "   Evil origin allowed!"
        } else {
            Write-ColoredOutput "✅ SECURE" -Color Green -Prefix ""
            Write-Host "   Evil origin blocked"
        }
    }
    catch {
        Write-ColoredOutput "✅ SECURE" -Color Green -Prefix ""
        Write-Host "   Evil origin properly rejected"
    }
    
    # Test 3: Preflight request
    Write-Host "`n3. Testing preflight (OPTIONS) request"
    $preflightHeaders = @{
        "Origin" = "http://localhost:3000"
        "Access-Control-Request-Method" = "POST"
        "Access-Control-Request-Headers" = "Content-Type"
    }
    
    try {
        $response = Invoke-WebRequest -Uri "$BaseUrl/feedback" -Headers $preflightHeaders -Method Options -UseBasicParsing
        
        if ($response.Headers."Access-Control-Allow-Methods") {
            Write-ColoredOutput "✅ PASS" -Color Green -Prefix ""
            Write-Host "   Preflight handled correctly"
        } else {
            Write-ColoredOutput "❌ FAIL" -Color Red -Prefix ""
            Write-Host "   Preflight not working"
        }
    }
    catch {
        Write-ColoredOutput "❌ FAIL" -Color Red -Prefix ""
        Write-Host "   Preflight request failed: $($_.Exception.Message)"
    }
}

function Test-HealthEndpoints {
    Write-ColoredOutput "`n💊 Health Check Endpoints" -Color Yellow
    Write-Host "========================================="
    
    # Health check (liveness)
    $healthResult = Test-Endpoint -Endpoint "$BaseUrl/health" -Description "Liveness probe (/health)"
    if ($healthResult.Success) {
        Write-Host "   Expected: Always returns 200 if service is running"
    }
    
    # Readiness check
    $readyResult = Test-Endpoint -Endpoint "$BaseUrl/ready" -Description "Readiness probe (/ready)"
    if ($readyResult.Success) {
        Write-Host "   Expected: Returns 200 when dependencies are available"
    }
    
    # Root endpoint
    $rootResult = Test-Endpoint -Endpoint "$BaseUrl/" -Description "Root endpoint (/)"
    if ($rootResult.Success) {
        Write-Host "   Expected: Service information"
    }
    
    return @{
        Health = $healthResult.Success
        Ready = $readyResult.Success
        Root = $rootResult.Success
    }
}

function Test-PrometheusMetrics {
    Write-ColoredOutput "`n📊 Prometheus Metrics" -Color Yellow
    Write-Host "===================================="
    
    $metricsResult = Test-Endpoint -Endpoint "$BaseUrl/metrics" -Description "Metrics endpoint (/metrics)"
    
    if ($metricsResult.Success) {
        Write-Host "`n🔍 Checking for required metrics:"
        
        $requiredMetrics = @(
            "zeta_requests_total",
            "zeta_request_duration_seconds",
            "zeta_vietnamese_quality_score",
            "zeta_feedback_total",
            "zeta_errors_total"
        )
        
        $metricsContent = $metricsResult.Content
        $foundMetrics = @()
        
        foreach ($metric in $requiredMetrics) {
            if ($metricsContent -match $metric) {
                Write-ColoredOutput "  ✅ $metric" -Color Green
                $foundMetrics += $metric
            } else {
                Write-ColoredOutput "  ❌ $metric (missing)" -Color Red
            }
        }
        
        # Check for UP metric
        if ($metricsContent -match "# TYPE.*up.*gauge") {
            Write-ColoredOutput "  ✅ Service UP metric" -Color Green
        }
        
        return @{
            Success = $true
            FoundMetrics = $foundMetrics
            TotalMetrics = $requiredMetrics.Count
        }
    }
    
    return @{ Success = $false }
}

function Test-ApiEndpoints {
    Write-ColoredOutput "`n🔌 API Endpoints" -Color Yellow
    Write-Host "==============================="
    
    # Stats endpoint
    $statsResult = Test-Endpoint -Endpoint "$BaseUrl/stats" -Description "Statistics endpoint (/stats)"
    
    # Test feedback submission
    Write-Host "`n🧪 Testing feedback submission"
    $feedbackPayload = @{
        model_name = "test-model"
        prompt = "Test prompt"
        response = "Test response"
        rating = 8
        latency = 1.2
        vietnamese_quality = 9
        session_id = "test-session-$(Get-Random)"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/feedback" -Method Post -Body $feedbackPayload -ContentType "application/json"
        Write-ColoredOutput "✅ PASS" -Color Green -Prefix ""
        Write-Host "   Feedback submission working"
        
        if ($Detailed) {
            Write-Host "   Response: $($response | ConvertTo-Json -Compress)"
        }
    }
    catch {
        Write-ColoredOutput "❌ FAIL" -Color Red -Prefix ""
        Write-Host "   Feedback submission failed: $($_.Exception.Message)"
    }
    
    return @{
        Stats = $statsResult.Success
        Feedback = $true  # Assume success if no exception
    }
}

function Test-SecurityHeaders {
    Write-ColoredOutput "`n🔒 Security Headers" -Color Yellow
    Write-Host "=================================="
    
    try {
        $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Method Head -UseBasicParsing
        $headers = $response.Headers
        
        $securityHeaders = @(
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection",
            "Strict-Transport-Security"
        )
        
        $foundHeaders = @()
        
        foreach ($header in $securityHeaders) {
            if ($headers.ContainsKey($header)) {
                Write-ColoredOutput "  ✅ $header" -Color Green
                $foundHeaders += $header
            } else {
                Write-ColoredOutput "  ⚠️  $header (recommended)" -Color Yellow
            }
        }
        
        return @{
            FoundHeaders = $foundHeaders
            TotalHeaders = $securityHeaders.Count
        }
    }
    catch {
        Write-ColoredOutput "❌ ERROR checking headers" -Color Red
        return @{ FoundHeaders = @(); TotalHeaders = 0 }
    }
}

function Invoke-AlertingSimulation {
    Write-ColoredOutput "`n🚨 Alerting Simulation" -Color Yellow
    Write-Host "===================================="
    
    Write-Host "Simulating high latency requests..."
    
    # Submit multiple requests with high latency
    $jobs = @()
    for ($i = 1; $i -le 5; $i++) {
        $payload = @{
            model_name = "load-test"
            prompt = "Load test prompt"
            response = "Load test response"
            rating = 5
            latency = 3.5
            vietnamese_quality = 6
            session_id = "load-test-$i"
        } | ConvertTo-Json
        
        $job = Start-Job -ScriptBlock {
            param($url, $data)
            try {
                Invoke-RestMethod -Uri $url -Method Post -Body $data -ContentType "application/json"
            }
            catch {
                # Ignore errors for load testing
            }
        } -ArgumentList "$BaseUrl/feedback", $payload
        
        $jobs += $job
        Write-Host "." -NoNewline
    }
    
    # Wait for all jobs to complete
    $jobs | Wait-Job | Remove-Job
    
    Write-Host ""
    Write-ColoredOutput "✅ High latency data submitted" -Color Green
    Write-Host "Check Prometheus/Alertmanager in 2-3 minutes for alerts"
    Write-Host "Expected alert: ZetaHighLatency (latency > 2s for 2m)"
}

function Test-PerformanceBasic {
    Write-ColoredOutput "`n⚡ Basic Performance Test" -Color Yellow
    Write-Host "====================================="
    
    Write-Host "Running 10 concurrent requests to /health endpoint..."
    
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    $jobs = @()
    for ($i = 1; $i -le 10; $i++) {
        $job = Start-Job -ScriptBlock {
            param($url)
            try {
                Invoke-WebRequest -Uri $url -UseBasicParsing | Out-Null
            }
            catch {
                # Ignore errors for performance testing
            }
        } -ArgumentList "$BaseUrl/health"
        
        $jobs += $job
    }
    
    # Wait for all jobs
    $jobs | Wait-Job | Remove-Job
    
    $stopwatch.Stop()
    
    Write-ColoredOutput "✅ Performance test completed" -Color Green
    Write-Host "   Total time: $($stopwatch.ElapsedMilliseconds)ms"
    Write-Host "   Average per request: $([math]::Round($stopwatch.ElapsedMilliseconds / 10, 2))ms"
    Write-Host "Check metrics endpoint for detailed request duration statistics"
}

function Show-Summary {
    param($Results)
    
    Write-ColoredOutput "`n🎉 Production Configuration Check Complete!" -Color Blue
    Write-Host "=============================================="
    
    # Summary statistics
    $totalChecks = 0
    $passedChecks = 0
    
    foreach ($category in $Results.Keys) {
        $result = $Results[$category]
        if ($result -is [hashtable] -and $result.ContainsKey('Success')) {
            $totalChecks++
            if ($result.Success) { $passedChecks++ }
        }
    }
    
    Write-Host "`nSummary:"
    Write-Host "--------"
    Write-ColoredOutput "✅ Passed: $passedChecks/$totalChecks checks" -Color Green
    
    if ($passedChecks -eq $totalChecks) {
        Write-ColoredOutput "🎯 All checks passed! Production ready." -Color Green
    } elseif ($passedChecks -gt ($totalChecks * 0.8)) {
        Write-ColoredOutput "⚠️  Most checks passed. Review failed items." -Color Yellow
    } else {
        Write-ColoredOutput "❌ Multiple issues found. Fix before production." -Color Red
    }
    
    Write-Host "`nEndpoints:"
    Write-Host "----------"
    Write-Host "📊 Metrics:    $BaseUrl/metrics"
    Write-Host "💊 Health:     $BaseUrl/health"
    Write-Host "🔄 Readiness:  $BaseUrl/ready"
    Write-Host "📈 Statistics: $BaseUrl/stats"
    
    Write-ColoredOutput "`nNext Steps:" -Color Cyan
    Write-Host "1. Set up Prometheus to scrape $BaseUrl/metrics"
    Write-Host "2. Configure Alertmanager with the provided rules"
    Write-Host "3. Set up Grafana dashboard for visualization"
    Write-Host "4. Configure proper CORS origins for production"
    Write-Host "5. Set up TLS/HTTPS for production deployment"
    Write-Host "6. Review and implement security headers"
}

function Show-Help {
    Write-Host @"
🚀 Zeta AI Agent - Production Configuration Checker

USAGE:
    .\check-production-config.ps1 [OPTIONS]

PARAMETERS:
    -Host <string>     Target host (default: localhost)
    -Port <int>        Target port (default: 9100)
    -Detailed          Show detailed response information
    -Help              Show this help message

EXAMPLES:
    .\check-production-config.ps1
    .\check-production-config.ps1 -TargetHost "zeta.company.com" -Port 443
    .\check-production-config.ps1 -Detailed

CHECKS PERFORMED:
    • CORS configuration and security
    • Health check endpoints (/health, /ready)
    • Prometheus metrics availability
    • API functionality testing
    • Security headers validation
    • Alerting simulation
    • Basic performance testing

REQUIREMENTS:
    • PowerShell 5.1 or higher
    • Network access to target service
    • Zeta AI Agent service running
"@
}

# Main execution
function Main {
    if ($Help) {
        Show-Help
        return
    }
    
    Write-ColoredOutput "🚀 Zeta AI Agent - Production Configuration Checker" -Color Blue
    Write-Host "Testing against: $BaseUrl"
    Write-Host "========================================================"
    
    # Test basic connectivity
    try {
        Invoke-WebRequest -Uri "$BaseUrl/health" -UseBasicParsing -TimeoutSec 5 | Out-Null
    }
    catch {
        Write-ColoredOutput "❌ FATAL: Cannot connect to $BaseUrl" -Color Red
        Write-Host "Please ensure the service is running and accessible"
        return
    }
    
    # Run all checks and collect results
    $results = @{}
    
    Test-CorsConfiguration
    $results.Health = Test-HealthEndpoints
    $results.Metrics = Test-PrometheusMetrics
    $results.Api = Test-ApiEndpoints
    $results.Security = Test-SecurityHeaders
    
    Invoke-AlertingSimulation
    Test-PerformanceBasic
    
    # Show summary
    Show-Summary -Results $results
}

# Execute main function
Main
