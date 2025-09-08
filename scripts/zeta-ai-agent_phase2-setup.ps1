#!/usr/bin/env powershell

# Phase 2 Setup Script - Advanced Production Features
# Sets up infrastructure for performance optimization, monitoring, and security

param(
    [ValidateSet("all", "performance", "monitoring", "security", "advanced", "cicd", "servicemesh")]
    [string]$Component = "all",
    
    [switch]$SkipConfirmation,
    [switch]$DryRun
)

# Configuration
$Phase2Dir = "$PSScriptRoot\..\phase2"
$InfraDir = "$PSScriptRoot\..\infra"

# Colors for output
function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function New-DirectoryStructure {
    Write-Status "Creating Phase 2 directory structure..." "Info"
    
    $Directories = @(
        "$Phase2Dir\performance\load-tests",
        "$Phase2Dir\performance\configs",
        "$Phase2Dir\monitoring\prometheus",
        "$Phase2Dir\monitoring\grafana\dashboards",
        "$Phase2Dir\monitoring\alertmanager",
        "$Phase2Dir\security\policies",
        "$Phase2Dir\security\scans",
        "$Phase2Dir\advanced\argocd",
        "$Phase2Dir\advanced\helmfile",
        "$Phase2Dir\cicd\workflows",
        "$Phase2Dir\cicd\quality-gates",
        "$Phase2Dir\servicemesh\istio",
        "$Phase2Dir\servicemesh\linkerd"
    )
    
    foreach ($Dir in $Directories) {
        if (-not (Test-Path $Dir)) {
            if (-not $DryRun) {
                New-Item -ItemType Directory -Path $Dir -Force | Out-Null
            }
            Write-Status "Created: $Dir" "Success"
        }
    }
}

function New-PerformanceConfigs {
    Write-Status "Setting up performance optimization..." "Info"
    
    # k6 Load Testing Script
    $K6LoadTest = @'
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
export let errorRate = new Rate('errors');

export let options = {
  stages: [
    { duration: '2m', target: 20 },   // Ramp up
    { duration: '5m', target: 100 },  // Stay at 100 RPS
    { duration: '2m', target: 200 },  // Ramp to 200 RPS  
    { duration: '5m', target: 200 },  // Stay at 200 RPS
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],   // 95% requests under 200ms
    http_req_failed: ['rate<0.01'],     // Error rate under 1%
    errors: ['rate<0.01'],              // Custom error rate
  },
};

const BASE_URL = __ENV.TARGET_URL || 'http://localhost:3000';

export default function() {
  // Health check
  let healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health check status is 200': (r) => r.status === 200,
    'health check response time < 100ms': (r) => r.timings.duration < 100,
  }) || errorRate.add(1);

  // API status
  let statusRes = http.get(`${BASE_URL}/api/v1/status`);
  check(statusRes, {
    'status API status is 200': (r) => r.status === 200,
    'status API response time < 200ms': (r) => r.timings.duration < 200,
  }) || errorRate.add(1);

  // Chat simulation
  let chatPayload = JSON.stringify({
    message: "Hello, can you help me with some code?",
    context: "performance testing"
  });
  
  let chatRes = http.post(`${BASE_URL}/api/v1/chat`, chatPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(chatRes, {
    'chat API status is 200': (r) => r.status === 200,
    'chat API response time < 500ms': (r) => r.timings.duration < 500,
  }) || errorRate.add(1);

  sleep(1); // 1 second delay between iterations
}
'@

    if (-not $DryRun) {
        $K6LoadTest | Out-File -FilePath "$Phase2Dir\performance\load-tests\basic-load.js" -Encoding UTF8
    }
    
    # Performance optimized values.yaml
    $PerformanceValues = @'
# Performance optimized configuration
replicaCount: 3

image:
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: "2000m"
    memory: "1Gi"
  requests:
    cpu: "500m"
    memory: "512Mi"

# Node.js performance tuning
env:
  NODE_ENV: "production"
  NODE_OPTIONS: "--max-old-space-size=512 --gc-interval=100"
  UV_THREADPOOL_SIZE: "8"

# Auto-scaling for performance
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

# Performance monitoring
metrics:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 15s

# Readiness/Liveness optimized
readinessProbe:
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

livenessProbe:
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
'@

    if (-not $DryRun) {
        $PerformanceValues | Out-File -FilePath "$Phase2Dir\performance\configs\values-performance.yaml" -Encoding UTF8
    }
    
    Write-Status "Performance configuration created" "Success"
}

function New-MonitoringStack {
    Write-Status "Setting up monitoring and observability..." "Info"
    
    # Prometheus values
    $PrometheusValues = @'
# Prometheus configuration for Zeta Agent monitoring
prometheus:
  prometheusSpec:
    retention: 15d
    storageSpec:
      volumeClaimTemplate:
        spec:
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 50Gi
    
    additionalScrapeConfigs:
      - job_name: 'zeta-agent'
        kubernetes_sd_configs:
          - role: endpoints
            namespaces:
              names:
                - zeta-agent
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_name]
            action: keep
            regex: zeta-agent

alertmanager:
  config:
    global:
      smtp_smarthost: 'localhost:587'
      smtp_from: 'alerts@your-domain.com'
    
    route:
      group_by: ['alertname']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 1h
      receiver: 'web.hook'
    
    receivers:
      - name: 'web.hook'
        webhook_configs:
          - url: 'http://your-webhook-url'

grafana:
  adminPassword: 'admin'  # Change in production
  persistence:
    enabled: true
    size: 10Gi
  
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
      - name: 'default'
        orgId: 1
        folder: ''
        type: file
        disableDeletion: false
        editable: true
        options:
          path: /var/lib/grafana/dashboards/default
'@

    if (-not $DryRun) {
        $PrometheusValues | Out-File -FilePath "$Phase2Dir\monitoring\prometheus\values.yaml" -Encoding UTF8
    }
    
    # Grafana Dashboard for Zeta Agent
    $GrafanaDashboard = @'
{
  "dashboard": {
    "id": null,
    "title": "Zeta Agent Overview",
    "tags": ["zeta-agent", "performance"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate (RPS)",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(zeta_agent_requests_total[5m]))",
            "legendFormat": "RPS"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 50},
                {"color": "red", "value": 100}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Response Time P95",
        "type": "stat",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(zeta_agent_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P95 Latency"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s",
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.2},
                {"color": "red", "value": 0.5}
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "Memory Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "avg(container_memory_usage_bytes{pod=~\"zeta-agent.*\"}) / 1024 / 1024",
            "legendFormat": "Memory MB"
          }
        ]
      },
      {
        "id": 4,
        "title": "CPU Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "avg(rate(container_cpu_usage_seconds_total{pod=~\"zeta-agent.*\"}[5m])) * 100",
            "legendFormat": "CPU %"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "5s"
  }
}
'@

    if (-not $DryRun) {
        $GrafanaDashboard | Out-File -FilePath "$Phase2Dir\monitoring\grafana\dashboards\zeta-agent-overview.json" -Encoding UTF8
    }
    
    Write-Status "Monitoring stack configuration created" "Success"
}

function New-SecurityConfigs {
    Write-Status "Setting up security hardening..." "Info"
    
    # Security hardened values.yaml
    $SecurityValues = @'
# Security hardened configuration
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 65534
  runAsGroup: 65534
  fsGroup: 65534
  seccompProfile:
    type: RuntimeDefault

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  capabilities:
    drop:
      - ALL

# Network policies
networkPolicy:
  enabled: true
  ingress:
    enabled: true
    rules:
      - from:
          - namespaceSelector:
              matchLabels:
                name: ingress-nginx
        ports:
          - protocol: TCP
            port: 3000
  egress:
    enabled: true
    rules:
      - to:
          - namespaceSelector:
              matchLabels:
                name: ollama-system
        ports:
          - protocol: TCP
            port: 11434

# Pod Security Standards
podSecurityStandard: "restricted"

# Service account with minimal permissions
serviceAccount:
  create: true
  automountServiceAccountToken: false
  
# RBAC with least privilege
rbac:
  create: true
  rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "list"]
'@

    if (-not $DryRun) {
        $SecurityValues | Out-File -FilePath "$Phase2Dir\security\values-security.yaml" -Encoding UTF8
    }
    
    # Network Policy template
    $NetworkPolicy = @'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: zeta-agent-strict-policy
  namespace: zeta-agent
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: zeta-agent
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow ingress from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 3000
    # Allow ingress from monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 3000
  egress:
    # DNS resolution
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
    # HTTPS outbound
    - to: []
      ports:
        - protocol: TCP
          port: 443
    # Ollama service
    - to:
        - namespaceSelector:
            matchLabels:
              name: ollama-system
      ports:
        - protocol: TCP
          port: 11434
'@

    if (-not $DryRun) {
        $NetworkPolicy | Out-File -FilePath "$Phase2Dir\security\policies\network-policy.yaml" -Encoding UTF8
    }
    
    Write-Status "Security configuration created" "Success"
}

function New-AdvancedFeatures {
    Write-Status "Setting up advanced features..." "Info"
    
    # Helmfile for multi-environment
    $Helmfile = @'
environments:
  dev:
    values:
      - ./helm/zeta-agent/values.yaml
      - ./phase2/performance/configs/values-performance.yaml
      - environment: dev
        replicas: 1
        
  staging:
    values:
      - ./helm/zeta-agent/values.yaml
      - ./phase2/performance/configs/values-performance.yaml
      - ./phase2/security/values-security.yaml
      - environment: staging
        replicas: 2
        
  prod:
    values:
      - ./helm/zeta-agent/values.yaml
      - ./phase2/performance/configs/values-performance.yaml
      - ./phase2/security/values-security.yaml
      - environment: prod
        replicas: 5

releases:
  - name: zeta-agent
    chart: ./infra/helm/zeta-agent
    namespace: zeta-agent-{{ .Environment.Name }}
    createNamespace: true
    wait: true
    timeout: 300
    values:
      - image:
          tag: {{ env "IMAGE_TAG" | default "latest" }}
      - global:
          environment: {{ .Environment.Name }}
'@

    if (-not $DryRun) {
        $Helmfile | Out-File -FilePath "$Phase2Dir\advanced\helmfile\helmfile.yaml" -Encoding UTF8
    }
    
    # ArgoCD Application
    $ArgoApp = @'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: zeta-agent
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/zeta-monorepo
    targetRevision: HEAD
    path: infra/helm/zeta-agent
    helm:
      valueFiles:
        - values.yaml
        - ../../phase2/performance/configs/values-performance.yaml
        - ../../phase2/security/values-security.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: zeta-agent
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
'@

    if (-not $DryRun) {
        $ArgoApp | Out-File -FilePath "$Phase2Dir\advanced\argocd\application.yaml" -Encoding UTF8
    }
    
    Write-Status "Advanced features configuration created" "Success"
}

function New-EnhancedCICD {
    Write-Status "Setting up enhanced CI/CD..." "Info"
    
    # Advanced CI/CD workflow
    $AdvancedWorkflow = @'
name: Advanced CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: docker.io
  IMAGE_NAME: zetaai/zeta-agent

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run SAST with Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
            
      - name: Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: zeta-agent
          path: .
          format: JSON
          
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: reports/

  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  build-and-test:
    needs: [security-scan, quality-gate]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Build and scan image
        run: |
          docker buildx build \
            --platform linux/amd64,linux/arm64 \
            --tag ${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --load \
            .
            
          # Security scan
          trivy image --exit-code 1 --severity HIGH,CRITICAL ${{ env.IMAGE_NAME }}:${{ github.sha }}
          
      - name: Performance Test
        run: |
          # Start container for testing
          docker run -d -p 3000:3000 --name zeta-test ${{ env.IMAGE_NAME }}:${{ github.sha }}
          
          # Wait for startup
          sleep 30
          
          # Run k6 load test
          docker run --rm -i grafana/k6:latest run - < phase2/performance/load-tests/basic-load.js

  canary-deployment:
    if: github.ref == 'refs/heads/main'
    needs: [build-and-test]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Canary
        run: |
          helm upgrade zeta-agent ./infra/helm/zeta-agent \
            --set image.tag=${{ github.sha }} \
            --set canary.enabled=true \
            --set canary.weight=10 \
            --wait \
            --timeout=300s
            
      - name: Canary Analysis
        run: |
          # Wait for metrics collection
          sleep 60
          
          # Check success rate
          SUCCESS_RATE=$(kubectl exec -n monitoring deployment/prometheus -- \
            promtool query instant \
            'rate(zeta_agent_requests_total{code!~"5.."}[5m]) / rate(zeta_agent_requests_total[5m])')
            
          if (( $(echo "$SUCCESS_RATE > 0.99" | bc -l) )); then
            echo "CANARY_SUCCESS=true" >> $GITHUB_ENV
          else
            echo "CANARY_SUCCESS=false" >> $GITHUB_ENV
          fi
          
      - name: Promote or Rollback
        run: |
          if [ "$CANARY_SUCCESS" = "true" ]; then
            helm upgrade zeta-agent ./infra/helm/zeta-agent \
              --set image.tag=${{ github.sha }} \
              --set canary.enabled=false
            echo "✅ Canary promoted to production"
          else
            helm rollback zeta-agent
            echo "❌ Canary failed, rolled back"
            exit 1
          fi
'@

    if (-not $DryRun) {
        $AdvancedWorkflow | Out-File -FilePath "$Phase2Dir\cicd\workflows\advanced-pipeline.yml" -Encoding UTF8
    }
    
    Write-Status "Enhanced CI/CD configuration created" "Success"
}

# Main execution
Write-Status "🚀 Starting Phase 2 Setup - Advanced Production Features" "Info"

if (-not $SkipConfirmation -and -not $DryRun) {
    $Confirmation = Read-Host "This will create Phase 2 configurations. Continue? (y/N)"
    if ($Confirmation -ne 'y' -and $Confirmation -ne 'Y') {
        Write-Status "Setup cancelled by user" "Warning"
        exit 0
    }
}

try {
    New-DirectoryStructure
    
    switch ($Component) {
        "all" {
            New-PerformanceConfigs
            New-MonitoringStack
            New-SecurityConfigs
            New-AdvancedFeatures
            New-EnhancedCICD
        }
        "performance" { New-PerformanceConfigs }
        "monitoring" { New-MonitoringStack }
        "security" { New-SecurityConfigs }
        "advanced" { New-AdvancedFeatures }
        "cicd" { New-EnhancedCICD }
    }
    
    Write-Status "🎉 Phase 2 setup completed successfully!" "Success"
    Write-Status "" "Info"
    Write-Status "Next steps:" "Info"
    Write-Status "1. Review configurations in ./phase2/ directory" "Info"
    Write-Status "2. Run: .\scripts\setup-monitoring.ps1" "Info"
    Write-Status "3. Run: .\scripts\setup-load-testing.ps1" "Info"
    Write-Status "4. Deploy with: helmfile -e dev sync" "Info"
    
} catch {
    Write-Status "❌ Error during setup: $($_.Exception.Message)" "Error"
    exit 1
}
