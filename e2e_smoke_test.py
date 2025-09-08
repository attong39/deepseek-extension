"""
End-to-End Smoke Test for Enhanced Zeta Core
"""
import asyncio
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List
import websockets
import requests
from dataclasses import dataclass
import Exception
import all
import base_url
import bool
import comp
import e
import exit
import field
import float
import isinstance
import key
import len
import list
import metric
import print
import r
import result
import self
import str
import sum
import value
import websocket


@dataclass
class TestResult:
    """Test result container"""
    test_name: str
    success: bool
    duration: float
    details: Dict[str, Any]
    error: str = None


class E2ESmokeTest:
    """End-to-end smoke test suite for Enhanced Zeta Core"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://")
        self.test_results: List[TestResult] = []
        self.session = requests.Session()
        
        # Test data
        self.test_jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJpYXQiOjE2MzQwNzAwMDAsImV4cCI6MTk0OTQzMDAwMCwicm9sZXMiOlsiYWRtaW4iLCJ1c2VyIl0sImF0dHJpYnV0ZXMiOnsib3JnIjoidGVzdF9vcmciLCJjbGVhcmFuY2UiOiJzZWNyZXQifX0.9lHB9QQaFKsP-FWGvSF8qKuUKwXkX6L1x_e6Qo-qBzE"
    
    def add_auth_headers(self) -> Dict[str, str]:
        """Add authentication headers"""
        return {
            "Authorization": f"Bearer {self.test_jwt_token}",
            "Content-Type": "application/json"
        }
    
    async def run_all_tests(self) -> bool:
        """Run all E2E tests"""
        print("🚀 Starting Enhanced Zeta Core E2E Smoke Tests...")
        print(f"   Target: {self.base_url}")
        print("-" * 60)
        
        # Core health tests
        await self.test_health_check()
        await self.test_enhanced_status()
        await self.test_prometheus_metrics()
        
        # Security tests
        await self.test_security_policy_evaluation()
        await self.test_risk_score_retrieval()
        
        # Agent orchestration tests
        await self.test_agent_team_listing()
        await self.test_agent_task_creation()
        
        # Knowledge graph tests
        await self.test_knowledge_graph_query()
        await self.test_rag_enhancement()
        
        # WebSocket tests
        await self.test_websocket_team_execution()
        
        # Print results
        self.print_test_summary()
        
        # Return overall success
        return all(result.success for result in self.test_results)
    
    async def test_health_check(self):
        """Test basic health check endpoint"""
        start_time = time.time()
        test_name = "Health Check"
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("status") == "healthy"
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=success,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "response": data
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Unexpected status code: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_enhanced_status(self):
        """Test enhanced status endpoint"""
        start_time = time.time()
        test_name = "Enhanced Status"
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/status",
                headers=self.add_auth_headers()
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required components
                required_components = [
                    "zero_trust", "agent_orchestrator", 
                    "knowledge_graph", "event_outbox"
                ]
                
                components_ok = all(
                    comp in data.get("components", {}) 
                    for comp in required_components
                )
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=components_ok,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "components": data.get("components", {}),
                        "features": data.get("features", {})
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Status endpoint failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_prometheus_metrics(self):
        """Test Prometheus metrics endpoint"""
        start_time = time.time()
        test_name = "Prometheus Metrics"
        
        try:
            response = self.session.get(f"{self.base_url}/metrics")
            duration = time.time() - start_time
            
            if response.status_code == 200:
                metrics_text = response.text
                
                # Check for key metrics
                expected_metrics = [
                    "zeta_zt_decisions_total",
                    "zeta_agent_executions_total", 
                    "zeta_kg_queries_total",
                    "zeta_app_requests_total"
                ]
                
                metrics_present = all(
                    metric in metrics_text 
                    for metric in expected_metrics
                )
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=metrics_present,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "metrics_count": len(metrics_text.split('\n')),
                        "expected_metrics_present": metrics_present
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Metrics endpoint failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_security_policy_evaluation(self):
        """Test security policy evaluation"""
        start_time = time.time()
        test_name = "Security Policy Evaluation"
        
        try:
            payload = {
                "resource_path": "/api/v1/agents/tasks",
                "action": "write",
                "context": {
                    "geo": "US",
                    "token_age": "300"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/security/policy/evaluate",
                headers=self.add_auth_headers(),
                json=payload
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["allowed", "risk_level", "reasons"]
                fields_present = all(field in data for field in required_fields)
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=fields_present,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "response": data,
                        "fields_present": fields_present
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Policy evaluation failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_risk_score_retrieval(self):
        """Test risk score retrieval"""
        start_time = time.time()
        test_name = "Risk Score Retrieval"
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/security/risk/test_user",
                headers=self.add_auth_headers()
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["user_id", "risk_score", "risk_label"]
                fields_present = all(field in data for field in required_fields)
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=fields_present,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "response": data,
                        "fields_present": fields_present
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Risk score retrieval failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_agent_team_listing(self):
        """Test agent team listing"""
        start_time = time.time()
        test_name = "Agent Team Listing"
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/agents/teams",
                headers=self.add_auth_headers()
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                has_teams = "teams" in data and isinstance(data["teams"], list)
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=has_teams,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "teams_count": len(data.get("teams", [])),
                        "response": data
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Team listing failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_agent_task_creation(self):
        """Test agent task creation"""
        start_time = time.time()
        test_name = "Agent Task Creation"
        
        try:
            payload = {
                "team_id": "default",
                "task_type": "analyze_code",
                "parameters": {
                    "code": "def hello(): return 'world'"
                },
                "priority": "normal",
                "timeout_seconds": 60
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/agents/tasks",
                headers=self.add_auth_headers(),
                json=payload
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["task_id", "status"]
                fields_present = all(field in data for field in required_fields)
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=fields_present,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "response": data,
                        "fields_present": fields_present
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Task creation failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_knowledge_graph_query(self):
        """Test knowledge graph BFS query"""
        start_time = time.time()
        test_name = "Knowledge Graph Query"
        
        try:
            payload = {
                "query": "Find path between AI concepts",
                "query_type": "bfs_path",
                "parameters": {
                    "start_id": "ai_ml",
                    "end_id": "neural_nets",
                    "max_depth": 4
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/knowledge/query",
                headers=self.add_auth_headers(),
                json=payload
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["results", "metadata", "execution_time"]
                fields_present = all(field in data for field in required_fields)
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=fields_present,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "response": data,
                        "fields_present": fields_present
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"Knowledge graph query failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_rag_enhancement(self):
        """Test RAG enhancement with knowledge graph"""
        start_time = time.time()
        test_name = "RAG Enhancement"
        
        try:
            payload = {
                "query": "What is machine learning?",
                "user_id": "test_user",
                "max_results": 5,
                "temporal_window_hours": 24,
                "include_related": True
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/knowledge/rag/enhance",
                headers=self.add_auth_headers(),
                json=payload
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                has_enhancement = "enhancement" in data
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=has_enhancement,
                    duration=duration,
                    details={
                        "status_code": response.status_code,
                        "response": data,
                        "has_enhancement": has_enhancement
                    }
                ))
            else:
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=False,
                    duration=duration,
                    details={"status_code": response.status_code},
                    error=f"RAG enhancement failed: {response.status_code}"
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    async def test_websocket_team_execution(self):
        """Test WebSocket team execution endpoint"""
        start_time = time.time()
        test_name = "WebSocket Team Execution"
        
        try:
            ws_uri = f"{self.ws_url}/api/v1/agents/teams/default/run"
            
            async with websockets.connect(ws_uri) as websocket:
                # Send connection verification
                await websocket.send(json.dumps({
                    "type": "get_status"
                }))
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                # Send a test task
                await websocket.send(json.dumps({
                    "type": "execute_task",
                    "task_type": "process_data",
                    "parameters": {
                        "data": [1, 2, 3, 4, 5],
                        "operation": "transform"
                    }
                }))
                
                # Wait for task started notification
                task_started = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                task_started_data = json.loads(task_started)
                
                # Wait for task completion
                task_completed = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                task_completed_data = json.loads(task_completed)
                
                duration = time.time() - start_time
                
                # Check if task completed successfully
                success = (
                    task_completed_data.get("type") == "task_completed" and
                    "results" in task_completed_data
                )
                
                self.test_results.append(TestResult(
                    test_name=test_name,
                    success=success,
                    duration=duration,
                    details={
                        "connection_response": data,
                        "task_started": task_started_data,
                        "task_completed": task_completed_data,
                        "websocket_success": success
                    }
                ))
                
        except Exception as e:
            self.test_results.append(TestResult(
                test_name=test_name,
                success=False,
                duration=time.time() - start_time,
                details={},
                error=str(e)
            ))
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("🧪 ENHANCED ZETA CORE E2E TEST RESULTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - passed_tests
        
        print(f"📊 SUMMARY: {passed_tests}/{total_tests} tests passed")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ⏱️  Total time: {sum(r.duration for r in self.test_results):.2f}s")
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 60)
        
        for result in self.test_results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"{status} {result.test_name} ({result.duration:.2f}s)")
            
            if not result.success and result.error:
                print(f"      Error: {result.error}")
            
            if result.details:
                for key, value in result.details.items():
                    if key not in ["response"]:  # Skip verbose response details
                        print(f"      {key}: {value}")
        
        print("\n" + "=" * 60)
        
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! Enhanced Zeta Core is ready for production.")
        else:
            print(f"⚠️  {failed_tests} test(s) failed. Please review the failures above.")
        
        print("=" * 60)


async def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Zeta Core E2E Smoke Tests")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Base URL for the API server")
    args = parser.parse_args()
    
    # Create and run test suite
    test_suite = E2ESmokeTest(base_url=args.url)
    success = await test_suite.run_all_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
