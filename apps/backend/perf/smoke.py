"""
HTTP performance smoke testing cho CI gates.

Thực hiện kiểm tra P95/P99 latency với FastAPI endpoints để đảm bảo SLO.
Tích hợp vào CI pipeline để phát hiện regression performance.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from statistics import quantiles
from typing import Any

import httpx
from apps.backend.perf.config import get_settings
from pydantic import BaseModel
import Exception
import bool
import cli
import client
import code
import config
import dict
import endpoint
import error
import errors
import exc
import f
import float
import i
import int
import isinstance
import latencies
import len
import list
import max
import min
import open
import out
import p
import print
import q
import range
import result
import round
import sorted
import status_code
import status_codes
import str
import sum
import t
import tuple

logger = logging.getLogger("zeta.perf.smoke")


class SmokeTestResult(BaseModel):
    """Kết quả smoke test performance."""

    endpoint: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    p95_ms: float
    p99_ms: float
    avg_ms: float
    min_ms: float
    max_ms: float
    slo_p95_passed: bool
    slo_p99_passed: bool
    error_rate: float


class SmokeTestConfig(BaseModel):
    """Cấu hình cho smoke testing."""

    endpoints: list[str]
    num_requests: int = 100
    concurrency: int = 10
    timeout_seconds: int = 30
    base_url: str = "http://localhost:8000"


async def _execute_request(
    client: httpx.AsyncClient, url: str
) -> tuple[float, int, str | None]:
    """
    Thực hiện một HTTP request và đo latency.

    Args:
        client: HTTP client
        url: URL để test

    Returns:
        Tuple of (latency_ms, status_code, error_message)
    """
    start_time = time.perf_counter()
    try:
        response = await client.get(url)
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        return latency_ms, response.status_code, None
    except Exception as exc:
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        return latency_ms, 0, str(exc)


async def _test_endpoint_performance(
    endpoint: str, config: SmokeTestConfig
) -> SmokeTestResult:
    """
    Test performance của một endpoint cụ thể.

    Args:
        endpoint: Endpoint path to test
        config: Test configuration

    Returns:
        Performance test results
    """
    url = f"{config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    latencies: list[float] = []
    status_codes: list[int] = []
    errors: list[str] = []

    # Create semaphore for concurrency control
    semaphore = asyncio.Semaphore(config.concurrency)

    async def _bounded_request(
        client: httpx.AsyncClient,
    ) -> tuple[float, int, str | None]:
        async with semaphore:
            return await _execute_request(client, url)

    # Execute requests with timeout
    timeout = httpx.Timeout(timeout=config.timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [_bounded_request(client) for _ in range(config.num_requests)]

        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as exc:
            logger.error("Failed to execute smoke test for %s: %s", endpoint, exc)
            # Return failed result
            return SmokeTestResult(
                endpoint=endpoint,
                total_requests=config.num_requests,
                successful_requests=0,
                failed_requests=config.num_requests,
                p95_ms=0.0,
                p99_ms=0.0,
                avg_ms=0.0,
                min_ms=0.0,
                max_ms=0.0,
                slo_p95_passed=False,
                slo_p99_passed=False,
                error_rate=1.0,
            )

    # Process results
    for result in results:
        if isinstance(result, Exception):
            errors.append(str(result))
            latencies.append(config.timeout_seconds * 1000)  # Timeout as max latency
            status_codes.append(0)
        else:
            latency_ms, status_code, error = result
            latencies.append(latency_ms)
            status_codes.append(status_code)
            if error:
                errors.append(error)

    # Calculate statistics
    successful_requests = sum(1 for code in status_codes if 200 <= code < 400)
    failed_requests = config.num_requests - successful_requests
    error_rate = failed_requests / config.num_requests

    if not latencies:
        logger.warning("No latency data collected for %s", endpoint)
        return SmokeTestResult(
            endpoint=endpoint,
            total_requests=config.num_requests,
            successful_requests=0,
            failed_requests=config.num_requests,
            p95_ms=0.0,
            p99_ms=0.0,
            avg_ms=0.0,
            min_ms=0.0,
            max_ms=0.0,
            slo_p95_passed=False,
            slo_p99_passed=False,
            error_rate=1.0,
        )

    # Calculate percentiles
    try:
        p95_ms = quantiles(latencies, n=20)[18]  # 95th percentile
        p99_ms = quantiles(latencies, n=100)[98]  # 99th percentile
    except Exception:
        # Fallback for small datasets
        sorted_latencies = sorted(latencies)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)
        p95_ms = (
            sorted_latencies[p95_idx]
            if p95_idx < len(sorted_latencies)
            else sorted_latencies[-1]
        )
        p99_ms = (
            sorted_latencies[p99_idx]
            if p99_idx < len(sorted_latencies)
            else sorted_latencies[-1]
        )

    avg_ms = sum(latencies) / len(latencies)
    min_ms = min(latencies)
    max_ms = max(latencies)

    # Check SLO compliance
    settings = get_settings()
    slo_p95_passed = p95_ms <= settings.PERF_SLO_P95_MS
    slo_p99_passed = p99_ms <= settings.PERF_SLO_P99_MS

    logger.info(
        "Endpoint %s: P95=%s ms, P99=%s ms, Success=%s/%s",
        endpoint,
        round(p95_ms, 2),
        round(p99_ms, 2),
        successful_requests,
        config.num_requests,
    )

    return SmokeTestResult(
        endpoint=endpoint,
        total_requests=config.num_requests,
        successful_requests=successful_requests,
        failed_requests=failed_requests,
        p95_ms=round(p95_ms, 2),
        p99_ms=round(p99_ms, 2),
        avg_ms=round(avg_ms, 2),
        min_ms=round(min_ms, 2),
        max_ms=round(max_ms, 2),
        slo_p95_passed=slo_p95_passed,
        slo_p99_passed=slo_p99_passed,
        error_rate=round(error_rate, 4),
    )


async def run_smoke_tests(config: SmokeTestConfig) -> list[SmokeTestResult]:
    """
    Chạy smoke tests cho tất cả endpoints.

    Args:
        config: Test configuration with endpoints and settings

    Returns:
        List of test results for each endpoint
    """
    logger.info(
        "Starting smoke tests for %s endpoints with %s requests each",
        len(config.endpoints),
        config.num_requests,
    )

    # Test all endpoints concurrently
    tasks = [
        _test_endpoint_performance(endpoint, config) for endpoint in config.endpoints
    ]
    results = await asyncio.gather(*tasks)

    # Log summary
    total_slo_violations = sum(
        1 for result in results if not (result.slo_p95_passed and result.slo_p99_passed)
    )

    if total_slo_violations > 0:
        logger.warning("SLO violations detected in %s endpoints", total_slo_violations)
    else:
        logger.info("All endpoints passed SLO requirements")

    return list(results)


def generate_smoke_report(results: list[SmokeTestResult]) -> dict[str, Any]:
    """
    Generate summary report from smoke test results.

    Args:
        results: List of test results

    Returns:
        Summary report dictionary
    """
    if not results:
        return {"status": "error", "message": "No test results"}

    total_endpoints = len(results)
    passed_endpoints = sum(1 for r in results if r.slo_p95_passed and r.slo_p99_passed)
    failed_endpoints = total_endpoints - passed_endpoints

    overall_p95 = sum(r.p95_ms for r in results) / total_endpoints
    overall_p99 = sum(r.p99_ms for r in results) / total_endpoints
    overall_error_rate = sum(r.error_rate for r in results) / total_endpoints

    settings = get_settings()
    slo_compliance = failed_endpoints == 0

    violations = [
        {
            "endpoint": r.endpoint,
            "p95_ms": r.p95_ms,
            "p99_ms": r.p99_ms,
            "p95_violation": not r.slo_p95_passed,
            "p99_violation": not r.slo_p99_passed,
            "error_rate": r.error_rate,
        }
        for r in results
        if not (r.slo_p95_passed and r.slo_p99_passed)
    ]

    return {
        "status": "pass" if slo_compliance else "fail",
        "summary": {
            "total_endpoints": total_endpoints,
            "passed_endpoints": passed_endpoints,
            "failed_endpoints": failed_endpoints,
            "slo_compliance": slo_compliance,
        },
        "performance": {
            "overall_p95_ms": round(overall_p95, 2),
            "overall_p99_ms": round(overall_p99, 2),
            "overall_error_rate": round(overall_error_rate, 4),
        },
        "slo_thresholds": {
            "p95_ms": settings.PERF_SLO_P95_MS,
            "p99_ms": settings.PERF_SLO_P99_MS,
        },
        "violations": violations,
        "detailed_results": [r.model_dump() for r in results],
    }


def _percentile(arr: list[float], p: float) -> float:
    """Calculate percentile from sorted array."""
    if not arr:
        return 0.0
    arr = sorted(arr)
    k = max(0, min(len(arr) - 1, int(round((p / 100) * (len(arr) - 1)))))
    return arr[k]


async def _worker(
    base: str, path: str, q: asyncio.Queue[int], out: list[float]
) -> None:
    """Worker coroutine for concurrent HTTP requests."""
    async with httpx.AsyncClient(base_url=base, timeout=10) as cli:
        while True:
            try:
                await q.get()
                t0 = time.perf_counter()
                try:
                    r = await cli.get(path)
                    r.raise_for_status()
                except Exception as exc:
                    logger.debug("Smoke test request failed for %s: %s", path, exc)
                out.append((time.perf_counter() - t0) * 1000.0)
                q.task_done()
            except asyncio.CancelledError:
                # Clean exit on cancellation
                raise


def main() -> int:
    """
    Simplified HTTP performance smoke test với environment configuration.

    Environment Variables:
        HTTP_PERF_BASE: Base URL (default: http://localhost:8000)
        HTTP_PERF_PATH: Test path (default: /health)
        HTTP_PERF_CONC: Concurrency (default: 50)
        HTTP_PERF_TOTAL: Total requests (default: 1000)
        PERF_SLO_P95_MS: P95 SLO threshold (default: 500)
        PERF_SLO_P99_MS: P99 SLO threshold (default: 1200)
        HTTP_PERF_OUT: Output file (default: reports/http_smoke.json)

    Returns:
        0 if SLO passed, 1 if failed
    """
    import os

    base = os.getenv("HTTP_PERF_BASE", "http://localhost:8000")
    path = os.getenv("HTTP_PERF_PATH", "/health")
    conc = int(os.getenv("HTTP_PERF_CONC", "50"))
    total = int(os.getenv("HTTP_PERF_TOTAL", "1000"))
    p95_slo = int(os.getenv("PERF_SLO_P95_MS", "500"))
    p99_slo = int(os.getenv("PERF_SLO_P99_MS", "1200"))
    out_path = os.getenv("HTTP_PERF_OUT", "reports/http_smoke.json")

    async def run():
        q: asyncio.Queue[int] = asyncio.Queue()
        for i in range(total):
            await q.put(i)
        lat: list[float] = []
        tasks = [asyncio.create_task(_worker(base, path, q, lat)) for _ in range(conc)]
        await q.join()
        for t in tasks:
            t.cancel()
        return lat

    lat = asyncio.run(run())
    p95 = _percentile(lat, 95)
    p99 = _percentile(lat, 99)

    data = {
        "base": base,
        "path": path,
        "conc": conc,
        "total": total,
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "avg_ms": round(sum(lat) / len(lat), 2) if lat else 0.0,
        "slo_p95_passed": p95 <= p95_slo,
        "slo_p99_passed": p99 <= p99_slo,
    }

    # Save report
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Console output
    print(json.dumps(data, indent=2))

    # Exit code based on SLO compliance
    return 0 if (data["slo_p95_passed"] and data["slo_p99_passed"]) else 1


if __name__ == "__main__":  # chạy: python -m zeta_vn.perf.smoke
    import sys

    sys.exit(main())
