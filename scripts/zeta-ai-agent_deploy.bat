@echo off
setlocal enabledelayedexpansion

REM Build and deployment automation scripts for Zeta AI Agent (Windows)
REM This script handles Docker builds, infrastructure provisioning, and deployment

REM Configuration
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
if not defined DOCKER_REGISTRY set "DOCKER_REGISTRY=docker.io"
if not defined DOCKER_NAMESPACE set "DOCKER_NAMESPACE=zetaai"
if not defined IMAGE_NAME set "IMAGE_NAME=zeta-agent"
if not defined PLATFORMS set "PLATFORMS=linux/amd64,linux/arm64"
if not defined ENVIRONMENT set "ENVIRONMENT=development"
if not defined NAMESPACE set "NAMESPACE=zeta-agent"

REM Get version from git or use 'latest'
for /f "delims=" %%i in ('git rev-parse --short HEAD 2^>nul') do set "VERSION=%%i"
if not defined VERSION set "VERSION=latest"

REM Colors for output (Windows compatible)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Logging functions
:log_info
echo %BLUE%[INFO]%NC% %~1
goto :eof

:log_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:log_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:log_error
echo %RED%[ERROR]%NC% %~1
goto :eof

REM Check if command exists
:command_exists
where %1 >nul 2>&1
goto :eof

REM Check prerequisites
:check_prerequisites
call :log_info "Checking prerequisites..."

call :command_exists docker
if errorlevel 1 (
    call :log_error "Docker is not installed or not in PATH"
    exit /b 1
)

call :command_exists kubectl
if errorlevel 1 (
    call :log_error "kubectl is not installed or not in PATH"
    exit /b 1
)

call :command_exists helm
if errorlevel 1 (
    call :log_error "helm is not installed or not in PATH"
    exit /b 1
)

call :command_exists terraform
if errorlevel 1 (
    call :log_error "terraform is not installed or not in PATH"
    exit /b 1
)

call :command_exists git
if errorlevel 1 (
    call :log_error "git is not installed or not in PATH"
    exit /b 1
)

REM Check Docker buildx
docker buildx version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker buildx is required for multi-platform builds"
    exit /b 1
)

REM Check if Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker daemon is not running"
    exit /b 1
)

call :log_success "All prerequisites satisfied"
goto :eof

REM Build Docker image
:build_docker
call :log_info "Building Docker image..."

set "FULL_IMAGE_NAME=%DOCKER_REGISTRY%/%DOCKER_NAMESPACE%/%IMAGE_NAME%:%VERSION%"
set "LATEST_IMAGE_NAME=%DOCKER_REGISTRY%/%DOCKER_NAMESPACE%/%IMAGE_NAME%:latest"

REM Check if buildx builder exists
docker buildx ls | findstr "zeta-builder" >nul
if errorlevel 1 (
    call :log_info "Creating Docker buildx builder..."
    docker buildx create --name zeta-builder --use
) else (
    docker buildx use zeta-builder
)

REM Build and push multi-platform image
call :log_info "Building multi-platform image: %FULL_IMAGE_NAME%"
docker buildx build ^
    --platform %PLATFORMS% ^
    --tag %FULL_IMAGE_NAME% ^
    --tag %LATEST_IMAGE_NAME% ^
    --push ^
    --file "%PROJECT_ROOT%\Dockerfile" ^
    "%PROJECT_ROOT%"

if errorlevel 1 (
    call :log_error "Docker build failed"
    exit /b 1
)

call :log_success "Docker image built and pushed: %FULL_IMAGE_NAME%"
goto :eof

REM Security scan
:security_scan
call :log_info "Running security scan..."

set "IMAGE_NAME_SCAN=%DOCKER_REGISTRY%/%DOCKER_NAMESPACE%/%IMAGE_NAME%:%VERSION%"

REM Check for security scanners
call :command_exists trivy
if not errorlevel 1 (
    call :log_info "Running Trivy security scan..."
    trivy image %IMAGE_NAME_SCAN%
    if errorlevel 1 (
        call :log_warning "Security scan completed with warnings"
    )
) else (
    call :log_warning "No security scanner available (trivy recommended)"
)

call :log_success "Security scan completed"
goto :eof

REM Terraform operations
:terraform_operations
set "OPERATION=%~1"
if "%OPERATION%"=="" set "OPERATION=plan"
set "TF_DIR=%PROJECT_ROOT%\infra\terraform"

call :log_info "Running Terraform %OPERATION%..."

if not exist "%TF_DIR%" (
    call :log_error "Terraform directory not found: %TF_DIR%"
    exit /b 1
)

pushd "%TF_DIR%"

REM Initialize Terraform
terraform init -upgrade

REM Set variables
set "TF_VAR_environment=%ENVIRONMENT%"
set "TF_VAR_namespace=%NAMESPACE%"
set "TF_VAR_image_tag=%VERSION%"
set "TF_VAR_image_repository=%DOCKER_REGISTRY%/%DOCKER_NAMESPACE%/%IMAGE_NAME%"

if "%OPERATION%"=="plan" (
    terraform plan -out=tfplan
) else if "%OPERATION%"=="apply" (
    terraform apply -auto-approve tfplan
) else if "%OPERATION%"=="destroy" (
    terraform destroy -auto-approve
) else (
    call :log_error "Unknown Terraform operation: %OPERATION%"
    popd
    exit /b 1
)

popd
call :log_success "Terraform %OPERATION% completed"
goto :eof

REM Helm operations
:helm_operations
set "OPERATION=%~1"
if "%OPERATION%"=="" set "OPERATION=install"
set "HELM_DIR=%PROJECT_ROOT%\infra\helm\zeta-agent"
set "RELEASE_NAME=zeta-agent"

call :log_info "Running Helm %OPERATION%..."

if not exist "%HELM_DIR%" (
    call :log_error "Helm chart directory not found: %HELM_DIR%"
    exit /b 1
)

REM Check if namespace exists, create if not
kubectl get namespace %NAMESPACE% >nul 2>&1
if errorlevel 1 (
    call :log_info "Creating namespace: %NAMESPACE%"
    kubectl create namespace %NAMESPACE%
)

REM Prepare values
set "VALUES_FILE=%HELM_DIR%\values-%ENVIRONMENT%.yaml"
if not exist "%VALUES_FILE%" (
    set "VALUES_FILE=%HELM_DIR%\values.yaml"
)

if "%OPERATION%"=="install" (
    helm upgrade --install %RELEASE_NAME% "%HELM_DIR%" ^
        --namespace %NAMESPACE% ^
        --values "%VALUES_FILE%" ^
        --set image.tag=%VERSION% ^
        --set image.repository=%DOCKER_REGISTRY%/%DOCKER_NAMESPACE%/%IMAGE_NAME% ^
        --wait ^
        --timeout=300s
) else if "%OPERATION%"=="upgrade" (
    helm upgrade %RELEASE_NAME% "%HELM_DIR%" ^
        --namespace %NAMESPACE% ^
        --values "%VALUES_FILE%" ^
        --set image.tag=%VERSION% ^
        --set image.repository=%DOCKER_REGISTRY%/%DOCKER_NAMESPACE%/%IMAGE_NAME% ^
        --wait ^
        --timeout=300s
) else if "%OPERATION%"=="uninstall" (
    helm uninstall %RELEASE_NAME% --namespace %NAMESPACE%
) else if "%OPERATION%"=="test" (
    helm test %RELEASE_NAME% --namespace %NAMESPACE%
) else (
    call :log_error "Unknown Helm operation: %OPERATION%"
    exit /b 1
)

call :log_success "Helm %OPERATION% completed"
goto :eof

REM Wait for deployment
:wait_for_deployment
call :log_info "Waiting for deployment to be ready..."

kubectl rollout status deployment/zeta-agent ^
    --namespace=%NAMESPACE% ^
    --timeout=300s

if errorlevel 1 (
    call :log_error "Deployment rollout failed"
    exit /b 1
)

REM Wait for pods to be ready
kubectl wait --for=condition=ready pod ^
    --selector=app.kubernetes.io/name=zeta-agent ^
    --namespace=%NAMESPACE% ^
    --timeout=300s

if errorlevel 1 (
    call :log_error "Pods failed to become ready"
    exit /b 1
)

call :log_success "Deployment is ready"
goto :eof

REM Health check
:health_check
call :log_info "Running health check..."

REM Get service information
for /f "delims=" %%i in ('kubectl get service zeta-agent --namespace=%NAMESPACE% --output=jsonpath^="{.spec.ports[0].port}" 2^>nul') do set "SERVICE_PORT=%%i"
if not defined SERVICE_PORT set "SERVICE_PORT=3000"

REM Port forward for health check
call :log_info "Port forwarding for health check..."
start /b kubectl port-forward service/zeta-agent 8080:%SERVICE_PORT% --namespace=%NAMESPACE%

REM Wait for port forward to be ready
timeout /t 5 /nobreak >nul

REM Health check with curl (if available) or powershell
call :command_exists curl
if not errorlevel 1 (
    set "HEALTH_CMD=curl -f http://localhost:8080/health"
) else (
    set "HEALTH_CMD=powershell -command "try { Invoke-WebRequest -Uri 'http://localhost:8080/health' -UseBasicParsing | Out-Null; exit 0 } catch { exit 1 }""
)

set "MAX_ATTEMPTS=10"
set "ATTEMPT=1"

:health_check_loop
%HEALTH_CMD% >nul 2>&1
if not errorlevel 1 (
    call :log_success "Health check passed"
    REM Kill port forward
    taskkill /f /im kubectl.exe >nul 2>&1
    goto :eof
)

call :log_info "Health check attempt %ATTEMPT%/%MAX_ATTEMPTS% failed, retrying..."
timeout /t 10 /nobreak >nul
set /a ATTEMPT+=1
if %ATTEMPT% leq %MAX_ATTEMPTS% goto health_check_loop

REM Kill port forward
taskkill /f /im kubectl.exe >nul 2>&1
call :log_error "Health check failed after %MAX_ATTEMPTS% attempts"
exit /b 1

REM Cleanup resources
:cleanup
call :log_info "Cleaning up resources..."

REM Remove buildx builder
docker buildx ls | findstr "zeta-builder" >nul
if not errorlevel 1 (
    docker buildx rm zeta-builder 2>nul
)

REM Kill any remaining port forwards
taskkill /f /im kubectl.exe >nul 2>&1

call :log_success "Cleanup completed"
goto :eof

REM Show deployment info
:show_deployment_info
call :log_info "Deployment Information:"
echo ==========================
echo Environment: %ENVIRONMENT%
echo Namespace: %NAMESPACE%
echo Image: %DOCKER_REGISTRY%/%DOCKER_NAMESPACE%/%IMAGE_NAME%:%VERSION%
echo ==========================

REM Show pods
call :log_info "Pods:"
kubectl get pods --namespace=%NAMESPACE% -l app.kubernetes.io/name=zeta-agent

REM Show services
call :log_info "Services:"
kubectl get services --namespace=%NAMESPACE%

REM Show ingress if exists
kubectl get ingress --namespace=%NAMESPACE% 2>nul | findstr zeta-agent >nul
if not errorlevel 1 (
    call :log_info "Ingress:"
    kubectl get ingress --namespace=%NAMESPACE%
)
goto :eof

REM Main deployment function
:deploy
call :log_info "Starting deployment process..."

call :check_prerequisites
if errorlevel 1 exit /b 1

call :build_docker
if errorlevel 1 exit /b 1

call :security_scan
if errorlevel 1 exit /b 1

call :terraform_operations "plan"
if errorlevel 1 exit /b 1

call :terraform_operations "apply"
if errorlevel 1 exit /b 1

call :helm_operations "install"
if errorlevel 1 exit /b 1

call :wait_for_deployment
if errorlevel 1 exit /b 1

call :health_check
if errorlevel 1 exit /b 1

call :show_deployment_info

call :log_success "Deployment completed successfully!"
goto :eof

REM Show usage
:usage
echo Usage: %~nx0 [COMMAND] [OPTIONS]
echo.
echo Commands:
echo   deploy              Full deployment (build, provision, deploy)
echo   build               Build Docker image only
echo   scan                Security scan only
echo   terraform [plan^|apply^|destroy]
echo   helm [install^|upgrade^|uninstall^|test]
echo   health              Health check only
echo   info                Show deployment info
echo   cleanup             Cleanup resources
echo.
echo Environment Variables:
echo   DOCKER_REGISTRY     Docker registry (default: docker.io)
echo   DOCKER_NAMESPACE    Docker namespace (default: zetaai)
echo   IMAGE_NAME          Image name (default: zeta-agent)
echo   VERSION             Image version (default: git short hash)
echo   PLATFORMS           Build platforms (default: linux/amd64,linux/arm64)
echo   ENVIRONMENT         Environment (default: development)
echo   NAMESPACE           Kubernetes namespace (default: zeta-agent)
goto :eof

REM Main script logic
set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=deploy"

if "%COMMAND%"=="deploy" (
    call :deploy
) else if "%COMMAND%"=="build" (
    call :check_prerequisites
    if not errorlevel 1 call :build_docker
) else if "%COMMAND%"=="scan" (
    call :security_scan
) else if "%COMMAND%"=="terraform" (
    call :terraform_operations "%~2"
) else if "%COMMAND%"=="helm" (
    call :helm_operations "%~2"
) else if "%COMMAND%"=="health" (
    call :health_check
) else if "%COMMAND%"=="info" (
    call :show_deployment_info
) else if "%COMMAND%"=="cleanup" (
    call :cleanup
) else if "%COMMAND%"=="help" (
    call :usage
) else if "%COMMAND%"=="--help" (
    call :usage
) else if "%COMMAND%"=="-h" (
    call :usage
) else (
    call :log_error "Unknown command: %COMMAND%"
    call :usage
    exit /b 1
)

REM Cleanup on exit
call :cleanup

endlocal
