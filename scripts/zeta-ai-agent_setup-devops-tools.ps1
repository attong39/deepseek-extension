# 🚀 DevOps Tools Installation Script for Zeta AI Agent
# 📋 Automated setup for Windows + Docker Desktop
# 💡 Run as Administrator for best results

param(
    [switch]$SkipDocker,
    [switch]$SkipKubernetes, 
    [switch]$SkipHelm,
    [switch]$SkipTerraform,
    [switch]$UseWinget,
    [switch]$QuickStart
)

# Colors for output
$Colors = @{
    Info = "Cyan"
    Success = "Green" 
    Warning = "Yellow"
    Error = "Red"
}

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Colors[$Type]
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-CommandExists {
    param([string]$Command)
    return Get-Command $Command -ErrorAction SilentlyContinue
}

function Install-Chocolatey {
    if (Test-CommandExists "choco") {
        Write-Status "Chocolatey is already installed" "Success"
        return
    }
    
    Write-Status "Installing Chocolatey package manager..." "Info"
    try {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Status "Chocolatey installed successfully" "Success"
    } catch {
        Write-Status "Failed to install Chocolatey: $($_.Exception.Message)" "Error"
        throw
    }
}

function Install-Package {
    param(
        [string]$PackageName,
        [string]$ChocoName,
        [string]$WingetName,
        [string]$Description
    )
    
    if (Test-CommandExists $PackageName) {
        Write-Status "$Description is already installed" "Success"
        return
    }
    
    Write-Status "Installing $Description..." "Info"
    
    try {
        if ($UseWinget -and (Test-CommandExists "winget")) {
            winget install $WingetName --accept-package-agreements --accept-source-agreements
        } else {
            choco install $ChocoName -y
        }
        
        if (Test-CommandExists $PackageName) {
            Write-Status "$Description installed successfully" "Success"
        } else {
            Write-Status "$Description installation may require PATH refresh" "Warning"
        }
    } catch {
        Write-Status "Failed to install $Description : $($_.Exception.Message)" "Error"
    }
}

function Test-DockerDesktop {
    Write-Status "Checking Docker Desktop status..." "Info"
    
    $dockerService = Get-Service -Name "com.docker.service" -ErrorAction SilentlyContinue
    if ($dockerService -and $dockerService.Status -eq "Running") {
        Write-Status "Docker Desktop service is running" "Success"
    } else {
        Write-Status "Docker Desktop service is not running - please start Docker Desktop" "Warning"
    }
    
    # Test Docker CLI
    try {
        $dockerVersion = docker --version 2>$null
        if ($dockerVersion) {
            Write-Status "Docker CLI: $dockerVersion" "Success"
        }
    } catch {
        Write-Status "Docker CLI not accessible - may need PATH refresh" "Warning"
    }
}

function Test-KubernetesCluster {
    Write-Status "Checking Kubernetes cluster connectivity..." "Info"
    
    try {
        $clusterInfo = kubectl cluster-info 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Kubernetes cluster is accessible" "Success"
            kubectl get nodes --no-headers 2>$null | ForEach-Object {
                Write-Status "Node: $($_.Split()[0]) - $($_.Split()[1])" "Info"
            }
        } else {
            Write-Status "Kubernetes cluster not accessible - check Docker Desktop Kubernetes or configure cluster" "Warning"
        }
    } catch {
        Write-Status "kubectl not accessible - may need PATH refresh" "Warning"
    }
}

function Show-PostInstallInstructions {
    Write-Host "`n" -NoNewline
    Write-Status "=== POST-INSTALLATION INSTRUCTIONS ===" "Info"
    Write-Host ""
    
    Write-Status "1. Restart PowerShell session to refresh PATH" "Warning"
    Write-Status "2. Start Docker Desktop if not already running" "Warning"
    Write-Status "3. Enable Kubernetes in Docker Desktop (Settings > Kubernetes > Enable)" "Warning"
    Write-Status "4. Wait for Kubernetes to start (green indicator in Docker Desktop)" "Warning"
    Write-Status "5. Verify installation with:" "Info"
    Write-Host "   docker --version" -ForegroundColor Gray
    Write-Host "   kubectl version --client" -ForegroundColor Gray
    Write-Host "   helm version" -ForegroundColor Gray
    Write-Host "   terraform version" -ForegroundColor Gray
    Write-Host ""
    
    Write-Status "6. Test Kubernetes connectivity:" "Info"
    Write-Host "   kubectl cluster-info" -ForegroundColor Gray
    Write-Host "   kubectl get nodes" -ForegroundColor Gray
    Write-Host ""
    
    Write-Status "7. Deploy Zeta AI Agent:" "Info"
    Write-Host "   .\scripts\deploy.ps1" -ForegroundColor Gray
    Write-Host ""
}

# Main installation process
Write-Status "Starting DevOps tools installation for Zeta AI Agent..." "Info"

if (-not (Test-Administrator)) {
    Write-Status "Warning: Not running as Administrator. Some installations may fail." "Warning"
    Write-Status "Consider running PowerShell as Administrator for best results." "Warning"
}

# Install package manager
if (-not $UseWinget) {
    Install-Chocolatey
}

# Install tools
if (-not $SkipDocker) {
    Install-Package "docker" "docker-desktop" "Docker.DockerDesktop" "Docker Desktop"
}

if (-not $SkipKubernetes) {
    Install-Package "kubectl" "kubernetes-cli" "Kubernetes.kubectl" "Kubernetes CLI (kubectl)"
}

if (-not $SkipHelm) {
    Install-Package "helm" "kubernetes-helm" "Helm.Helm" "Helm Package Manager"
}

if (-not $SkipTerraform) {
    Install-Package "terraform" "terraform" "HashiCorp.Terraform" "Terraform"
}

# Install Git if not present
if (-not (Test-CommandExists "git")) {
    Install-Package "git" "git" "Git.Git" "Git"
}

Write-Host "`n" -NoNewline
Write-Status "=== INSTALLATION SUMMARY ===" "Info"

# Test installations
$tools = @(
    @{Name="docker"; Description="Docker"},
    @{Name="kubectl"; Description="Kubernetes CLI"},
    @{Name="helm"; Description="Helm"},
    @{Name="terraform"; Description="Terraform"},
    @{Name="git"; Description="Git"}
)

foreach ($tool in $tools) {
    if (Test-CommandExists $tool.Name) {
        Write-Status "✓ $($tool.Description)" "Success"
    } else {
        Write-Status "✗ $($tool.Description) - not found in PATH" "Error"
    }
}

# Additional tests
Test-DockerDesktop
Test-KubernetesCluster

Show-PostInstallInstructions

Write-Status "Installation process completed!" "Success"
