#!/bin/bash
# =============================================================================
# 🚀 Zeta AI Agent - Production Configuration Checker
# Kiểm tra tất cả các cấu hình production (CORS, CSP, Alerting, Health checks)
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_HOST="localhost"
DEFAULT_PORT="9100"
HOST="${1:-$DEFAULT_HOST}"
PORT="${2:-$DEFAULT_PORT}"
BASE_URL="http://${HOST}:${PORT}"

echo -e "${BLUE}🚀 Zeta AI Agent Production Configuration Checker${NC}"
echo "Testing against: $BASE_URL"
echo "========================================================"

# Function to check HTTP response
check_endpoint() {
    local endpoint="$1"
    local expected_status="$2"
    local description="$3"
    
    echo -e "\n${BLUE}🔍 Testing: $description${NC}"
    echo "Endpoint: $endpoint"
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}\nTIME:%{time_total}" "$endpoint" 2>/dev/null || echo "HTTPSTATUS:000")
    http_code=$(echo "$response" | grep "HTTPSTATUS:" | cut -d: -f2)
    response_time=$(echo "$response" | grep "TIME:" | cut -d: -f2)
    body=$(echo "$response" | sed -E '/^(HTTPSTATUS|TIME):/d')
    
    if [ "$http_code" = "$expected_status" ]; then
        echo -e "✅ ${GREEN}PASS${NC} - HTTP $http_code (${response_time}s)"
        return 0
    else
        echo -e "❌ ${RED}FAIL${NC} - Expected HTTP $expected_status, got $http_code"
        return 1
    fi
}

# Function to check CORS
check_cors() {
    echo -e "\n${YELLOW}🔒 CORS Configuration Check${NC}"
    echo "============================================="
    
    # Test allowed origin
    echo -e "\n1. Testing allowed origin (localhost)"
    cors_response=$(curl -s -I -H "Origin: http://localhost:3000" "$BASE_URL/health" 2>/dev/null || echo "")
    if echo "$cors_response" | grep -q "Access-Control-Allow-Origin"; then
        echo -e "✅ ${GREEN}PASS${NC} - CORS headers present"
        echo "$cors_response" | grep "Access-Control-Allow-Origin"
    else
        echo -e "❌ ${RED}FAIL${NC} - CORS headers missing"
    fi
    
    # Test evil origin (should be blocked)
    echo -e "\n2. Testing blocked origin (evil.com)"
    evil_response=$(curl -s -I -H "Origin: https://evil.com" "$BASE_URL/health" 2>/dev/null || echo "")
    if echo "$evil_response" | grep -q "Access-Control-Allow-Origin: https://evil.com"; then
        echo -e "❌ ${RED}SECURITY RISK${NC} - Evil origin allowed!"
    else
        echo -e "✅ ${GREEN}SECURE${NC} - Evil origin blocked"
    fi
    
    # Test preflight request
    echo -e "\n3. Testing preflight (OPTIONS) request"
    options_response=$(curl -s -X OPTIONS -I \
        -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        "$BASE_URL/feedback" 2>/dev/null || echo "")
    
    if echo "$options_response" | grep -q "Access-Control-Allow-Methods"; then
        echo -e "✅ ${GREEN}PASS${NC} - Preflight handled correctly"
    else
        echo -e "❌ ${RED}FAIL${NC} - Preflight not working"
    fi
}

# Function to check health endpoints
check_health_endpoints() {
    echo -e "\n${YELLOW}💊 Health Check Endpoints${NC}"
    echo "========================================="
    
    # Health check
    if check_endpoint "$BASE_URL/health" "200" "Liveness probe (/health)"; then
        echo "  Expected: Always returns 200 if service is running"
    fi
    
    # Readiness check
    if check_endpoint "$BASE_URL/ready" "200" "Readiness probe (/ready)"; then
        echo "  Expected: Returns 200 when dependencies are available"
    fi
    
    # Root endpoint
    if check_endpoint "$BASE_URL/" "200" "Root endpoint (/)"; then
        echo "  Expected: Service information"
    fi
}

# Function to check metrics
check_metrics() {
    echo -e "\n${YELLOW}📊 Prometheus Metrics${NC}"
    echo "===================================="
    
    if check_endpoint "$BASE_URL/metrics" "200" "Metrics endpoint (/metrics)"; then
        echo -e "\n🔍 Checking for required metrics:"
        
        metrics_response=$(curl -s "$BASE_URL/metrics" 2>/dev/null || echo "")
        
        # Check for specific metrics
        required_metrics=(
            "zeta_requests_total"
            "zeta_request_duration_seconds"
            "zeta_vietnamese_quality_score"
            "zeta_feedback_total"
            "zeta_errors_total"
        )
        
        for metric in "${required_metrics[@]}"; do
            if echo "$metrics_response" | grep -q "$metric"; then
                echo -e "  ✅ ${GREEN}$metric${NC}"
            else
                echo -e "  ❌ ${RED}$metric (missing)${NC}"
            fi
        done
        
        # Check UP metric
        if echo "$metrics_response" | grep -q "# TYPE.*up.*gauge"; then
            echo -e "  ✅ ${GREEN}Service UP metric${NC}"
        fi
    fi
}

# Function to check API endpoints
check_api_endpoints() {
    echo -e "\n${YELLOW}🔌 API Endpoints${NC}"
    echo "==============================="
    
    # Stats endpoint
    if check_endpoint "$BASE_URL/stats" "200" "Statistics endpoint (/stats)"; then
        echo "  Expected: Comprehensive statistics"
    fi
    
    # Test feedback submission
    echo -e "\n🧪 Testing feedback submission"
    feedback_payload='{
        "model_name": "test-model",
        "prompt": "Test prompt",
        "response": "Test response",
        "rating": 8,
        "latency": 1.2,
        "vietnamese_quality": 9,
        "session_id": "test-session-123"
    }'
    
    feedback_response=$(curl -s -X POST "$BASE_URL/feedback" \
        -H "Content-Type: application/json" \
        -d "$feedback_payload" \
        -w "HTTPSTATUS:%{http_code}" 2>/dev/null || echo "HTTPSTATUS:000")
    
    feedback_code=$(echo "$feedback_response" | grep "HTTPSTATUS:" | cut -d: -f2)
    if [ "$feedback_code" = "200" ]; then
        echo -e "✅ ${GREEN}PASS${NC} - Feedback submission working"
    else
        echo -e "❌ ${RED}FAIL${NC} - Feedback submission failed (HTTP $feedback_code)"
    fi
}

# Function to check security headers
check_security_headers() {
    echo -e "\n${YELLOW}🔒 Security Headers${NC}"
    echo "=================================="
    
    headers_response=$(curl -s -I "$BASE_URL/health" 2>/dev/null || echo "")
    
    # Check for security headers
    security_headers=(
        "X-Content-Type-Options"
        "X-Frame-Options"
        "X-XSS-Protection"
        "Strict-Transport-Security"
    )
    
    for header in "${security_headers[@]}"; do
        if echo "$headers_response" | grep -qi "$header"; then
            echo -e "  ✅ ${GREEN}$header${NC}"
        else
            echo -e "  ⚠️  ${YELLOW}$header (recommended)${NC}"
        fi
    done
}

# Function to simulate load and check alerting
check_alerting_simulation() {
    echo -e "\n${YELLOW}🚨 Alerting Simulation${NC}"
    echo "===================================="
    
    echo "Simulating high latency requests..."
    
    # Submit multiple requests with high latency to trigger alerts
    for i in {1..5}; do
        high_latency_payload='{
            "model_name": "load-test",
            "prompt": "Load test prompt",
            "response": "Load test response",
            "rating": 5,
            "latency": 3.5,
            "vietnamese_quality": 6,
            "session_id": "load-test-'$i'"
        }'
        
        curl -s -X POST "$BASE_URL/feedback" \
            -H "Content-Type: application/json" \
            -d "$high_latency_payload" > /dev/null 2>&1
        
        echo -n "."
    done
    
    echo -e "\n✅ ${GREEN}High latency data submitted${NC}"
    echo "Check Prometheus/Alertmanager in 2-3 minutes for alerts"
    echo "Expected alert: ZetaHighLatency (latency > 2s for 2m)"
}

# Function to check Docker health
check_docker_health() {
    echo -e "\n${YELLOW}🐳 Docker Health (if running in container)${NC}"
    echo "=================================================="
    
    # Try to detect if running in Docker
    if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null; then
        echo -e "✅ ${GREEN}Running in Docker container${NC}"
        
        # Check container health
        if command -v docker >/dev/null 2>&1; then
            container_id=$(hostname)
            echo "Container ID: $container_id"
            
            # Check if health check is configured
            docker inspect "$container_id" --format='{{.State.Health.Status}}' 2>/dev/null || echo "No health check configured"
        fi
    else
        echo -e "ℹ️  ${BLUE}Not running in Docker container${NC}"
    fi
}

# Function to performance test
performance_test() {
    echo -e "\n${YELLOW}⚡ Basic Performance Test${NC}"
    echo "====================================="
    
    echo "Running 10 concurrent requests to /health endpoint..."
    
    # Simple load test
    for i in {1..10}; do
        curl -s "$BASE_URL/health" > /dev/null &
    done
    wait
    
    echo -e "✅ ${GREEN}Performance test completed${NC}"
    echo "Check metrics endpoint for request duration statistics"
}

# Main execution
main() {
    echo -e "${BLUE}Starting comprehensive production checks...${NC}\n"
    
    # Basic connectivity test
    if ! curl -s "$BASE_URL/health" > /dev/null 2>&1; then
        echo -e "❌ ${RED}FATAL: Cannot connect to $BASE_URL${NC}"
        echo "Please ensure the service is running and accessible"
        exit 1
    fi
    
    # Run all checks
    check_cors
    check_health_endpoints
    check_metrics
    check_api_endpoints
    check_security_headers
    check_alerting_simulation
    check_docker_health
    performance_test
    
    # Summary
    echo -e "\n${BLUE}🎉 Production Configuration Check Complete!${NC}"
    echo "=============================================="
    echo -e "📊 View metrics: ${BASE_URL}/metrics"
    echo -e "💊 Health check: ${BASE_URL}/health"
    echo -e "📈 Statistics: ${BASE_URL}/stats"
    echo ""
    echo -e "${GREEN}Next steps:${NC}"
    echo "1. Set up Prometheus to scrape ${BASE_URL}/metrics"
    echo "2. Configure Alertmanager with the provided rules"
    echo "3. Set up Grafana dashboard for visualization"
    echo "4. Configure proper CORS origins for production"
    echo "5. Set up TLS/HTTPS for production deployment"
}

# Help function
show_help() {
    echo "Usage: $0 [HOST] [PORT]"
    echo ""
    echo "Examples:"
    echo "  $0                          # Test localhost:9100"
    echo "  $0 localhost 8080           # Test localhost:8080"
    echo "  $0 zeta.yourcompany.com 443 # Test production"
    echo ""
    echo "This script checks:"
    echo "  - CORS configuration"
    echo "  - Health check endpoints"
    echo "  - Prometheus metrics"
    echo "  - API functionality"
    echo "  - Security headers"
    echo "  - Alerting simulation"
}

# Check for help flag
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Run main function
main
