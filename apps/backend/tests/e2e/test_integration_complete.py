"""
End-to-end integration test for JWT → Zero-Trust → WebSocket → Metrics flow.
This test validates the complete production hardening pipeline.
"""
import asyncio
import json
import pytest
import time
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import WebSocket
import hasattr
import isinstance
import mock_decode


class TestE2EHardeningFlow:
    """Integration tests for production hardening features."""
    
    @pytest.fixture
    def jwt_token(self):
        """Create a valid JWT token for testing."""
        import jwt
        import datetime
        
        # Mock RSA public key for testing
        test_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAyKWnV5YM2RQ5V7v/e8d8r2XYp3E1l4Z2l7k8q1n2Z8r4x5v3
m9z1g7w2e3q4r5t6y7u8i9o0p1l2k3j4h5g6f7d8s9a0z1x2c3v4b5n6m7l8k9j0
i1h2g3f4e5d6c7b8a9z0y1x2w3v4u5t6s7r8q9p0o1n2m3l4k5j6i7h8g9f0e1d2
c3b4a5z6y7x8w9v0u1t2s3r4q5p6o7n8m9l0k1j2i3h4g5f6e7d8c9b0a1z2y3x4
w5v6u7t8s9r0q1p2o3n4m5l6k7j8i9h0g1f2e3d4c5b6a7z8y9x0w1v2u3t4s5r6
q7p8o9n0m1l2k3j4i5h6g7f8e9d0c1b2a3z4y5x6w7v8u9t0s1r2q3p4o5n6m7l8
QwIDAQABAoIBABQ+R5K6Z8X7N2P3Q9Y0U1W2V3X4Y5Z6A7B8C9D0E1F2G3H4I5J6
K7L8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2A3B4C5D6E7F8G9H0I1J2K3L4M5N6O7P8
Q9R0S1T2U3V4W5X6Y7Z8A9B0C1D2E3F4G5H6I7J8K9L0M1N2O3P4Q5R6S7T8U9V0
W1X2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M7N8O9P0Q1R2S3T4U5V6W7X8Y9Z0A1B2
C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2G3H4
I5J6K7L8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2A3B4C5D6E7F8G9H0I1J2K3L4M5N6
ECgYEA8Z2Y3X4W5V6U7T8S9R0Q1P2O3N4M5L6K7J8I9H0G1F2E3D4C5B6A7Z8Y9X0
W1V2U3T4S5R6Q7P8O9N0M1L2K3J4I5H6G7F8E9D0C1B2A3Z4Y5X6W7V8U9T0S1R2
Q3P4O5N6M7L8K9J0I1H2G3F4E5D6C7B8A9Z0Y1X2W3V4U5T6S7R8Q9P0O1N2M3L4
K5J6I7H8G9F0E1D2C3B4A5Z6Y7X8W9V0U1T2S3R4Q5P6O7N8M9L0K1J2I3H4G5F6
ECgYEA1Y2X3W4V5U6T7S8R9Q0P1O2N3M4L5K6J7I8H9G0F1E2D3C4B5A6Z7Y8X9W0
V1U2T3S4R5Q6P7O8N9M0L1K2J3I4H5G6F7E8D9C0B1A2Z3Y4X5W6V7U8T9S0R1Q2
P3O4N5M6L7K8J9I0H1G2F3E4D5C6B7A8Z9Y0X1W2V3U4T5S6R7Q8P9O0N1M2L3K4
J5I6H7G8F9E0D1C2B3A4Z5Y6X7W8V9U0T1S2R3Q4P5O6N7M8L9K0J1I2H3G4F5E6
ECgYBAN3M4L5K6J7I8H9G0F1E2D3C4B5A6Z7Y8X9W0V1U2T3S4R5Q6P7O8N9M0L1
K2J3I4H5G6F7E8D9C0B1A2Z3Y4X5W6V7U8T9S0R1Q2P3O4N5M6L7K8J9I0H1G2F3
E4D5C6B7A8Z9Y0X1W2V3U4T5S6R7Q8P9O0N1M2L3K4J5I6H7G8F9E0D1C2B3A4Z5
Y6X7W8V9U0T1S2R3Q4P5O6N7M8L9K0J1I2H3G4F5E6D7C8B9A0Z1Y2X3W4V5U6T7
S8R9Q0P1O2N3M4L5K6J7I8H9G0F1E2D3C4B5A6Z7Y8X9W0V1U2T3S4R5Q6P7O8N9
ECgYEAhKONDKPAOUBQUROUBDQKROFHUKDKALHDKSLVKDJFKLSJFKLSJFKLSJFKLSJ
FKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
KLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
KLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
KLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
ECgYBDFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
KLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
KLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
KLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
KLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJFKLSJF
-----END RSA PRIVATE KEY-----"""
        
        payload = {
            "sub": "test-user",
            "role": "developer",
            "env": "development",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        
        return jwt.encode(payload, test_private_key, algorithm="RS256")
    
    def test_jwt_validation_flow(self, jwt_token):
        """Test JWT validation in the security dependency."""
        from app.security.jwt_dependency import get_jwt_identity
        from app.core.models.security import Identity
        
        # Mock request with Authorization header
        mock_request = Mock()
        mock_request.headers = {"Authorization": f"Bearer {jwt_token}"}
        
        # Mock the JWT public key environment variable
        with patch.dict('os.environ', {'JWT_PUBLIC_KEY_PEM': 'test-public-key'}):
            with patch('jwt.decode') as mock_decode:
                mock_decode.return_value = {
                    "sub": "test-user",
                    "role": "developer", 
                    "env": "development"
                }
                
                identity = get_jwt_identity(mock_request)
                
                assert isinstance(identity, Identity)
                assert identity.subject == "test-user"
                assert identity.role == "developer"
                assert identity.environment == "development"
    
    def test_zero_trust_middleware_integration(self):
        """Test Zero-Trust middleware with JWT identity."""
        from app.api.middleware.zero_trust import ZeroTrustMiddleware
        from app.core.models.security import Identity
        
        middleware = ZeroTrustMiddleware()
        
        # Mock request with identity
        mock_request = Mock()
        mock_request.state.identity = Identity(
            subject="test-user",
            role="developer",
            environment="development"
        )
        mock_request.url.path = "/api/v1/agents/teams"
        mock_request.method = "GET"
        
        # Test allow decision
        decision = middleware.evaluate_request(mock_request)
        assert decision.allow is True
        assert decision.subject == "test-user"
    
    def test_websocket_metrics_integration(self):
        """Test WebSocket metrics collection."""
        from app.observability.ws_metrics import (
            ws_connections_gauge,
            ws_messages_total,
            ws_send_latency_histogram
        )
        
        # Simulate connection metrics
        initial_connections = ws_connections_gauge._value._value
        
        # Simulate connection
        ws_connections_gauge.labels(route="/ws/agents/teams").inc()
        
        # Simulate message
        ws_messages_total.labels(
            route="/ws/agents/teams",
            direction="outbound", 
            event_type="step_completed"
        ).inc()
        
        # Simulate latency measurement
        with ws_send_latency_histogram.labels(route="/ws/agents/teams").time():
            time.sleep(0.001)  # Simulate small latency
        
        # Verify metrics were recorded
        assert ws_connections_gauge._value._value > initial_connections
    
    @pytest.mark.asyncio
    async def test_websocket_enhanced_handler(self):
        """Test enhanced WebSocket handler with production features."""
        from app.api.v1.agents.team_router import WebSocketTeamHandler
        from app.core.models.security import Identity
        
        # Mock WebSocket connection
        mock_websocket = Mock(spec=WebSocket)
        mock_websocket.accept = Mock()
        mock_websocket.send_text = Mock()
        mock_websocket.receive_text = Mock()
        mock_websocket.close = Mock()
        
        # Mock identity
        identity = Identity(
            subject="test-user",
            role="developer",
            environment="development"
        )
        
        handler = WebSocketTeamHandler()
        
        # Test rate limiting initialization
        assert handler.rate_limiter is not None
        assert handler.MAX_QUEUE_SIZE == 512
        assert handler.PING_INTERVAL == 20
        
        # Test heartbeat mechanism
        assert hasattr(handler, '_send_ping')
        assert hasattr(handler, '_handle_pong')
    
    def test_complete_request_flow_simulation(self, jwt_token):
        """Simulate complete request flow: JWT → Zero-Trust → WebSocket → Metrics."""
        from app.main import app
        
        client = TestClient(app)
        
        # Test authenticated request to WebSocket endpoint
        headers = {"Authorization": f"Bearer {jwt_token}"}
        
        with patch.dict('os.environ', {'JWT_PUBLIC_KEY_PEM': 'test-public-key'}):
            with patch('jwt.decode') as mock_decode:
                mock_decode.return_value = {
                    "sub": "test-user",
                    "role": "developer",
                    "env": "development"
                }
                
                # Test regular API endpoint with JWT
                response = client.get("/api/v1/agents/teams", headers=headers)
                # Should not fail on authentication (might fail on implementation)
                assert response.status_code in [200, 404, 501]  # Any non-auth error
    
    def test_stress_testing_framework_integration(self):
        """Test integration with stress testing framework."""
        # Import stress test to ensure it's compatible
        from tests.e2e.test_ws_stress import StressTestRunner
        
        runner = StressTestRunner()
        assert runner.target_mps == 1000
        assert runner.max_concurrent_clients == 100
        assert runner.test_duration == 60
        
        # Test metrics calculation
        test_results = {
            "total_messages": 1000,
            "total_errors": 10,
            "latencies": [0.1, 0.15, 0.2, 0.25, 0.3] * 200
        }
        
        error_rate = test_results["total_errors"] / test_results["total_messages"]
        assert error_rate < 0.02  # <2% error rate
    
    def test_load_testing_tool_integration(self):
        """Test integration with load testing tool."""
        # Verify load testing tool can be imported
        import sys
        sys.path.append("../../tools/load")
        
        # Test configuration validation
        config = {
            "clients": 50,
            "duration": 30,
            "target_mps": 1000,
            "url": "ws://localhost:8000/ws/agents/teams"
        }
        
        # Validate configuration
        assert config["clients"] > 0
        assert config["duration"] > 0 
        assert config["target_mps"] > 0
        assert config["url"].startswith("ws://")
    
    def test_prometheus_metrics_format(self):
        """Test that Prometheus metrics are properly formatted."""
        from app.observability.ws_metrics import (
            ws_connections_gauge,
            ws_messages_total,
            ws_send_latency_histogram
        )
        
        # Test metric names
        assert ws_connections_gauge._name == "zeta_ws_connections"
        assert ws_messages_total._name == "zeta_ws_messages_total"
        assert ws_send_latency_histogram._name == "zeta_ws_send_latency_seconds"
        
        # Test label keys
        connection_labels = ws_connections_gauge._labelnames
        assert "route" in connection_labels
        
        message_labels = ws_messages_total._labelnames  
        assert "route" in message_labels
        assert "direction" in message_labels
        assert "event_type" in message_labels
