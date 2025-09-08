"""
End-to-End WebSocket Stress Testing
===================================

Tests WebSocket streaming with 100+ concurrent clients.
Verifies error rate <2% and P95 latency <200ms under load.
"""

import asyncio
import json
import os
import time
from typing import Dict, List
import pytest
import websockets
from websockets.exceptions import WebSocketException
import Exception
import any
import bool
import e
import enumerate
import float
import i
import int
import isinstance
import len
import max
import message
import num_clients
import print
import property
import r
import range
import self
import size
import str
import sum
import team_id
import websocket


# Test configuration
WS_BASE_URL = os.getenv("WS_URL", "ws://127.0.0.1:8000/api/v1/agents/teams")
TEST_TEAM_ID = "stress_test_team"
CONCURRENT_CLIENTS = 100
ERROR_RATE_THRESHOLD = 0.02  # 2% max error rate
P95_LATENCY_THRESHOLD = 0.2  # 200ms max P95 latency

# Test payload
STRESS_TEST_TASK = {
    "goal": "stress_test_execution",
    "input": {
        "test_mode": True,
        "duration": 10,
        "iterations": 50
    },
    "priority": "normal"
}

class WebSocketTestResult:
    """Results from a single WebSocket client test."""
    
    def __init__(self):
        self.connected = False
        self.messages_received = 0
        self.error = None
        self.latencies: List[float] = []
        self.start_time = 0.0
        self.end_time = 0.0
        self.completion_event_received = False
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time
    
    @property
    def success(self) -> bool:
        return self.connected and self.completion_event_received and self.error is None

async def single_ws_client(client_id: int, team_id: str) -> WebSocketTestResult:
    """
    Single WebSocket client that connects, sends task, and measures performance.
    
    Args:
        client_id: Unique client identifier
        team_id: Team ID to connect to
        
    Returns:
        WebSocketTestResult with performance metrics
    """
    result = WebSocketTestResult()
    result.start_time = time.perf_counter()
    
    ws_url = f"{WS_BASE_URL}/{team_id}/run"
    
    try:
        async with websockets.connect(
            ws_url, 
            max_queue=None,
            ping_interval=None,  # Disable auto-ping for testing
            ping_timeout=None
        ) as websocket:
            result.connected = True
            
            # Send initial task request
            task_json = json.dumps(STRESS_TEST_TASK)
            send_start = time.perf_counter()
            await websocket.send(task_json)
            
            # Receive messages until completion
            async for message in websocket:
                receive_time = time.perf_counter()
                latency = receive_time - send_start
                result.latencies.append(latency)
                result.messages_received += 1
                
                try:
                    event = json.loads(message)
                    
                    # Check for completion events
                    if event.get("event") == "team.done":
                        result.completion_event_received = True
                        break
                    elif event.get("event") == "error":
                        result.error = event.get("error", "Unknown error")
                        break
                    elif event.get("type") == "ping":
                        # Respond to ping with pong (if needed)
                        continue
                        
                    # Reset send time for next message latency calculation
                    send_start = receive_time
                    
                except json.JSONDecodeError:
                    # Skip non-JSON messages (e.g., ping frames)
                    continue
                
                # Safety timeout: don't run forever
                if time.perf_counter() - result.start_time > 60.0:
                    result.error = "Test timeout after 60 seconds"
                    break
                    
    except WebSocketException as e:
        result.error = f"WebSocket error: {str(e)}"
    except asyncio.TimeoutError:
        result.error = "Connection timeout"
    except Exception as e:
        result.error = f"Unexpected error: {str(e)}"
    finally:
        result.end_time = time.perf_counter()
    
    return result

async def run_concurrent_stress_test(
    num_clients: int, 
    team_id: str = TEST_TEAM_ID
) -> Dict[str, any]:
    """
    Run stress test with specified number of concurrent WebSocket clients.
    
    Args:
        num_clients: Number of concurrent clients to simulate
        team_id: Team ID for WebSocket connection
        
    Returns:
        Dictionary with test results and performance metrics
    """
    print(f"🚀 Starting stress test with {num_clients} concurrent clients...")
    
    # Launch all clients concurrently
    start_time = time.perf_counter()
    
    tasks = [
        asyncio.create_task(single_ws_client(i, team_id))
        for i in range(num_clients)
    ]
    
    # Wait for all clients to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    
    # Process results
    successful_results = []
    errors = []
    all_latencies = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            errors.append(f"Client {i}: {str(result)}")
        elif isinstance(result, WebSocketTestResult):
            if result.success:
                successful_results.append(result)
                all_latencies.extend(result.latencies)
            else:
                errors.append(f"Client {i}: {result.error or 'Failed to complete'}")
        else:
            errors.append(f"Client {i}: Unknown result type")
    
    # Calculate performance metrics
    success_count = len(successful_results)
    error_count = len(errors)
    total_clients = num_clients
    error_rate = error_count / total_clients if total_clients > 0 else 1.0
    
    # Latency statistics
    if all_latencies:
        all_latencies.sort()
        p50_latency = all_latencies[len(all_latencies) // 2]
        p95_latency = all_latencies[int(len(all_latencies) * 0.95)]
        p99_latency = all_latencies[int(len(all_latencies) * 0.99)]
        avg_latency = sum(all_latencies) / len(all_latencies)
        max_latency = max(all_latencies)
    else:
        p50_latency = p95_latency = p99_latency = avg_latency = max_latency = 0.0
    
    # Message throughput
    total_messages = sum(r.messages_received for r in successful_results)
    messages_per_second = total_messages / total_duration if total_duration > 0 else 0
    
    return {
        "test_config": {
            "concurrent_clients": num_clients,
            "team_id": team_id,
            "duration": total_duration
        },
        "results": {
            "successful_clients": success_count,
            "failed_clients": error_count,
            "error_rate": error_rate,
            "total_messages": total_messages,
            "messages_per_second": messages_per_second
        },
        "latency_metrics": {
            "p50_ms": p50_latency * 1000,
            "p95_ms": p95_latency * 1000,
            "p99_ms": p99_latency * 1000,
            "avg_ms": avg_latency * 1000,
            "max_ms": max_latency * 1000
        },
        "errors": errors[:10],  # Show first 10 errors
        "passed": error_rate <= ERROR_RATE_THRESHOLD and p95_latency <= P95_LATENCY_THRESHOLD
    }

# Pytest test cases

@pytest.mark.asyncio
@pytest.mark.timeout(120)  # 2 minute timeout
async def test_ws_stress_small():
    """Test WebSocket streaming with 10 concurrent clients (smoke test)."""
    results = await run_concurrent_stress_test(10)
    
    print(f"📊 Small stress test results:")
    print(f"   Success rate: {(1-results['results']['error_rate'])*100:.1f}%")
    print(f"   P95 latency: {results['latency_metrics']['p95_ms']:.1f}ms")
    print(f"   Throughput: {results['results']['messages_per_second']:.1f} MPS")
    
    # Assertions
    assert results["results"]["error_rate"] <= ERROR_RATE_THRESHOLD, \
        f"Error rate {results['results']['error_rate']:.2%} exceeds threshold {ERROR_RATE_THRESHOLD:.2%}"
    
    assert results["latency_metrics"]["p95_ms"] <= P95_LATENCY_THRESHOLD * 1000, \
        f"P95 latency {results['latency_metrics']['p95_ms']:.1f}ms exceeds threshold {P95_LATENCY_THRESHOLD*1000:.1f}ms"

@pytest.mark.asyncio  
@pytest.mark.timeout(180)  # 3 minute timeout
async def test_ws_stress_medium():
    """Test WebSocket streaming with 50 concurrent clients."""
    results = await run_concurrent_stress_test(50)
    
    print(f"📊 Medium stress test results:")
    print(f"   Success rate: {(1-results['results']['error_rate'])*100:.1f}%")
    print(f"   P95 latency: {results['latency_metrics']['p95_ms']:.1f}ms")
    print(f"   Throughput: {results['results']['messages_per_second']:.1f} MPS")
    
    # More lenient thresholds for higher load
    assert results["results"]["error_rate"] <= 0.05, \
        f"Error rate {results['results']['error_rate']:.2%} exceeds 5% threshold"
    
    assert results["latency_metrics"]["p95_ms"] <= 500, \
        f"P95 latency {results['latency_metrics']['p95_ms']:.1f}ms exceeds 500ms threshold"

@pytest.mark.asyncio
@pytest.mark.timeout(300)  # 5 minute timeout  
@pytest.mark.slow
async def test_ws_stress_large():
    """Test WebSocket streaming with 100 concurrent clients (full stress test)."""
    results = await run_concurrent_stress_test(CONCURRENT_CLIENTS)
    
    print(f"📊 Large stress test results:")
    print(f"   Concurrent clients: {results['test_config']['concurrent_clients']}")
    print(f"   Success rate: {(1-results['results']['error_rate'])*100:.1f}%")
    print(f"   Failed clients: {results['results']['failed_clients']}")
    print(f"   Total messages: {results['results']['total_messages']}")
    print(f"   Throughput: {results['results']['messages_per_second']:.1f} MPS")
    print(f"   P50 latency: {results['latency_metrics']['p50_ms']:.1f}ms")
    print(f"   P95 latency: {results['latency_metrics']['p95_ms']:.1f}ms")
    print(f"   P99 latency: {results['latency_metrics']['p99_ms']:.1f}ms")
    print(f"   Max latency: {results['latency_metrics']['max_ms']:.1f}ms")
    
    if results["errors"]:
        print(f"   Sample errors: {results['errors'][:3]}")
    
    # Production-grade assertions
    assert results["results"]["error_rate"] <= ERROR_RATE_THRESHOLD, \
        f"Error rate {results['results']['error_rate']:.2%} exceeds threshold {ERROR_RATE_THRESHOLD:.2%}"
    
    assert results["latency_metrics"]["p95_ms"] <= P95_LATENCY_THRESHOLD * 1000, \
        f"P95 latency {results['latency_metrics']['p95_ms']:.1f}ms exceeds threshold {P95_LATENCY_THRESHOLD*1000:.1f}ms"
    
    # Additional throughput check
    assert results["results"]["messages_per_second"] >= 1000, \
        f"Throughput {results['results']['messages_per_second']:.1f} MPS below minimum 1000 MPS"
    
    print("✅ Large stress test PASSED - System ready for production load!")

# Manual test runner for development
if __name__ == "__main__":
    async def main():
        print("🔥 WebSocket Stress Test Runner")
        print("=" * 50)
        
        # Run progressively larger tests
        test_sizes = [10, 25, 50, 100]
        
        for size in test_sizes:
            print(f"\n🎯 Testing {size} concurrent clients...")
            try:
                results = await run_concurrent_stress_test(size)
                
                if results["passed"]:
                    print(f"✅ {size} clients: PASSED")
                else:
                    print(f"❌ {size} clients: FAILED")
                    print(f"   Error rate: {results['results']['error_rate']:.2%}")
                    print(f"   P95 latency: {results['latency_metrics']['p95_ms']:.1f}ms")
                    break
                    
            except Exception as e:
                print(f"❌ {size} clients: EXCEPTION - {str(e)}")
                break
        
        print("\n🏁 Stress testing completed!")
    
    asyncio.run(main())
