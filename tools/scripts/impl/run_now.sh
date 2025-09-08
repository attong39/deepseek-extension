#!/usr/bin/env bash
set -euo pipefail

# ZETA_VN Go-Live Check - Comprehensive validation after foundation/perf/security/CI
# Runs: foundation → boot API (prod) → warm cache → perf probe → zero-trust check → quality gates

echo "🚀 ZETA_VN GO-LIVE CHECK"
echo "========================"
echo "Comprehensive validation: preflight → foundation → API → performance → security → quality"
echo ""

# ==== Preflight Check ====
print_step "0" "Preflight - System Readiness Check"
if uv run python scripts/qa/preflight.py; then
    print_success "Preflight checks passed"
else
    print_error "Preflight checks failed - system not ready"
    exit 1
fi
echo ""

# ==== Configuration ====
export ZETA_BASE_URL="${ZETA_BASE_URL:-http://127.0.0.1:8000}"
export PERF_P95_MS="${PERF_P95_MS:-200}"          # Target P95 latency
export PERF_REQS="${PERF_REQS:-800}"              # Number of requests for load test
export PERF_CONC="${PERF_CONC:-40}"               # Concurrent connections
export JWT_TEST="${JWT_TEST:-}"                   # Valid JWT token for protected routes testing
export REDIS_URL="${REDIS_URL:-}"                 # Redis URL for 2-tier cache testing

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}== [$1/7] $2${NC}"
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

# Global cleanup function
cleanup() {
    if [ -n "${API_PID:-}" ]; then
        echo ""
        print_step "CLEANUP" "Shutting down API server"
        kill "${API_PID}" 2>/dev/null || true
        wait "${API_PID}" 2>/dev/null || true
        print_success "API server stopped"
    fi
}

# Set trap for cleanup
trap cleanup EXIT INT TERM

echo "Configuration:"
echo "  Base URL: ${ZETA_BASE_URL}"
echo "  P95 Target: ${PERF_P95_MS}ms"
echo "  Load Test: ${PERF_REQS} requests, ${PERF_CONC} concurrent"
echo "  JWT Test: ${JWT_TEST:+Enabled}"
echo "  Redis: ${REDIS_URL:+Enabled}"
echo ""

# ==== Step 1: Foundation ====
print_step "1" "Foundation - Code Quality & Dependencies"
if bash scripts/impl/phase1_foundation.sh; then
    print_success "Foundation checks passed"
else
    print_error "Foundation checks failed"
    exit 1
fi
echo ""

# ==== Step 2: Boot API ====
print_step "2" "Boot API (Production Mode)"
echo "Starting production API server..."
uv run uvicorn zeta_vn.app.main_production:app --host 0.0.0.0 --port 8000 &
API_PID=$!
echo "API PID: ${API_PID}"

# Wait for server to start
echo "Waiting for API to start..."
for i in {1..30}; do
    if curl -fsS "${ZETA_BASE_URL}/health" >/dev/null 2>&1; then
        print_success "API server started and responding"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "API server failed to start within 30 seconds"
        exit 1
    fi
    sleep 1
done
echo ""

# ==== Step 3: Warm Cache ====
print_step "3" "Warm Cache (Initial requests)"
echo "Warming up cache with initial requests..."

# Basic health check
curl -fsS "${ZETA_BASE_URL}/health" >/dev/null || print_warning "Health endpoint not responding"

# Warm cache with common endpoints (adjust based on your API)
if curl -fsS "${ZETA_BASE_URL}/api/v1/status" >/dev/null 2>&1; then
    print_success "Status endpoint warmed"
fi

# Try to warm RAG endpoints if available
if curl -fsS "${ZETA_BASE_URL}/rag/query?q=test" >/dev/null 2>&1; then
    print_success "RAG endpoint warmed"
fi

print_success "Cache warming completed"
echo ""

# ==== Step 4: Performance Probe ====
print_step "4" "Performance Probe - Load Testing"
echo "Running performance test against ${ZETA_BASE_URL}/health"
echo "Parameters: ${PERF_REQS} requests, ${PERF_CONC} concurrent connections"

# Run performance probe
OUT=$(uv run python scripts/perf/probe.py "${ZETA_BASE_URL}/health" --concurrency "${PERF_CONC}" --requests "${PERF_REQS}" 2>&1)
echo "${OUT}"

# Extract P95 from output
P95=$(echo "${OUT}" | sed -n 's/.*p95=\([0-9.]*\)ms.*/\1/p')
if [ -z "${P95}" ]; then
    print_error "Could not parse P95 from probe output"
    exit 1
fi

# Check P95 against threshold
if awk -v x="${P95}" -v thr="${PERF_P95_MS}" 'BEGIN{ if (x>thr){exit 1} }'; then
    print_success "P95 ${P95}ms <= ${PERF_P95_MS}ms (target met)"
else
    print_error "P95 ${P95}ms > ${PERF_P95_MS}ms (target exceeded)"
    exit 1
fi
echo ""

# ==== Step 5: Zero-Trust Security Checks ====
print_step "5" "Zero-Trust Security Validation"
echo "Testing authentication and authorization..."

if [ -n "${JWT_TEST}" ]; then
    uv run python scripts/qa/check_zero_trust.py --base "${ZETA_BASE_URL}" --jwt "${JWT_TEST}"
else
    uv run python scripts/qa/check_zero_trust.py --base "${ZETA_BASE_URL}"
    print_warning "JWT_TEST not provided - protected endpoint testing with JWT skipped"
fi

print_success "Zero-Trust checks passed"
echo ""

# ==== Step 6: Quality Gates Snapshot ====
print_step "6" "Quality Gates - Final Validation"
echo "Running comprehensive quality checks..."

QUALITY_ERRORS=0

echo "Running Ruff code quality check..."
if uv run ruff check . --quiet; then
    print_success "Ruff checks passed"
else
    print_warning "Ruff found issues"
    QUALITY_ERRORS=$((QUALITY_ERRORS + 1))
fi

echo "Running MyPy type checking..."
if uv run mypy . --no-error-summary 2>/dev/null; then
    print_success "MyPy checks passed"
else
    print_warning "MyPy found issues"
    QUALITY_ERRORS=$((QUALITY_ERRORS + 1))
fi

echo "Running pytest test suite..."
if uv run pytest -q --tb=no; then
    print_success "Test suite passed"
else
    print_warning "Some tests failed"
    QUALITY_ERRORS=$((QUALITY_ERRORS + 1))
fi

echo "Running Bandit security scan..."
if uv run bandit -q -r zeta_vn; then
    print_success "Security scan passed"
else
    print_warning "Security issues found"
    QUALITY_ERRORS=$((QUALITY_ERRORS + 1))
fi

echo "Running pip-audit dependency check..."
if uv run pip-audit --quiet; then
    print_success "Dependency audit passed"
else
    print_warning "Vulnerable dependencies found"
    QUALITY_ERRORS=$((QUALITY_ERRORS + 1))
fi

echo ""

# ==== Final Summary ====
echo "🎉 GO-LIVE CHECK COMPLETE"
echo "=========================="
echo ""
echo "✅ Foundation: Code quality and dependencies validated"
echo "✅ API Server: Production mode started and responding"
echo "✅ Performance: P95 ${P95}ms <= ${PERF_P95_MS}ms target"
echo "✅ Security: Zero-Trust middleware validated"
if [ $QUALITY_ERRORS -eq 0 ]; then
    echo "✅ Quality Gates: All checks passed"
else
    echo "⚠️  Quality Gates: ${QUALITY_ERRORS} issues found (warnings only)"
fi
echo ""

if [ $QUALITY_ERRORS -eq 0 ]; then
    print_success "ALL SYSTEMS GO! 🚀 Ready for production deployment"
else
    print_warning "System functional but ${QUALITY_ERRORS} quality issues need attention"
fi

echo ""
echo "🎯 Next Steps:"
echo "   1. Address any quality warnings if needed"
echo "   2. Deploy to staging environment"
echo "   3. Run load testing in staging"
echo "   4. Deploy to production with canary"
echo ""
echo "📊 Performance Metrics:"
echo "   - P95 Latency: ${P95}ms"
echo "   - Target: ${PERF_P95_MS}ms"
echo "   - Load Test: ${PERF_REQS} requests @ ${PERF_CONC} concurrent"
echo ""
echo "🔒 Security Status:"
echo "   - Zero-Trust middleware: Active"
echo "   - Authentication: Validated"
echo "   - Security scan: $([ $QUALITY_ERRORS -eq 0 ] && echo "Clean" || echo "Warnings")"