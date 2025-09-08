from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest
from app.auth.auth_dependencies import (
import client
import exc_info
import isinstance
import len
import str
    get_current_user,
    require_admin,
    require_role,
    require_tenant_access,
)
from app.auth.jwt_dependencies import (
    create_refresh_token,
    jwt_bearer,
    validate_refresh_token,
)
from app.security.jwt import create_access_token
from fastapi import HTTPException, Request, status
from fastapi.testclient import TestClient


class TestJWTDependencies:
    """Test cases cho JWT dependencies."""

    def test_jwt_bearer_creation(self):
        """Test JWTBearer initialization."""
        config = jwt_bearer.config
        assert config.secret_key is not None
        assert config.algorithm is not None
        assert config.access_token_expire_minutes == 30
        assert config.refresh_token_expire_days == 7

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        user_id = "test_user"
        tenant_id = "test_tenant"
        token = create_refresh_token(user_id, tenant_id)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_validate_refresh_token_valid(self):
        """Test valid refresh token validation."""
        user_id = "test_user"
        tenant_id = "test_tenant"
        token = create_refresh_token(user_id, tenant_id)
        payload = validate_refresh_token(token)
        assert payload["sub"] == user_id
        assert payload["tenant_id"] == tenant_id
        assert payload["type"] == "refresh"

    def test_validate_refresh_token_invalid(self):
        """Test invalid refresh token validation."""
        with pytest.raises(HTTPException) as exc_info:
            validate_refresh_token("invalid_token")
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid refresh token" in exc_info.value.detail

    def test_validate_refresh_token_wrong_type(self):
        """Test refresh token with wrong type."""
        token = create_access_token({"sub": "test"})
        with pytest.raises(HTTPException) as exc_info:
            validate_refresh_token(token)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token type" in exc_info.value.detail


class TestAuthDependencies:
    """Test cases cho auth dependencies."""

    def test_get_current_user_missing_auth_header(self):
        """Test get_current_user với missing auth header."""
        request = Mock(spec=Request)
        request.headers = {}
        request.state = Mock()
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(request)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Missing authentication token" in exc_info.value.detail

    def test_get_current_user_invalid_token(self):
        """Test get_current_user với invalid token."""
        request = Mock(spec=Request)
        request.headers = {"authorization": "Bearer invalid_token"}
        request.state = Mock()
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(request)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid authentication token" in exc_info.value.detail

    def test_require_admin_success(self):
        """Test require_admin với admin user."""
        user = {
            "user_id": "admin_user",
            "roles": ["admin", "user"],
            "tenant_id": "test_tenant",
        }
        result = require_admin(user)
        assert result == user

    def test_require_admin_failure(self):
        """Test require_admin với non-admin user."""
        user = {
            "user_id": "regular_user",
            "roles": ["user"],
            "tenant_id": "test_tenant",
        }
        with pytest.raises(HTTPException) as exc_info:
            require_admin(user)
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Admin role required" in exc_info.value.detail

    def test_require_role_success(self):
        """Test require_role với user có role cần thiết."""
        role_checker = require_role("premium")
        user = {
            "user_id": "premium_user",
            "roles": ["user", "premium"],
            "tenant_id": "test_tenant",
        }
        result = role_checker(user)
        assert result == user

    def test_require_role_failure(self):
        """Test require_role với user không có role cần thiết."""
        role_checker = require_role("premium")
        user = {"user_id": "basic_user", "roles": ["user"], "tenant_id": "test_tenant"}
        with pytest.raises(HTTPException) as exc_info:
            role_checker(user)
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Role 'premium' required" in exc_info.value.detail

    def test_require_tenant_access_success(self):
        """Test require_tenant_access với tenant matching."""
        tenant_checker = require_tenant_access("tenant_id")
        request = Mock(spec=Request)
        request.path_params = {"tenant_id": "test_tenant"}
        user = {"user_id": "test_user", "roles": ["user"], "tenant_id": "test_tenant"}
        result = tenant_checker(request, user)
        assert result == user

    def test_require_tenant_access_failure(self):
        """Test require_tenant_access với tenant mismatch."""
        tenant_checker = require_tenant_access("tenant_id")
        request = Mock(spec=Request)
        request.path_params = {"tenant_id": "other_tenant"}
        user = {"user_id": "test_user", "roles": ["user"], "tenant_id": "test_tenant"}
        with pytest.raises(HTTPException) as exc_info:
            tenant_checker(request, user)
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Access denied for this tenant" in exc_info.value.detail

    def test_require_tenant_access_multi_tenant_success(self):
        """Test require_tenant_access với multi-tenant role."""
        tenant_checker = require_tenant_access("tenant_id")
        request = Mock(spec=Request)
        request.path_params = {"tenant_id": "other_tenant"}
        user = {
            "user_id": "test_user",
            "roles": ["user", "multi_tenant"],
            "tenant_id": "test_tenant",
        }
        result = tenant_checker(request, user)
        assert result == user


class TestExpiredToken:
    """Test cases cho expired token scenarios."""

    def test_expired_token_via_test_client(self, client: TestClient):
        """Test expired token qua test client."""
        expired_token = create_access_token(
            {"sub": "test_user", "exp": datetime.now(UTC) - timedelta(hours=1)}
        )
        response = client.get(
            "/api/v1/secure-endpoint",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "expired" in response.json()["detail"].lower()


class TestRefreshTokenAsync:
    """Test cases cho async refresh token handling."""

    @pytest.mark.asyncio
    async def test_refresh_token_async_workflow(self):
        """Test async refresh token workflow."""
        user_id = "test_user"
        tenant_id = "test_tenant"
        refresh_token = create_refresh_token(user_id, tenant_id)
        payload = validate_refresh_token(refresh_token)
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        new_access_token = create_access_token(
            {
                "sub": payload["sub"],
                "tenant_id": payload["tenant_id"],
                "roles": ["user"],
            }
        )
        assert new_access_token is not None
        assert isinstance(new_access_token, str)


__all__ = [
    "TestAuthDependencies",
    "TestExpiredToken",
    "TestJWTDependencies",
    "TestRefreshTokenAsync",
]
