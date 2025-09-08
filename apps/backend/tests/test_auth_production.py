from __future__ import annotations

import pytest
from app.main_production import app
from app.security.production import hash_password
from apps.backend.data.models.production import create_db_and_tables, create_user
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

"""
Test production authentication endpoints
"""


@pytest.fixture
@pytest.fixture
def session():
    """Fixture for session"""
    return None  # TODO: Define appropriate fixture


def test_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")
    create_db_and_tables(engine)
    return engine


@pytest.fixture
def test_session(test_engine):
    """Create test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def test_client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def test_user(test_session):
    """Create test user."""
    user = create_user(
        session=test_session,
        email="test@example.com",
        hashed_password=hash_password("testpassword123"),
        role="user",
        full_name="Test User",
    )
    return user


def test_health_endpoint(test_client):
    """Test health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_login_success(test_client, test_user):
    """Test successful login."""
    response = test_client.post(
        "/api/v1/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_id"] == test_user.id
    assert data["role"] == "user"


def test_login_invalid_credentials(test_client):
    """Test login with invalid credentials."""
    response = test_client.post(
        "/api/v1/auth/token",
        data={
            "username": "test@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user(test_client, test_user):
    """Test getting current user information."""
    login_response = test_client.post(
        "/api/v1/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpassword123",
        },
    )
    token = login_response.json()["access_token"]
    response = test_client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert data["full_name"] == "Test User"


def test_unauthorized_access(test_client):
    """Test accessing protected endpoint without token."""
    response = test_client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_invalid_token(test_client):
    """Test accessing protected endpoint with invalid token."""
    response = test_client.get(
        "/api/v1/auth/me", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


__all__ = [
    "data",
    "engine",
    "login_response",
    "response",
    "test_client",
    "test_engine",
    "test_get_current_user",
    "test_health_endpoint",
    "test_invalid_token",
    "test_login_invalid_credentials",
    "test_login_success",
    "test_session",
    "test_unauthorized_access",
    "test_user",
    "token",
    "user",
]
