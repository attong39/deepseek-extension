#!/usr/bin/env powershell

# Zeta AI Agent - Deployment Verification Script
# This script verifies the deployment and infrastructure status

param(
    [string]$Environment = "development",
    [string]$Namespace = "zeta-agent",
    [switch]$SkipDockerTests,
    [switch]$SkipKubernetesTests,
    [switch]$SkipHealthChecks,
    [switch]$Verbose
)

# Colors for output
$Colors = @{
    Info = "Cyan"
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Header = "Magenta"
}

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $timestamp = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$timestamp] $Message" -ForegroundColor $Colors[$Type]
}

function Write-Header {
    param([string]$Title)
    Write-Host "`n" -NoNewline
    Write-Host "=" * 60 -ForegroundColor $Colors.Header
    Write-Host " $Title" -ForegroundColor $Colors.Header
    Write-Host "=" * 60 -ForegroundColor $Colors.Header
}

function Test-CommandExists {
    param([string]$Command)
    return Get-Command $Command -ErrorAction SilentlyContinue
}

function Test-Prerequisites {
    Write-Header "CHECKING PREREQUISITES"
    
    $tools = @(
        @{Name="docker"; Required=$true; Description="Docker"},
        @{Name="kubectl"; Required=$true; Description="Kubernetes CLI"},
        @{Name="helm"; Required=$true; Description="Helm Package Manager"},
        @{Name="terraform"; Required=$false; Description="Terraform"},
        @{Name="git"; Required=$false; Description="Git"}
    )
    
    $missingRequired = @()
    $missingOptional = @()
    
    foreach ($tool in $tools) {
        if (Test-CommandExists $tool.Name) {
            Write-Status "✓ $($tool.Description) - Available" "Success"
            
            if ($Verbose) {
                try {
                    $version = & $tool.Name --version 2>$null | Select-Object -First 1
                    Write-Status "  Version: $version" "Info"
                } catch {
                    Write-Status "  Version: Unable to determine" "Warning"
                }
            }
        } else {
            Write-Status "✗ $($tool.Description) - Not found" "Error"
            if ($tool.Required) {
                $missingRequired += $tool.Name
            } else {
                $missingOptional += $tool.Name
            }
        }
    }
    
    if ($missingRequired.Count -gt 0) {
        Write-Status "Missing required tools: $($missingRequired -join ', ')" "Error"
        Write-Status "Please run: .\scripts\setup-devops-tools.ps1" "Warning"
        return $false
    }
    
    if ($missingOptional.Count -gt 0) {
        Write-Status "Missing optional tools: $($missingOptional -join ', ')" "Warning"
    }
    
    return $true
}

function Test-DockerEnvironment {
    if ($SkipDockerTests) {
        Write-Status "Skipping Docker tests" "Warning"
        return $true
    }
    
    Write-Header "DOCKER ENVIRONMENT VERIFICATION"
    
    # Test Docker daemon
    try {
        $dockerInfo = docker info --format "{{.ServerVersion}}" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✓ Docker daemon running (version: $dockerInfo)" "Success"
        } else {
            Write-Status "✗ Docker daemon not accessible" "Error"
            return $false
        }
    } catch {
        Write-Status "✗ Docker command failed: $($_.Exception.Message)" "Error"
        return $false
    }
    
    # Test Docker buildx
    try {
        $buildxVersion = docker buildx version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✓ Docker buildx available" "Success"
        } else {
            Write-Status "✗ Docker buildx not available" "Error"
        }
    } catch {
        Write-Status "✗ Docker buildx test failed" "Error"
    }
    
    # Check for existing Zeta Agent images
    try {
        $images = docker images --filter "reference=*zeta-agent*" --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
        if ($images -match "zeta-agent") {
            Write-Status "✓ Found Zeta Agent Docker images:" "Success"
            $images | ForEach-Object { Write-Status "  $_" "Info" }
        } else {
            Write-Status "ℹ No Zeta Agent images found locally" "Warning"
        }
    } catch {
        Write-Status "✗ Failed to check Docker images" "Error"
    }
    
    return $true
}

function Test-KubernetesEnvironment {
    if ($SkipKubernetesTests) {
        Write-Status "Skipping Kubernetes tests" "Warning"
        return $true
    }
    
    Write-Header "KUBERNETES ENVIRONMENT VERIFICATION"
    
    # Test cluster connectivity
    try {
        $clusterInfo = kubectl cluster-info --request-timeout=10s 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✓ Kubernetes cluster accessible" "Success"
            if ($Verbose) {
                Write-Status "  Cluster info:" "Info"
                $clusterInfo | ForEach-Object { Write-Status "    $_" "Info" }
            }
        } else {
            Write-Status "✗ Kubernetes cluster not accessible" "Error"
            Write-Status "  Check: kubectl config current-context" "Warning"
            return $false
        }
    } catch {
        Write-Status "✗ kubectl command failed: $($_.Exception.Message)" "Error"
        return $false
    }
    
    # Check current context
    try {
        $currentContext = kubectl config current-context 2>$null
        Write-Status "Current context: $currentContext" "Info"
    } catch {
        Write-Status "Could not determine current context" "Warning"
    }
    
    # Check nodes
    try {
        $nodes = kubectl get nodes --no-headers 2>$null
        if ($LASTEXITCODE -eq 0 -and $nodes) {
            Write-Status "✓ Cluster nodes:" "Success"
            $nodes | ForEach-Object {
                $parts = $_ -split '\s+'
                Write-Status "  $($parts[0]) - $($parts[1])" "Info"
            }
        } else {
            Write-Status "✗ No cluster nodes found" "Error"
        }
    } catch {
        Write-Status "✗ Failed to check cluster nodes" "Error"
    }
    
    # Check target namespace
    try {
        $nsExists = kubectl get namespace $Namespace 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✓ Target namespace '$Namespace' exists" "Success"
        } else {
            Write-Status "ℹ Target namespace '$Namespace' does not exist" "Warning"
            Write-Status "  Will be created during deployment" "Info"
        }
    } catch {
        Write-Status "Could not check namespace" "Warning"
    }
    
    return $true
}

function Test-ZetaAgentDeployment {
    if ($SkipKubernetesTests) {
        Write-Status "Skipping deployment tests" "Warning"
        return $true
    }
    
    Write-Header "ZETA AGENT DEPLOYMENT STATUS"
    
    # Check if namespace exists
    try {
        kubectl get namespace $Namespace >$null 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Status "ℹ Namespace '$Namespace' not found - deployment not yet done" "Warning"
            return $true
        }
    } catch {
        Write-Status "Could not check namespace" "Warning"
        return $true
    }
    
    # Check Helm releases
    try {
        $helmReleases = helm list --namespace $Namespace --output json 2>$null | ConvertFrom-Json
        if ($helmReleases -and $helmReleases.Count -gt 0) {
            Write-Status "✓ Found Helm releases in namespace:" "Success"
            foreach ($release in $helmReleases) {
                Write-Status "  $($release.name) - $($release.status) (chart: $($release.chart))" "Info"
            }
        } else {
            Write-Status "ℹ No Helm releases found in namespace" "Warning"
        }
    } catch {
        Write-Status "Could not check Helm releases" "Warning"
    }
    
    # Check deployments
    try {
        $deployments = kubectl get deployments --namespace $Namespace --no-headers 2>$null
        if ($LASTEXITCODE -eq 0 -and $deployments) {
            Write-Status "✓ Found deployments:" "Success"
            $deployments | ForEach-Object {
                $parts = $_ -split '\s+'
                Write-Status "  $($parts[0]) - $($parts[1]) replicas" "Info"
            }
        } else {
            Write-Status "ℹ No deployments found in namespace" "Warning"
        }
    } catch {
        Write-Status "Could not check deployments" "Warning"
    }
    
    # Check services
    try {
        $services = kubectl get services --namespace $Namespace --no-headers 2>$null
        if ($LASTEXITCODE -eq 0 -and $services) {
            Write-Status "✓ Found services:" "Success"
            $services | ForEach-Object {
                $parts = $_ -split '\s+'
                Write-Status "  $($parts[0]) - $($parts[1]) - $($parts[4])" "Info"
            }
        } else {
            Write-Status "ℹ No services found in namespace" "Warning"
        }
    } catch {
        Write-Status "Could not check services" "Warning"
    }
    
    return $true
}

function Test-HealthEndpoints {
    if ($SkipHealthChecks -or $SkipKubernetesTests) {
        Write-Status "Skipping health checks" "Warning"
        return $true
    }
    
    Write-Header "APPLICATION HEALTH CHECKS"
    
    # Check if there are any running pods
    try {
        $pods = kubectl get pods --namespace $Namespace --field-selector=status.phase=Running --no-headers 2>$null
        if (-not $pods) {
            Write-Status "ℹ No running pods found - skipping health checks" "Warning"
            return $true
        }
        
        Write-Status "Found running pods:" "Info"
        $pods | ForEach-Object {
            $parts = $_ -split '\s+'
            Write-Status "  $($parts[0]) - $($parts[1])" "Info"
        }
    } catch {
        Write-Status "Could not check pods" "Warning"
        return $true
    }
    
    # Try to port-forward and test health endpoint
    try {
        $serviceName = "zeta-agent"
        $service = kubectl get service $serviceName --namespace $Namespace 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Status "ℹ Service '$serviceName' not found - skipping health check" "Warning"
            return $true
        }
        
        Write-Status "Testing health endpoint via port-forward..." "Info"
        
        # Start port-forward in background
        $portForwardJob = Start-Job -ScriptBlock {
            param($ServiceName, $Namespace)
            kubectl port-forward service/$ServiceName 8080:3000 --namespace $Namespace
        } -ArgumentList $serviceName, $Namespace
        
        # Wait for port-forward to be ready
        Start-Sleep 5
        
        # Test health endpoint
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                Write-Status "✓ Health endpoint responding (status: $($response.StatusCode))" "Success"
            } else {
                Write-Status "⚠ Health endpoint returned status: $($response.StatusCode)" "Warning"
            }
        } catch {
            Write-Status "✗ Health endpoint not accessible: $($_.Exception.Message)" "Error"
        }
        
        # Cleanup port-forward
        Stop-Job $portForwardJob -ErrorAction SilentlyContinue
        Remove-Job $portForwardJob -ErrorAction SilentlyContinue
        
    } catch {
        Write-Status "Health check failed: $($_.Exception.Message)" "Error"
    }
    
    return $true
}

function Show-DeploymentCommands {
    Write-Header "DEPLOYMENT COMMANDS"
    
    Write-Status "To setup DevOps tools:" "Info"
    Write-Host "  .\scripts\setup-devops-tools.ps1" -ForegroundColor Gray
    Write-Host ""
    
    Write-Status "To build Docker image:" "Info"
    Write-Host "  .\scripts\build_docker.sh" -ForegroundColor Gray
    Write-Host "  # or for PowerShell:" -ForegroundColor Gray
    Write-Host "  docker buildx build --platform linux/amd64,linux/arm64 --tag zetaai/zeta-agent:latest ." -ForegroundColor Gray
    Write-Host ""
    
    Write-Status "To deploy to Kubernetes:" "Info"
    Write-Host "  .\scripts\deploy.ps1" -ForegroundColor Gray
    Write-Host "  # or step by step:" -ForegroundColor Gray
    Write-Host "  terraform -chdir=infra/terraform init" -ForegroundColor Gray
    Write-Host "  terraform -chdir=infra/terraform apply" -ForegroundColor Gray
    Write-Host "  helm upgrade --install zeta-agent infra/helm/zeta-agent --namespace $Namespace --create-namespace" -ForegroundColor Gray
    Write-Host ""
    
    Write-Status "To run integration tests:" "Info"
    Write-Host "  .\scripts\test_integration.sh" -ForegroundColor Gray
    Write-Host ""
    
    Write-Status "To check deployment status:" "Info"
    Write-Host "  kubectl get all --namespace $Namespace" -ForegroundColor Gray
    Write-Host "  helm list --namespace $Namespace" -ForegroundColor Gray
    Write-Host ""
}

function Show-Summary {
    param([bool]$AllPassed)
    
    Write-Header "VERIFICATION SUMMARY"
    
    if ($AllPassed) {
        Write-Status "🎉 All verifications passed!" "Success"
        Write-Status "Your environment is ready for Zeta AI Agent deployment." "Success"
    } else {
        Write-Status "⚠️  Some verifications failed or incomplete." "Warning"
        Write-Status "Please review the issues above before proceeding." "Warning"
    }
    
    Write-Host ""
    Write-Status "Environment: $Environment" "Info"
    Write-Status "Target Namespace: $Namespace" "Info"
    Write-Status "Verification Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "Info"
}

# Main verification process
Write-Header "ZETA AI AGENT - DEPLOYMENT VERIFICATION"
Write-Status "Starting deployment verification process..." "Info"
Write-Status "Environment: $Environment" "Info"
Write-Status "Namespace: $Namespace" "Info"

$allPassed = $true

# Run verifications
$allPassed = $allPassed -and (Test-Prerequisites)
$allPassed = $allPassed -and (Test-DockerEnvironment)
$allPassed = $allPassed -and (Test-KubernetesEnvironment)
$allPassed = $allPassed -and (Test-ZetaAgentDeployment)
$allPassed = $allPassed -and (Test-HealthEndpoints)

Show-DeploymentCommands
Show-Summary $allPassed

if (-not $allPassed) {
    exit 1
}
