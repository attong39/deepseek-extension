"""
Authentication Flow Integration Tests

Tests authentication, authorization, and security flows.
"""

from datetime import UTC, datetime, timedelta

import jwt
import pytest
from httpx import AsyncClient
import ValueError
import ac
import current_user
import dict
import e
import email
import invalid_token
import len
import password
import self
import str
import user


class MockAuthService:
    """Mock authentication service."""

    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.secret_key = "test-secret-key"

    async def register_user(self, username: str, email: str, password: str) -> dict:
        """Register new user."""
        if username in self.users:
            raise ValueError("Username already exists")

        user_id = f"user_{len(self.users) + 1}"
        user_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.now(UTC),
        }

        self.users[username] = user_data
        return user_data

    async def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user credentials."""
        if username not in self.users:
            raise ValueError("Invalid credentials")

        # In real implementation, would check password hash
        if password != "correct_password":
            raise ValueError("Invalid credentials")

        return self.users[username]

    async def create_access_token(self, user_data: dict) -> str:
        """Create JWT access token."""
        payload = {
            "sub": user_data["id"],
            "username": user_data["username"],
            "exp": datetime.now(UTC) + timedelta(minutes=30),
            "iat": datetime.now(UTC),
        }

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    async def verify_token(self, token: str) -> dict:
        """Verify JWT token and return user data."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            username = payload.get("username")

            if username not in self.users:
                raise ValueError("User not found")

            return self.users[username]
        except jwt.InvalidTokenError as e:
            raise ValueError("Invalid token") from e


@pytest.fixture
def auth_service():
    """Authentication service fixture."""
    return MockAuthService()


@pytest.fixture
async def mock_app(auth_service):
    """Mock FastAPI app with auth endpoints."""
    from fastapi import Depends, FastAPI, HTTPException
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

    app = FastAPI()
    security = HTTPBearer()

    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        try:
            _ = await auth_service.verify_token(credentials.credentials)
            return user
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e

    @app.post("/auth/register")
    async def register(user_data: dict):
        try:
            _ = await auth_service.register_user(
                user_data["username"], user_data["email"], user_data["password"]
            )
            return {"user": user, "message": "User registered successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.post("/auth/login")
    async def login(credentials: dict):
        try:
            _ = await auth_service.authenticate_user(
                credentials["username"], credentials["password"]
            )
            token = await auth_service.create_access_token(user)
            return {"access_token": token, "token_type": "bearer", "user": user}
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e

    @app.get("/auth/me")
    async def get_me(current_user: dict = Depends(get_current_user)):
        return current_user

    @app.get("/protected")
    async def protected_endpoint(current_user: dict = Depends(get_current_user)):
        return {"message": f"Hello {current_user['username']}, this is protected!"}

    return app


@pytest.fixture
async def client(mock_app):
    """HTTP client for testing."""
    async with AsyncClient(app=mock_app, base_url="http://test") as ac:
        yield ac


class TestUserRegistration:
    """Test user registration flow."""

    @pytest.mark.asyncio
    async def test_successful_registration(self, client: AsyncClient):
        """Test successful user registration."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secure_password",
        }

        response = await client.post("/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert data["user"]["username"] == "newuser"
        assert data["user"]["email"] == "newuser@example.com"
        assert "message" in data

    @pytest.mark.asyncio
    async def test_duplicate_username_registration(self, client: AsyncClient):
        """Test registration with duplicate username."""
        user_data = {
            "username": "testuser",
            "email": "test1@example.com",
            "password": "password1",
        }

        # First registration should succeed
        response1 = await client.post("/auth/register", json=user_data)
        assert response1.status_code == 200

        # Second registration with same username should fail
        user_data["email"] = "test2@example.com"
        response2 = await client.post("/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]


class TestUserLogin:
    """Test user login flow."""

    @pytest.mark.asyncio
    async def test_successful_login(self, client: AsyncClient, auth_service):
        """Test successful user login."""
        # Register user first
        await auth_service.register_user(
            "testuser", "test@example.com", "correct_password"
        )

        credentials = {"username": "testuser", "password": "correct_password"}

        response = await client.post("/auth/login", json=credentials)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_invalid_credentials_login(self, client: AsyncClient, auth_service):
        """Test login with invalid credentials."""
        # Register user first
        await auth_service.register_user(
            "testuser", "test@example.com", "correct_password"
        )

        credentials = {"username": "testuser", "password": "wrong_password"}

        response = await client.post("/auth/login", json=credentials)

        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_nonexistent_user_login(self, client: AsyncClient):
        """Test login with non-existent user."""
        credentials = {"username": "nonexistent", "password": "any_password"}

        response = await client.post("/auth/login", json=credentials)

        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]


class TestTokenVerification:
    """Test JWT token verification and protected endpoints."""

    @pytest.mark.asyncio
    async def test_access_protected_endpoint_with_valid_token(
        self, client: AsyncClient, auth_service
    ):
        """Test accessing protected endpoint with valid token."""
        # Register and login user
        await auth_service.register_user(
            "testuser", "test@example.com", "correct_password"
        )

        credentials = {"username": "testuser", "password": "correct_password"}
        login_response = await client.post("/auth/login", json=credentials)

        token = login_response.json()["access_token"]

        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/protected", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert "Hello testuser" in data["message"]

    @pytest.mark.asyncio
    async def test_access_protected_endpoint_without_token(self, client: AsyncClient):
        """Test accessing protected endpoint without token."""
        response = await client.get("/protected")

        assert (
            response.status_code == 403
        )  # FastAPI HTTPBearer returns 403 for missing token

    @pytest.mark.asyncio
    async def test_access_protected_endpoint_with_invalid_token(
        self, client: AsyncClient
    ):
        """Test accessing protected endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/protected", headers=headers)

        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_current_user_info(self, client: AsyncClient, auth_service):
        """Test getting current user information."""
        # Register and login user
        await auth_service.register_user(
            "testuser", "test@example.com", "correct_password"
        )

        credentials = {"username": "testuser", "password": "correct_password"}
        login_response = await client.post("/auth/login", json=credentials)

        token = login_response.json()["access_token"]

        # Get user info
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/auth/me", headers=headers)

        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == "testuser"
        assert user_data["email"] == "test@example.com"


class TestTokenExpiration:
    """Test JWT token expiration handling."""

    @pytest.mark.asyncio
    async def test_expired_token_handling(self, auth_service):
        """Test handling of expired tokens."""
        # Create user
        user_data = await auth_service.register_user(
            "testuser", "test@example.com", "password"
        )

        # Create token with short expiration
        import jwt

        payload = {
            "sub": user_data["id"],
            "username": user_data["username"],
            "exp": datetime.now(UTC) - timedelta(minutes=1),  # Already expired
            "iat": datetime.now(UTC) - timedelta(minutes=2),
        }

        expired_token = jwt.encode(payload, auth_service.secret_key, algorithm="HS256")

        # Try to verify expired token
        with pytest.raises(ValueError, match="Invalid token"):
            await auth_service.verify_token(expired_token)


class TestSecurityFeatures:
    """Test security features and edge cases."""

    @pytest.mark.asyncio
    async def test_token_tampering_protection(self, auth_service):
        """Test protection against token tampering."""
        # Create valid token
        user_data = await auth_service.register_user(
            "testuser", "test@example.com", "password"
        )
        token = await auth_service.create_access_token(user_data)

        # Tamper with token
        tampered_token = token[:-5] + "XXXXX"

        # Verify tampering is detected
        with pytest.raises(ValueError, match="Invalid token"):
            await auth_service.verify_token(tampered_token)

    @pytest.mark.asyncio
    async def test_token_structure_validation(self, auth_service):
        """Test token structure validation."""
        invalid_tokens = [
            "not.a.jwt",
            "still.not.valid",
            "",
            "onlyonepart",
            "two.parts",
        ]

        for invalid_token in invalid_tokens:
            with pytest.raises(ValueError, match="Invalid token"):
                await auth_service.verify_token(invalid_token)


class TestAuthenticationFlow:
    """Test complete authentication flows."""

    @pytest.mark.asyncio
    async def test_complete_auth_flow(self, client: AsyncClient):
        """Test complete authentication flow."""
        # 1. Register user
        user_data = {
            "username": "flowuser",
            "email": "flow@example.com",
            "password": "secure_password",
        }

        register_response = await client.post("/auth/register", json=user_data)
        assert register_response.status_code == 200

        # 2. Login user
        credentials = {"username": "flowuser", "password": "secure_password"}

        login_response = await client.post("/auth/login", json=credentials)
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        # 3. Access user info
        headers = {"Authorization": f"Bearer {token}"}
        me_response = await client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200

        user_info = me_response.json()
        assert user_info["username"] == "flowuser"

        # 4. Access protected resource
        protected_response = await client.get("/protected", headers=headers)
        assert protected_response.status_code == 200
        assert "Hello flowuser" in protected_response.json()["message"]


if __name__ == "__main__":
    pytest.main([__file__])
