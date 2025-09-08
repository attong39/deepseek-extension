"""
WebSocket Load Testing Tool (ws_blast.py)
========================================

Standalone tool for measuring WebSocket throughput and latency.
Supports configurable concurrency and duration for performance benchmarking.
Target: ≥2k MPS (Messages Per Second) with acceptable latency.
"""

import asyncio
import argparse
import json
import signal
import statistics
import sys
import time
from dataclasses import dataclass
from typing import List, Dict, Optional
import Exception
import ImportError
import KeyboardInterrupt
import bool
import client_id
import e
import error
import f
import float
import i
import int
import isinstance
import k
import len
import m
import max
import min
import open
import print
import property
import range
import self
import signum
import str
import sum
import task
import websocket

try:
    import websockets
    from websockets.exceptions import WebSocketException
except ImportError:
    print("❌ ERROR: websockets library not installed")
    print("   Install with: pip install websockets")
    sys.exit(1)

@dataclass
class LoadTestConfig:
    """Configuration for load testing."""
    url: str
    concurrency: int
    duration: int
    team_id: str = "load_test_team"
    task_payload: Optional[Dict] = None
    
    def __post_init__(self):
        if self.task_payload is None:
            self.task_payload = {
                "goal": "load_test_benchmark",
                "input": {
                    "test_mode": True,
                    "duration": self.duration,
                    "fast_mode": True
                }
            }

@dataclass
class ClientMetrics:
    """Metrics from a single WebSocket client."""
    client_id: int
    connected: bool = False
    messages_sent: int = 0
    messages_received: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    latencies: List[float] = None
    errors: List[str] = None
    start_time: float = 0.0
    end_time: float = 0.0
    
    def __post_init__(self):
        if self.latencies is None:
            self.latencies = []
        if self.errors is None:
            self.errors = []
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time > self.start_time else 0.0
    
    @property
    def success(self) -> bool:
        return self.connected and len(self.errors) == 0
    
    @property
    def avg_latency(self) -> float:
        return statistics.mean(self.latencies) if self.latencies else 0.0

class LoadTestRunner:
    """Main load testing orchestrator."""
    
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.running = True
        self.start_time = 0.0
        self.end_time = 0.0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
    
    async def _single_client_worker(self, client_id: int) -> ClientMetrics:
        """Single WebSocket client worker that measures performance."""
        metrics = ClientMetrics(client_id=client_id)
        metrics.start_time = time.perf_counter()
        
        try:
            # Connect to WebSocket
            async with websockets.connect(
                self.config.url,
                max_queue=512,
                ping_interval=30,
                ping_timeout=10,
                close_timeout=5
            ) as websocket:
                metrics.connected = True
                
                # Send initial task
                task_json = json.dumps(self.config.task_payload)
                send_time = time.perf_counter()
                await websocket.send(task_json)
                metrics.messages_sent += 1
                metrics.bytes_sent += len(task_json.encode())
                
                # Receive messages until duration expires
                test_end_time = self.start_time + self.config.duration
                
                while self.running and time.perf_counter() < test_end_time:
                    try:
                        # Receive with timeout
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        receive_time = time.perf_counter()
                        
                        # Calculate latency (time since last send)
                        latency = receive_time - send_time
                        metrics.latencies.append(latency)
                        metrics.messages_received += 1
                        metrics.bytes_received += len(message.encode())
                        
                        # Parse message
                        try:
                            event = json.loads(message)
                            
                            # Check for completion or error
                            if event.get("event") == "team.done":
                                break
                            elif event.get("event") == "error":
                                metrics.errors.append(f"Server error: {event.get('error')}")
                                break
                            elif event.get("type") == "ping":
                                # Respond to ping if needed
                                continue
                                
                        except json.JSONDecodeError:
                            # Skip non-JSON messages
                            pass
                        
                        # Update send time for next latency calculation
                        send_time = receive_time
                        
                    except asyncio.TimeoutError:
                        # No message received, continue
                        continue
                    except WebSocketException as e:
                        metrics.errors.append(f"WebSocket error: {str(e)}")
                        break
                        
        except Exception as e:
            metrics.errors.append(f"Connection error: {str(e)}")
        
        metrics.end_time = time.perf_counter()
        return metrics
    
    async def run_load_test(self) -> Dict:
        """Execute the load test with specified configuration."""
        print(f"🚀 Starting load test:")
        print(f"   URL: {self.config.url}")
        print(f"   Concurrency: {self.config.concurrency}")
        print(f"   Duration: {self.config.duration}s")
        print(f"   Target: ≥2000 MPS")
        print()
        
        self.start_time = time.perf_counter()
        
        # Launch all client workers
        tasks = [
            asyncio.create_task(self._single_client_worker(i))
            for i in range(self.config.concurrency)
        ]
        
        # Wait for completion or timeout
        try:
            metrics_list = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=self.config.duration + 30  # Add 30s buffer
            )
        except asyncio.TimeoutError:
            print("⚠️  Load test timed out, collecting partial results...")
            # Cancel remaining tasks
            for task in tasks:
                if not task.done():
                    task.cancel()
            
            # Collect completed results
            metrics_list = []
            for task in tasks:
                try:
                    if task.done() and not task.cancelled():
                        metrics_list.append(task.result())
                except Exception:
                    pass
        
        self.end_time = time.perf_counter()
        
        # Process results
        return self._calculate_results(metrics_list)
    
    def _calculate_results(self, metrics_list: List) -> Dict:
        """Calculate aggregate performance metrics."""
        valid_metrics = [
            m for m in metrics_list 
            if isinstance(m, ClientMetrics)
        ]
        
        if not valid_metrics:
            return {
                "error": "No valid client metrics collected",
                "success": False
            }
        
        # Aggregate statistics
        total_duration = self.end_time - self.start_time
        successful_clients = sum(1 for m in valid_metrics if m.success)
        failed_clients = len(valid_metrics) - successful_clients
        
        total_messages_sent = sum(m.messages_sent for m in valid_metrics)
        total_messages_received = sum(m.messages_received for m in valid_metrics)
        total_bytes_sent = sum(m.bytes_sent for m in valid_metrics)
        total_bytes_received = sum(m.bytes_received for m in valid_metrics)
        
        # Latency statistics
        all_latencies = []
        for m in valid_metrics:
            all_latencies.extend(m.latencies)
        
        if all_latencies:
            all_latencies.sort()
            latency_stats = {
                "min_ms": min(all_latencies) * 1000,
                "max_ms": max(all_latencies) * 1000,
                "avg_ms": statistics.mean(all_latencies) * 1000,
                "p50_ms": all_latencies[len(all_latencies) // 2] * 1000,
                "p95_ms": all_latencies[int(len(all_latencies) * 0.95)] * 1000,
                "p99_ms": all_latencies[int(len(all_latencies) * 0.99)] * 1000,
                "std_ms": statistics.stdev(all_latencies) * 1000 if len(all_latencies) > 1 else 0.0
            }
        else:
            latency_stats = {k: 0.0 for k in ["min_ms", "max_ms", "avg_ms", "p50_ms", "p95_ms", "p99_ms", "std_ms"]}
        
        # Throughput calculations
        messages_per_second = total_messages_received / total_duration if total_duration > 0 else 0
        bytes_per_second = total_bytes_received / total_duration if total_duration > 0 else 0
        
        # Collect sample errors
        all_errors = []
        for m in valid_metrics:
            all_errors.extend(m.errors)
        
        # Success criteria
        error_rate = failed_clients / len(valid_metrics) if valid_metrics else 1.0
        meets_throughput = messages_per_second >= 2000
        meets_latency = latency_stats["p95_ms"] <= 200
        meets_error_rate = error_rate <= 0.02
        
        return {
            "config": {
                "url": self.config.url,
                "concurrency": self.config.concurrency,
                "duration": self.config.duration,
                "actual_duration": total_duration
            },
            "clients": {
                "total": len(valid_metrics),
                "successful": successful_clients,
                "failed": failed_clients,
                "error_rate": error_rate
            },
            "throughput": {
                "messages_sent": total_messages_sent,
                "messages_received": total_messages_received,
                "messages_per_second": messages_per_second,
                "bytes_sent": total_bytes_sent,
                "bytes_received": total_bytes_received,
                "bytes_per_second": bytes_per_second
            },
            "latency": latency_stats,
            "errors": all_errors[:10],  # Sample of errors
            "success_criteria": {
                "meets_throughput": meets_throughput,
                "meets_latency": meets_latency,
                "meets_error_rate": meets_error_rate,
                "overall_pass": meets_throughput and meets_latency and meets_error_rate
            }
        }

def print_results(results: Dict):
    """Print formatted test results."""
    if "error" in results:
        print(f"❌ {results['error']}")
        return
    
    print("📊 LOAD TEST RESULTS")
    print("=" * 50)
    
    # Configuration
    config = results["config"]
    print(f"URL: {config['url']}")
    print(f"Concurrency: {config['concurrency']} clients")
    print(f"Duration: {config['duration']}s (actual: {config['actual_duration']:.1f}s)")
    print()
    
    # Client success
    clients = results["clients"]
    print(f"📡 CLIENT PERFORMANCE")
    print(f"   Total clients: {clients['total']}")
    print(f"   Successful: {clients['successful']} ({(1-clients['error_rate'])*100:.1f}%)")
    print(f"   Failed: {clients['failed']} ({clients['error_rate']*100:.1f}%)")
    print()
    
    # Throughput
    throughput = results["throughput"]
    print(f"🚄 THROUGHPUT")
    print(f"   Messages received: {throughput['messages_received']:,}")
    print(f"   Messages/second: {throughput['messages_per_second']:.1f} MPS")
    print(f"   Data received: {throughput['bytes_received']:,} bytes ({throughput['bytes_per_second']/1024/1024:.1f} MB/s)")
    print()
    
    # Latency
    latency = results["latency"]
    print(f"⏱️  LATENCY")
    print(f"   Average: {latency['avg_ms']:.1f}ms")
    print(f"   P50: {latency['p50_ms']:.1f}ms")
    print(f"   P95: {latency['p95_ms']:.1f}ms")
    print(f"   P99: {latency['p99_ms']:.1f}ms")
    print(f"   Max: {latency['max_ms']:.1f}ms")
    print()
    
    # Success criteria
    criteria = results["success_criteria"]
    print(f"✅ SUCCESS CRITERIA")
    print(f"   Throughput ≥2000 MPS: {'✅' if criteria['meets_throughput'] else '❌'} ({throughput['messages_per_second']:.1f})")
    print(f"   P95 latency ≤200ms: {'✅' if criteria['meets_latency'] else '❌'} ({latency['p95_ms']:.1f}ms)")
    print(f"   Error rate ≤2%: {'✅' if criteria['meets_error_rate'] else '❌'} ({clients['error_rate']*100:.1f}%)")
    print()
    
    overall = "🎉 PASS" if criteria["overall_pass"] else "💥 FAIL"
    print(f"🏁 OVERALL RESULT: {overall}")
    
    # Show sample errors if any
    if results["errors"]:
        print(f"\n⚠️  SAMPLE ERRORS:")
        for error in results["errors"][:5]:
            print(f"   • {error}")

async def main():
    """Main entry point for load testing tool."""
    parser = argparse.ArgumentParser(description="WebSocket Load Testing Tool")
    parser.add_argument(
        "--url", 
        default="ws://127.0.0.1:8000/api/v1/agents/teams/load_test_team/run",
        help="WebSocket URL to test"
    )
    parser.add_argument(
        "--concurrency", 
        type=int, 
        default=50,
        help="Number of concurrent connections"
    )
    parser.add_argument(
        "--duration", 
        type=int, 
        default=15,
        help="Test duration in seconds"
    )
    parser.add_argument(
        "--team-id",
        default="load_test_team",
        help="Team ID for WebSocket connection"
    )
    parser.add_argument(
        "--output",
        help="Output file for JSON results"
    )
    
    args = parser.parse_args()
    
    # Build WebSocket URL
    ws_url = args.url
    if not ws_url.endswith("/run"):
        # Construct URL from base and team ID
        base_url = args.url.rstrip("/")
        ws_url = f"{base_url}/api/v1/agents/teams/{args.team_id}/run"
    
    config = LoadTestConfig(
        url=ws_url,
        concurrency=args.concurrency,
        duration=args.duration,
        team_id=args.team_id
    )
    
    runner = LoadTestRunner(config)
    results = await runner.run_load_test()
    
    # Print results
    print_results(results)
    
    # Save to file if requested
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")
    
    # Exit with appropriate code
    if results.get("success_criteria", {}).get("overall_pass", False):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Load test interrupted by user")
        sys.exit(130)
