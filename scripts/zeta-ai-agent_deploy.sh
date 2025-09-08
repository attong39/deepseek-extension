#!/bin/bash

# Build and deployment automation scripts for Zeta AI Agent
# This script handles Docker builds, infrastructure provisioning, and deployment

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCKER_REGISTRY="${DOCKER_REGISTRY:-docker.io}"
DOCKER_NAMESPACE="${DOCKER_NAMESPACE:-zetaai}"
IMAGE_NAME="${IMAGE_NAME:-zeta-agent}"
VERSION="${VERSION:-$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"
ENVIRONMENT="${ENVIRONMENT:-development}"
NAMESPACE="${NAMESPACE:-zeta-agent}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command_exists docker; then
        missing_tools+=("docker")
    fi
    
    if ! command_exists kubectl; then
        missing_tools+=("kubectl")
    fi
    
    if ! command_exists helm; then
        missing_tools+=("helm")
    fi
    
    if ! command_exists terraform; then
        missing_tools+=("terraform")
    fi
    
    if ! command_exists git; then
        missing_tools+=("git")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_error "Please install the missing tools and try again."
        exit 1
    fi
    
    # Check Docker buildx
    if ! docker buildx version >/dev/null 2>&1; then
        log_error "Docker buildx is required for multi-platform builds"
        exit 1
    fi
    
    # Check if logged into Docker registry
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    log_success "All prerequisites satisfied"
}

# Build Docker image
build_docker() {
    log_info "Building Docker image..."
    
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${VERSION}"
    local latest_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:latest"
    
    # Create buildx builder if it doesn't exist
    if ! docker buildx ls | grep -q "zeta-builder"; then
        log_info "Creating Docker buildx builder..."
        docker buildx create --name zeta-builder --use
    else
        docker buildx use zeta-builder
    fi
    
    # Build and push multi-platform image
    log_info "Building multi-platform image: $full_image_name"
    docker buildx build \
        --platform "$PLATFORMS" \
        --tag "$full_image_name" \
        --tag "$latest_image_name" \
        --push \
        --file "$PROJECT_ROOT/Dockerfile" \
        "$PROJECT_ROOT"
    
    log_success "Docker image built and pushed: $full_image_name"
}

# Security scan
security_scan() {
    log_info "Running security scan..."
    
    local image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${VERSION}"
    
    # Use Docker Scout if available, fallback to basic checks
    if command_exists docker-scout; then
        log_info "Running Docker Scout security scan..."
        docker scout cves "$image_name" || log_warning "Security scan completed with warnings"
    elif command_exists trivy; then
        log_info "Running Trivy security scan..."
        trivy image "$image_name" || log_warning "Security scan completed with warnings"
    else
        log_warning "No security scanner available (docker-scout or trivy recommended)"
    fi
    
    log_success "Security scan completed"
}

# Terraform operations
terraform_operations() {
    local operation="${1:-plan}"
    local tf_dir="$PROJECT_ROOT/infra/terraform"
    
    log_info "Running Terraform $operation..."
    
    if [ ! -d "$tf_dir" ]; then
        log_error "Terraform directory not found: $tf_dir"
        exit 1
    fi
    
    cd "$tf_dir"
    
    # Initialize Terraform
    terraform init -upgrade
    
    # Set variables
    export TF_VAR_environment="$ENVIRONMENT"
    export TF_VAR_namespace="$NAMESPACE"
    export TF_VAR_image_tag="$VERSION"
    export TF_VAR_image_repository="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}"
    
    case "$operation" in
        "plan")
            terraform plan -out=tfplan
            ;;
        "apply")
            terraform apply -auto-approve tfplan
            ;;
        "destroy")
            terraform destroy -auto-approve
            ;;
        *)
            log_error "Unknown Terraform operation: $operation"
            exit 1
            ;;
    esac
    
    cd "$PROJECT_ROOT"
    log_success "Terraform $operation completed"
}

# Helm operations
helm_operations() {
    local operation="${1:-install}"
    local helm_dir="$PROJECT_ROOT/infra/helm/zeta-agent"
    local release_name="zeta-agent"
    
    log_info "Running Helm $operation..."
    
    if [ ! -d "$helm_dir" ]; then
        log_error "Helm chart directory not found: $helm_dir"
        exit 1
    fi
    
    # Check if namespace exists, create if not
    if ! kubectl get namespace "$NAMESPACE" >/dev/null 2>&1; then
        log_info "Creating namespace: $NAMESPACE"
        kubectl create namespace "$NAMESPACE"
    fi
    
    # Prepare values
    local values_file="$helm_dir/values-$ENVIRONMENT.yaml"
    if [ ! -f "$values_file" ]; then
        values_file="$helm_dir/values.yaml"
    fi
    
    case "$operation" in
        "install")
            helm upgrade --install "$release_name" "$helm_dir" \
                --namespace "$NAMESPACE" \
                --values "$values_file" \
                --set image.tag="$VERSION" \
                --set image.repository="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}" \
                --wait \
                --timeout=300s
            ;;
        "upgrade")
            helm upgrade "$release_name" "$helm_dir" \
                --namespace "$NAMESPACE" \
                --values "$values_file" \
                --set image.tag="$VERSION" \
                --set image.repository="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}" \
                --wait \
                --timeout=300s
            ;;
        "uninstall")
            helm uninstall "$release_name" --namespace "$NAMESPACE"
            ;;
        "test")
            helm test "$release_name" --namespace "$NAMESPACE"
            ;;
        *)
            log_error "Unknown Helm operation: $operation"
            exit 1
            ;;
    esac
    
    log_success "Helm $operation completed"
}

# Wait for deployment
wait_for_deployment() {
    log_info "Waiting for deployment to be ready..."
    
    kubectl rollout status deployment/zeta-agent \
        --namespace="$NAMESPACE" \
        --timeout=300s
    
    # Wait for pods to be ready
    kubectl wait --for=condition=ready pod \
        --selector=app.kubernetes.io/name=zeta-agent \
        --namespace="$NAMESPACE" \
        --timeout=300s
    
    log_success "Deployment is ready"
}

# Health check
health_check() {
    log_info "Running health check..."
    
    # Get service information
    local service_name="zeta-agent"
    local service_port=$(kubectl get service "$service_name" \
        --namespace="$NAMESPACE" \
        --output=jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "3000")
    
    # Port forward for health check
    log_info "Port forwarding for health check..."
    kubectl port-forward service/"$service_name" \
        8080:"$service_port" \
        --namespace="$NAMESPACE" &
    
    local port_forward_pid=$!
    
    # Wait for port forward to be ready
    sleep 5
    
    # Health check
    local health_url="http://localhost:8080/health"
    local max_attempts=10
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "$health_url" >/dev/null 2>&1; then
            log_success "Health check passed"
            kill $port_forward_pid 2>/dev/null || true
            return 0
        fi
        
        log_info "Health check attempt $attempt/$max_attempts failed, retrying..."
        sleep 10
        ((attempt++))
    done
    
    kill $port_forward_pid 2>/dev/null || true
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Cleanup resources
cleanup() {
    log_info "Cleaning up resources..."
    
    # Remove buildx builder
    if docker buildx ls | grep -q "zeta-builder"; then
        docker buildx rm zeta-builder || true
    fi
    
    # Kill any remaining port forwards
    pkill -f "kubectl port-forward" 2>/dev/null || true
    
    log_success "Cleanup completed"
}

# Show deployment info
show_deployment_info() {
    log_info "Deployment Information:"
    echo "=========================="
    echo "Environment: $ENVIRONMENT"
    echo "Namespace: $NAMESPACE"
    echo "Image: ${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${VERSION}"
    echo "=========================="
    
    # Show pods
    log_info "Pods:"
    kubectl get pods --namespace="$NAMESPACE" -l app.kubernetes.io/name=zeta-agent
    
    # Show services
    log_info "Services:"
    kubectl get services --namespace="$NAMESPACE"
    
    # Show ingress if exists
    if kubectl get ingress --namespace="$NAMESPACE" 2>/dev/null | grep -q zeta-agent; then
        log_info "Ingress:"
        kubectl get ingress --namespace="$NAMESPACE"
    fi
}

# Main deployment function
deploy() {
    log_info "Starting deployment process..."
    
    check_prerequisites
    build_docker
    security_scan
    terraform_operations "plan"
    terraform_operations "apply"
    helm_operations "install"
    wait_for_deployment
    health_check
    show_deployment_info
    
    log_success "Deployment completed successfully!"
}

# Show usage
usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  deploy              Full deployment (build, provision, deploy)"
    echo "  build               Build Docker image only"
    echo "  scan                Security scan only"
    echo "  terraform [plan|apply|destroy]"
    echo "  helm [install|upgrade|uninstall|test]"
    echo "  health              Health check only"
    echo "  info                Show deployment info"
    echo "  cleanup             Cleanup resources"
    echo ""
    echo "Environment Variables:"
    echo "  DOCKER_REGISTRY     Docker registry (default: docker.io)"
    echo "  DOCKER_NAMESPACE    Docker namespace (default: zetaai)"
    echo "  IMAGE_NAME          Image name (default: zeta-agent)"
    echo "  VERSION             Image version (default: git short hash)"
    echo "  PLATFORMS           Build platforms (default: linux/amd64,linux/arm64)"
    echo "  ENVIRONMENT         Environment (default: development)"
    echo "  NAMESPACE           Kubernetes namespace (default: zeta-agent)"
}

# Trap cleanup on exit
trap cleanup EXIT

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "build")
        check_prerequisites
        build_docker
        ;;
    "scan")
        security_scan
        ;;
    "terraform")
        terraform_operations "${2:-plan}"
        ;;
    "helm")
        helm_operations "${2:-install}"
        ;;
    "health")
        health_check
        ;;
    "info")
        show_deployment_info
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"--help"|"-h")
        usage
        ;;
    *)
        log_error "Unknown command: $1"
        usage
        exit 1
        ;;
esac
