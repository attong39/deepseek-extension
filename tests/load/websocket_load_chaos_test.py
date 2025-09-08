"""
Load and Chaos Testing for WebSocket at 10k msg/s
"""
import asyncio
import json
import logging
import time
import statistics
from typing import Dict, List, Any
from datetime import datetime, timedelta

import websockets
import aiohttp
from prometheus_client import Counter, Histogram, Gauge
import Exception
import bool
import chaos_mode
import concurrent_connections
import connection_id
import duration_seconds
import e
import float
import i
import int
import key
import max
import message_size_bytes
import min
import print
import range
import scenario
import self
import str
import target_url
import value
import websocket


logger = logging.getLogger(__name__)

# Prometheus metrics
ws_messages_sent = Counter("load_test_ws_messages_sent_total", "WebSocket messages sent")
ws_messages_received = Counter("load_test_ws_messages_received_total", "WebSocket messages received")
ws_message_latency = Histogram("load_test_ws_message_latency_seconds", "WebSocket message latency")
ws_connections_active = Gauge("load_test_ws_connections_active", "Active WebSocket connections")
ws_errors_total = Counter("load_test_ws_errors_total", "WebSocket errors", ["error_type"])


class LoadTestConfig:
    """Load test configuration"""
    
    def __init__(
        self,
        target_url: str = "ws://localhost:8000/ws",
        target_rps: int = 10000,  # 10k messages per second
        duration_seconds: int = 60,
        concurrent_connections: int = 100,
        message_size_bytes: int = 1024,
        chaos_mode: bool = False
    ):
        self.target_url = target_url
        self.target_rps = target_rps
        self.duration_seconds = duration_seconds
        self.concurrent_connections = concurrent_connections
        self.message_size_bytes = message_size_bytes
        self.chaos_mode = chaos_mode
        
        # Calculated values
        self.messages_per_connection = target_rps // concurrent_connections
        self.interval_between_messages = 1.0 / self.messages_per_connection if self.messages_per_connection > 0 else 1.0


class LoadTestResult:
    """Load test results"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.messages_sent = 0
        self.messages_received = 0
        self.errors = 0
        self.latencies = []
        self.connection_errors = 0
        self.message_errors = 0
        
    def add_latency(self, latency: float):
        """Add message latency measurement"""
        self.latencies.append(latency)
        ws_message_latency.observe(latency)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get test statistics"""
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0
        
        stats = {
            "duration_seconds": duration,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "errors": self.errors,
            "connection_errors": self.connection_errors,
            "message_errors": self.message_errors,
            "success_rate": self.messages_received / max(self.messages_sent, 1),
            "messages_per_second": self.messages_sent / max(duration, 1),
            "received_per_second": self.messages_received / max(duration, 1)
        }
        
        if self.latencies:
            stats.update({
                "latency_p50": statistics.median(self.latencies),
                "latency_p95": statistics.quantiles(self.latencies, n=20)[18],  # 95th percentile
                "latency_p99": statistics.quantiles(self.latencies, n=100)[98],  # 99th percentile
                "latency_avg": statistics.mean(self.latencies),
                "latency_min": min(self.latencies),
                "latency_max": max(self.latencies)
            })
        
        return stats


class WebSocketLoadTester:
    """WebSocket load tester"""
    
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.result = LoadTestResult()
        self.active_connections = 0
        
    async def create_test_message(self, connection_id: int, message_id: int) -> str:
        """Create test message payload"""
        message = {
            "type": "load_test",
            "connection_id": connection_id,
            "message_id": message_id,
            "timestamp": time.time(),
            "payload": "x" * max(0, self.config.message_size_bytes - 200)  # Padding to reach target size
        }
        return json.dumps(message)
    
    async def connection_worker(self, connection_id: int):
        """Worker for a single WebSocket connection"""
        try:
            async with websockets.connect(self.config.target_url) as websocket:
                self.active_connections += 1
                ws_connections_active.set(self.active_connections)
                
                logger.debug(f"Connection {connection_id} established")
                
                # Send messages at target rate
                message_id = 0
                start_time = time.time()
                
                while time.time() - start_time < self.config.duration_seconds:
                    try:
                        # Create and send message
                        message = await self.create_test_message(connection_id, message_id)
                        send_time = time.time()
                        
                        await websocket.send(message)
                        ws_messages_sent.inc()
                        self.result.messages_sent += 1
                        
                        # Try to receive response (with timeout)
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                            receive_time = time.time()
                            
                            # Calculate latency
                            latency = receive_time - send_time
                            self.result.add_latency(latency)
                            
                            ws_messages_received.inc()
                            self.result.messages_received += 1
                            
                        except asyncio.TimeoutError:
                            logger.warning(f"Connection {connection_id} timeout on message {message_id}")
                            ws_errors_total.labels(error_type="timeout").inc()
                            self.result.message_errors += 1
                        
                        message_id += 1
                        
                        # Rate limiting
                        if self.config.interval_between_messages > 0:
                            await asyncio.sleep(self.config.interval_between_messages)
                            
                        # Chaos mode: random disconnections
                        if self.config.chaos_mode and message_id % 100 == 0:
                            import random
                            if random.random() < 0.01:  # 1% chance of chaos
                                logger.info(f"Chaos mode: disconnecting connection {connection_id}")
                                break
                                
                    except Exception as e:
                        logger.error(f"Connection {connection_id} message error: {e}")
                        ws_errors_total.labels(error_type="message").inc()
                        self.result.message_errors += 1
                        
        except Exception as e:
            logger.error(f"Connection {connection_id} failed: {e}")
            ws_errors_total.labels(error_type="connection").inc()
            self.result.connection_errors += 1
            
        finally:
            self.active_connections -= 1
            ws_connections_active.set(self.active_connections)
            logger.debug(f"Connection {connection_id} closed")
    
    async def run_load_test(self) -> LoadTestResult:
        """Run the load test"""
        logger.info(f"Starting WebSocket load test: {self.config.target_rps} msg/s for {self.config.duration_seconds}s")
        logger.info(f"Target: {self.config.target_url}")
        logger.info(f"Connections: {self.config.concurrent_connections}")
        logger.info(f"Message size: {self.config.message_size_bytes} bytes")
        logger.info(f"Chaos mode: {self.config.chaos_mode}")
        
        self.result.start_time = datetime.now()
        
        # Create connection workers
        tasks = []
        for i in range(self.config.concurrent_connections):
            task = asyncio.create_task(self.connection_worker(i))
            tasks.append(task)
        
        # Wait for all connections to complete
        await asyncio.gather(*tasks, return_exceptions=True)
        
        self.result.end_time = datetime.now()
        
        logger.info("Load test completed")
        return self.result


class ChaosTestRunner:
    """Chaos testing runner"""
    
    def __init__(self, target_url: str = "http://localhost:8000"):
        self.target_url = target_url
        
    async def chaos_cpu_spike(self, duration: int = 30):
        """Simulate CPU spike"""
        logger.info(f"Chaos: CPU spike for {duration}s")
        # This would typically trigger external chaos tool
        await asyncio.sleep(duration)
        
    async def chaos_memory_pressure(self, duration: int = 30):
        """Simulate memory pressure"""
        logger.info(f"Chaos: Memory pressure for {duration}s")
        # This would typically trigger external chaos tool
        await asyncio.sleep(duration)
        
    async def chaos_network_partition(self, duration: int = 30):
        """Simulate network partition"""
        logger.info(f"Chaos: Network partition for {duration}s")
        # This would typically trigger external chaos tool
        await asyncio.sleep(duration)
        
    async def run_chaos_scenarios(self):
        """Run chaos scenarios during load test"""
        scenarios = [
            self.chaos_cpu_spike,
            self.chaos_memory_pressure,
            self.chaos_network_partition
        ]
        
        for scenario in scenarios:
            await asyncio.sleep(20)  # Wait between scenarios
            await scenario(30)


async def run_comprehensive_load_test():
    """Run comprehensive load and chaos test"""
    config = LoadTestConfig(
        target_url="ws://localhost:8000/ws",
        target_rps=10000,
        duration_seconds=300,  # 5 minutes
        concurrent_connections=200,
        message_size_bytes=1024,
        chaos_mode=True
    )
    
    tester = WebSocketLoadTester(config)
    chaos_runner = ChaosTestRunner()
    
    # Run load test and chaos scenarios concurrently
    load_task = asyncio.create_task(tester.run_load_test())
    chaos_task = asyncio.create_task(chaos_runner.run_chaos_scenarios())
    
    # Wait for load test to complete
    result = await load_task
    
    # Cancel chaos scenarios
    chaos_task.cancel()
    
    # Print results
    stats = result.get_stats()
    print("\n" + "="*50)
    print("LOAD TEST RESULTS")
    print("="*50)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Validate performance requirements
    print("\n" + "="*50)
    print("PERFORMANCE VALIDATION")
    print("="*50)
    
    target_rps = config.target_rps
    actual_rps = stats["messages_per_second"]
    success_rate = stats["success_rate"]
    
    print(f"Target RPS: {target_rps}")
    print(f"Actual RPS: {actual_rps:.2f}")
    print(f"Success Rate: {success_rate:.2%}")
    
    # Performance gates
    if actual_rps < target_rps * 0.8:  # Allow 20% tolerance
        print("❌ PERFORMANCE GATE FAILED: RPS below 80% of target")
        return False
        
    if success_rate < 0.95:  # 95% success rate required
        print("❌ RELIABILITY GATE FAILED: Success rate below 95%")
        return False
        
    if "latency_p95" in stats and stats["latency_p95"] > 1.0:  # P95 latency under 1s
        print("❌ LATENCY GATE FAILED: P95 latency above 1s")
        return False
    
    print("✅ ALL PERFORMANCE GATES PASSED")
    return True


if __name__ == "__main__":
    import sys
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run test
    success = asyncio.run(run_comprehensive_load_test())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
