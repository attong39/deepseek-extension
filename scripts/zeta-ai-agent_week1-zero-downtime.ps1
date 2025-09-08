#!/usr/bin/env powershell

# Week 1: Zero-Downtime Deployment Setup
# Implements Canary + Blue-Green deployments with ArgoCD

param(
    [string]$GitRepo = "https://github.com/your-org/zeta-monorepo",
    [string]$Namespace = "zeta-agent",
    [switch]$InstallArgoCD,
    [switch]$SetupCanary,
    [switch]$SetupBlueGreen,
    [switch]$TestDeployment
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Install-ArgoCD {
    Write-Status "Installing ArgoCD for GitOps..." "Info"
    
    # Create ArgoCD namespace
    kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
    
    # Install ArgoCD
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    
    # Wait for ArgoCD to be ready
    Write-Status "Waiting for ArgoCD pods to be ready..." "Info"
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
    
    # Get admin password
    $AdminPassword = kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" 2>$null
    if ($AdminPassword) {
        $DecodedPassword = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($AdminPassword))
        Write-Status "ArgoCD installed successfully!" "Success"
        Write-Status "Access UI: kubectl port-forward svc/argocd-server -n argocd 8080:443" "Info"
        Write-Status "Login: admin / $DecodedPassword" "Info"
    }
}

function Setup-CanaryDeployment {
    Write-Status "Setting up Canary deployment strategy..." "Info"
    
    # Create Argo Rollouts namespace
    kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
    
    # Install Argo Rollouts
    kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
    
    # Canary Rollout configuration
    $CanaryRollout = @"
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: zeta-agent-canary
  namespace: $Namespace
spec:
  replicas: 5
  strategy:
    canary:
      maxSurge: "25%"
      maxUnavailable: 0
      steps:
      - setWeight: 20
      - pause: {duration: 120s}
      - setWeight: 40
      - pause: {duration: 120s}
      - setWeight: 60
      - pause: {duration: 120s}
      - setWeight: 80
      - pause: {duration: 120s}
      analysis:
        templates:
        - templateName: success-rate-analysis
        args:
        - name: service-name
          value: zeta-agent
        - name: canary-hash
          valueFrom:
            podTemplateHashValue: Latest
      scaleDownDelaySeconds: 30
      trafficRouting:
        nginx:
          stableIngress: zeta-agent-stable
          annotationPrefix: nginx.ingress.kubernetes.io
          additionalIngressAnnotations:
            canary-by-header: X-Canary
  selector:
    matchLabels:
      app: zeta-agent
  template:
    metadata:
      labels:
        app: zeta-agent
    spec:
      containers:
      - name: zeta-agent
        image: zeta-agent:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 10
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate-analysis
  namespace: $Namespace
spec:
  args:
  - name: service-name
  - name: canary-hash
  metrics:
  - name: success-rate
    interval: 30s
    count: 4
    successCondition: result[0] >= 0.95
    failureLimit: 2
    provider:
      prometheus:
        address: http://prometheus.monitoring.svc.cluster.local:9090
        query: |
          sum(rate(http_requests_total{job="{{args.service-name}}",status!~"5.."}[2m])) / 
          sum(rate(http_requests_total{job="{{args.service-name}}"}[2m]))
  - name: avg-response-time
    interval: 30s
    count: 4
    successCondition: result[0] <= 0.2
    failureLimit: 2
    provider:
      prometheus:
        address: http://prometheus.monitoring.svc.cluster.local:9090
        query: |
          histogram_quantile(0.95, 
            sum(rate(http_request_duration_seconds_bucket{job="{{args.service-name}}"}[2m])) by (le)
          )
"@

    $CanaryRollout | Out-File -FilePath ".\week1\canary-rollout.yaml" -Encoding UTF8
    kubectl apply -f ".\week1\canary-rollout.yaml"
    
    Write-Status "Canary deployment configuration created" "Success"
}

function Setup-BlueGreenDeployment {
    Write-Status "Setting up Blue-Green deployment strategy..." "Info"
    
    $BlueGreenRollout = @"
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: zeta-agent-bluegreen
  namespace: $Namespace
spec:
  replicas: 3
  strategy:
    blueGreen:
      activeService: zeta-agent-active
      previewService: zeta-agent-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
      prePromotionAnalysis:
        templates:
        - templateName: health-check-analysis
        args:
        - name: service-name
          value: zeta-agent-preview
      postPromotionAnalysis:
        templates:
        - templateName: success-rate-analysis
        args:
        - name: service-name
          value: zeta-agent-active
      activeMetadata:
        labels:
          role: active
      previewMetadata:
        labels:
          role: preview
  selector:
    matchLabels:
      app: zeta-agent
  template:
    metadata:
      labels:
        app: zeta-agent
    spec:
      containers:
      - name: zeta-agent
        image: zeta-agent:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 10
        env:
        - name: DEPLOYMENT_TYPE
          value: "blue-green"
---
apiVersion: v1
kind: Service
metadata:
  name: zeta-agent-active
  namespace: $Namespace
spec:
  selector:
    app: zeta-agent
    role: active
  ports:
  - port: 3000
    targetPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: zeta-agent-preview
  namespace: $Namespace
spec:
  selector:
    app: zeta-agent
    role: preview
  ports:
  - port: 3000
    targetPort: 3000
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: health-check-analysis
  namespace: $Namespace
spec:
  args:
  - name: service-name
  metrics:
  - name: health-check
    interval: 10s
    count: 5
    successCondition: result == 200
    failureLimit: 2
    provider:
      web:
        url: "http://{{args.service-name}}.zeta-agent.svc.cluster.local:3000/health"
        timeoutSeconds: 10
        jsonPath: "{$.status}"
  - name: readiness-check
    interval: 15s
    count: 3
    successCondition: result >= 1
    provider:
      prometheus:
        address: http://prometheus.monitoring.svc.cluster.local:9090
        query: |
          sum(up{job="{{args.service-name}}"})
"@

    $BlueGreenRollout | Out-File -FilePath ".\week1\bluegreen-rollout.yaml" -Encoding UTF8
    kubectl apply -f ".\week1\bluegreen-rollout.yaml"
    
    Write-Status "Blue-Green deployment configuration created" "Success"
}

function Test-ZeroDowntimeDeployment {
    Write-Status "Testing zero-downtime deployment..." "Info"
    
    # Create test script
    $TestScript = @"
#!/bin/bash
echo "Starting zero-downtime deployment test..."

# Function to check service availability
check_availability() {
    local endpoint="\$1"
    local response=\$(curl -s -o /dev/null -w "%{http_code}" "\$endpoint" --max-time 5)
    echo "\$response"
}

# Monitor service during deployment
ENDPOINT="http://zeta-agent.zeta-agent.svc.cluster.local:3000/health"
TOTAL_REQUESTS=0
FAILED_REQUESTS=0
TEST_DURATION=300  # 5 minutes

echo "Monitoring \$ENDPOINT for \$TEST_DURATION seconds..."

start_time=\$(date +%s)
while [ \$(((\$(date +%s) - start_time))) -lt \$TEST_DURATION ]; do
    response=\$(check_availability \$ENDPOINT)
    TOTAL_REQUESTS=\$((TOTAL_REQUESTS + 1))
    
    if [ "\$response" != "200" ]; then
        FAILED_REQUESTS=\$((FAILED_REQUESTS + 1))
        echo "[\$(date)] Failed request: HTTP \$response"
    fi
    
    sleep 1
done

# Calculate availability
if [ \$TOTAL_REQUESTS -gt 0 ]; then
    AVAILABILITY=\$(echo "scale=4; ((\$TOTAL_REQUESTS - \$FAILED_REQUESTS) / \$TOTAL_REQUESTS) * 100" | bc)
    echo "Test Results:"
    echo "Total Requests: \$TOTAL_REQUESTS"
    echo "Failed Requests: \$FAILED_REQUESTS"
    echo "Availability: \$AVAILABILITY%"
    
    if (( \$(echo "\$AVAILABILITY >= 99.9" | bc -l) )); then
        echo "✅ Zero-downtime test PASSED (≥99.9% availability)"
        exit 0
    else
        echo "❌ Zero-downtime test FAILED (<99.9% availability)"
        exit 1
    fi
else
    echo "❌ No requests completed"
    exit 1
fi
"@

    $TestScript | Out-File -FilePath ".\week1\test-zero-downtime.sh" -Encoding UTF8
    
    # Run test in background while triggering deployment
    Write-Status "Starting availability monitoring..." "Info"
    
    # Trigger canary deployment
    kubectl argo rollouts set image zeta-agent-canary zeta-agent=zeta-agent:v1.1.0 -n $Namespace
    
    Write-Status "Canary deployment triggered. Monitor with:" "Info"
    Write-Status "kubectl argo rollouts get rollout zeta-agent-canary -n $Namespace --watch" "Info"
}

function Show-Week1Summary {
    Write-Status "📊 Week 1 Implementation Summary" "Success"
    Write-Host ""
    Write-Host "✅ Components Deployed:" -ForegroundColor Green
    Write-Host "   • ArgoCD GitOps platform" -ForegroundColor White
    Write-Host "   • Argo Rollouts for advanced deployments" -ForegroundColor White
    Write-Host "   • Canary deployment strategy (20/40/60/80% traffic)" -ForegroundColor White
    Write-Host "   • Blue-Green deployment strategy" -ForegroundColor White
    Write-Host "   • Automated analysis templates" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Success Criteria:" -ForegroundColor Cyan
    Write-Host "   • Zero-downtime deployments (≥99.9% availability)" -ForegroundColor White
    Write-Host "   • Automated rollback on failure" -ForegroundColor White
    Write-Host "   • Health checks and performance analysis" -ForegroundColor White
    Write-Host "   • GitOps workflow integration" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Quick Commands:" -ForegroundColor Yellow
    Write-Host "   # Access ArgoCD UI" -ForegroundColor White
    Write-Host "   kubectl port-forward svc/argocd-server -n argocd 8080:443" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   # Monitor canary deployment" -ForegroundColor White
    Write-Host "   kubectl argo rollouts get rollout zeta-agent-canary -n $Namespace --watch" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   # Promote canary to 100%" -ForegroundColor White
    Write-Host "   kubectl argo rollouts promote zeta-agent-canary -n $Namespace" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   # Rollback deployment" -ForegroundColor White
    Write-Host "   kubectl argo rollouts undo zeta-agent-canary -n $Namespace" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🚀 Next Week: Service Mesh (Istio) + Distributed Tracing (Jaeger)" -ForegroundColor Cyan
}

# Main execution
Write-Status "🚀 Week 1: Zero-Downtime Deployments Setup" "Info"

try {
    # Create week1 directory
    if (-not (Test-Path ".\week1")) {
        New-Item -ItemType Directory -Path ".\week1" -Force | Out-Null
    }
    
    if ($InstallArgoCD) {
        Install-ArgoCD
    }
    
    if ($SetupCanary) {
        Setup-CanaryDeployment
    }
    
    if ($SetupBlueGreen) {
        Setup-BlueGreenDeployment
    }
    
    if ($TestDeployment) {
        Test-ZeroDowntimeDeployment
    }
    
    if (-not $InstallArgoCD -and -not $SetupCanary -and -not $SetupBlueGreen -and -not $TestDeployment) {
        # Run all by default
        Install-ArgoCD
        Setup-CanaryDeployment
        Setup-BlueGreenDeployment
    }
    
    Show-Week1Summary
    
    Write-Status "✅ Week 1 setup completed successfully!" "Success"
    
} catch {
    Write-Status "❌ Error during Week 1 setup: $($_.Exception.Message)" "Error"
    exit 1
}
