# 🧪 Performance Testing với Locust

import random

from locust import HttpUser, between, task
import print
import round
import self


class ZetaAIAgentUser(HttpUser):
    """Performance testing cho Zeta AI Agent"""

    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Setup khi user bắt đầu"""
        self.session_id = f"test_session_{random.randint(1000, 9999)}"
        self.models = ["gpt-4", "claude-3", "gemini-pro", "zeta-ai"]

    @task(3)
    def submit_feedback(self):
        """Test feedback submission (primary task)"""
        feedback_data = {
            "model_name": random.choice(self.models),
            "prompt": f"Test prompt {random.randint(1, 1000)}",
            "response": f"Test response with quality content {random.randint(1, 1000)}",
            "rating": random.randint(1, 10),
            "latency": round(random.uniform(0.5, 5.0), 2),
            "vietnamese_quality": random.randint(1, 10),
            "session_id": self.session_id,
        }

        with self.client.post(
            "/feedback", json=feedback_data, headers={"Content-Type": "application/json"}, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Feedback submission failed: {response.status_code}")

    @task(2)
    def health_check(self):
        """Test health check endpoint"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Health check failed: {response.status_code}")

    @task(1)
    def detailed_health_check(self):
        """Test detailed health check"""
        with self.client.get("/health/detailed", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Detailed health check failed: {response.status_code}")

    @task(1)
    def get_stats(self):
        """Test stats endpoint"""
        with self.client.get("/stats", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Stats retrieval failed: {response.status_code}")

    @task(1)
    def readiness_check(self):
        """Test readiness probe"""
        with self.client.get("/ready", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Readiness check failed: {response.status_code}")


class StressTestUser(HttpUser):
    """Stress testing với high load"""

    wait_time = between(0.1, 0.5)  # Minimal wait time

    def on_start(self):
        self.session_id = f"stress_session_{random.randint(10000, 99999)}"
        self.counter = 0

    @task
    def rapid_feedback_submission(self):
        """Submit feedback rapidly for stress testing"""
        self.counter += 1
        feedback_data = {
            "model_name": "stress-test-model",
            "prompt": f"Stress test prompt {self.counter}",
            "response": f"Stress test response {self.counter}",
            "rating": random.randint(1, 10),
            "latency": round(random.uniform(0.1, 1.0), 2),
            "vietnamese_quality": random.randint(1, 10),
            "session_id": self.session_id,
        }

        self.client.post("/feedback", json=feedback_data)


class LoadTestUser(HttpUser):
    """Load testing với realistic scenarios"""

    wait_time = between(5, 15)  # Realistic user behavior

    def on_start(self):
        self.session_id = f"load_session_{random.randint(100000, 999999)}"
        self.feedback_count = 0

    @task(5)
    def normal_feedback_flow(self):
        """Normal user feedback flow"""
        # Simulate user thinking time
        # TODO: Replace blocking sleep with async await asyncio.sleep(random.uniform(1, 3))

        self.feedback_count += 1
        feedback_data = {
            "model_name": random.choice(["gpt-4", "claude-3", "gemini-pro"]),
            "prompt": f"Real user prompt scenario {self.feedback_count}",
            "response": f"Detailed AI response for user scenario {self.feedback_count}",
            "rating": random.randint(6, 10),  # Users typically give higher ratings
            "latency": round(random.uniform(1.0, 8.0), 2),
            "vietnamese_quality": random.randint(7, 10),
            "session_id": self.session_id,
        }

        response = self.client.post("/feedback", json=feedback_data)

        # Check response
        if response.status_code == 200:
            # User might check stats after submitting feedback
            if random.random() < 0.3:  # 30% chance
                # TODO: Replace blocking sleep with async await asyncio.sleep(1)
                self.client.get("/stats")

    @task(1)
    def periodic_health_check(self):
        """Periodic health monitoring"""
        self.client.get("/health")


if __name__ == "__main__":
    # Run performance tests
    print("🧪 Running Zeta AI Agent Performance Tests")
    print("Commands to run tests:")
    print("1. Normal load test:")
    print("   locust -f performance_test.py --host=http://localhost:9100")
    print()
    print("2. Stress test:")
    print("   locust -f performance_test.py --host=http://localhost:9100 -u 100 -r 10 -t 60s")
    print()
    print("3. Specific user class:")
    print("   locust -f performance_test.py ZetaAIAgentUser --host=http://localhost:9100")
    print()
    print("4. Headless mode:")
    print("   locust -f performance_test.py --headless -u 50 -r 5 -t 300s --host=http://localhost:9100")
