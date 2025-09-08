#!/usr/bin/env powershell

# PowerShell deployment script for Zeta AI Agent
# Cross-platform deployment automation for Windows, Linux, and macOS

param(
    [Parameter(Position=0)]
    [ValidateSet("deploy", "build", "scan", "terraform", "helm", "health", "info", "cleanup", "help")]
    [string]$Command = "deploy",
    
    [Parameter(Position=1)]
    [string]$SubCommand = "",
    
    [string]$DockerRegistry = $(if ($env:DOCKER_REGISTRY) { $env:DOCKER_REGISTRY } else { "docker.io" }),
    [string]$DockerNamespace = $(if ($env:DOCKER_NAMESPACE) { $env:DOCKER_NAMESPACE } else { "zetaai" }),
    [string]$ImageName = $(if ($env:IMAGE_NAME) { $env:IMAGE_NAME } else { "zeta-agent" }),
    [string]$Version = $env:VERSION,
    [string]$Platforms = $(if ($env:PLATFORMS) { $env:PLATFORMS } else { "linux/amd64,linux/arm64" }),
    [string]$Environment = $(if ($env:ENVIRONMENT) { $env:ENVIRONMENT } else { "development" }),
    [string]$Namespace = $(if ($env:NAMESPACE) { $env:NAMESPACE } else { "zeta-agent" })
)

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Get version from git if not specified
if (-not $Version) {
    try {
        $Version = git rev-parse --short HEAD 2>$null
        if (-not $Version) { $Version = "latest" }
    } catch {
        $Version = "latest"
    }
}

# Logging functions with colors
function Write-LogInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-LogSuccess {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-LogWarning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if command exists
function Test-CommandExists {
    param([string]$Command)
    return Get-Command $Command -ErrorAction SilentlyContinue
}

# Check prerequisites
function Test-Prerequisites {
    Write-LogInfo "Checking prerequisites..."
    
    $MissingTools = @()
    
    if (-not (Test-CommandExists "docker")) { $MissingTools += "docker" }
    if (-not (Test-CommandExists "kubectl")) { $MissingTools += "kubectl" }
    if (-not (Test-CommandExists "helm")) { $MissingTools += "helm" }
    if (-not (Test-CommandExists "terraform")) { $MissingTools += "terraform" }
    if (-not (Test-CommandExists "git")) { $MissingTools += "git" }
    
    if ($MissingTools.Count -gt 0) {
        Write-LogError "Missing required tools: $($MissingTools -join ', ')"
        Write-LogError "Please install the missing tools and try again."
        exit 1
    }
    
    # Check Docker buildx
    try {
        docker buildx version | Out-Null
    } catch {
        Write-LogError "Docker buildx is required for multi-platform builds"
        exit 1
    }
    
    # Check if Docker daemon is running
    try {
        docker info | Out-Null
    } catch {
        Write-LogError "Docker daemon is not running"
        exit 1
    }
    
    Write-LogSuccess "All prerequisites satisfied"
}

# Build Docker image
function Invoke-DockerBuild {
    Write-LogInfo "Building Docker image..."
    
    $FullImageName = "$DockerRegistry/$DockerNamespace/$ImageName`:$Version"
    $LatestImageName = "$DockerRegistry/$DockerNamespace/$ImageName`:latest"
    
    # Create buildx builder if it doesn't exist
    $BuilderExists = docker buildx ls | Select-String "zeta-builder"
    if (-not $BuilderExists) {
        Write-LogInfo "Creating Docker buildx builder..."
        docker buildx create --name zeta-builder --use
    } else {
        docker buildx use zeta-builder
    }
    
    # Build and push multi-platform image
    Write-LogInfo "Building multi-platform image: $FullImageName"
    
    $BuildArgs = @(
        "buildx", "build",
        "--platform", $Platforms,
        "--tag", $FullImageName,
        "--tag", $LatestImageName,
        "--push",
        "--file", "$ProjectRoot/Dockerfile",
        $ProjectRoot
    )
    
    $Process = Start-Process -FilePath "docker" -ArgumentList $BuildArgs -Wait -PassThru -NoNewWindow
    
    if ($Process.ExitCode -ne 0) {
        Write-LogError "Docker build failed"
        exit 1
    }
    
    Write-LogSuccess "Docker image built and pushed: $FullImageName"
}

# Security scan
function Invoke-SecurityScan {
    Write-LogInfo "Running security scan..."
    
    $ImageNameScan = "$DockerRegistry/$DockerNamespace/$ImageName`:$Version"
    
    # Check for available security scanners
    if (Test-CommandExists "trivy") {
        Write-LogInfo "Running Trivy security scan..."
        try {
            trivy image $ImageNameScan
        } catch {
            Write-LogWarning "Security scan completed with warnings"
        }
    } elseif (Test-CommandExists "docker-scout") {
        Write-LogInfo "Running Docker Scout security scan..."
        try {
            docker scout cves $ImageNameScan
        } catch {
            Write-LogWarning "Security scan completed with warnings"
        }
    } else {
        Write-LogWarning "No security scanner available (trivy or docker-scout recommended)"
    }
    
    Write-LogSuccess "Security scan completed"
}

# Terraform operations
function Invoke-TerraformOperation {
    param([string]$Operation = "plan")
    
    $TfDir = "$ProjectRoot/infra/terraform"
    
    Write-LogInfo "Running Terraform $Operation..."
    
    if (-not (Test-Path $TfDir)) {
        Write-LogError "Terraform directory not found: $TfDir"
        exit 1
    }
    
    Push-Location $TfDir
    
    try {
        # Initialize Terraform
        terraform init -upgrade
        
        # Set environment variables
        $env:TF_VAR_environment = $Environment
        $env:TF_VAR_namespace = $Namespace
        $env:TF_VAR_image_tag = $Version
        $env:TF_VAR_image_repository = "$DockerRegistry/$DockerNamespace/$ImageName"
        
        switch ($Operation) {
            "plan" {
                terraform plan -out=tfplan
            }
            "apply" {
                terraform apply -auto-approve tfplan
            }
            "destroy" {
                terraform destroy -auto-approve
            }
            default {
                Write-LogError "Unknown Terraform operation: $Operation"
                exit 1
            }
        }
    } finally {
        Pop-Location
    }
    
    Write-LogSuccess "Terraform $Operation completed"
}

# Helm operations
function Invoke-HelmOperation {
    param([string]$Operation = "install")
    
    $HelmDir = "$ProjectRoot/infra/helm/zeta-agent"
    $ReleaseName = "zeta-agent"
    
    Write-LogInfo "Running Helm $Operation..."
    
    if (-not (Test-Path $HelmDir)) {
        Write-LogError "Helm chart directory not found: $HelmDir"
        exit 1
    }
    
    # Check if namespace exists, create if not
    try {
        kubectl get namespace $Namespace | Out-Null
    } catch {
        Write-LogInfo "Creating namespace: $Namespace"
        kubectl create namespace $Namespace
    }
    
    # Prepare values file
    $ValuesFile = "$HelmDir/values-$Environment.yaml"
    if (-not (Test-Path $ValuesFile)) {
        $ValuesFile = "$HelmDir/values.yaml"
    }
    
    $HelmArgs = @()
    
    switch ($Operation) {
        "install" {
            $HelmArgs = @(
                "upgrade", "--install", $ReleaseName, $HelmDir,
                "--namespace", $Namespace,
                "--values", $ValuesFile,
                "--set", "image.tag=$Version",
                "--set", "image.repository=$DockerRegistry/$DockerNamespace/$ImageName",
                "--wait",
                "--timeout=300s"
            )
        }
        "upgrade" {
            $HelmArgs = @(
                "upgrade", $ReleaseName, $HelmDir,
                "--namespace", $Namespace,
                "--values", $ValuesFile,
                "--set", "image.tag=$Version",
                "--set", "image.repository=$DockerRegistry/$DockerNamespace/$ImageName",
                "--wait",
                "--timeout=300s"
            )
        }
        "uninstall" {
            $HelmArgs = @("uninstall", $ReleaseName, "--namespace", $Namespace)
        }
        "test" {
            $HelmArgs = @("test", $ReleaseName, "--namespace", $Namespace)
        }
        default {
            Write-LogError "Unknown Helm operation: $Operation"
            exit 1
        }
    }
    
    $Process = Start-Process -FilePath "helm" -ArgumentList $HelmArgs -Wait -PassThru -NoNewWindow
    
    if ($Process.ExitCode -ne 0) {
        Write-LogError "Helm $Operation failed"
        exit 1
    }
    
    Write-LogSuccess "Helm $Operation completed"
}

# Wait for deployment
function Wait-ForDeployment {
    Write-LogInfo "Waiting for deployment to be ready..."
    
    # Wait for rollout
    $RolloutArgs = @(
        "rollout", "status", "deployment/zeta-agent",
        "--namespace=$Namespace",
        "--timeout=300s"
    )
    
    $Process = Start-Process -FilePath "kubectl" -ArgumentList $RolloutArgs -Wait -PassThru -NoNewWindow
    
    if ($Process.ExitCode -ne 0) {
        Write-LogError "Deployment rollout failed"
        exit 1
    }
    
    # Wait for pods to be ready
    $WaitArgs = @(
        "wait", "--for=condition=ready", "pod",
        "--selector=app.kubernetes.io/name=zeta-agent",
        "--namespace=$Namespace",
        "--timeout=300s"
    )
    
    $Process = Start-Process -FilePath "kubectl" -ArgumentList $WaitArgs -Wait -PassThru -NoNewWindow
    
    if ($Process.ExitCode -ne 0) {
        Write-LogError "Pods failed to become ready"
        exit 1
    }
    
    Write-LogSuccess "Deployment is ready"
}

# Health check
function Test-Health {
    Write-LogInfo "Running health check..."
    
    # Get service port
    try {
        $ServicePort = kubectl get service zeta-agent --namespace=$Namespace --output=jsonpath='{.spec.ports[0].port}' 2>$null
        if (-not $ServicePort) { $ServicePort = "3000" }
    } catch {
        $ServicePort = "3000"
    }
    
    # Start port forward
    Write-LogInfo "Port forwarding for health check..."
    $PortForwardJob = Start-Job -ScriptBlock {
        param($ServicePort, $Namespace)
        kubectl port-forward service/zeta-agent 8080:$ServicePort --namespace=$Namespace
    } -ArgumentList $ServicePort, $Namespace
    
    # Wait for port forward to be ready
    Start-Sleep 5
    
    # Health check
    $HealthUrl = "http://localhost:8080/health"
    $MaxAttempts = 10
    $Attempt = 1
    $HealthCheckPassed = $false
    
    while ($Attempt -le $MaxAttempts) {
        try {
            $Response = Invoke-WebRequest -Uri $HealthUrl -UseBasicParsing -TimeoutSec 5
            if ($Response.StatusCode -eq 200) {
                Write-LogSuccess "Health check passed"
                $HealthCheckPassed = $true
                break
            }
        } catch {
            Write-LogInfo "Health check attempt $Attempt/$MaxAttempts failed, retrying..."
            Start-Sleep 10
            $Attempt++
        }
    }
    
    # Cleanup port forward
    Stop-Job $PortForwardJob -ErrorAction SilentlyContinue
    Remove-Job $PortForwardJob -ErrorAction SilentlyContinue
    
    if (-not $HealthCheckPassed) {
        Write-LogError "Health check failed after $MaxAttempts attempts"
        exit 1
    }
}

# Cleanup resources
function Invoke-Cleanup {
    Write-LogInfo "Cleaning up resources..."
    
    # Remove buildx builder
    try {
        $BuilderExists = docker buildx ls | Select-String "zeta-builder"
        if ($BuilderExists) {
            docker buildx rm zeta-builder 2>$null
        }
    } catch {
        # Ignore cleanup errors
    }
    
    # Stop any port forward jobs
    Get-Job | Where-Object { $_.Command -like "*kubectl port-forward*" } | Stop-Job -ErrorAction SilentlyContinue
    Get-Job | Where-Object { $_.Command -like "*kubectl port-forward*" } | Remove-Job -ErrorAction SilentlyContinue
    
    Write-LogSuccess "Cleanup completed"
}

# Show deployment info
function Show-DeploymentInfo {
    Write-LogInfo "Deployment Information:"
    Write-Host "=========================="
    Write-Host "Environment: $Environment"
    Write-Host "Namespace: $Namespace" 
    Write-Host "Image: $DockerRegistry/$DockerNamespace/$ImageName`:$Version"
    Write-Host "=========================="
    
    # Show pods
    Write-LogInfo "Pods:"
    kubectl get pods --namespace=$Namespace -l app.kubernetes.io/name=zeta-agent
    
    # Show services
    Write-LogInfo "Services:"
    kubectl get services --namespace=$Namespace
    
    # Show ingress if exists
    try {
        $IngressExists = kubectl get ingress --namespace=$Namespace 2>$null | Select-String "zeta-agent"
        if ($IngressExists) {
            Write-LogInfo "Ingress:"
            kubectl get ingress --namespace=$Namespace
        }
    } catch {
        # Ignore if ingress doesn't exist
    }
}

# Main deployment function
function Invoke-Deploy {
    Write-LogInfo "Starting deployment process..."
    
    Test-Prerequisites
    Invoke-DockerBuild
    Invoke-SecurityScan
    Invoke-TerraformOperation "plan"
    Invoke-TerraformOperation "apply"
    Invoke-HelmOperation "install"
    Wait-ForDeployment
    Test-Health
    Show-DeploymentInfo
    
    Write-LogSuccess "Deployment completed successfully!"
}

# Show usage
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [COMMAND] [OPTIONS]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  deploy              Full deployment (build, provision, deploy)"
    Write-Host "  build               Build Docker image only"
    Write-Host "  scan                Security scan only"
    Write-Host "  terraform [plan|apply|destroy]"
    Write-Host "  helm [install|upgrade|uninstall|test]"
    Write-Host "  health              Health check only"
    Write-Host "  info                Show deployment info"
    Write-Host "  cleanup             Cleanup resources"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -DockerRegistry     Docker registry (default: docker.io)"
    Write-Host "  -DockerNamespace    Docker namespace (default: zetaai)"
    Write-Host "  -ImageName          Image name (default: zeta-agent)"
    Write-Host "  -Version            Image version (default: git short hash)"
    Write-Host "  -Platforms          Build platforms (default: linux/amd64,linux/arm64)"
    Write-Host "  -Environment        Environment (default: development)"
    Write-Host "  -Namespace          Kubernetes namespace (default: zeta-agent)"
}

# Trap cleanup on exit
Register-EngineEvent PowerShell.Exiting -Action { Invoke-Cleanup }

# Main script logic
try {
    switch ($Command) {
        "deploy" {
            Invoke-Deploy
        }
        "build" {
            Test-Prerequisites
            Invoke-DockerBuild
        }
        "scan" {
            Invoke-SecurityScan
        }
        "terraform" {
            Invoke-TerraformOperation $SubCommand
        }
        "helm" {
            Invoke-HelmOperation $SubCommand
        }
        "health" {
            Test-Health
        }
        "info" {
            Show-DeploymentInfo
        }
        "cleanup" {
            Invoke-Cleanup
        }
        "help" {
            Show-Usage
        }
        default {
            Write-LogError "Unknown command: $Command"
            Show-Usage
            exit 1
        }
    }
} finally {
    Invoke-Cleanup
}
