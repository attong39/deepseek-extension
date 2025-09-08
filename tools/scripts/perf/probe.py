"""
Lightweight performance probe tool for ZETA_VN API testing
Provides P50, P95, max latency metrics without heavy dependencies
"""

import argparse
import http.client
import queue
import statistics
import sys
import threading
import time
import urllib.parse


def hit_endpoint(url: str, output_queue: queue.Queue) -> None:
    """Single HTTP request to endpoint with latency measurement"""
    try:
        parsed_url = urllib.parse.urlsplit(url)
        path = parsed_url.path or "/"

        start_time = time.perf_counter()

        # Create connection
        if parsed_url.scheme == "https":
            conn = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port or 443, timeout=10)
        else:
            conn = http.client.HTTPConnection(parsed_url.hostname, parsed_url.port or 80, timeout=10)

        # Make request
        conn.request("GET", path)
        response = conn.getresponse()
        _ = response.read()  # Read response body
        conn.close()

        # Calculate latency in milliseconds
        latency_ms = (time.perf_counter() - start_time) * 1000
        output_queue.put(latency_ms)

    except Exception:
        # Put error marker (negative value)
        output_queue.put(-1)


def run_performance_probe(url: str, concurrency: int, total_requests: int) -> None:
    """Run performance probe with specified parameters"""
    print("🚀 Performance probe starting...")
    print(f"   Target: {url}")
    print(f"   Concurrency: {concurrency}")
    print(f"   Total requests: {total_requests}")
    print()

    result_queue = queue.Queue()
    latencies: list[float] = []
    errors = 0

    start_time = time.time()

    # Launch requests with concurrency control
    requests_sent = 0
    while requests_sent < total_requests:
        # Control concurrency
        while threading.active_count() > concurrency + 1:  # +1 for main thread
            # TODO: Replace blocking sleep with async await asyncio.sleep(0.001)

        # Start new request thread
        thread = threading.Thread(target=hit_endpoint, args=(url, result_queue), daemon=True)
        thread.start()
        requests_sent += 1

        # Show progress
        if requests_sent % 100 == 0:
            print(f"📊 Sent {requests_sent}/{total_requests} requests...")

    # Collect all results
    while len(latencies) + errors < total_requests:
        try:
            result = result_queue.get(timeout=30)
            if result < 0:
                errors += 1
            else:
                latencies.append(result)
        except queue.Empty:
            print("⚠️ Timeout waiting for responses")
            break

    total_time = time.time() - start_time

    # Calculate statistics
    if latencies:
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 20 else max(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        avg_latency = statistics.mean(latencies)
        rps = len(latencies) / total_time if total_time > 0 else 0

        print("\n📊 Performance Results:")
        print("=" * 50)
        print(f"✅ Successful requests: {len(latencies)}")
        print(f"❌ Failed requests: {errors}")
        print(f"⏱️  Total time: {total_time:.2f}s")
        print(f"🚀 Requests/sec: {rps:.1f}")
        print()
        print("📈 Latency Statistics:")
        print(f"   Min:  {min_latency:.1f}ms")
        print(f"   Avg:  {avg_latency:.1f}ms")
        print(f"   P50:  {p50:.1f}ms")
        print(f"   P95:  {p95:.1f}ms")
        print(f"   Max:  {max_latency:.1f}ms")

        # Performance assessment
        print("\n🎯 Performance Assessment:")
        if p95 < 100:
            print("   🟢 EXCELLENT: P95 < 100ms")
        elif p95 < 200:
            print("   🟡 GOOD: P95 < 200ms")
        elif p95 < 500:
            print("   🟠 FAIR: P95 < 500ms")
        else:
            print("   🔴 NEEDS OPTIMIZATION: P95 > 500ms")

    else:
        print("\n❌ No successful requests completed!")
        print("🔧 Check if the server is running and accessible")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Lightweight performance probe for ZETA_VN API")
    parser.add_argument("url", help="Target URL to test")
    parser.add_argument("--concurrency", type=int, default=20, help="Number of concurrent requests (default: 20)")
    parser.add_argument("--requests", type=int, default=400, help="Total number of requests to send (default: 400)")

    args = parser.parse_args()

    # Validate arguments
    if args.concurrency < 1 or args.concurrency > 200:
        print("❌ Concurrency must be between 1 and 200")
        sys.exit(1)

    if args.requests < 1 or args.requests > 10000:
        print("❌ Requests must be between 1 and 10,000")
        sys.exit(1)

    try:
        run_performance_probe(args.url, args.concurrency, args.requests)
    except KeyboardInterrupt:
        print("\n🛑 Performance probe interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Performance probe failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
