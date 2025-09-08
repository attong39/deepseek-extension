#!/usr/bin/env powershell

# Quick Environment Setup and Health Check Script
# Installs necessary tools and performs health verification

param(
    [switch]$InstallTools,
    [switch]$HealthCheck,
    [switch]$SetupLocal,
    [string]$KubeContext = "",
    [switch]$SkipInstall
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Colors = @{ Info = "Cyan"; Success = "Green"; Warning = "Yellow"; Error = "Red" }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Test-Command {
    param([string]$Command)
    return (Get-Command $Command -ErrorAction SilentlyContinue) -ne $null
}

function Install-RequiredTools {
    Write-Status "🔧 Installing required tools..." "Info"
    
    # Install Chocolatey if not present
    if (-not (Test-Command "choco")) {
        Write-Status "Installing Chocolatey..." "Info"
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # Refresh environment
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }
    
    # Install tools via Chocolatey
    $tools = @("kubernetes-cli", "docker-desktop", "kubernetes-helm", "k6", "curl")
    
    foreach ($tool in $tools) {
        if ($tool -eq "docker-desktop" -and (Test-Command "docker")) {
            Write-Status "Docker already installed" "Success"
            continue
        }
        if ($tool -eq "kubernetes-cli" -and (Test-Command "kubectl")) {
            Write-Status "kubectl already installed" "Success"
            continue
        }
        if ($tool -eq "kubernetes-helm" -and (Test-Command "helm")) {
            Write-Status "Helm already installed" "Success"
            continue
        }
        
        Write-Status "Installing $tool..." "Info"
        choco install $tool -y --no-progress
    }
    
    Write-Status "✅ Tools installation completed!" "Success"
    Write-Status "⚠️  Please restart PowerShell or refresh environment variables" "Warning"
}

function Setup-LocalKubernetes {
    Write-Status "🐳 Setting up local Kubernetes..." "Info"
    
    # Check if Docker Desktop is running
    try {
        docker version | Out-Null
        Write-Status "Docker is running" "Success"
    } catch {
        Write-Status "Please start Docker Desktop and enable Kubernetes" "Warning"
        Write-Status "1. Open Docker Desktop" "Info"
        Write-Status "2. Go to Settings > Kubernetes" "Info"
        Write-Status "3. Check 'Enable Kubernetes'" "Info"
        Write-Status "4. Click 'Apply & Restart'" "Info"
        return $false
    }
    
    # Wait for Kubernetes to be ready
    Write-Status "Waiting for Kubernetes to be ready..." "Info"
    $maxAttempts = 30
    $attempts = 0
    
    while ($attempts -lt $maxAttempts) {
        try {
            kubectl cluster-info --request-timeout=5s | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Status "Kubernetes is ready!" "Success"
                return $true
            }
        } catch {
            # Continue waiting
        }
        
        Start-Sleep 5
        $attempts++
        Write-Host "." -NoNewline
    }
    
    Write-Status "❌ Kubernetes not ready after $($maxAttempts * 5) seconds" "Error"
    return $false
}

function Test-KubernetesHealth {
    Write-Status "🔍 Checking Kubernetes cluster health..." "Info"
    
    # Check cluster info
    try {
        $clusterInfo = kubectl cluster-info 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ Kubernetes cluster is accessible" "Success"
            Write-Host $clusterInfo
        } else {
            Write-Status "❌ Cannot access Kubernetes cluster" "Error"
            return $false
        }
    } catch {
        Write-Status "❌ kubectl command failed" "Error"
        return $false
    }
    
    # Check nodes
    try {
        $nodes = kubectl get nodes --no-headers 2>$null
        if ($LASTEXITCODE -eq 0) {
            $nodeCount = ($nodes | Measure-Object).Count
            Write-Status "✅ Found $nodeCount node(s)" "Success"
            kubectl get nodes
        }
    } catch {
        Write-Status "⚠️  Could not get node information" "Warning"
    }
    
    return $true
}

function Test-ZetaAgentDeployment {
    Write-Status "🚀 Checking Zeta Agent deployment..." "Info"
    
    # Check if namespace exists
    $namespace = kubectl get namespace zeta-agent --no-headers --ignore-not-found 2>$null
    if (-not $namespace) {
        Write-Status "⚠️  zeta-agent namespace not found" "Warning"
        Write-Status "Creating zeta-agent namespace..." "Info"
        kubectl create namespace zeta-agent
        Write-Status "✅ zeta-agent namespace created" "Success"
    } else {
        Write-Status "✅ zeta-agent namespace exists" "Success"
    }
    
    # Check HPA
    Write-Status "Checking HPA (Horizontal Pod Autoscaler)..." "Info"
    try {
        $hpa = kubectl get hpa -n zeta-agent --no-headers 2>$null
        if ($hpa) {
            Write-Status "✅ HPA found:" "Success"
            kubectl get hpa -n zeta-agent
        } else {
            Write-Status "⚠️  No HPA found in zeta-agent namespace" "Warning"
        }
    } catch {
        Write-Status "❌ Error checking HPA" "Error"
    }
    
    # Check pods
    Write-Status "Checking pods..." "Info"
    try {
        $pods = kubectl get pods -n zeta-agent --no-headers 2>$null
        if ($pods) {
            Write-Status "✅ Pods found:" "Success"
            kubectl get pods -n zeta-agent
            
            # Check pod metrics if metrics server is available
            Write-Status "Checking pod metrics..." "Info"
            try {
                kubectl top pods -n zeta-agent 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-Status "✅ Pod metrics available" "Success"
                } else {
                    Write-Status "⚠️  Pod metrics not available (metrics-server may not be installed)" "Warning"
                }
            } catch {
                Write-Status "⚠️  Could not get pod metrics" "Warning"
            }
        } else {
            Write-Status "⚠️  No pods found in zeta-agent namespace" "Warning"
        }
    } catch {
        Write-Status "❌ Error checking pods" "Error"
    }
    
    # Check services
    Write-Status "Checking services..." "Info"
    try {
        $services = kubectl get svc -n zeta-agent --no-headers 2>$null
        if ($services) {
            Write-Status "✅ Services found:" "Success"
            kubectl get svc -n zeta-agent
        } else {
            Write-Status "⚠️  No services found in zeta-agent namespace" "Warning"
        }
    } catch {
        Write-Status "❌ Error checking services" "Error"
    }
}

function Test-MonitoringStack {
    Write-Status "📊 Checking monitoring stack..." "Info"
    
    # Check monitoring namespace
    $monitoringNs = kubectl get namespace monitoring --no-headers --ignore-not-found 2>$null
    if (-not $monitoringNs) {
        Write-Status "⚠️  monitoring namespace not found" "Warning"
        return
    } else {
        Write-Status "✅ monitoring namespace exists" "Success"
    }
    
    # Check Prometheus
    Write-Status "Checking Prometheus..." "Info"
    try {
        $promPods = kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus --no-headers 2>$null
        if ($promPods) {
            Write-Status "✅ Prometheus pods found" "Success"
            kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus
        } else {
            Write-Status "⚠️  No Prometheus pods found" "Warning"
        }
    } catch {
        Write-Status "❌ Error checking Prometheus" "Error"
    }
    
    # Check Grafana
    Write-Status "Checking Grafana..." "Info"
    try {
        $grafanaPods = kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana --no-headers 2>$null
        if ($grafanaPods) {
            Write-Status "✅ Grafana pods found" "Success"
            kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana
        } else {
            Write-Status "⚠️  No Grafana pods found" "Warning"
        }
    } catch {
        Write-Status "❌ Error checking Grafana" "Error"
    }
    
    # Check Alertmanager
    Write-Status "Checking Alertmanager..." "Info"
    try {
        $alertPods = kubectl get pods -n monitoring -l app.kubernetes.io/name=alertmanager --no-headers 2>$null
        if ($alertPods) {
            Write-Status "✅ Alertmanager pods found" "Success"
            kubectl get pods -n monitoring -l app.kubernetes.io/name=alertmanager
        } else {
            Write-Status "⚠️  No Alertmanager pods found" "Warning"
        }
    } catch {
        Write-Status "❌ Error checking Alertmanager" "Error"
    }
}

function Start-PortForwards {
    Write-Status "🔗 Setting up port forwards for easy access..." "Info"
    
    # Kill existing port forwards
    Get-Process | Where-Object {$_.ProcessName -eq "kubectl" -and $_.CommandLine -like "*port-forward*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    
    $portForwards = @()
    
    # Prometheus port forward
    try {
        $promSvc = kubectl get svc -n monitoring -l app.kubernetes.io/name=prometheus --no-headers 2>$null
        if ($promSvc) {
            Write-Status "Starting Prometheus port-forward..." "Info"
            $portForwards += Start-Process kubectl -ArgumentList "port-forward", "svc/prometheus-kube-prometheus-prometheus", "9090:9090", "-n", "monitoring" -PassThru -WindowStyle Minimized
            Start-Sleep 2
        }
    } catch {
        Write-Status "Could not start Prometheus port-forward" "Warning"
    }
    
    # Grafana port forward
    try {
        $grafanaSvc = kubectl get svc -n monitoring -l app.kubernetes.io/name=grafana --no-headers 2>$null
        if ($grafanaSvc) {
            Write-Status "Starting Grafana port-forward..." "Info"
            $portForwards += Start-Process kubectl -ArgumentList "port-forward", "svc/prometheus-grafana", "3000:80", "-n", "monitoring" -PassThru -WindowStyle Minimized
            Start-Sleep 2
        }
    } catch {
        Write-Status "Could not start Grafana port-forward" "Warning"
    }
    
    # Alertmanager port forward
    try {
        $alertSvc = kubectl get svc -n monitoring -l app.kubernetes.io/name=alertmanager --no-headers 2>$null
        if ($alertSvc) {
            Write-Status "Starting Alertmanager port-forward..." "Info"
            $portForwards += Start-Process kubectl -ArgumentList "port-forward", "svc/prometheus-kube-prometheus-alertmanager", "9093:9093", "-n", "monitoring" -PassThru -WindowStyle Minimized
            Start-Sleep 2
        }
    } catch {
        Write-Status "Could not start Alertmanager port-forward" "Warning"
    }
    
    # Zeta Agent port forward (if service exists)
    try {
        $zetaSvc = kubectl get svc -n zeta-agent --no-headers 2>$null
        if ($zetaSvc) {
            Write-Status "Starting Zeta Agent port-forward..." "Info"
            $portForwards += Start-Process kubectl -ArgumentList "port-forward", "svc/zeta-agent", "8080:3000", "-n", "zeta-agent" -PassThru -WindowStyle Minimized
            Start-Sleep 2
        }
    } catch {
        Write-Status "Could not start Zeta Agent port-forward" "Warning"
    }
    
    if ($portForwards.Count -gt 0) {
        Write-Status "✅ Port forwards started successfully!" "Success"
        Write-Host ""
        Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
        Write-Host "   📈 Grafana: http://localhost:3000 (admin/zetaAdmin123!)" -ForegroundColor Green
        Write-Host "   🔍 Prometheus: http://localhost:9090" -ForegroundColor Green
        Write-Host "   🚨 Alertmanager: http://localhost:9093" -ForegroundColor Green
        Write-Host "   🚀 Zeta Agent: http://localhost:8080" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Quick Health Checks:" -ForegroundColor Yellow
        Write-Host "   curl http://localhost:8080/health" -ForegroundColor White
        Write-Host "   curl http://localhost:8080/metrics" -ForegroundColor White
        Write-Host "   start http://localhost:9090/graph" -ForegroundColor White
    } else {
        Write-Status "⚠️  No port forwards could be started" "Warning"
    }
}

function Show-QuickCommands {
    Write-Status "🎯 Quick Health Check Commands:" "Info"
    Write-Host ""
    Write-Host "# Kubernetes Health:" -ForegroundColor Cyan
    Write-Host "kubectl get nodes" -ForegroundColor White
    Write-Host "kubectl get pods --all-namespaces" -ForegroundColor White
    Write-Host ""
    Write-Host "# Zeta Agent Status:" -ForegroundColor Cyan
    Write-Host "kubectl get pods -n zeta-agent" -ForegroundColor White
    Write-Host "kubectl get hpa -n zeta-agent" -ForegroundColor White
    Write-Host "kubectl top pods -n zeta-agent" -ForegroundColor White
    Write-Host ""
    Write-Host "# Monitoring Stack:" -ForegroundColor Cyan
    Write-Host "kubectl get pods -n monitoring" -ForegroundColor White
    Write-Host "kubectl get svc -n monitoring" -ForegroundColor White
    Write-Host ""
    Write-Host "# Application Health:" -ForegroundColor Cyan
    Write-Host "curl http://localhost:8080/health" -ForegroundColor White
    Write-Host "curl http://localhost:8080/api/v1/status" -ForegroundColor White
    Write-Host "curl http://localhost:8080/metrics" -ForegroundColor White
    Write-Host ""
    Write-Host "# Monitoring Access:" -ForegroundColor Cyan
    Write-Host "start http://localhost:3000  # Grafana" -ForegroundColor White
    Write-Host "start http://localhost:9090  # Prometheus" -ForegroundColor White
    Write-Host "start http://localhost:9093  # Alertmanager" -ForegroundColor White
}

# Main execution
Write-Status "🚀 Zeta Agent Environment Health Check" "Info"

try {
    if ($InstallTools -and -not $SkipInstall) {
        Install-RequiredTools
        Write-Status "Please restart PowerShell and run again with -HealthCheck" "Warning"
        exit 0
    }
    
    if ($SetupLocal) {
        $k8sReady = Setup-LocalKubernetes
        if (-not $k8sReady) {
            Write-Status "Please ensure Docker Desktop with Kubernetes is running" "Error"
            exit 1
        }
    }
    
    # Check if kubectl is available
    if (-not (Test-Command "kubectl")) {
        Write-Status "kubectl not found. Installing tools..." "Warning"
        Install-RequiredTools
        Write-Status "Please restart PowerShell and run: .\scripts\health-check.ps1 -HealthCheck" "Warning"
        exit 0
    }
    
    if ($HealthCheck -or (-not $InstallTools -and -not $SetupLocal)) {
        # Perform comprehensive health check
        $k8sHealthy = Test-KubernetesHealth
        if ($k8sHealthy) {
            Test-ZetaAgentDeployment
            Test-MonitoringStack
            Start-PortForwards
        }
        
        Show-QuickCommands
    }
    
    Write-Status "✅ Health check completed!" "Success"
    
} catch {
    Write-Status "❌ Error during health check: $($_.Exception.Message)" "Error"
    exit 1
}
