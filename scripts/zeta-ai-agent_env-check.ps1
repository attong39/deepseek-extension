#!/usr/bin/env powershell

# Simple Environment Check and Setup for Development
# Works without admin privileges using portable tools

param(
    [switch]$CheckOnly,
    [switch]$SetupPortable,
    [switch]$ShowCommands
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Test-Command {
    param([string]$Command)
    return $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

function Test-DockerDesktop {
    Write-Status "🐳 Checking Docker Desktop..." "Info"
    
    if (Test-Command "docker") {
        try {
            $version = docker version --format "{{.Server.Version}}" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Status "✅ Docker Desktop is running (v$version)" "Success"
                
                # Check if Kubernetes is enabled
                try {
                    $k8sEnabled = docker info --format "{{.ServerVersion}}" | Select-String -Pattern ".*" -Quiet
                    if ($k8sEnabled) {
                        Write-Status "✅ Docker Desktop detected" "Success"
                        return $true
                    }
                } catch {
                    Write-Status "⚠️  Docker running but Kubernetes status unknown" "Warning"
                }
            }
        } catch {
            Write-Status "❌ Docker Desktop is not running" "Error"
        }
    } else {
        Write-Status "❌ Docker not found" "Error"
        Write-Status "📥 Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" "Info"
    }
    return $false
}

function Test-Kubernetes {
    Write-Status "☸️  Checking Kubernetes..." "Info"
    
    if (Test-Command "kubectl") {
        try {
            $clusterInfo = kubectl cluster-info --request-timeout=5s 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Status "✅ Kubernetes cluster is accessible" "Success"
                Write-Host $clusterInfo
                return $true
            } else {
                Write-Status "❌ Kubernetes cluster not accessible" "Error"
            }
        } catch {
            Write-Status "❌ kubectl failed to connect" "Error"
        }
    } else {
        Write-Status "❌ kubectl not found" "Error"
        Write-Status "📥 Please install kubectl" "Info"
    }
    return $false
}

function Test-EnvironmentAlternatives {
    Write-Status "🔧 Checking alternative environments..." "Info"
    
    # Check for WSL
    if (Test-Command "wsl") {
        Write-Status "✅ WSL available - can run Linux containers" "Success"
        try {
            $wslVersion = wsl --status 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Status "WSL Status: Available" "Success"
            }
        } catch {
            Write-Status "WSL may not be properly configured" "Warning"
        }
    }
    
    # Check for Podman
    if (Test-Command "podman") {
        Write-Status "✅ Podman available as Docker alternative" "Success"
    }
    
    # Check for Minikube
    if (Test-Command "minikube") {
        try {
            $minikubeStatus = minikube status --format="{{.Host}}" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Status "✅ Minikube available" "Success"
            }
        } catch {
            Write-Status "Minikube found but not running" "Warning"
        }
    }
    
    # Check for Kind
    if (Test-Command "kind") {
        try {
            $kindClusters = kind get clusters 2>$null
            if ($LASTEXITCODE -eq 0 -and $kindClusters) {
                Write-Status "✅ Kind clusters available: $kindClusters" "Success"
            }
        } catch {
            Write-Status "Kind found but no clusters" "Warning"
        }
    }
}

function Show-LocalDevelopmentOptions {
    Write-Status "🎯 Local Development Options:" "Info"
    Write-Host ""
    
    Write-Host "📋 Quick Status Check Commands:" -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Command "docker") {
        Write-Host "✅ Docker Commands:" -ForegroundColor Green
        Write-Host "   docker ps                    # Running containers" -ForegroundColor White
        Write-Host "   docker images                # Available images" -ForegroundColor White
        Write-Host "   docker system df             # Disk usage" -ForegroundColor White
        Write-Host ""
    }
    
    if (Test-Command "kubectl") {
        Write-Host "✅ Kubernetes Commands:" -ForegroundColor Green
        Write-Host "   kubectl get nodes            # Cluster nodes" -ForegroundColor White
        Write-Host "   kubectl get pods --all-namespaces  # All pods" -ForegroundColor White
        Write-Host "   kubectl get namespaces       # Available namespaces" -ForegroundColor White
        Write-Host ""
        
        Write-Host "🚀 Zeta Agent Commands:" -ForegroundColor Yellow
        Write-Host "   kubectl get pods -n zeta-agent      # Zeta Agent pods" -ForegroundColor White
        Write-Host "   kubectl get hpa -n zeta-agent       # Auto-scaling status" -ForegroundColor White
        Write-Host "   kubectl get svc -n zeta-agent       # Services" -ForegroundColor White
        Write-Host ""
        
        Write-Host "📊 Monitoring Commands:" -ForegroundColor Yellow
        Write-Host "   kubectl get pods -n monitoring      # Monitoring stack" -ForegroundColor White
        Write-Host "   kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring" -ForegroundColor White
        Write-Host "   kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "❌ kubectl not available. Install options:" -ForegroundColor Red
        Write-Host "   1. Enable Kubernetes in Docker Desktop" -ForegroundColor White
        Write-Host "   2. Install kubectl from: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/" -ForegroundColor White
        Write-Host "   3. Use minikube: https://minikube.sigs.k8s.io/docs/start/" -ForegroundColor White
        Write-Host ""
    }
    
    Write-Host "🌐 Application Health Check URLs:" -ForegroundColor Cyan
    Write-Host "   http://localhost:3000/health         # Application health" -ForegroundColor White
    Write-Host "   http://localhost:3000/api/v1/status  # API status" -ForegroundColor White
    Write-Host "   http://localhost:3000/metrics        # Prometheus metrics" -ForegroundColor White
    Write-Host ""
    
    Write-Host "📈 Monitoring Access:" -ForegroundColor Cyan
    Write-Host "   http://localhost:3000                # Grafana (admin/zetaAdmin123!)" -ForegroundColor White
    Write-Host "   http://localhost:9090                # Prometheus" -ForegroundColor White
    Write-Host "   http://localhost:9093                # Alertmanager" -ForegroundColor White
}

function Test-ZetaAgentDeployment {
    if (-not (Test-Command "kubectl")) {
        Write-Status "kubectl not available - cannot check deployment" "Warning"
        return
    }
    
    Write-Status "🚀 Checking Zeta Agent deployment..." "Info"
    
    # Check namespace
    try {
        $namespace = kubectl get namespace zeta-agent --no-headers --ignore-not-found 2>$null
        if ($namespace) {
            Write-Status "✅ zeta-agent namespace exists" "Success"
            
            # Check pods
            $pods = kubectl get pods -n zeta-agent --no-headers 2>$null
            if ($pods) {
                Write-Status "✅ Pods found in zeta-agent namespace:" "Success"
                kubectl get pods -n zeta-agent
                Write-Host ""
                
                # Check HPA
                $hpa = kubectl get hpa -n zeta-agent --no-headers 2>$null
                if ($hpa) {
                    Write-Status "✅ HPA (Horizontal Pod Autoscaler) found:" "Success"
                    kubectl get hpa -n zeta-agent
                    Write-Host ""
                } else {
                    Write-Status "⚠️  No HPA found" "Warning"
                }
                
                # Try to get pod metrics
                try {
                    kubectl top pods -n zeta-agent 2>$null
                    if ($LASTEXITCODE -eq 0) {
                        Write-Status "✅ Pod metrics available:" "Success"
                        kubectl top pods -n zeta-agent
                    } else {
                        Write-Status "⚠️  Pod metrics not available (metrics-server needed)" "Warning"
                    }
                } catch {
                    Write-Status "⚠️  Could not get pod metrics" "Warning"
                }
                
            } else {
                Write-Status "⚠️  No pods found in zeta-agent namespace" "Warning"
                Write-Status "Deploy with: helm install zeta-agent ./infra/helm/zeta-agent" "Info"
            }
        } else {
            Write-Status "⚠️  zeta-agent namespace not found" "Warning"
            Write-Status "Create with: kubectl create namespace zeta-agent" "Info"
        }
    } catch {
        Write-Status "❌ Error checking zeta-agent deployment" "Error"
    }
}

function Test-MonitoringStack {
    if (-not (Test-Command "kubectl")) {
        return
    }
    
    Write-Status "📊 Checking monitoring stack..." "Info"
    
    try {
        $monitoringNs = kubectl get namespace monitoring --no-headers --ignore-not-found 2>$null
        if ($monitoringNs) {
            Write-Status "✅ monitoring namespace exists" "Success"
            
            # Check Prometheus
            $promPods = kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus --no-headers 2>$null
            if ($promPods) {
                Write-Status "✅ Prometheus pods found" "Success"
                kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus
            } else {
                Write-Status "⚠️  No Prometheus pods found" "Warning"
            }
            
            # Check Grafana
            $grafanaPods = kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana --no-headers 2>$null
            if ($grafanaPods) {
                Write-Status "✅ Grafana pods found" "Success"
                kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana
            } else {
                Write-Status "⚠️  No Grafana pods found" "Warning"
            }
            
        } else {
            Write-Status "⚠️  monitoring namespace not found" "Warning"
            Write-Status "Deploy with: .\scripts\setup-monitoring.ps1" "Info"
        }
    } catch {
        Write-Status "❌ Error checking monitoring stack" "Error"
    }
}

function Show-NextSteps {
    Write-Status "🎯 Next Steps Based on Current Environment:" "Info"
    Write-Host ""
    
    if (-not (Test-Command "docker")) {
        Write-Host "1️⃣ Install Docker Desktop:" -ForegroundColor Yellow
        Write-Host "   - Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor White
        Write-Host "   - Enable Kubernetes in settings" -ForegroundColor White
        Write-Host ""
    }
    
    if (Test-Command "docker" -and -not (Test-Command "kubectl")) {
        Write-Host "2️⃣ Enable Kubernetes:" -ForegroundColor Yellow
        Write-Host "   - Open Docker Desktop settings" -ForegroundColor White
        Write-Host "   - Go to Kubernetes tab" -ForegroundColor White
        Write-Host "   - Check 'Enable Kubernetes'" -ForegroundColor White
        Write-Host "   - Click 'Apply & Restart'" -ForegroundColor White
        Write-Host ""
    }
    
    if (Test-Command "kubectl") {
        Write-Host "3️⃣ Deploy Zeta Agent:" -ForegroundColor Yellow
        Write-Host "   helm install zeta-agent ./infra/helm/zeta-agent --create-namespace --namespace zeta-agent" -ForegroundColor White
        Write-Host ""
        
        Write-Host "4️⃣ Setup Monitoring:" -ForegroundColor Yellow
        Write-Host "   .\scripts\setup-monitoring.ps1 -CreateDashboards -SetupAlerts" -ForegroundColor White
        Write-Host ""
        
        Write-Host "5️⃣ Run Performance Tests:" -ForegroundColor Yellow
        Write-Host "   .\scripts\setup-performance.ps1 -TargetRPS 100" -ForegroundColor White
        Write-Host ""
    }
    
    Write-Host "🔍 Development Mode (without Kubernetes):" -ForegroundColor Cyan
    Write-Host "   # Run locally with Docker" -ForegroundColor White
    Write-Host "   docker build -t zeta-agent ." -ForegroundColor White
    Write-Host "   docker run -p 3000:3000 zeta-agent" -ForegroundColor White
    Write-Host ""
    Write-Host "   # Run with Node.js directly" -ForegroundColor White
    Write-Host "   npm install" -ForegroundColor White
    Write-Host "   npm start" -ForegroundColor White
}

# Main execution
Write-Status "🔍 Zeta Agent Environment Assessment" "Info"
Write-Host ""

# Test core environment
$dockerOk = Test-DockerDesktop
$k8sOk = Test-Kubernetes

if (-not $dockerOk -and -not $k8sOk) {
    Test-EnvironmentAlternatives
}

if ($k8sOk) {
    Test-ZetaAgentDeployment
    Test-MonitoringStack
}

if ($ShowCommands -or $CheckOnly) {
    Show-LocalDevelopmentOptions
}

Show-NextSteps

Write-Status "✅ Environment assessment completed!" "Success"
Write-Status "Run with -ShowCommands for detailed command list" "Info"
