#!/usr/bin/env bash
set -euo pipefail

# ==== GO-LIVE CHECK LITE - Simplified Testing Version ====
#
# Tests only components that don't require running server
#

# ==== Configuration ====
export ZETA_BASE_URL="${ZETA_BASE_URL:-http://127.0.0.1:8000}"
export PERF_P95_MS="${PERF_P95_MS:-200}"

# Create artifacts directory
ART="artifacts/go-live-lite-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$ART"

echo "🚀 GO-LIVE CHECK LITE"
echo "====================="
echo "Testing: Preflight + Code Quality + Configuration"
echo "Artifacts: $ART"
echo ""

# ==== Step 0: Preflight System Check ====
echo "== [0] PREFLIGHT - System Readiness"
echo "Checking: uv, ports, RAM, Redis, packages, disk..."

if ! uv run python scripts/qa/preflight.py 2>&1 | tee "$ART/preflight.txt"; then
    echo "❌ PREFLIGHT FAILED - System not ready"
    echo "Check: $ART/preflight.txt"
    exit 1
fi

echo "✅ Preflight passed"
echo ""

# ==== Step 1: Code Quality ====
echo "== [1] CODE QUALITY - Static Analysis"
echo "Running: ruff check, mypy..."

# Ruff check
echo "  → Running ruff check..."
if ! uv run ruff check . 2>&1 | tee "$ART/ruff_check.txt"; then
    echo "❌ Ruff check failed"
    RUFF_ERRORS=$(wc -l < "$ART/ruff_check.txt")
else
    echo "✅ Ruff check passed"
    RUFF_ERRORS=0
fi

# MyPy check
echo "  → Running mypy..."
if ! uv run mypy . 2>&1 | tee "$ART/mypy_check.txt"; then
    echo "❌ MyPy check failed"
    MYPY_ERRORS=$(grep -c "error:" "$ART/mypy_check.txt" || echo "0")
else
    echo "✅ MyPy check passed"
    MYPY_ERRORS=0
fi

echo ""

# ==== Step 2: Unit Tests ====
echo "== [2] UNIT TESTS - Fast Tests Only"
echo "Running: pytest with fast tests..."

if ! uv run pytest -x --tb=short -q 2>&1 | tee "$ART/pytest.txt"; then
    echo "❌ Unit tests failed"
    TEST_FAILURES=$(grep -c "FAILED" "$ART/pytest.txt" || echo "0")
else
    echo "✅ Unit tests passed"
    TEST_FAILURES=0
fi

echo ""

# ==== Step 3: Configuration Validation ====
echo "== [3] CONFIGURATION - Environment Check"
echo "Validating: environment variables, config files..."

# Check important config files exist
CONFIG_ISSUES=0

if [[ ! -f "pyproject.toml" ]]; then
    echo "❌ pyproject.toml missing"
    ((CONFIG_ISSUES++))
else
    echo "✅ pyproject.toml found"
fi

if [[ ! -f ".env.example" ]]; then
    echo "❌ .env.example missing"
    ((CONFIG_ISSUES++))
else
    echo "✅ .env.example found"
fi

echo ""

# ==== Step JUDGE: Lite Analysis ====
echo "== [JUDGE] LITE ANALYSIS - Code Quality Assessment"

# Create summary
cat > "$ART/lite_summary.json" <<JSON
{
  "timestamp": "$(date -Iseconds)",
  "test_type": "lite",
  "results": {
    "preflight": "passed",
    "ruff_errors": $RUFF_ERRORS,
    "mypy_errors": $MYPY_ERRORS,
    "test_failures": $TEST_FAILURES,
    "config_issues": $CONFIG_ISSUES
  },
  "criteria": {
    "code_quality_pass": $(( RUFF_ERRORS == 0 && MYPY_ERRORS == 0 )),
    "tests_pass": $(( TEST_FAILURES == 0 )),
    "config_pass": $(( CONFIG_ISSUES == 0 ))
  },
  "overall_pass": $(( RUFF_ERRORS == 0 && MYPY_ERRORS == 0 && TEST_FAILURES == 0 && CONFIG_ISSUES == 0 )),
  "recommendations": []
}
JSON

# Add recommendations based on results
OVERALL_PASS=$((RUFF_ERRORS == 0 && MYPY_ERRORS == 0 && TEST_FAILURES == 0 && CONFIG_ISSUES == 0))

echo ""
echo "📁 ARTIFACTS SAVED TO: $ART"
echo "   - preflight.txt     (system readiness)"
echo "   - ruff_check.txt    (code style)"
echo "   - mypy_check.txt    (type checking)"
echo "   - pytest.txt        (unit tests)"
echo "   - lite_summary.json (final results)"
echo ""

if [[ $OVERALL_PASS -eq 1 ]]; then
    echo "🎉 GO-LIVE CHECK LITE: PASS"
    echo "✅ Code quality ready for production"
    echo ""
    echo "💡 Next steps:"
    echo "   1. Start server manually: uv run uvicorn zeta_vn.app.main_production:app --host 0.0.0.0 --port 8000"
    echo "   2. Test endpoints with: uv run python scripts/qa/warm_and_probe_rag.py"
    echo "   3. Run full go-live when server is stable"
    exit 0
else
    echo "💥 GO-LIVE CHECK LITE: FAIL"
    echo "❌ Code quality issues detected:"
    [[ $RUFF_ERRORS -gt 0 ]] && echo "   - $RUFF_ERRORS ruff errors"
    [[ $MYPY_ERRORS -gt 0 ]] && echo "   - $MYPY_ERRORS mypy errors"
    [[ $TEST_FAILURES -gt 0 ]] && echo "   - $TEST_FAILURES test failures"
    [[ $CONFIG_ISSUES -gt 0 ]] && echo "   - $CONFIG_ISSUES config issues"
    echo ""
    echo "🔧 Fix issues above before proceeding"
    exit 2
fi