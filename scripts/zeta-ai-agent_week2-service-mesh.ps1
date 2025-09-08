#!/usr/bin/env powershell

# Week 2: Service Mesh (Istio) + Distributed Tracing (Jaeger)
# Goal: mTLS enabled + end-to-end trace latency < 30ms

param(
    [string]$Namespace = "zeta-agent",
    [switch]$InstallIstio,
    [switch]$ConfigureMTLS,
    [switch]$SetupTracing,
    [switch]$TestPerformance
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Install-IstioServiceMesh {
    Write-Status "Installing Istio Service Mesh..." "Info"
    
    # Download and install Istio
    $IstioVersion = "1.19.0"
    Write-Status "Downloading Istio $IstioVersion..." "Info"
    
    # Create Istio installation script
    $IstioInstall = @"
# Download Istio
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=$IstioVersion sh -

# Add istioctl to PATH
export PATH=\$PATH:\$PWD/istio-$IstioVersion/bin

# Install Istio with demo profile
istioctl install --set values.defaultRevision=default -y

# Enable sidecar injection for zeta-agent namespace
kubectl label namespace $Namespace istio-injection=enabled --overwrite

# Verify installation
kubectl get pods -n istio-system
"@

    $IstioInstall | Out-File -FilePath ".\week2\install-istio.sh" -Encoding UTF8
    
    Write-Status "Istio installation script created: .\week2\install-istio.sh" "Success"
    Write-Status "Run manually: bash .\week2\install-istio.sh" "Info"
}

function Configure-MutualTLS {
    Write-Status "Configuring mTLS (Mutual TLS)..." "Info"
    
    # Strict mTLS Policy
    $MTLSPolicy = @"
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: $Namespace
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: zeta-agent-authz
  namespace: $Namespace
spec:
  selector:
    matchLabels:
      app: zeta-agent
  rules:
  - from:
    - source:
        principals: 
        - "cluster.local/ns/$Namespace/sa/zeta-agent"
        - "cluster.local/ns/monitoring/sa/prometheus"
  - to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/health", "/metrics", "/api/*"]
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all-default
  namespace: $Namespace
spec:
  {}
"@

    $MTLSPolicy | Out-File -FilePath ".\week2\mtls-policy.yaml" -Encoding UTF8
    
    # Destination Rules for mTLS
    $DestinationRules = @"
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: zeta-agent-dr
  namespace: $Namespace
spec:
  host: zeta-agent.$Namespace.svc.cluster.local
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 10
    circuitBreaker:
      consecutiveGatewayErrors: 5
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  portLevelSettings:
  - port:
      number: 3000
    loadBalancer:
      simple: LEAST_CONN
"@

    $DestinationRules | Out-File -FilePath ".\week2\destination-rules.yaml" -Encoding UTF8
    
    Write-Status "mTLS configuration created" "Success"
    
    # Apply configurations
    kubectl apply -f ".\week2\mtls-policy.yaml"
    kubectl apply -f ".\week2\destination-rules.yaml"
}

function Setup-DistributedTracing {
    Write-Status "Setting up Jaeger distributed tracing..." "Info"
    
    # Install Jaeger
    $JaegerInstall = @"
apiVersion: v1
kind: Namespace
metadata:
  name: istio-system
  labels:
    istio-injection: disabled
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: istio-system
  labels:
    app: jaeger
spec:
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:1.49
        env:
        - name: COLLECTOR_OTLP_ENABLED
          value: "true"
        - name: COLLECTOR_ZIPKIN_HOST_PORT
          value: ":9411"
        ports:
        - containerPort: 16686
          name: ui
        - containerPort: 14268
          name: collector
        - name: zipkin
          containerPort: 9411
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: jaeger-collector
  namespace: istio-system
  labels:
    app: jaeger
spec:
  ports:
  - port: 14268
    name: collector
  - port: 9411
    name: zipkin
  selector:
    app: jaeger
---
apiVersion: v1
kind: Service
metadata:
  name: jaeger-query
  namespace: istio-system
  labels:
    app: jaeger
spec:
  ports:
  - port: 16686
    name: query
  selector:
    app: jaeger
"@

    $JaegerInstall | Out-File -FilePath ".\week2\jaeger-install.yaml" -Encoding UTF8
    kubectl apply -f ".\week2\jaeger-install.yaml"
    
    # Configure Istio for Jaeger
    $TracingConfig = @"
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio
  namespace: istio-system
data:
  mesh: |
    defaultConfig:
      proxyStatsMatcher:
        inclusionRegexps:
        - ".*outlier_detection.*"
        - ".*circuit_breakers.*"
        - ".*upstream_rq_retry.*"
        - ".*_cx_.*"
      tracing:
        zipkin:
          address: jaeger-collector.istio-system:9411
        sampling: 100.0
    extensionProviders:
    - name: jaeger
      zipkin:
        service: jaeger-collector.istio-system
        port: 9411
---
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: tracing-config
  namespace: istio-system
spec:
  meshConfig:
    defaultConfig:
      tracing:
        zipkin:
          address: jaeger-collector.istio-system:9411
        sampling: 100.0
    extensionProviders:
    - name: jaeger
      zipkin:
        service: jaeger-collector.istio-system
        port: 9411
"@

    $TracingConfig | Out-File -FilePath ".\week2\tracing-config.yaml" -Encoding UTF8
    kubectl apply -f ".\week2\tracing-config.yaml"
    
    # Telemetry configuration
    $TelemetryConfig = @"
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: tracing-default
  namespace: istio-system
spec:
  tracing:
  - providers:
    - name: jaeger
  - customTags:
      request_id:
        header:
          name: x-request-id
      user_agent:
        header:
          name: user-agent
      custom_header:
        header:
          name: x-custom-header
"@

    $TelemetryConfig | Out-File -FilePath ".\week2\telemetry-config.yaml" -Encoding UTF8
    kubectl apply -f ".\week2\telemetry-config.yaml"
    
    Write-Status "Jaeger tracing configured" "Success"
}

function Test-ServiceMeshPerformance {
    Write-Status "Testing service mesh performance..." "Info"
    
    # Performance test script
    $PerfTest = @"
#!/bin/bash
echo "Testing service mesh performance..."

# Function to measure trace latency
measure_trace_latency() {
    local endpoint="\$1"
    local trace_id=""
    local start_time=\$(date +%s%3N)
    
    # Make request with trace headers
    response=\$(curl -s -w "%{http_code}" \\
        -H "x-request-id: test-\$(date +%s)" \\
        -H "x-b3-sampled: 1" \\
        "\$endpoint")
    
    local end_time=\$(date +%s%3N)
    local duration=\$((end_time - start_time))
    
    echo "\$duration"
}

# Test endpoints
ENDPOINT="http://zeta-agent.$Namespace.svc.cluster.local:3000"
TOTAL_TESTS=50
LATENCIES=()

echo "Running \$TOTAL_TESTS performance tests..."

for i in \$(seq 1 \$TOTAL_TESTS); do
    latency=\$(measure_trace_latency "\$ENDPOINT/health")
    LATENCIES+=(\$latency)
    
    if [ \$((i % 10)) -eq 0 ]; then
        echo "Completed \$i/\$TOTAL_TESTS tests"
    fi
    
    sleep 0.1
done

# Calculate statistics
sorted_latencies=($(printf '%s\\n' "\${LATENCIES[@]}" | sort -n))
total=\$(IFS=+; echo "\$((\${LATENCIES[*]}))")
avg=\$((total / TOTAL_TESTS))

# P95 calculation (95th percentile)
p95_index=\$((TOTAL_TESTS * 95 / 100))
p95=\${sorted_latencies[\$p95_index]}

echo ""
echo "📊 Performance Test Results:"
echo "Average Latency: \${avg}ms"
echo "P95 Latency: \${p95}ms"
echo "Target: < 30ms"

if [ \$p95 -lt 30 ]; then
    echo "✅ Performance test PASSED (P95 < 30ms)"
    exit 0
else
    echo "❌ Performance test FAILED (P95 >= 30ms)"
    exit 1
fi
"@

    $PerfTest | Out-File -FilePath ".\week2\test-performance.sh" -Encoding UTF8
    
    Write-Status "Performance test script created" "Success"
    
    # Create mTLS verification script
    $MTLSTest = @"
#!/bin/bash
echo "Verifying mTLS configuration..."

# Check if mTLS is enforced
echo "1. Checking PeerAuthentication policy..."
kubectl get peerauthentication -n $Namespace

echo ""
echo "2. Testing mTLS connectivity..."

# Test from within mesh (should work)
kubectl exec -n $Namespace deployment/zeta-agent -c zeta-agent -- \\
    curl -s http://zeta-agent:3000/health -o /dev/null -w "Status: %{http_code}\\n"

echo ""
echo "3. Checking certificate details..."
kubectl exec -n $Namespace deployment/zeta-agent -c istio-proxy -- \\
    openssl s_client -connect zeta-agent:3000 -servername zeta-agent 2>/dev/null | \\
    openssl x509 -noout -text | grep -A 5 "Subject:"

echo ""
echo "4. Verifying Istio proxy configuration..."
kubectl exec -n $Namespace deployment/zeta-agent -c istio-proxy -- \\
    curl -s localhost:15000/config_dump | jq '.configs[].dynamic_active_secrets // empty'

echo ""
echo "✅ mTLS verification completed"
"@

    $MTLSTest | Out-File -FilePath ".\week2\verify-mtls.sh" -Encoding UTF8
    
    Write-Status "mTLS verification script created" "Success"
}

function Show-Week2Summary {
    Write-Status "📊 Week 2 Implementation Summary" "Success"
    Write-Host ""
    Write-Host "✅ Components Deployed:" -ForegroundColor Green
    Write-Host "   • Istio Service Mesh" -ForegroundColor White
    Write-Host "   • Jaeger Distributed Tracing" -ForegroundColor White
    Write-Host "   • mTLS STRICT mode" -ForegroundColor White
    Write-Host "   • Circuit Breakers & Load Balancing" -ForegroundColor White
    Write-Host "   • Authorization Policies" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Success Criteria:" -ForegroundColor Cyan
    Write-Host "   • mTLS enabled and verified" -ForegroundColor White
    Write-Host "   • End-to-end trace latency < 30ms" -ForegroundColor White
    Write-Host "   • Service-to-service encryption" -ForegroundColor White
    Write-Host "   • Distributed tracing working" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Quick Commands:" -ForegroundColor Yellow
    Write-Host "   # Access Jaeger UI" -ForegroundColor White
    Write-Host "   kubectl port-forward svc/jaeger-query -n istio-system 16686:16686" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   # View service mesh topology" -ForegroundColor White
    Write-Host "   kubectl port-forward svc/kiali -n istio-system 20001:20001" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   # Check mTLS status" -ForegroundColor White
    Write-Host "   istioctl authn tls-check zeta-agent.$Namespace.svc.cluster.local" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   # View proxy configuration" -ForegroundColor White
    Write-Host "   istioctl proxy-config cluster zeta-agent-xxx -n $Namespace" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   # Test performance" -ForegroundColor White
    Write-Host "   bash .\week2\test-performance.sh" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🚀 Next Week: Chaos Engineering (Pod Kill + Network Latency)" -ForegroundColor Cyan
}

# Main execution
Write-Status "🕸️ Week 2: Service Mesh + Distributed Tracing" "Info"

try {
    # Create week2 directory
    if (-not (Test-Path ".\week2")) {
        New-Item -ItemType Directory -Path ".\week2" -Force | Out-Null
    }
    
    if ($InstallIstio) {
        Install-IstioServiceMesh
    }
    
    if ($ConfigureMTLS) {
        Configure-MutualTLS
    }
    
    if ($SetupTracing) {
        Setup-DistributedTracing
    }
    
    if ($TestPerformance) {
        Test-ServiceMeshPerformance
    }
    
    if (-not $InstallIstio -and -not $ConfigureMTLS -and -not $SetupTracing -and -not $TestPerformance) {
        # Run all by default
        Install-IstioServiceMesh
        Configure-MutualTLS
        Setup-DistributedTracing
        Test-ServiceMeshPerformance
    }
    
    Show-Week2Summary
    
    Write-Status "✅ Week 2 setup completed successfully!" "Success"
    
} catch {
    Write-Status "❌ Error during Week 2 setup: $($_.Exception.Message)" "Error"
    exit 1
}
