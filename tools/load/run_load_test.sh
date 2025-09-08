#!/bin/bash

# =================================================================
# Zeta WebSocket Load Testing Suite
# Comprehensive load testing for 10k msg/s with k6 and chaos testing
# =================================================================

set -e

# Default configuration
WS_URL="${WS_URL:-ws://localhost:8000/api/v1/agents/teams/load-test/run}"
JWT_TOKEN="${JWT_TOKEN:-eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...}"
TARGET_MPS="${TARGET_MPS:-10000}"
MAX_CONNECTIONS="${MAX_CONNECTIONS:-400}"
TEST_DURATION="${TEST_DURATION:-300}" # 5 minutes
OUTPUT_DIR="${OUTPUT_DIR:-./load-test-results}"
CHAOS_ENABLED="${CHAOS_ENABLED:-false}"

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

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check k6
    if ! command -v k6 &> /dev/null; then
        log_error "k6 is not installed. Please install from https://k6.io/docs/getting-started/installation/"
        exit 1
    fi
    
    # Check jq for JSON processing
    if ! command -v jq &> /dev/null; then
        log_warning "jq not found. Some result processing may be limited."
    fi
    
    # Check curl for health checks
    if ! command -v curl &> /dev/null; then
        log_error "curl is required for health checks"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Health check before testing
health_check() {
    log_info "Performing health check..."
    
    # Convert WebSocket URL to HTTP for health check
    HTTP_URL=$(echo "$WS_URL" | sed 's/ws:/http:/' | sed 's/wss:/https:/' | sed 's|/api/v1/agents/teams/.*|/health|')
    
    if curl -s -f "$HTTP_URL" > /dev/null; then
        log_success "Health check passed - server is responding"
    else
        log_error "Health check failed - server not responding at $HTTP_URL"
        exit 1
    fi
}

# Setup test environment
setup_test() {
    log_info "Setting up test environment..."
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    # Calculate per-connection message rate
    MSG_PER_CONN=$(( TARGET_MPS / MAX_CONNECTIONS ))
    MSG_INTERVAL=$(( 1000 / MSG_PER_CONN ))
    
    log_info "Test Configuration:"
    log_info "  WebSocket URL: $WS_URL"
    log_info "  Target MPS: $TARGET_MPS"
    log_info "  Max Connections: $MAX_CONNECTIONS"
    log_info "  Messages per Connection: $MSG_PER_CONN/s"
    log_info "  Message Interval: ${MSG_INTERVAL}ms"
    log_info "  Test Duration: ${TEST_DURATION}s"
    log_info "  Output Directory: $OUTPUT_DIR"
    
    # Export environment variables for k6
    export WS_URL
    export JWT_TOKEN
    export MESSAGE_INTERVAL="$MSG_INTERVAL"
    export CONNECTION_TIMEOUT="5000"
}

# Run WebSocket load test
run_load_test() {
    log_info "Starting WebSocket load test..."
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local results_file="$OUTPUT_DIR/load_test_${timestamp}.json"
    local summary_file="$OUTPUT_DIR/load_test_${timestamp}_summary.txt"
    
    # Run k6 with custom options
    k6 run \
        --duration "${TEST_DURATION}s" \
        --vus "$MAX_CONNECTIONS" \
        --out json="$results_file" \
        --summary-export="$summary_file" \
        tools/load/ws_k6.js \
        2>&1 | tee "$OUTPUT_DIR/load_test_${timestamp}.log"
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_success "Load test completed successfully"
        analyze_results "$results_file" "$summary_file"
    else
        log_error "Load test failed with exit code $exit_code"
        return $exit_code
    fi
}

# Analyze test results
analyze_results() {
    local results_file="$1"
    local summary_file="$2"
    
    log_info "Analyzing test results..."
    
    if [ -f "$results_file" ] && command -v jq &> /dev/null; then
        log_info "Extracting key metrics..."
        
        # Extract key metrics from k6 results
        local total_messages=$(jq -r '.metrics.ws_messages_total.count // 0' "$results_file")
        local error_rate=$(jq -r '.metrics.ws_error_rate.rate // 0' "$results_file")
        local p95_latency=$(jq -r '.metrics.ws_latency.p95 // 0' "$results_file")
        local avg_connections=$(jq -r '.metrics.ws_connections_total.count // 0' "$results_file")
        
        echo ""
        log_info "=== LOAD TEST RESULTS ==="
        log_info "Total Messages: $total_messages"
        log_info "Error Rate: $(echo "$error_rate * 100" | bc -l 2>/dev/null || echo "$error_rate")%"
        log_info "P95 Latency: ${p95_latency}ms"
        log_info "Average Connections: $avg_connections"
        
        # Check performance thresholds
        echo ""
        log_info "=== PERFORMANCE ANALYSIS ==="
        
        # Message rate check
        local actual_mps=$(echo "$total_messages / $TEST_DURATION" | bc -l 2>/dev/null || echo "0")
        local mps_threshold=$(echo "$TARGET_MPS * 0.8" | bc -l 2>/dev/null || echo "$TARGET_MPS") # 80% of target
        
        if (( $(echo "$actual_mps >= $mps_threshold" | bc -l 2>/dev/null || echo "0") )); then
            log_success "✓ Message rate: ${actual_mps} MPS (target: $TARGET_MPS MPS)"
        else
            log_error "✗ Message rate: ${actual_mps} MPS (below 80% of target: $TARGET_MPS MPS)"
        fi
        
        # Error rate check
        if (( $(echo "$error_rate < 0.01" | bc -l 2>/dev/null || echo "0") )); then
            log_success "✓ Error rate: $(echo "$error_rate * 100" | bc -l 2>/dev/null || echo "$error_rate")% (target: <1%)"
        else
            log_error "✗ Error rate: $(echo "$error_rate * 100" | bc -l 2>/dev/null || echo "$error_rate")% (target: <1%)"
        fi
        
        # Latency check
        if (( $(echo "$p95_latency < 200" | bc -l 2>/dev/null || echo "0") )); then
            log_success "✓ P95 Latency: ${p95_latency}ms (target: <200ms)"
        else
            log_error "✗ P95 Latency: ${p95_latency}ms (target: <200ms)"
        fi
        
    else
        log_warning "Could not analyze detailed results (missing jq or results file)"
    fi
    
    if [ -f "$summary_file" ]; then
        log_info ""
        log_info "=== K6 SUMMARY ==="
        cat "$summary_file"
    fi
}

# Chaos testing (optional)
run_chaos_test() {
    if [ "$CHAOS_ENABLED" != "true" ]; then
        log_info "Chaos testing disabled (set CHAOS_ENABLED=true to enable)"
        return 0
    fi
    
    log_info "Starting chaos testing..."
    
    # This is a basic chaos test - in production you'd use tools like Chaos Monkey
    # For now, we'll simulate connection drops and network issues
    
    log_warning "Chaos testing not fully implemented yet"
    log_info "Consider integrating with:"
    log_info "  - Chaos Monkey for random instance termination"
    log_info "  - Pumba for network chaos (delays, packet loss)"
    log_info "  - Gremlin for comprehensive failure injection"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up..."
    # Kill any remaining k6 processes
    pkill -f k6 2>/dev/null || true
}

# Main execution
main() {
    log_info "Starting Zeta WebSocket Load Testing Suite"
    log_info "================================================"
    
    # Setup cleanup trap
    trap cleanup EXIT
    
    # Run test sequence
    check_prerequisites
    health_check
    setup_test
    run_load_test
    
    if [ "$CHAOS_ENABLED" == "true" ]; then
        run_chaos_test
    fi
    
    log_success "Load testing completed!"
    log_info "Results saved to: $OUTPUT_DIR"
}

# Help function
show_help() {
    echo "Zeta WebSocket Load Testing Suite"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -u, --url URL           WebSocket URL (default: ws://localhost:8000/api/v1/agents/teams/load-test/run)"
    echo "  -t, --token TOKEN       JWT token for authentication"
    echo "  -m, --mps MPS           Target messages per second (default: 10000)"
    echo "  -c, --connections NUM   Max concurrent connections (default: 400)"
    echo "  -d, --duration SECONDS  Test duration in seconds (default: 300)"
    echo "  -o, --output DIR        Output directory (default: ./load-test-results)"
    echo "  --chaos                 Enable chaos testing"
    echo "  -h, --help              Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  WS_URL          WebSocket URL"
    echo "  JWT_TOKEN       JWT authentication token"
    echo "  TARGET_MPS      Target messages per second"
    echo "  MAX_CONNECTIONS Maximum concurrent connections"
    echo "  TEST_DURATION   Test duration in seconds"
    echo "  OUTPUT_DIR      Output directory"
    echo "  CHAOS_ENABLED   Enable chaos testing (true/false)"
    echo ""
    echo "Examples:"
    echo "  $0                                                    # Run with defaults"
    echo "  $0 -m 5000 -c 200 -d 180                            # 5k MPS, 200 connections, 3 minutes"
    echo "  $0 -u ws://staging.zeta.ai/ws/test --chaos           # Test staging with chaos"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--url)
            WS_URL="$2"
            shift 2
            ;;
        -t|--token)
            JWT_TOKEN="$2"
            shift 2
            ;;
        -m|--mps)
            TARGET_MPS="$2"
            shift 2
            ;;
        -c|--connections)
            MAX_CONNECTIONS="$2"
            shift 2
            ;;
        -d|--duration)
            TEST_DURATION="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --chaos)
            CHAOS_ENABLED="true"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Run main function
main
