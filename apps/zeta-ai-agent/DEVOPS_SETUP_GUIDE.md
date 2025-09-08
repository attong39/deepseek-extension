# Zeta AI Agent - DevOps Tools Setup Guide

## Prerequisites Installation

### 1. Docker Desktop (Required)
```powershell
# Download and install Docker Desktop for Windows
# https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

# Or using Chocolatey
choco install docker-desktop

# Or using winget
winget install Docker.DockerDesktop
```

### 2. Kubernetes CLI (kubectl)
```powershell
# Using Chocolatey
choco install kubernetes-cli

# Or using winget
winget install Kubernetes.kubectl

# Or manual download
curl.exe -LO "https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe"
```

### 3. Helm Package Manager
```powershell
# Using Chocolatey
choco install kubernetes-helm

# Or using winget
winget install Helm.Helm

# Or using PowerShell
Invoke-WebRequest -Uri "https://get.helm.sh/helm-v3.12.0-windows-amd64.zip" -OutFile "helm.zip"
Expand-Archive -Path "helm.zip" -DestinationPath "C:\helm"
# Add C:\helm\windows-amd64 to PATH
```

### 4. Terraform
```powershell
# Using Chocolatey
choco install terraform

# Or using winget
winget install HashiCorp.Terraform

# Or manual download
Invoke-WebRequest -Uri "https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_windows_amd64.zip" -OutFile "terraform.zip"
```

### 5. Git (if not installed)
```powershell
# Using winget
winget install Git.Git

# Or using Chocolatey
choco install git
```

## Quick Setup Script

Save this as `setup-devops-tools.ps1`:

```powershell
# Check if Chocolatey is installed
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install DevOps tools
Write-Host "Installing DevOps tools..." -ForegroundColor Green
choco install docker-desktop kubernetes-cli kubernetes-helm terraform git -y

Write-Host "Setup completed! Please restart your PowerShell session." -ForegroundColor Green
Write-Host "Note: Docker Desktop requires a restart after installation." -ForegroundColor Yellow
```

## Kubernetes Cluster Options

### Option 1: Docker Desktop Kubernetes (Recommended for development)
1. Install Docker Desktop
2. Enable Kubernetes in Docker Desktop settings
3. Wait for Kubernetes to start

### Option 2: Minikube
```powershell
choco install minikube
minikube start --driver=docker
```

### Option 3: Kind (Kubernetes in Docker)
```powershell
choco install kind
kind create cluster --name zeta-cluster
```

### Option 4: Cloud Providers
- **Azure AKS**: `az aks create`
- **AWS EKS**: `eksctl create cluster`
- **Google GKE**: `gcloud container clusters create`

## Verification Commands

After installation, verify with:
```powershell
docker --version
kubectl version --client
helm version
terraform version
git --version

# Test Kubernetes connection
kubectl cluster-info
kubectl get nodes
```

## Next Steps

1. **Install tools**: Run the setup script above
2. **Restart PowerShell**: To pick up PATH changes
3. **Start Docker Desktop**: And enable Kubernetes
4. **Run verification**: Use the commands above
5. **Deploy Zeta Agent**: Use `.\scripts\deploy.ps1`

## Troubleshooting

### Docker Issues
- Ensure Docker Desktop is running
- Check Windows features: Hyper-V, WSL2
- Restart Docker service: `Restart-Service docker`

### Kubernetes Issues
- Verify cluster connection: `kubectl cluster-info`
- Check context: `kubectl config current-context`
- Switch context if needed: `kubectl config use-context docker-desktop`

### PATH Issues
- Add tool directories to system PATH
- Restart PowerShell session
- Use full paths if needed: `C:\Program Files\Docker\Docker\resources\bin\kubectl.exe`
