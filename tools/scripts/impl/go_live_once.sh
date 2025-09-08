#!/usr/bin/env bash
set -euo pipefail

# ==== GO-LIVE CHECK ONCE - Complete End-to-End Validation ====
#
# Chạy full pipeline: Preflight → QA checks → RAG probe → Auto judge
# Output: PASS/FAIL với artifacts và gợi ý rollback
#

# ==== Configuration ====
export ZETA_BASE_URL="${ZETA_BASE_URL:-http://127.0.0.1:8000}"
export PERF_P95_MS="${PERF_P95_MS:-200}"
export PERF_REQS="${PERF_REQS:-800}"
export PERF_CONC="${PERF_CONC:-40}"
export RAG_INGEST="${RAG_INGEST:-/api/v1/rag/ingest}"
export RAG_SEARCH="${RAG_SEARCH:-/api/v1/rag/search}"
export RAG_QUERY="${RAG_QUERY:-one click learning}"
export RAG_DELTA_MIN="${RAG_DELTA_MIN:-0.60}"   # >=60% cache improvement required
export JWT_TEST="${JWT_TEST:-}"

# Create artifacts directory
ART="artifacts/go-live-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$ART"

echo "🚀 GO-LIVE CHECK ONCE"
echo "====================="
echo "Base URL: $ZETA_BASE_URL"
echo "P95 threshold: ${PERF_P95_MS}ms"
echo "RAG improvement required: ${RAG_DELTA_MIN}"
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

# ==== Step 1-6: Master Quality Run ====
echo "== [1-6] MASTER RUN - Code Quality & Performance"
echo "Running: ruff, mypy, pytest, bandit, performance tests..."

if ! bash scripts/impl/run_now.sh 2>&1 | tee "$ART/run_now.txt"; then
    echo "❌ MASTER RUN FAILED - Quality checks failed"
    echo "Check: $ART/run_now.txt"
    exit 1
fi

echo "✅ Master run completed"
echo ""

# ==== Step RAG: Cache & Performance Probe ====
echo "== [RAG] WARM & PROBE - Cache Effectiveness"
echo "Testing: ingest → search x3 → measure cache hit & latency improvement"

RAG_CMD="uv run python scripts/qa/warm_and_probe_rag.py --base \"$ZETA_BASE_URL\" --ingest \"$RAG_INGEST\" --search \"$RAG_SEARCH\" --query \"$RAG_QUERY\""

if [[ -n "$JWT_TEST" ]]; then
    RAG_CMD="$RAG_CMD --jwt \"$JWT_TEST\""
fi

if ! eval "$RAG_CMD" 2>&1 | tee "$ART/rag_probe.json"; then
    echo "❌ RAG PROBE FAILED - Cache testing failed"
    echo "Check: $ART/rag_probe.json"
    exit 1
fi

echo "✅ RAG probe completed"
echo ""

# ==== Step JUDGE: Auto Analysis & Decision ====
echo "== [JUDGE] AUTO ANALYSIS - PASS/FAIL Decision"

# Parse results and make go-live decision
uv run python - <<JUDGE_PY "$ART" "$PERF_P95_MS" "$RAG_DELTA_MIN"
import json, re, sys, pathlib
from typing import Dict, Any

def parse_results(art_path: str, p95_threshold: float, delta_threshold: float) -> Dict[str, Any]:
    art = pathlib.Path(art_path)
    
    # Parse run_now.sh results for P95
    run_now_text = (art / "run_now.txt").read_text(encoding="utf-8")
    p95_match = re.search(r"p95=([0-9.]+)ms", run_now_text)
    p95_ms = float(p95_match.group(1)) if p95_match else 99999.0
    
    # Check for test failures
    test_failures = len(re.findall(r"FAILED|ERROR", run_now_text, re.IGNORECASE))
    
    # Parse RAG probe results
    try:
        rag_data = json.loads((art / "rag_probe.json").read_text(encoding="utf-8"))
        rag_analysis = rag_data.get("rag_test_results", {}).get("cache_analysis", {})
        
        first_search_ms = rag_analysis.get("first_search_ms", 0)
        subsequent_ms = rag_analysis.get("subsequent_searches_ms", [])
        second_search_ms = subsequent_ms[0] if subsequent_ms else first_search_ms
        
        # Calculate improvement
        if first_search_ms > 0:
            latency_delta = (first_search_ms - second_search_ms) / first_search_ms
        else:
            latency_delta = 0.0
            
        cache_headers = rag_analysis.get("cache_headers", [])
        second_cache_hit = len(cache_headers) >= 2 and cache_headers[1] == "HIT"
        
    except Exception as e:
        print(f"Warning: Could not parse RAG results: {e}")
        first_search_ms = 99999.0
        second_search_ms = 99999.0
        latency_delta = 0.0
        second_cache_hit = False
    
    # Evaluate criteria
    pass_p95 = p95_ms <= p95_threshold
    pass_tests = test_failures == 0
    pass_cache_improvement = latency_delta >= delta_threshold or second_cache_hit
    
    # Overall decision
    overall_pass = pass_p95 and pass_tests and pass_cache_improvement
    
    summary = {
        "timestamp": "$(date -Iseconds)",
        "criteria": {
            "p95_ms": round(p95_ms, 1),
            "p95_threshold": p95_threshold,
            "pass_p95": pass_p95,
            "test_failures": test_failures,
            "pass_tests": pass_tests,
            "rag_first_search_ms": round(first_search_ms, 1),
            "rag_second_search_ms": round(second_search_ms, 1),
            "rag_improvement_ratio": round(latency_delta, 3),
            "rag_improvement_threshold": delta_threshold,
            "rag_second_cache_hit": second_cache_hit,
            "pass_cache": pass_cache_improvement
        },
        "decision": {
            "overall_pass": overall_pass,
            "ready_for_production": overall_pass
        },
        "recommendations": []
    }
    
    # Add specific recommendations
    if not pass_p95:
        summary["recommendations"].append(f"🔴 P95 latency too high ({p95_ms:.1f}ms > {p95_threshold}ms) - optimize performance")
    
    if not pass_tests:
        summary["recommendations"].append(f"🔴 {test_failures} test failures - fix all failing tests")
    
    if not pass_cache_improvement:
        if not second_cache_hit:
            summary["recommendations"].append("🔴 Cache not hitting on second search - check cache configuration")
        summary["recommendations"].append(f"🔴 Cache improvement insufficient ({latency_delta:.1%} < {delta_threshold:.1%}) - optimize cache strategy")
    
    if overall_pass:
        summary["recommendations"].extend([
            "✅ All criteria passed - ready for production deployment",
            "💡 Monitor metrics after deployment",
            "💡 Consider gradual rollout with canary deployment"
        ])
    else:
        summary["recommendations"].extend([
            "❌ DO NOT DEPLOY - fix issues above first",
            "🔧 Run individual components to debug: preflight.py, run_now.sh, warm_and_probe_rag.py",
            "📊 Review detailed logs in artifacts directory"
        ])
    
    return summary

# Main execution
try:
    art_path, p95_str, delta_str = sys.argv[1], sys.argv[2], sys.argv[3]
    results = parse_results(art_path, float(p95_str), float(delta_str))
    
    # Output results
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save summary
    with open(pathlib.Path(art_path) / "summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Exit with appropriate code
    if results["decision"]["overall_pass"]:
        print("\n🎉 GO-LIVE CHECK PASSED - READY FOR PRODUCTION!")
        sys.exit(0)
    else:
        print("\n💥 GO-LIVE CHECK FAILED - DO NOT DEPLOY")
        sys.exit(2)
        
except Exception as e:
    print(f"❌ Judge analysis failed: {e}")
    sys.exit(3)
JUDGE_PY

JUDGE_EXIT=$?

echo ""
echo "📁 ARTIFACTS SAVED TO: $ART"
echo "   - preflight.txt     (system readiness)"
echo "   - run_now.txt       (quality & performance)"
echo "   - rag_probe.json    (cache effectiveness)"
echo "   - summary.json      (final decision)"
echo ""

case $JUDGE_EXIT in
    0)
        echo "🎉 GO-LIVE CHECK: PASS"
        echo "✅ System ready for production deployment"
        ;;
    2)
        echo "💥 GO-LIVE CHECK: FAIL"
        echo "❌ DO NOT DEPLOY - Check summary.json for specific issues"
        ;;
    *)
        echo "⚠️  GO-LIVE CHECK: ERROR"
        echo "🔧 Judge analysis failed - manual review required"
        ;;
esac

exit $JUDGE_EXIT