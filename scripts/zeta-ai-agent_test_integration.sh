#!/bin/bash

# End-to-end integration testing script for Zeta AI Agent DevOps pipeline
# Tests complete pipeline from code commit to production deployment

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEST_NAMESPACE="zeta-agent-test"
TEST_RELEASE="zeta-agent-test"
DOCKER_REGISTRY="${DOCKER_REGISTRY:-docker.io}"
DOCKER_NAMESPACE="${DOCKER_NAMESPACE:-zetaai}"
IMAGE_NAME="${IMAGE_NAME:-zeta-agent}"
VERSION="${VERSION:-test-$(date +%Y%m%d-%H%M%S)}"
PLATFORMS="${PLATFORMS:-linux/amd64}"
TIMEOUT="${TIMEOUT:-600}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results tracking
TESTS_PASSED=0
TESTS_FAILED=0
FAILED_TESTS=()

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

# Test result functions
test_passed() {
    ((TESTS_PASSED++))
    log_success "✓ $1"
}

test_failed() {
    ((TESTS_FAILED++))
    FAILED_TESTS+=("$1")
    log_error "✗ $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Setup test environment
setup_test_environment() {
    log_info "Setting up test environment..."
    
    # Create test namespace
    if kubectl get namespace "$TEST_NAMESPACE" >/dev/null 2>&1; then
        log_info "Test namespace already exists, cleaning up..."
        kubectl delete namespace "$TEST_NAMESPACE" --timeout=60s || true
        
        # Wait for namespace to be deleted
        while kubectl get namespace "$TEST_NAMESPACE" >/dev/null 2>&1; do
            log_info "Waiting for namespace deletion..."
            sleep 5
        done
    fi
    
    kubectl create namespace "$TEST_NAMESPACE"
    test_passed "Test namespace created: $TEST_NAMESPACE"
    
    # Label namespace for testing
    kubectl label namespace "$TEST_NAMESPACE" environment=test purpose=integration-testing
    test_passed "Test namespace labeled"
}

# Test Docker build
test_docker_build() {
    log_info "Testing Docker build process..."
    
    # Test single platform build for faster testing
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${VERSION}"
    
    # Create test builder
    if ! docker buildx ls | grep -q "test-builder"; then
        docker buildx create --name test-builder --use
    else
        docker buildx use test-builder
    fi
    
    # Build test image
    if docker buildx build \
        --platform "$PLATFORMS" \
        --tag "$full_image_name" \
        --load \
        --file "$PROJECT_ROOT/Dockerfile" \
        "$PROJECT_ROOT"; then
        test_passed "Docker build successful"
    else
        test_failed "Docker build failed"
        return 1
    fi
    
    # Test image properties
    if docker inspect "$full_image_name" >/dev/null 2>&1; then
        test_passed "Docker image inspection successful"
        
        # Check image size (should be reasonable)
        local image_size=$(docker images "$full_image_name" --format "{{.Size}}")
        log_info "Image size: $image_size"
        
        # Check for required labels
        local labels=$(docker inspect "$full_image_name" --format='{{.Config.Labels}}')
        if echo "$labels" | grep -q "version"; then
            test_passed "Image has version label"
        else
            test_failed "Image missing version label"
        fi
        
    else
        test_failed "Docker image inspection failed"
    fi
}

# Test container functionality
test_container_functionality() {
    log_info "Testing container functionality..."
    
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${VERSION}"
    local container_name="zeta-test-container-$$"
    
    # Start container
    local container_id=$(docker run -d --name "$container_name" -p 3001:3000 "$full_image_name")
    
    if [ -n "$container_id" ]; then
        test_passed "Container started successfully"
        
        # Wait for container to be ready
        sleep 10
        
        # Check if container is running
        if docker ps --quiet --filter id="$container_id" | grep -q "$container_id"; then
            test_passed "Container is running"
            
            # Test health endpoint
            local max_attempts=10
            local attempt=1
            local health_ok=false
            
            while [ $attempt -le $max_attempts ]; do
                if curl -f "http://localhost:3001/health" --connect-timeout 5 --max-time 10 >/dev/null 2>&1; then
                    test_passed "Health endpoint responding"
                    health_ok=true
                    break
                fi
                log_info "Health check attempt $attempt/$max_attempts..."
                sleep 5
                ((attempt++))
            done
            
            if [ "$health_ok" = false ]; then
                test_failed "Health endpoint not responding"
            fi
            
            # Check logs for errors
            local logs=$(docker logs "$container_id" 2>&1)
            if echo "$logs" | grep -qi "error\|exception\|fatal"; then
                test_failed "Container logs contain errors"
                echo "$logs" | grep -i "error\|exception\|fatal" | head -5
            else
                test_passed "Container logs clean"
            fi
            
        else
            test_failed "Container stopped unexpectedly"
            docker logs "$container_id"
        fi
        
        # Cleanup container
        docker rm -f "$container_id" >/dev/null 2>&1
        
    else
        test_failed "Container failed to start"
    fi
}

# Test Terraform configuration
test_terraform_config() {
    log_info "Testing Terraform configuration..."
    
    local tf_dir="$PROJECT_ROOT/infra/terraform"
    
    if [ ! -d "$tf_dir" ]; then
        test_failed "Terraform directory not found"
        return 1
    fi
    
    cd "$tf_dir"
    
    # Test terraform init
    if terraform init -backend=false >/dev/null 2>&1; then
        test_passed "Terraform init successful"
    else
        test_failed "Terraform init failed"
        cd "$PROJECT_ROOT"
        return 1
    fi
    
    # Test terraform validate
    if terraform validate; then
        test_passed "Terraform configuration valid"
    else
        test_failed "Terraform configuration invalid"
    fi
    
    # Test terraform plan (dry run)
    export TF_VAR_environment="test"
    export TF_VAR_namespace="$TEST_NAMESPACE"
    export TF_VAR_image_tag="$VERSION"
    export TF_VAR_image_repository="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}"
    
    if terraform plan -out=/dev/null >/dev/null 2>&1; then
        test_passed "Terraform plan successful"
    else
        test_failed "Terraform plan failed"
    fi
    
    cd "$PROJECT_ROOT"
}

# Test Helm chart
test_helm_chart() {
    log_info "Testing Helm chart..."
    
    local helm_dir="$PROJECT_ROOT/infra/helm/zeta-agent"
    
    if [ ! -d "$helm_dir" ]; then
        test_failed "Helm chart directory not found"
        return 1
    fi
    
    # Test helm lint
    if helm lint "$helm_dir"; then
        test_passed "Helm chart linting successful"
    else
        test_failed "Helm chart linting failed"
    fi
    
    # Test helm template
    if helm template test-release "$helm_dir" \
        --namespace "$TEST_NAMESPACE" \
        --set image.tag="$VERSION" \
        --set image.repository="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}" \
        >/dev/null; then
        test_passed "Helm template rendering successful"
    else
        test_failed "Helm template rendering failed"
    fi
    
    # Test helm dry-run
    if helm install "$TEST_RELEASE" "$helm_dir" \
        --namespace "$TEST_NAMESPACE" \
        --set image.tag="$VERSION" \
        --set image.repository="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}" \
        --dry-run >/dev/null; then
        test_passed "Helm dry-run successful"
    else
        test_failed "Helm dry-run failed"
    fi
}

# Test Kubernetes deployment
test_kubernetes_deployment() {
    log_info "Testing Kubernetes deployment..."
    
    local helm_dir="$PROJECT_ROOT/infra/helm/zeta-agent"
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${VERSION}"
    
    # Install Helm chart
    if helm install "$TEST_RELEASE" "$helm_dir" \
        --namespace "$TEST_NAMESPACE" \
        --set image.tag="$VERSION" \
        --set image.repository="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}" \
        --set image.pullPolicy="Never" \
        --set replicaCount=1 \
        --wait \
        --timeout="${TIMEOUT}s"; then
        test_passed "Helm installation successful"
    else
        test_failed "Helm installation failed"
        kubectl get events --namespace="$TEST_NAMESPACE" --sort-by=.metadata.creationTimestamp
        return 1
    fi
    
    # Check deployment status
    if kubectl rollout status deployment/"$TEST_RELEASE" --namespace="$TEST_NAMESPACE" --timeout="${TIMEOUT}s"; then
        test_passed "Deployment rollout successful"
    else
        test_failed "Deployment rollout failed"
        kubectl describe deployment/"$TEST_RELEASE" --namespace="$TEST_NAMESPACE"
        return 1
    fi
    
    # Check pods
    local pods=$(kubectl get pods --namespace="$TEST_NAMESPACE" --selector=app.kubernetes.io/name=zeta-agent --output=jsonpath='{.items[*].status.phase}')
    if echo "$pods" | grep -q "Running"; then
        test_passed "Pods are running"
    else
        test_failed "Pods are not running: $pods"
        kubectl describe pods --namespace="$TEST_NAMESPACE" --selector=app.kubernetes.io/name=zeta-agent
    fi
    
    # Check service
    if kubectl get service "$TEST_RELEASE" --namespace="$TEST_NAMESPACE" >/dev/null 2>&1; then
        test_passed "Service created successfully"
    else
        test_failed "Service not found"
    fi
}

# Test application health in Kubernetes
test_k8s_application_health() {
    log_info "Testing application health in Kubernetes..."
    
    # Get service port
    local service_port=$(kubectl get service "$TEST_RELEASE" \
        --namespace="$TEST_NAMESPACE" \
        --output=jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "3000")
    
    # Port forward for testing
    kubectl port-forward service/"$TEST_RELEASE" 3002:"$service_port" \
        --namespace="$TEST_NAMESPACE" &
    local port_forward_pid=$!
    
    # Wait for port forward
    sleep 5
    
    # Test health endpoint
    local max_attempts=10
    local attempt=1
    local health_ok=false
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "http://localhost:3002/health" --connect-timeout 5 --max-time 10 >/dev/null 2>&1; then
            test_passed "K8s application health endpoint responding"
            health_ok=true
            break
        fi
        log_info "K8s health check attempt $attempt/$max_attempts..."
        sleep 5
        ((attempt++))
    done
    
    if [ "$health_ok" = false ]; then
        test_failed "K8s application health endpoint not responding"
    fi
    
    # Test API endpoint
    if curl -f "http://localhost:3002/api/v1/status" --connect-timeout 5 --max-time 10 >/dev/null 2>&1; then
        test_passed "K8s application API endpoint responding"
    else
        test_failed "K8s application API endpoint not responding"
    fi
    
    # Cleanup port forward
    kill $port_forward_pid 2>/dev/null || true
}

# Test Helm tests
test_helm_tests() {
    log_info "Running Helm tests..."
    
    if helm test "$TEST_RELEASE" --namespace="$TEST_NAMESPACE" --timeout="${TIMEOUT}s"; then
        test_passed "Helm tests successful"
    else
        test_failed "Helm tests failed"
        kubectl logs --namespace="$TEST_NAMESPACE" --selector=app.kubernetes.io/component=test
    fi
}

# Test scaling
test_scaling() {
    log_info "Testing application scaling..."
    
    # Scale up
    if kubectl scale deployment/"$TEST_RELEASE" --replicas=2 --namespace="$TEST_NAMESPACE"; then
        test_passed "Scale up command successful"
        
        # Wait for scale up
        if kubectl rollout status deployment/"$TEST_RELEASE" --namespace="$TEST_NAMESPACE" --timeout="120s"; then
            test_passed "Scale up completed"
            
            # Verify replica count
            local replicas=$(kubectl get deployment/"$TEST_RELEASE" --namespace="$TEST_NAMESPACE" --output=jsonpath='{.status.readyReplicas}')
            if [ "$replicas" = "2" ]; then
                test_passed "Correct number of replicas running"
            else
                test_failed "Incorrect replica count: $replicas (expected 2)"
            fi
        else
            test_failed "Scale up timeout"
        fi
    else
        test_failed "Scale up command failed"
    fi
    
    # Scale back down
    kubectl scale deployment/"$TEST_RELEASE" --replicas=1 --namespace="$TEST_NAMESPACE"
    kubectl rollout status deployment/"$TEST_RELEASE" --namespace="$TEST_NAMESPACE" --timeout="60s"
}

# Test resource cleanup
test_cleanup() {
    log_info "Testing resource cleanup..."
    
    # Uninstall Helm release
    if helm uninstall "$TEST_RELEASE" --namespace="$TEST_NAMESPACE"; then
        test_passed "Helm uninstall successful"
    else
        test_failed "Helm uninstall failed"
    fi
    
    # Wait for resources to be cleaned up
    sleep 30
    
    # Check that pods are gone
    local remaining_pods=$(kubectl get pods --namespace="$TEST_NAMESPACE" --selector=app.kubernetes.io/name=zeta-agent --output=jsonpath='{.items[*].metadata.name}' 2>/dev/null || echo "")
    if [ -z "$remaining_pods" ]; then
        test_passed "All pods cleaned up"
    else
        test_failed "Pods still remaining: $remaining_pods"
    fi
    
    # Delete test namespace
    if kubectl delete namespace "$TEST_NAMESPACE" --timeout=60s; then
        test_passed "Test namespace deleted"
    else
        test_failed "Test namespace deletion failed"
    fi
    
    # Cleanup Docker resources
    docker rm -f $(docker ps -a --filter name="zeta-test-*" --quiet) 2>/dev/null || true
    docker buildx rm test-builder 2>/dev/null || true
    
    # Remove test image
    docker rmi "${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${VERSION}" 2>/dev/null || true
}

# Show test results
show_test_results() {
    log_info "Integration Test Results:"
    echo "=========================="
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"
    echo "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
    echo "=========================="
    
    if [ $TESTS_FAILED -gt 0 ]; then
        log_error "Failed Tests:"
        for test in "${FAILED_TESTS[@]}"; do
            echo "  ✗ $test"
        done
        echo "=========================="
        return 1
    else
        log_success "All tests passed!"
        return 0
    fi
}

# Main test execution
run_integration_tests() {
    log_info "Starting integration tests for Zeta AI Agent DevOps pipeline..."
    log_info "Test version: $VERSION"
    log_info "Test namespace: $TEST_NAMESPACE"
    echo "=========================="
    
    # Prerequisites check
    local missing_tools=()
    for tool in docker kubectl helm terraform curl; do
        if ! command_exists "$tool"; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi
    
    # Check cluster connectivity
    if ! kubectl cluster-info >/dev/null 2>&1; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    # Run tests
    setup_test_environment
    test_docker_build
    test_container_functionality
    test_terraform_config
    test_helm_chart
    test_kubernetes_deployment
    test_k8s_application_health
    test_helm_tests
    test_scaling
    test_cleanup
    
    # Show results
    show_test_results
}

# Cleanup on exit
trap 'test_cleanup 2>/dev/null || true' EXIT

# Show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Environment Variables:"
    echo "  DOCKER_REGISTRY     Docker registry (default: docker.io)"
    echo "  DOCKER_NAMESPACE    Docker namespace (default: zetaai)"
    echo "  IMAGE_NAME          Image name (default: zeta-agent)"
    echo "  VERSION             Image version (default: test-YYYYMMDD-HHMMSS)"
    echo "  PLATFORMS           Build platforms (default: linux/amd64)"
    echo "  TIMEOUT             Test timeout in seconds (default: 600)"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run with defaults"
    echo "  VERSION=v1.0.0 $0                    # Run with specific version"
    echo "  TIMEOUT=300 $0                       # Run with 5-minute timeout"
}

# Main script logic
case "${1:-test}" in
    "test"|"")
        run_integration_tests
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
