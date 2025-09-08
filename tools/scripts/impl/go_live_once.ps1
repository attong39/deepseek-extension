# GO-LIVE CHECK ONCE - PowerShell Version
# Complete end-to-end validation for Windows

param(
    [string]$BaseUrl = "http://127.0.0.1:8000",
    [int]$PerfP95Ms = 200,
    [string]$RagQuery = "one click learning",
    [double]$RagDeltaMin = 0.6,
    [string]$JwtTest = ""
)

# Configuration with environment variable fallbacks
$ErrorActionPreference = "Stop"

if ($env:ZETA_BASE_URL) { $BaseUrl = $env:ZETA_BASE_URL }
if ($env:PERF_P95_MS) { $PerfP95Ms = [int]$env:PERF_P95_MS }
if ($env:RAG_QUERY) { $RagQuery = $env:RAG_QUERY }
if ($env:RAG_DELTA_MIN) { $RagDeltaMin = [double]$env:RAG_DELTA_MIN }
if ($env:JWT_TEST) { $JwtTest = $env:JWT_TEST }

$RagIngest = if ($env:RAG_INGEST) { $env:RAG_INGEST } else { "/api/v1/rag/ingest" }
$RagSearch = if ($env:RAG_SEARCH) { $env:RAG_SEARCH } else { "/api/v1/rag/search" }

# Create artifacts directory
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ArtifactsDir = "artifacts\go-live-$Timestamp"
New-Item -ItemType Directory -Path $ArtifactsDir -Force | Out-Null

Write-Host "🚀 GO-LIVE CHECK ONCE (PowerShell)" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Base URL: $BaseUrl"
Write-Host "P95 threshold: ${PerfP95Ms}ms"
Write-Host "RAG improvement required: $RagDeltaMin"
Write-Host "Artifacts: $ArtifactsDir"
Write-Host ""

try {
    # Step 0: Preflight
    Write-Host "== [0] PREFLIGHT - System Readiness" -ForegroundColor Yellow
    Write-Host "Checking: uv, ports, RAM, Redis, packages, disk..."
    
    $PreflightOutput = & uv run python scripts/qa/preflight.py 2>&1
    $PreflightOutput | Out-File -FilePath "$ArtifactsDir\preflight.txt" -Encoding UTF8
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ PREFLIGHT FAILED - System not ready" -ForegroundColor Red
        Write-Host "Check: $ArtifactsDir\preflight.txt"
        exit 1
    }
    
    Write-Host "✅ Preflight passed" -ForegroundColor Green
    Write-Host ""

    # Step 1-6: Master Run
    Write-Host "== [1-6] MASTER RUN - Code Quality & Performance" -ForegroundColor Yellow
    Write-Host "Running: ruff, mypy, pytest, bandit, performance tests..."
    
    $MasterOutput = & scripts/impl/run_now.ps1 2>&1
    $MasterOutput | Out-File -FilePath "$ArtifactsDir\run_now.txt" -Encoding UTF8
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ MASTER RUN FAILED - Quality checks failed" -ForegroundColor Red
        Write-Host "Check: $ArtifactsDir\run_now.txt"
        exit 1
    }
    
    Write-Host "✅ Master run completed" -ForegroundColor Green
    Write-Host ""

    # Step RAG: Cache Probe
    Write-Host "== [RAG] WARM & PROBE - Cache Effectiveness" -ForegroundColor Yellow
    Write-Host "Testing: ingest → search x3 → measure cache hit & latency improvement"
    
    $RagArgs = @(
        "scripts/qa/warm_and_probe_rag.py",
        "--base", $BaseUrl,
        "--ingest", $RagIngest,
        "--search", $RagSearch,
        "--query", $RagQuery
    )
    
    if ($JwtTest) {
        $RagArgs += @("--jwt", $JwtTest)
    }
    
    $RagOutput = & uv run python @RagArgs 2>&1
    $RagOutput | Out-File -FilePath "$ArtifactsDir\rag_probe.json" -Encoding UTF8
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ RAG PROBE FAILED - Cache testing failed" -ForegroundColor Red
        Write-Host "Check: $ArtifactsDir\rag_probe.json"
        exit 1
    }
    
    Write-Host "✅ RAG probe completed" -ForegroundColor Green
    Write-Host ""

    # Step JUDGE: Auto Analysis
    Write-Host "== [JUDGE] AUTO ANALYSIS - PASS/FAIL Decision" -ForegroundColor Yellow
    
    # Create Python judge script
    $JudgeScript = @"
import json, re, sys, pathlib
from typing import Dict, Any

def parse_results(art_path: str, p95_threshold: float, delta_threshold: float) -> Dict[str, Any]:
    art = pathlib.Path(art_path)
    
    # Parse run_now results for P95
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
        "timestamp": "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz')",
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
            "🔧 Run individual components to debug: preflight.py, run_now.ps1, warm_and_probe_rag.py",
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
"@

    # Run judge analysis
    $JudgeOutput = $JudgeScript | uv run python - $ArtifactsDir $PerfP95Ms $RagDeltaMin 2>&1
    $JudgeExitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "📁 ARTIFACTS SAVED TO: $ArtifactsDir" -ForegroundColor Cyan
    Write-Host "   - preflight.txt     (system readiness)"
    Write-Host "   - run_now.txt       (quality & performance)"
    Write-Host "   - rag_probe.json    (cache effectiveness)"
    Write-Host "   - summary.json      (final decision)"
    Write-Host ""
    
    switch ($JudgeExitCode) {
        0 {
            Write-Host "🎉 GO-LIVE CHECK: PASS" -ForegroundColor Green
            Write-Host "✅ System ready for production deployment" -ForegroundColor Green
        }
        2 {
            Write-Host "💥 GO-LIVE CHECK: FAIL" -ForegroundColor Red
            Write-Host "❌ DO NOT DEPLOY - Check summary.json for specific issues" -ForegroundColor Red
        }
        default {
            Write-Host "⚠️  GO-LIVE CHECK: ERROR" -ForegroundColor Yellow
            Write-Host "🔧 Judge analysis failed - manual review required" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
    Write-Host $JudgeOutput
    
    exit $JudgeExitCode

}
catch {
    Write-Host "💥 GO-LIVE CHECK FAILED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}