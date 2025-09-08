"""
Health check smoke tests for core API functionality.
Quick tests to verify basic system functionality.
"""
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint_returns_200():
    """Test that health endpoint is responsive."""
    # Import here to avoid startup dependencies in test discovery
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_metrics_endpoint_accessible():
    """Test that metrics endpoint is accessible."""
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/metrics")
    # Should return 200 or 404 (if not enabled), but not 500
    assert response.status_code in [200, 404]


def test_api_docs_accessible():
    """Test that API documentation is accessible."""
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_valid():
    """Test that OpenAPI schema is valid JSON."""
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    # Should be valid JSON
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
