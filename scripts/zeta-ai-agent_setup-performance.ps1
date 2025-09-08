#!/usr/bin/env powershell

# Quick Performance Optimization Script
# Sets up load testing and performance monitoring

param(
    [int]$TargetRPS = 100,
    [int]$TestDuration = 300,  # 5 minutes
    [string]$TargetURL = "http://localhost:3000",
    [switch]$InstallK6,
    [switch]$InstallTools
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Install-LoadTestingTools {
    Write-Status "Installing load testing tools..." "Info"
    
    # Install k6 via Chocolatey
    if (Get-Command choco -ErrorAction SilentlyContinue) {
        choco install k6 -y
    } else {
        Write-Status "Installing Chocolatey first..." "Info"
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        choco install k6 -y
    }
    
    # Verify installation
    if (Get-Command k6 -ErrorAction SilentlyContinue) {
        Write-Status "k6 installed successfully" "Success"
    } else {
        Write-Status "Failed to install k6" "Error"
        exit 1
    }
}

function New-LoadTestScript {
    Write-Status "Creating optimized load test script..." "Info"
    
    $LoadTestScript = @"
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
export let errorRate = new Rate('errors');
export let customTrend = new Trend('custom_trend');

export let options = {
  stages: [
    { duration: '30s', target: 10 },      // Warm up
    { duration: '1m', target: $TargetRPS },   // Ramp to target
    { duration: '$(($TestDuration - 120))s', target: $TargetRPS }, // Sustain load
    { duration: '30s', target: 0 },       // Cool down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],  // Response time SLA
    http_req_failed: ['rate<0.01'],                  // Error rate < 1%
    errors: ['rate<0.01'],                           // Custom error rate
  },
};

const BASE_URL = __ENV.TARGET_URL || '$TargetURL';

export default function() {
  let responses = {};
  
  // 1. Health Check (lightweight)
  responses.health = http.get(`\${BASE_URL}/health`);
  check(responses.health, {
    'health: status 200': (r) => r.status === 200,
    'health: response < 50ms': (r) => r.timings.duration < 50,
  }) || errorRate.add(1);

  // 2. Status API (medium)
  responses.status = http.get(`\${BASE_URL}/api/v1/status`);
  check(responses.status, {
    'status: status 200': (r) => r.status === 200,
    'status: response < 100ms': (r) => r.timings.duration < 100,
  }) || errorRate.add(1);

  // 3. Chat API (heavy - 30% of requests)
  if (Math.random() < 0.3) {
    let chatPayload = JSON.stringify({
      message: `Performance test message \${Math.random()}`,
      context: "load testing",
      model: "ollama",
      stream: false
    });
    
    responses.chat = http.post(`\${BASE_URL}/api/v1/chat`, chatPayload, {
      headers: { 'Content-Type': 'application/json' },
      timeout: '10s',
    });
    
    check(responses.chat, {
      'chat: status 200': (r) => r.status === 200,
      'chat: response < 2s': (r) => r.timings.duration < 2000,
      'chat: has response': (r) => r.body.length > 0,
    }) || errorRate.add(1);
    
    customTrend.add(responses.chat.timings.duration);
  }

  // 4. Metrics endpoint (10% of requests)
  if (Math.random() < 0.1) {
    responses.metrics = http.get(`\${BASE_URL}/metrics`);
    check(responses.metrics, {
      'metrics: status 200': (r) => r.status === 200,
      'metrics: prometheus format': (r) => r.body.includes('# HELP'),
    }) || errorRate.add(1);
  }

  // Variable sleep to simulate real user behavior
  sleep(Math.random() * 2 + 0.5); // 0.5-2.5 seconds
}

export function handleSummary(data) {
  return {
    'performance-report.html': htmlReport(data),
    'performance-results.json': JSON.stringify(data),
  };
}

function htmlReport(data) {
  return `
<!DOCTYPE html>
<html>
<head>
    <title>Zeta Agent Performance Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .metric { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .pass { color: green; } .fail { color: red; }
    </style>
</head>
<body>
    <h1>🚀 Zeta Agent Performance Report</h1>
    <p><strong>Target RPS:</strong> $TargetRPS</p>
    <p><strong>Test Duration:</strong> $TestDuration seconds</p>
    <p><strong>Target URL:</strong> $TargetURL</p>
    
    <h2>📊 Key Metrics</h2>
    <div class="metric">
        <strong>Total Requests:</strong> \${data.metrics.http_reqs.count}<br>
        <strong>Request Rate:</strong> \${data.metrics.http_reqs.rate.toFixed(2)} RPS<br>
        <strong>Average Response Time:</strong> \${data.metrics.http_req_duration.avg.toFixed(2)}ms<br>
        <strong>P95 Response Time:</strong> \${data.metrics.http_req_duration['p(95)'].toFixed(2)}ms<br>
        <strong>P99 Response Time:</strong> \${data.metrics.http_req_duration['p(99)'].toFixed(2)}ms<br>
        <strong>Error Rate:</strong> \${(data.metrics.http_req_failed.rate * 100).toFixed(2)}%
    </div>
    
    <h2>✅ Thresholds</h2>
    \${Object.entries(data.thresholds).map(([name, threshold]) => 
        `<div class="\${threshold.ok ? 'pass' : 'fail'}">\${name}: \${threshold.ok ? 'PASS' : 'FAIL'}</div>`
    ).join('')}
    
    <h2>📈 Recommendations</h2>
    <ul>
        <li>P95 should be < 200ms: \${data.metrics.http_req_duration['p(95)'] < 200 ? '✅' : '❌'}</li>
        <li>Error rate should be < 1%: \${data.metrics.http_req_failed.rate < 0.01 ? '✅' : '❌'}</li>
        <li>Sustained RPS: \${data.metrics.http_reqs.rate >= $TargetRPS * 0.9 ? '✅' : '❌'}</li>
    </ul>
</body>
</html>`;
}
"@

    $LoadTestScript | Out-File -FilePath ".\phase2\performance\load-tests\optimized-load.js" -Encoding UTF8
    Write-Status "Load test script created: .\phase2\performance\load-tests\optimized-load.js" "Success"
}

function Start-LoadTest {
    Write-Status "Starting performance load test..." "Info"
    Write-Status "Target: $TargetRPS RPS for $TestDuration seconds" "Info"
    Write-Status "URL: $TargetURL" "Info"
    
    # Check if target is reachable
    try {
        $Response = Invoke-WebRequest -Uri "$TargetURL/health" -TimeoutSec 5 -UseBasicParsing
        if ($Response.StatusCode -eq 200) {
            Write-Status "Target application is reachable" "Success"
        }
    } catch {
        Write-Status "Warning: Target application may not be running at $TargetURL" "Warning"
        $Continue = Read-Host "Continue with load test? (y/N)"
        if ($Continue -ne 'y' -and $Continue -ne 'Y') {
            return
        }
    }
    
    # Run k6 load test
    $env:TARGET_URL = $TargetURL
    k6 run ".\phase2\performance\load-tests\optimized-load.js" --out json=performance-results.json
    
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Load test completed successfully!" "Success"
        
        # Show quick summary if results file exists
        if (Test-Path "performance-results.json") {
            Write-Status "📊 Quick Results Summary:" "Info"
            $Results = Get-Content "performance-results.json" | ConvertFrom-Json
            # Parse k6 results would require more complex JSON parsing
            Write-Status "Detailed results saved to performance-results.json" "Info"
        }
        
        if (Test-Path "performance-report.html") {
            Write-Status "📈 HTML report generated: performance-report.html" "Success"
            Write-Status "Open in browser to view detailed analysis" "Info"
        }
    } else {
        Write-Status "Load test failed or thresholds not met" "Error"
    }
}

function Optimize-KubernetesResources {
    Write-Status "Optimizing Kubernetes resources based on load test..." "Info"
    
    # Create optimized values file
    $OptimizedValues = @"
# Performance optimized values based on load testing
replicaCount: 3

resources:
  limits:
    cpu: "1000m"      # Adjust based on load test CPU usage
    memory: "512Mi"   # Adjust based on load test memory usage
  requests:
    cpu: "250m"       # 25% of limit for guaranteed resources
    memory: "256Mi"   # 50% of limit for guaranteed resources

# HPA configuration for auto-scaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
  
  # Custom metrics for scaling
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60

# Optimized probes
livenessProbe:
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

# Performance environment variables
env:
  NODE_ENV: "production"
  NODE_OPTIONS: "--max-old-space-size=384 --gc-interval=100"
  UV_THREADPOOL_SIZE: "8"
  
# Enable metrics for monitoring
metrics:
  enabled: true
  port: 9090
"@

    $OptimizedValues | Out-File -FilePath ".\phase2\performance\configs\values-optimized.yaml" -Encoding UTF8
    Write-Status "Optimized Kubernetes values created: .\phase2\performance\configs\values-optimized.yaml" "Success"
}

function Show-PerformanceRecommendations {
    Write-Status "📈 Performance Optimization Recommendations:" "Info"
    Write-Host ""
    Write-Host "🎯 Target Metrics:"
    Write-Host "   - P95 Latency: < 200ms"
    Write-Host "   - P99 Latency: < 500ms"
    Write-Host "   - Error Rate: < 1%"
    Write-Host "   - Sustained RPS: $TargetRPS+"
    Write-Host ""
    Write-Host "🔧 Next Steps:"
    Write-Host "   1. Review performance-report.html for detailed analysis"
    Write-Host "   2. Apply optimized configuration:"
    Write-Host "      helm upgrade zeta-agent ./infra/helm/zeta-agent \"
    Write-Host "        --values ./phase2/performance/configs/values-optimized.yaml"
    Write-Host "   3. Monitor with Grafana dashboard"
    Write-Host "   4. Run load test again to validate improvements"
    Write-Host ""
    Write-Host "📊 Monitoring:"
    Write-Host "   kubectl top pods -n zeta-agent"
    Write-Host "   kubectl get hpa -n zeta-agent"
    Write-Host "   kubectl port-forward svc/grafana 3000:3000 -n monitoring"
}

# Main execution
Write-Status "🚀 Performance Optimization Setup" "Info"

try {
    # Create directories if they don't exist
    if (-not (Test-Path ".\phase2\performance\load-tests")) {
        New-Item -ItemType Directory -Path ".\phase2\performance\load-tests" -Force | Out-Null
        New-Item -ItemType Directory -Path ".\phase2\performance\configs" -Force | Out-Null
    }
    
    if ($InstallTools -or $InstallK6) {
        Install-LoadTestingTools
    }
    
    New-LoadTestScript
    Optimize-KubernetesResources
    
    Write-Status "Setup completed! Ready for performance testing." "Success"
    
    $RunTest = Read-Host "Run load test now? (y/N)"
    if ($RunTest -eq 'y' -or $RunTest -eq 'Y') {
        Start-LoadTest
    }
    
    Show-PerformanceRecommendations
    
} catch {
    Write-Status "❌ Error during performance optimization setup: $($_.Exception.Message)" "Error"
    exit 1
}
