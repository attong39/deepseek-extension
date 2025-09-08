#!/bin/bash

# Docker build automation script for Zeta AI Agent
# Handles multi-platform builds, security scanning, and registry operations

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCKER_REGISTRY="${DOCKER_REGISTRY:-docker.io}"
DOCKER_NAMESPACE="${DOCKER_NAMESPACE:-zetaai}"
IMAGE_NAME="${IMAGE_NAME:-zeta-agent}"
VERSION="${VERSION:-$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"
BUILD_ARGS="${BUILD_ARGS:-}"
CACHE_FROM="${CACHE_FROM:-}"
CACHE_TO="${CACHE_TO:-}"
PUSH="${PUSH:-true}"
LOAD="${LOAD:-false}"

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

# Check Docker prerequisites
check_docker_prerequisites() {
    log_info "Checking Docker prerequisites..."
    
    if ! command_exists docker; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    if ! docker buildx version >/dev/null 2>&1; then
        log_error "Docker buildx is required for multi-platform builds"
        exit 1
    fi
    
    log_success "Docker prerequisites satisfied"
}

# Setup buildx builder
setup_builder() {
    local builder_name="zeta-builder"
    
    log_info "Setting up buildx builder..."
    
    # Check if builder exists
    if docker buildx ls | grep -q "$builder_name"; then
        log_info "Using existing builder: $builder_name"
        docker buildx use "$builder_name"
    else
        log_info "Creating new builder: $builder_name"
        docker buildx create \
            --name "$builder_name" \
            --driver docker-container \
            --use \
            --bootstrap
    fi
    
    # Inspect builder to ensure it supports required platforms
    log_info "Inspecting builder capabilities..."
    docker buildx inspect --bootstrap
    
    log_success "Builder setup completed"
}

# Prepare build context
prepare_build_context() {
    log_info "Preparing build context..."
    
    # Check if Dockerfile exists
    if [ ! -f "$PROJECT_ROOT/Dockerfile" ]; then
        log_error "Dockerfile not found in project root"
        exit 1
    fi
    
    # Check if .dockerignore exists
    if [ ! -f "$PROJECT_ROOT/.dockerignore" ]; then
        log_warning ".dockerignore not found, build context may be larger than necessary"
    fi
    
    # Validate build context size
    local context_size=$(du -sh "$PROJECT_ROOT" 2>/dev/null | cut -f1 || echo "unknown")
    log_info "Build context size: $context_size"
    
    log_success "Build context prepared"
}

# Generate image tags
generate_tags() {
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}"
    
    tags=(
        "${full_image_name}:${VERSION}"
        "${full_image_name}:latest"
    )
    
    # Add branch tag if in git repo
    if git rev-parse --git-dir >/dev/null 2>&1; then
        local branch_name=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        if [ -n "$branch_name" ] && [ "$branch_name" != "HEAD" ]; then
            # Sanitize branch name for Docker tag
            local sanitized_branch=$(echo "$branch_name" | sed 's/[^a-zA-Z0-9._-]/-/g')
            tags+=("${full_image_name}:${sanitized_branch}")
        fi
    fi
    
    # Add timestamp tag for uniqueness
    local timestamp=$(date +%Y%m%d-%H%M%S)
    tags+=("${full_image_name}:${timestamp}")
    
    printf '%s\n' "${tags[@]}"
}

# Build Docker image
build_image() {
    local operation="${1:-build}"
    
    log_info "Building Docker image..."
    
    # Generate tags
    local tags=($(generate_tags))
    local tag_args=()
    
    for tag in "${tags[@]}"; do
        tag_args+=(--tag "$tag")
        log_info "Will tag as: $tag"
    done
    
    # Prepare build arguments
    local build_arg_list=()
    if [ -n "$BUILD_ARGS" ]; then
        IFS=',' read -ra ARGS <<< "$BUILD_ARGS"
        for arg in "${ARGS[@]}"; do
            build_arg_list+=(--build-arg "$arg")
        done
    fi
    
    # Add common build args
    build_arg_list+=(
        --build-arg "VERSION=$VERSION"
        --build-arg "BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
        --build-arg "VCS_REF=$(git rev-parse HEAD 2>/dev/null || echo 'unknown')"
    )
    
    # Prepare cache arguments
    local cache_args=()
    if [ -n "$CACHE_FROM" ]; then
        cache_args+=(--cache-from "$CACHE_FROM")
    fi
    if [ -n "$CACHE_TO" ]; then
        cache_args+=(--cache-to "$CACHE_TO")
    fi
    
    # Build command
    local build_cmd=(
        docker buildx "$operation"
        --platform "$PLATFORMS"
        "${tag_args[@]}"
        "${build_arg_list[@]}"
        "${cache_args[@]}"
        --file "$PROJECT_ROOT/Dockerfile"
    )
    
    # Add output options
    if [ "$PUSH" = "true" ]; then
        build_cmd+=(--push)
        log_info "Will push to registry after build"
    elif [ "$LOAD" = "true" ]; then
        build_cmd+=(--load)
        log_info "Will load to local Docker after build"
    fi
    
    # Add build context
    build_cmd+=("$PROJECT_ROOT")
    
    # Execute build
    log_info "Executing build command..."
    "${build_cmd[@]}"
    
    log_success "Docker image build completed"
}

# Security scan with multiple tools
security_scan() {
    local image_tag="${1:-latest}"
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${image_tag}"
    
    log_info "Running security scan on: $full_image_name"
    
    # Pull image if it exists remotely
    if [ "$PUSH" = "true" ]; then
        log_info "Pulling image for security scan..."
        docker pull "$full_image_name" || log_warning "Could not pull image, using local if available"
    fi
    
    local scan_results=0
    
    # Docker Scout scan
    if command_exists docker-scout || docker scout version >/dev/null 2>&1; then
        log_info "Running Docker Scout security scan..."
        if docker scout cves "$full_image_name"; then
            log_success "Docker Scout scan passed"
        else
            log_warning "Docker Scout scan found vulnerabilities"
            scan_results=1
        fi
    fi
    
    # Trivy scan
    if command_exists trivy; then
        log_info "Running Trivy security scan..."
        if trivy image --exit-code 1 --severity HIGH,CRITICAL "$full_image_name"; then
            log_success "Trivy scan passed"
        else
            log_warning "Trivy scan found HIGH/CRITICAL vulnerabilities"
            scan_results=1
        fi
    fi
    
    # Grype scan
    if command_exists grype; then
        log_info "Running Grype security scan..."
        if grype "$full_image_name" --fail-on high; then
            log_success "Grype scan passed"
        else
            log_warning "Grype scan found high severity vulnerabilities"
            scan_results=1
        fi
    fi
    
    # Fallback: basic image inspection
    if ! command_exists docker-scout && ! command_exists trivy && ! command_exists grype; then
        log_warning "No security scanners available"
        log_info "Running basic image inspection..."
        
        # Check image history
        docker history "$full_image_name"
        
        # Check for common security issues
        log_info "Checking for potential security issues..."
        
        # Check if running as root
        local user_check=$(docker inspect "$full_image_name" --format='{{.Config.User}}' || echo "")
        if [ -z "$user_check" ] || [ "$user_check" = "root" ] || [ "$user_check" = "0" ]; then
            log_warning "Image may be running as root user"
            scan_results=1
        fi
        
        # Check for exposed ports
        local exposed_ports=$(docker inspect "$full_image_name" --format='{{.Config.ExposedPorts}}' || echo "")
        if [ -n "$exposed_ports" ] && [ "$exposed_ports" != "map[]" ]; then
            log_info "Exposed ports detected: $exposed_ports"
        fi
    fi
    
    if [ $scan_results -eq 0 ]; then
        log_success "Security scan completed without critical issues"
    else
        log_warning "Security scan found issues - review recommended"
    fi
    
    return $scan_results
}

# Image analysis
analyze_image() {
    local image_tag="${1:-latest}"
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${image_tag}"
    
    log_info "Analyzing image: $full_image_name"
    
    # Image size
    local image_size=$(docker images "$full_image_name" --format "table {{.Size}}" | tail -n 1)
    log_info "Image size: $image_size"
    
    # Layer count
    local layer_count=$(docker history "$full_image_name" --quiet | wc -l)
    log_info "Layer count: $layer_count"
    
    # Image details
    log_info "Image details:"
    docker inspect "$full_image_name" --format='
Architecture: {{.Architecture}}
OS: {{.Os}}
Created: {{.Created}}
Size: {{.Size}} bytes
Virtual Size: {{.VirtualSize}} bytes
' 2>/dev/null || log_warning "Could not inspect image details"
    
    # Check for best practices
    log_info "Checking image best practices..."
    
    # Check for health check
    local healthcheck=$(docker inspect "$full_image_name" --format='{{.Config.Healthcheck}}' 2>/dev/null || echo "")
    if [ -n "$healthcheck" ] && [ "$healthcheck" != "<nil>" ]; then
        log_success "Health check configured"
    else
        log_warning "No health check configured"
    fi
    
    # Check labels
    local labels=$(docker inspect "$full_image_name" --format='{{.Config.Labels}}' 2>/dev/null || echo "")
    if [ -n "$labels" ] && [ "$labels" != "map[]" ]; then
        log_success "Labels present"
    else
        log_warning "No labels found"
    fi
    
    log_success "Image analysis completed"
}

# Test image functionality
test_image() {
    local image_tag="${1:-latest}"
    local full_image_name="${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${IMAGE_NAME}:${image_tag}"
    
    log_info "Testing image functionality: $full_image_name"
    
    # Test container startup
    log_info "Testing container startup..."
    local container_id=$(docker run -d --name "zeta-test-$$" "$full_image_name")
    
    if [ -n "$container_id" ]; then
        log_success "Container started successfully: $container_id"
        
        # Wait a moment for startup
        sleep 5
        
        # Check if container is still running
        if docker ps --quiet --filter id="$container_id" | grep -q "$container_id"; then
            log_success "Container is running"
            
            # Check logs for errors
            local logs=$(docker logs "$container_id" 2>&1)
            if echo "$logs" | grep -qi "error\|exception\|fatal"; then
                log_warning "Found error messages in logs:"
                echo "$logs" | grep -i "error\|exception\|fatal" | head -5
            else
                log_success "No error messages in logs"
            fi
            
            # Test health endpoint if available
            local container_ip=$(docker inspect "$container_id" --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
            if [ -n "$container_ip" ]; then
                log_info "Testing health endpoint..."
                if curl -f "http://$container_ip:3000/health" --connect-timeout 5 --max-time 10 >/dev/null 2>&1; then
                    log_success "Health endpoint responding"
                else
                    log_warning "Health endpoint not responding or not available"
                fi
            fi
        else
            log_error "Container stopped unexpectedly"
            docker logs "$container_id"
        fi
        
        # Cleanup test container
        docker rm -f "$container_id" >/dev/null 2>&1
    else
        log_error "Failed to start container"
        return 1
    fi
    
    log_success "Image functionality test completed"
}

# Cleanup Docker resources
cleanup_docker() {
    log_info "Cleaning up Docker resources..."
    
    # Remove test containers
    docker ps -a --filter name="zeta-test-*" --quiet | xargs -r docker rm -f
    
    # Remove dangling images
    docker image prune -f
    
    # Remove unused build cache
    docker buildx prune -f
    
    log_success "Docker cleanup completed"
}

# Show build information
show_build_info() {
    log_info "Build Information:"
    echo "==================="
    echo "Project: $PROJECT_ROOT"
    echo "Registry: $DOCKER_REGISTRY"
    echo "Namespace: $DOCKER_NAMESPACE"
    echo "Image: $IMAGE_NAME"
    echo "Version: $VERSION"
    echo "Platforms: $PLATFORMS"
    echo "Push: $PUSH"
    echo "Load: $LOAD"
    echo "==================="
    
    # Show generated tags
    log_info "Generated tags:"
    generate_tags | while read -r tag; do
        echo "  - $tag"
    done
}

# Show usage
usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  build               Build Docker image"
    echo "  scan [TAG]          Security scan image"
    echo "  analyze [TAG]       Analyze image"
    echo "  test [TAG]          Test image functionality"
    echo "  info                Show build information"
    echo "  cleanup             Cleanup Docker resources"
    echo ""
    echo "Environment Variables:"
    echo "  DOCKER_REGISTRY     Docker registry (default: docker.io)"
    echo "  DOCKER_NAMESPACE    Docker namespace (default: zetaai)"
    echo "  IMAGE_NAME          Image name (default: zeta-agent)"
    echo "  VERSION             Image version (default: git short hash)"
    echo "  PLATFORMS           Build platforms (default: linux/amd64,linux/arm64)"
    echo "  BUILD_ARGS          Comma-separated build args"
    echo "  CACHE_FROM          Cache source"
    echo "  CACHE_TO            Cache destination"
    echo "  PUSH                Push to registry (default: true)"
    echo "  LOAD                Load to local Docker (default: false)"
}

# Trap cleanup on exit
trap cleanup_docker EXIT

# Main script logic
case "${1:-build}" in
    "build")
        show_build_info
        check_docker_prerequisites
        setup_builder
        prepare_build_context
        build_image
        if [ "$LOAD" = "true" ] || [ "$PUSH" = "false" ]; then
            analyze_image "$VERSION"
            test_image "$VERSION"
        fi
        ;;
    "scan")
        security_scan "${2:-$VERSION}"
        ;;
    "analyze")
        analyze_image "${2:-$VERSION}"
        ;;
    "test")
        test_image "${2:-$VERSION}"
        ;;
    "info")
        show_build_info
        ;;
    "cleanup")
        cleanup_docker
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
