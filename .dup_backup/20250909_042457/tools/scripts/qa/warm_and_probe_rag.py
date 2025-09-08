#!/usr/bin/env python3
"""
RAG Warm & Probe - Real RAG Testing with Cache Hit Measurement

Tests real RAG functionality by:
1. Ingesting sample document
2. Performing search twice to measure cache effectiveness
3. Measuring latency improvements and cache hit rates
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any
import Exception
import base_url
import bool
import bytearray
import bytes
import dict
import e
import exit
import float
import i
import ingest_path
import int
import isinstance
import latency
import len
import method
import min
import print
import query
import range
import response
import round
import s
import search_path
import status
import str
import tuple


def make_request(
    method: str, url: str, data: Any = None, headers: dict[str, str] | None = None
) -> tuple[int, str, dict[str, str], float]:
    """Make HTTP request and return status, body, headers, and latency."""
    headers = headers or {}

    # Prepare request data
    if data is not None and not isinstance(data, (bytes, bytearray)):
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    # Create request
    req = urllib.request.Request(url, method=method, data=data, headers=headers)

    # Measure timing
    start_time = time.perf_counter()

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            response_headers = dict(response.getheaders())
            latency_ms = (time.perf_counter() - start_time) * 1000
            return response.status, body, response_headers, latency_ms
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            error_body = ""
        response_headers = dict(e.headers or {})
        latency_ms = (time.perf_counter() - start_time) * 1000
        return e.code, error_body, response_headers, latency_ms


def test_rag_ingest(base_url: str, ingest_path: str, headers: dict[str, str]) -> bool:
    """Test document ingestion."""
    print("📝 Testing RAG document ingestion...")

    # Sample document for testing
    sample_doc = {
        "source": "demo-test",
        "text": (
            "One-Click Learning: A comprehensive RAG system that performs "
            "document ingestion, extraction, chunking, embedding, and indexing. "
            "Features hybrid BM25 and vector search with intelligent reranking "
            "for optimal retrieval accuracy and performance."
        ),
        "metadata": {"type": "test-document", "created_for": "go-live-check"},
    }

    url = base_url.rstrip("/") + ingest_path
    status, body, response_headers, latency = make_request("POST", url, sample_doc, headers)

    if 200 <= status < 300:
        print(f"  ✅ Document ingested successfully ({latency:.1f}ms)")
        try:
            response_data = json.loads(body)
            if "id" in response_data or "success" in response_data:
                print(f"  📄 Response: {json.dumps(response_data, indent=2)}")
        except json.JSONDecodeError:
            print(f"  📄 Response: {body[:100]}...")
        return True
    else:
        print(f"  ❌ Ingestion failed: {status} - {body}")
        return False


def test_rag_search_with_cache(base_url: str, search_path: str, query: str, headers: dict[str, str]) -> dict[str, Any]:
    """Test RAG search twice to measure cache effectiveness."""
    print(f"🔍 Testing RAG search with query: '{query}'")

    # Prepare search data (POST request with JSON body)
    search_url = f"{base_url.rstrip('/')}{search_path}"
    search_data = {"query": query, "top_k": 5}

    results = {"query": query, "searches": [], "cache_analysis": {}}

    # Perform multiple searches to test caching
    for i in range(1, 4):  # 3 searches to see cache behavior
        print(f"  Search #{i}...")

        status, body, response_headers, latency = make_request("POST", search_url, search_data, headers)

        if 200 <= status < 300:
            cache_header = response_headers.get("X-Cache", "UNKNOWN")

            search_result = {
                "attempt": i,
                "status": status,
                "latency_ms": round(latency, 1),
                "cache_status": cache_header,
                "timestamp": time.time(),
            }

            try:
                response_data = json.loads(body)
                search_result["response_size"] = len(body)
                search_result["results_count"] = len(response_data.get("hits", []))
            except json.JSONDecodeError:
                search_result["response_size"] = len(body)
                search_result["results_count"] = 0

            results["searches"].append(search_result)
            print(f"    ✅ {status} in {latency:.1f}ms, Cache: {cache_header}")
        else:
            print(f"    ❌ Search failed: {status} - {body}")
            results["searches"].append(
                {
                    "attempt": i,
                    "status": status,
                    "latency_ms": round(latency, 1),
                    "error": body[:100],
                    "timestamp": time.time(),
                }
            )

    # Analyze cache performance
    if len(results["searches"]) >= 2:
        latencies = [s["latency_ms"] for s in results["searches"] if s.get("latency_ms")]
        cache_statuses = [s.get("cache_status", "UNKNOWN") for s in results["searches"]]

        results["cache_analysis"] = {
            "first_search_ms": latencies[0] if latencies else 0,
            "subsequent_searches_ms": latencies[1:] if len(latencies) > 1 else [],
            "avg_latency_ms": round(statistics.mean(latencies), 1) if latencies else 0,
            "cache_hit_rate": cache_statuses.count("HIT") / len(cache_statuses) if cache_statuses else 0,
            "cache_headers": cache_statuses,
            "performance_improvement": {
                "absolute_ms": round(latencies[0] - min(latencies[1:]), 1) if len(latencies) > 1 else 0,
                "percentage": round((1 - min(latencies[1:]) / latencies[0]) * 100, 1)
                if len(latencies) > 1 and latencies[0] > 0
                else 0,
            },
        }

    return results


def main():
    parser = argparse.ArgumentParser(description="RAG warm & probe testing")
    parser.add_argument("--base", default="http://127.0.0.1:8000", help="Base URL of the API")
    parser.add_argument("--ingest", default="/api/v1/rag/ingest", help="Ingest endpoint path")
    parser.add_argument("--search", default="/api/v1/rag/search", help="Search endpoint path")
    parser.add_argument("--jwt", default="", help="JWT token for authentication")
    parser.add_argument("--query", default="one click learning", help="Search query to test")

    args = parser.parse_args()

    print("🔥 RAG WARM & PROBE")
    print("===================")
    print(f"Base URL: {args.base}")
    print(f"Ingest endpoint: {args.ingest}")
    print(f"Search endpoint: {args.search}")
    print(f"Test query: '{args.query}'")
    print(f"Authentication: {'Enabled' if args.jwt else 'Disabled'}")
    print()

    # Prepare headers
    headers = {}
    if args.jwt:
        headers["Authorization"] = f"Bearer {args.jwt}"

    try:
        # Step 1: Test document ingestion
        if not test_rag_ingest(args.base, args.ingest, headers):
            print("❌ RAG ingestion test failed")
            return 1

        print()

        # Step 2: Test search with cache measurement
        search_results = test_rag_search_with_cache(args.base, args.search, args.query, headers)

        print()
        print("📊 RAG PERFORMANCE ANALYSIS")
        print("============================")

        # Output results as JSON for easy parsing
        output = {
            "rag_test_results": search_results,
            "summary": {
                "total_searches": len(search_results["searches"]),
                "successful_searches": len([s for s in search_results["searches"] if s.get("status", 0) == 200]),
                "cache_effectiveness": search_results.get("cache_analysis", {}),
            },
            "recommendations": [],
        }

        # Add recommendations based on results
        cache_analysis = search_results.get("cache_analysis", {})
        if cache_analysis:
            hit_rate = cache_analysis.get("cache_hit_rate", 0)
            improvement = cache_analysis.get("performance_improvement", {}).get("percentage", 0)

            if hit_rate < 0.5:
                output["recommendations"].append("Low cache hit rate - consider increasing cache TTL")

            if improvement < 20:
                output["recommendations"].append("Limited performance improvement from caching - review cache strategy")

            if cache_analysis.get("first_search_ms", 0) > 1000:
                output["recommendations"].append(
                    "Initial search latency high - consider optimizing embedding/retrieval"
                )

        print(json.dumps(output, indent=2, ensure_ascii=False))

        # Return success/failure based on results
        successful_searches = output["summary"]["successful_searches"]
        if successful_searches >= 2:
            print()
            print("✅ RAG warm & probe completed successfully!")
            return 0
        else:
            print()
            print("❌ RAG warm & probe failed - insufficient successful searches")
            return 1

    except Exception as e:
        print(f"❌ RAG warm & probe failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
