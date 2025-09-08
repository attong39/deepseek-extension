#!/usr/bin/env powershell

# Monitoring Stack Quick Setup
# Deploys Prometheus, Grafana, and Alertmanager for Zeta Agent monitoring

param(
    [string]$Namespace = "monitoring",
    [switch]$InstallHelm,
    [switch]$CreateDashboards,
    [switch]$SetupAlerts,
    [string]$AdminPassword = "zetaAdmin123!",
    [switch]$PortForward
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Install-MonitoringStack {
    Write-Status "Installing Prometheus and Grafana monitoring stack..." "Info"
    
    # Create namespace
    kubectl create namespace $Namespace --dry-run=client -o yaml | kubectl apply -f -
    
    # Add Prometheus Helm repo
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update
    
    # Install kube-prometheus-stack (includes Prometheus, Grafana, Alertmanager)
    Write-Status "Installing kube-prometheus-stack..." "Info"
    helm upgrade --install prometheus prometheus-community/kube-prometheus-stack `
        --namespace $Namespace `
        --set grafana.adminPassword=$AdminPassword `
        --set grafana.service.type=LoadBalancer `
        --set prometheus.service.type=LoadBalancer `
        --set grafana.persistence.enabled=true `
        --set grafana.persistence.size=2Gi `
        --set prometheus.prometheusSpec.retention=7d `
        --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=10Gi `
        --wait --timeout=300s
    
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Monitoring stack installed successfully!" "Success"
    } else {
        Write-Status "Failed to install monitoring stack" "Error"
        return $false
    }
    
    return $true
}

function Create-ZetaAgentDashboards {
    Write-Status "Creating Zeta Agent specific Grafana dashboards..." "Info"
    
    # Zeta Agent Performance Dashboard JSON
    $ZetaAgentDashboard = @"
{
  "dashboard": {
    "id": null,
    "title": "🚀 Zeta Agent Performance",
    "tags": ["zeta-agent", "performance"],
    "style": "dark",
    "timezone": "browser",
    "refresh": "5s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "panels": [
      {
        "id": 1,
        "title": "📊 Request Rate (RPS)",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=~\".*zeta-agent.*\"}[5m]))",
            "legendFormat": "RPS"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": { "mode": "thresholds" },
            "thresholds": {
              "steps": [
                { "color": "red", "value": 0 },
                { "color": "yellow", "value": 50 },
                { "color": "green", "value": 100 }
              ]
            }
          }
        },
        "gridPos": { "h": 8, "w": 6, "x": 0, "y": 0 }
      },
      {
        "id": 2,
        "title": "⚡ Response Time P95",
        "type": "stat",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job=~\".*zeta-agent.*\"}[5m])) by (le)) * 1000",
            "legendFormat": "P95 (ms)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "ms",
            "color": { "mode": "thresholds" },
            "thresholds": {
              "steps": [
                { "color": "green", "value": 0 },
                { "color": "yellow", "value": 200 },
                { "color": "red", "value": 500 }
              ]
            }
          }
        },
        "gridPos": { "h": 8, "w": 6, "x": 6, "y": 0 }
      },
      {
        "id": 3,
        "title": "❌ Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=~\".*zeta-agent.*\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{job=~\".*zeta-agent.*\"}[5m])) * 100",
            "legendFormat": "Error %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "color": { "mode": "thresholds" },
            "thresholds": {
              "steps": [
                { "color": "green", "value": 0 },
                { "color": "yellow", "value": 1 },
                { "color": "red", "value": 5 }
              ]
            }
          }
        },
        "gridPos": { "h": 8, "w": 6, "x": 12, "y": 0 }
      },
      {
        "id": 4,
        "title": "🔄 Active Replicas",
        "type": "stat",
        "targets": [
          {
            "expr": "kube_deployment_status_replicas_available{deployment=\"zeta-agent\"}",
            "legendFormat": "Replicas"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": { "mode": "thresholds" },
            "thresholds": {
              "steps": [
                { "color": "red", "value": 0 },
                { "color": "yellow", "value": 1 },
                { "color": "green", "value": 2 }
              ]
            }
          }
        },
        "gridPos": { "h": 8, "w": 6, "x": 18, "y": 0 }
      },
      {
        "id": 5,
        "title": "📈 Request Rate Over Time",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=~\".*zeta-agent.*\"}[5m])) by (status)",
            "legendFormat": "Status: {{status}}"
          }
        ],
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 8 }
      },
      {
        "id": 6,
        "title": "⏱️ Response Time Percentiles",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{job=~\".*zeta-agent.*\"}[5m])) by (le)) * 1000",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job=~\".*zeta-agent.*\"}[5m])) by (le)) * 1000",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{job=~\".*zeta-agent.*\"}[5m])) by (le)) * 1000",
            "legendFormat": "P99"
          }
        ],
        "fieldConfig": {
          "defaults": { "unit": "ms" }
        },
        "gridPos": { "h": 8, "w": 12, "x": 12, "y": 8 }
      },
      {
        "id": 7,
        "title": "💾 Memory Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(container_memory_usage_bytes{pod=~\"zeta-agent.*\"}) by (pod) / 1024 / 1024",
            "legendFormat": "{{pod}}"
          }
        ],
        "fieldConfig": {
          "defaults": { "unit": "MB" }
        },
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 16 }
      },
      {
        "id": 8,
        "title": "🔧 CPU Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(container_cpu_usage_seconds_total{pod=~\"zeta-agent.*\"}[5m])) by (pod) * 100",
            "legendFormat": "{{pod}}"
          }
        ],
        "fieldConfig": {
          "defaults": { "unit": "percent" }
        },
        "gridPos": { "h": 8, "w": 12, "x": 12, "y": 16 }
      }
    ]
  },
  "folderId": 0,
  "overwrite": true
}
"@

    # Save dashboard JSON to file
    $ZetaAgentDashboard | Out-File -FilePath ".\phase2\monitoring\dashboards\zeta-agent-performance.json" -Encoding UTF8
    Write-Status "Zeta Agent dashboard JSON created" "Success"
}

function Setup-AlertingRules {
    Write-Status "Setting up Prometheus alerting rules..." "Info"
    
    $AlertingRules = @"
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: zeta-agent-alerts
  namespace: $Namespace
  labels:
    app: zeta-agent
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
  - name: zeta-agent.rules
    rules:
    # High Error Rate Alert
    - alert: ZetaAgentHighErrorRate
      expr: sum(rate(http_requests_total{job=~".*zeta-agent.*",status=~"5.."}[5m])) / sum(rate(http_requests_total{job=~".*zeta-agent.*"}[5m])) > 0.05
      for: 2m
      labels:
        severity: critical
        service: zeta-agent
      annotations:
        summary: "Zeta Agent error rate is above 5%"
        description: "Error rate is {{ \$value | humanizePercentage }} for the last 5 minutes."
        
    # High Response Time Alert  
    - alert: ZetaAgentHighLatency
      expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job=~".*zeta-agent.*"}[5m])) by (le)) > 0.5
      for: 3m
      labels:
        severity: warning
        service: zeta-agent
      annotations:
        summary: "Zeta Agent P95 latency is high"
        description: "P95 latency is {{ \$value }}s for the last 5 minutes."
        
    # Low Request Rate Alert
    - alert: ZetaAgentLowRequestRate
      expr: sum(rate(http_requests_total{job=~".*zeta-agent.*"}[5m])) < 1
      for: 5m
      labels:
        severity: warning
        service: zeta-agent
      annotations:
        summary: "Zeta Agent receiving very few requests"
        description: "Request rate is {{ \$value }} RPS for the last 5 minutes."
        
    # High Memory Usage Alert
    - alert: ZetaAgentHighMemoryUsage
      expr: sum(container_memory_usage_bytes{pod=~"zeta-agent.*"}) / sum(container_spec_memory_limit_bytes{pod=~"zeta-agent.*"}) > 0.8
      for: 3m
      labels:
        severity: warning
        service: zeta-agent
      annotations:
        summary: "Zeta Agent memory usage is high"
        description: "Memory usage is {{ \$value | humanizePercentage }} of limit."
        
    # Pod Restart Alert
    - alert: ZetaAgentPodRestarting
      expr: increase(kube_pod_container_status_restarts_total{pod=~"zeta-agent.*"}[1h]) > 3
      for: 0m
      labels:
        severity: warning
        service: zeta-agent
      annotations:
        summary: "Zeta Agent pod restarting frequently"
        description: "Pod {{ \$labels.pod }} has restarted {{ \$value }} times in the last hour."
        
    # HPA Scaling Alert
    - alert: ZetaAgentHPAMaxReplicas
      expr: kube_horizontalpodautoscaler_status_current_replicas{horizontalpodautoscaler="zeta-agent"} >= kube_horizontalpodautoscaler_spec_max_replicas{horizontalpodautoscaler="zeta-agent"}
      for: 5m
      labels:
        severity: warning
        service: zeta-agent
      annotations:
        summary: "Zeta Agent HPA at maximum replicas"
        description: "HPA has scaled to maximum {{ \$value }} replicas. Consider increasing limits."
"@

    $AlertingRules | Out-File -FilePath ".\phase2\monitoring\alerts\zeta-agent-alerts.yaml" -Encoding UTF8
    Write-Status "Alerting rules created: .\phase2\monitoring\alerts\zeta-agent-alerts.yaml" "Success"
    
    # Apply the alerting rules
    kubectl apply -f ".\phase2\monitoring\alerts\zeta-agent-alerts.yaml"
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Alerting rules applied successfully!" "Success"
    }
}

function Setup-ServiceMonitor {
    Write-Status "Setting up ServiceMonitor for Zeta Agent..." "Info"
    
    $ServiceMonitor = @"
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: zeta-agent
  namespace: $Namespace
  labels:
    app: zeta-agent
    release: prometheus
spec:
  selector:
    matchLabels:
      app: zeta-agent
  namespaceSelector:
    matchNames:
    - zeta-agent
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
    honorLabels: true
"@

    $ServiceMonitor | Out-File -FilePath ".\phase2\monitoring\servicemonitor.yaml" -Encoding UTF8
    Write-Status "ServiceMonitor created: .\phase2\monitoring\servicemonitor.yaml" "Success"
    
    # Apply ServiceMonitor
    kubectl apply -f ".\phase2\monitoring\servicemonitor.yaml"
    if ($LASTEXITCODE -eq 0) {
        Write-Status "ServiceMonitor applied successfully!" "Success"
    }
}

function Show-MonitoringInfo {
    Write-Status "📊 Monitoring Stack Information:" "Info"
    Write-Host ""
    Write-Host "🎯 Access Points:"
    
    # Get service information
    $Services = kubectl get svc -n $Namespace -o json | ConvertFrom-Json
    
    foreach ($Service in $Services.items) {
        if ($Service.metadata.name -like "*grafana*") {
            Write-Host "   📈 Grafana: http://localhost:3000" -ForegroundColor Green
            Write-Host "      Username: admin" -ForegroundColor Yellow
            Write-Host "      Password: $AdminPassword" -ForegroundColor Yellow
        }
        if ($Service.metadata.name -like "*prometheus*" -and $Service.metadata.name -notlike "*operator*") {
            Write-Host "   🔍 Prometheus: http://localhost:9090" -ForegroundColor Green
        }
        if ($Service.metadata.name -like "*alertmanager*") {
            Write-Host "   🚨 Alertmanager: http://localhost:9093" -ForegroundColor Green
        }
    }
    
    Write-Host ""
    Write-Host "🚀 Quick Commands:"
    Write-Host "   # Port forward Grafana"
    Write-Host "   kubectl port-forward svc/prometheus-grafana 3000:80 -n $Namespace"
    Write-Host ""
    Write-Host "   # Port forward Prometheus"
    Write-Host "   kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n $Namespace"
    Write-Host ""
    Write-Host "   # View alerts"
    Write-Host "   kubectl get prometheusrules -n $Namespace"
    Write-Host ""
    Write-Host "   # Check ServiceMonitor"
    Write-Host "   kubectl get servicemonitor -n $Namespace"
    Write-Host ""
    Write-Host "📊 Dashboard Import:"
    Write-Host "   1. Login to Grafana (admin/$AdminPassword)"
    Write-Host "   2. Go to Dashboards > Import"
    Write-Host "   3. Upload: .\phase2\monitoring\dashboards\zeta-agent-performance.json"
}

function Start-PortForwards {
    Write-Status "Setting up port forwards for easy access..." "Info"
    
    # Start port forwards in background
    Start-Process powershell -ArgumentList "-Command", "kubectl port-forward svc/prometheus-grafana 3000:80 -n $Namespace" -WindowStyle Minimized
    Start-Sleep 2
    Start-Process powershell -ArgumentList "-Command", "kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n $Namespace" -WindowStyle Minimized
    Start-Sleep 2
    Start-Process powershell -ArgumentList "-Command", "kubectl port-forward svc/prometheus-kube-prometheus-alertmanager 9093:9093 -n $Namespace" -WindowStyle Minimized
    
    Write-Status "Port forwards started! Access services at:" "Success"
    Write-Host "   📈 Grafana: http://localhost:3000" -ForegroundColor Green
    Write-Host "   🔍 Prometheus: http://localhost:9090" -ForegroundColor Green  
    Write-Host "   🚨 Alertmanager: http://localhost:9093" -ForegroundColor Green
}

# Main execution
Write-Status "🔍 Monitoring Stack Setup for Zeta Agent" "Info"

try {
    # Create directories
    if (-not (Test-Path ".\phase2\monitoring")) {
        New-Item -ItemType Directory -Path ".\phase2\monitoring\dashboards" -Force | Out-Null
        New-Item -ItemType Directory -Path ".\phase2\monitoring\alerts" -Force | Out-Null
    }
    
    # Install monitoring stack
    $Success = Install-MonitoringStack
    if (-not $Success) {
        Write-Status "Failed to install monitoring stack" "Error"
        exit 1
    }
    
    # Wait for pods to be ready
    Write-Status "Waiting for monitoring pods to be ready..." "Info"
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana -n $Namespace --timeout=300s
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=prometheus -n $Namespace --timeout=300s
    
    if ($CreateDashboards) {
        Create-ZetaAgentDashboards
    }
    
    if ($SetupAlerts) {
        Setup-AlertingRules
    }
    
    Setup-ServiceMonitor
    
    if ($PortForward) {
        Start-PortForwards
    }
    
    Show-MonitoringInfo
    
    Write-Status "✅ Monitoring stack setup completed successfully!" "Success"
    Write-Status "🎯 Next: Import dashboards and configure alerts in Grafana" "Info"
    
} catch {
    Write-Status "❌ Error during monitoring setup: $($_.Exception.Message)" "Error"
    exit 1
}
