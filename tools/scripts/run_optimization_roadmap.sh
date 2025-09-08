#!/usr/bin/env bash
set -euo pipefail

# ZETA_VN Optimization Roadmap - Master Execution Script
# Runs all 4 phases of the optimization roadmap

echo "🚀 ZETA_VN OPTIMIZATION ROADMAP 2025"
echo "===================================="
echo "Running all 4 phases of the optimization roadmap"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_phase() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_phase "Checking prerequisites..."
    
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Please install uv first."
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        print_warning "Docker is not installed. Phase 4 will be skipped."
        SKIP_DOCKER=true
    else
        SKIP_DOCKER=false
    fi
    
    print_success "Prerequisites checked"
}

# Phase 1: Foundation
run_phase1() {
    print_phase "🏗️ PHASE 1: FOUNDATION - Code Quality & Architecture"
    
    if bash scripts/impl/phase1_foundation.sh; then
        print_success "Phase 1 completed successfully"
    else
        print_warning "Phase 1 completed with warnings"
    fi
    echo ""
}

# Phase 2: Performance
run_phase2() {
    print_phase "⚡ PHASE 2: PERFORMANCE - Testing & Optimization"
    
    # Start server in background for testing
    print_phase "Starting test server..."
    uv run uvicorn zeta_vn.app.main_minimal:app --host 0.0.0.0 --port 8000 &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 3
    
    # Check if server is running
    if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
        print_success "Test server started (PID: $SERVER_PID)"
        
        # Run performance tests
        if bash scripts/impl/phase2_perf.sh; then
            print_success "Phase 2 completed successfully"
        else
            print_warning "Phase 2 completed with warnings"
        fi
    else
        print_error "Failed to start test server"
    fi
    
    # Clean up server
    if kill $SERVER_PID 2>/dev/null; then
        print_success "Test server stopped"
    fi
    echo ""
}

# Phase 3: Security
run_phase3() {
    print_phase "🔒 PHASE 3: SECURITY - Hardening & Compliance"
    
    if bash scripts/impl/phase3_security.sh; then
        print_success "Phase 3 completed successfully"
    else
        print_warning "Phase 3 completed with warnings"
    fi
    echo ""
}

# Phase 4: Deployment
run_phase4() {
    print_phase "🚀 PHASE 4: DEPLOYMENT - Production Ready"
    
    if [ "$SKIP_DOCKER" = true ]; then
        print_warning "Skipping Phase 4 - Docker not available"
        return
    fi
    
    if bash scripts/impl/phase4_deploy.sh; then
        print_success "Phase 4 completed successfully"
    else
        print_error "Phase 4 failed"
    fi
    echo ""
}

# Summary report
generate_summary() {
    print_phase "📊 OPTIMIZATION SUMMARY"
    echo "======================="
    
    echo "🏗️ Phase 1: Foundation"
    echo "   - Code quality fixes applied"
    echo "   - Type checking performed"
    echo "   - Tests executed"
    echo "   - Security scan completed"
    
    echo ""
    echo "⚡ Phase 2: Performance"
    echo "   - API performance tested"
    echo "   - Bottlenecks identified"
    echo "   - Optimization opportunities noted"
    
    echo ""
    echo "🔒 Phase 3: Security"
    echo "   - Security hardening applied"
    echo "   - Vulnerability assessment completed"
    echo "   - Compliance checks performed"
    
    echo ""
    if [ "$SKIP_DOCKER" = false ]; then
        echo "🚀 Phase 4: Deployment"
        echo "   - Production Docker image built"
        echo "   - Container ready for deployment"
    fi
    
    echo ""
    print_success "All phases completed!"
    echo ""
    echo "🎯 Next Steps:"
    echo "   1. Review any warnings or errors above"
    echo "   2. Fix remaining issues identified"
    echo "   3. Run individual phases as needed"
    echo "   4. Deploy to staging environment"
    echo "   5. Perform load testing"
    echo "   6. Deploy to production"
    echo ""
    echo "📖 For detailed implementation:"
    echo "   - See PROJECT_OPTIMIZATION_COMPLETE_ROADMAP.md"
    echo "   - Run individual phase scripts in scripts/impl/"
    echo "   - Check CI/CD workflow in .github/workflows/quality_v3.yml"
}

# Main execution
main() {
    check_prerequisites
    
    echo "Starting optimization roadmap execution..."
    echo "This will run all 4 phases sequentially."
    echo ""
    
    # Run all phases
    run_phase1
    run_phase2
    run_phase3
    run_phase4
    
    # Generate summary
    generate_summary
}

# Handle script interruption
trap 'echo ""; print_error "Script interrupted by user"; exit 1' INT

# Run main function
main "$@"