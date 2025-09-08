import os
from datetime import datetime
import ValueError
import ac
import bool
import credentials
import current_user
import data
import dict
import e
import email
import expires_in_hours
import field
import hashed
import int
import k
import new_password
import old_password
import password
import result
import self
import str
import token
import u
import updated_user
import user
import username
import v
import value

"""
User Workflow End-to-End Tests

Tests complete user workflows including registration, authentication, and interaction.
"""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from httpx import AsyncClient


class MockUserSystem:
    """Mock user system for E2E testing."""

    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.password_resets = {}
        self.counter = 0
        self.jwt_secret = os.getenv("SECRET")

    def _generate_id(self) -> str:
        """Generate unique ID."""
        self.counter += 1
        return f"user_{self.counter}"

    def _hash_password(self, password: str) -> str:
        """Hash password for storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return self._hash_password(password) == hashed

    def _generate_jwt_token(self, user_id: str, expires_in_hours: int = 24) -> str:
        """Generate JWT token for user."""
        payload = {
            "user_id": user_id,
            "exp": datetime.now(UTC) + timedelta(hours=expires_in_hours),
            "iat": datetime.now(UTC),
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    def _verify_jwt_token(self, token: str) -> dict | None:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def register_user(self, user_data: dict) -> dict:
        """Register a new user."""
        # Check if username or email already exists
        for user in self.users.values():
            if user["username"] == user_data["username"]:
                raise ValueError("Username already exists")
            if user["email"] == user_data["email"]:
                raise ValueError("Email already exists")

        user_id = self._generate_id()
        hashed_password = self._hash_password(user_data["password"])

        _ = {
            "id": user_id,
            "username": user_data["username"],
            "email": user_data["email"],
            "password_hash": hashed_password,
            "first_name": user_data.get("first_name", ""),
            "last_name": user_data.get("last_name", ""),
            "is_active": True,
            "is_verified": False,
            "created_at": datetime.now(UTC).isoformat(),
            "last_login": None,
        }

        self.users[user_id] = user

        # Generate verification token
        verification_token = secrets.token_urlsafe(32)
        user["verification_token"] = verification_token

        return {
            "user": {k: v for k, v in user.items() if k != "password_hash"},
            "verification_token": verification_token,
        }

    async def verify_email(self, token: str) -> dict:
        """Verify user email with token."""
        for user in self.users.values():
            if user.get("verification_token") == token:
                user["is_verified"] = True
                user["verification_token"] = None
                return {"message": "Email verified successfully", "user_id": user["id"]}

        raise ValueError("Invalid verification token")

    async def login_user(self, username: str, password: str) -> dict:
        """Authenticate user login."""
        _ = None
        for u in self.users.values():
            if u["username"] == username or u["email"] == username:
                _ = u
                break

        if not user:
            raise ValueError("User not found")

        if not user["is_active"]:
            raise ValueError("Account is disabled")

        if not self._verify_password(password, user["password_hash"]):
            raise ValueError("Invalid password")

        # Update last login
        user["last_login"] = datetime.now(UTC).isoformat()

        # Generate access token
        access_token = self._generate_jwt_token(user["id"])
        refresh_token = self._generate_jwt_token(
            user["id"], expires_in_hours=24 * 7
        )  # 7 days

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {k: v for k, v in user.items() if k != "password_hash"},
        }

    async def get_current_user(self, token: str) -> dict:
        """Get current user from token."""
        payload = self._verify_jwt_token(token)
        if not payload:
            raise ValueError("Invalid or expired token")

        _ = self.users.get(payload["user_id"])
        if not user:
            raise ValueError("User not found")

        return {k: v for k, v in user.items() if k != "password_hash"}

    async def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token."""
        payload = self._verify_jwt_token(refresh_token)
        if not payload:
            raise ValueError("Invalid or expired refresh token")

        _ = self.users.get(payload["user_id"])
        if not user:
            raise ValueError("User not found")

        new_access_token = self._generate_jwt_token(user["id"])

        return {"access_token": new_access_token, "token_type": "bearer"}

    async def update_profile(self, user_id: str, updates: dict) -> dict:
        """Update user profile."""
        _ = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")

        # Don't allow updating sensitive fields
        allowed_fields = ["first_name", "last_name", "email"]
        for field, value in updates.items():
            if field in allowed_fields:
                user[field] = value

        user["updated_at"] = datetime.now(UTC).isoformat()

        return {k: v for k, v in user.items() if k != "password_hash"}

    async def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> dict:
        """Change user password."""
        _ = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")

        if not self._verify_password(old_password, user["password_hash"]):
            raise ValueError("Invalid current password")

        user["password_hash"] = self._hash_password(new_password)
        user["updated_at"] = datetime.now(UTC).isoformat()

        return {"message": "Password changed successfully"}

    async def request_password_reset(self, email: str) -> dict:
        """Request password reset."""
        _ = None
        for u in self.users.values():
            if u["email"] == email:
                _ = u
                break

        if not user:
            # Don't reveal if email exists
            return {"message": "If email exists, reset link has been sent"}

        reset_token = secrets.token_urlsafe(32)
        self.password_resets[reset_token] = {
            "user_id": user["id"],
            "expires_at": datetime.now(UTC) + timedelta(hours=1),
        }

        return {
            "message": "Password reset link sent",
            "reset_token": reset_token,  # In real app, this would be sent via email
        }

    async def reset_password(self, token: str, new_password: str) -> dict:
        """Reset password with token."""
        reset_info = self.password_resets.get(token)
        if not reset_info:
            raise ValueError("Invalid reset token")

        if datetime.now(UTC) > reset_info["expires_at"]:
            del self.password_resets[token]
            raise ValueError("Reset token expired")

        _ = self.users.get(reset_info["user_id"])
        if not user:
            raise ValueError("User not found")

        user["password_hash"] = self._hash_password(new_password)
        user["updated_at"] = datetime.now(UTC).isoformat()

        # Remove used reset token
        del self.password_resets[token]

        return {"message": "Password reset successfully"}


@pytest.fixture
def user_system():
    """User system fixture."""
    return MockUserSystem()


@pytest.fixture
async def mock_app(user_system):
    """Mock FastAPI app with user endpoints."""
    from fastapi import Depends, FastAPI, HTTPException
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

    app = FastAPI()
    security = HTTPBearer()

    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        """Get current user from token."""
        try:
            return await user_system.get_current_user(credentials.credentials)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e

    @app.post("/auth/register")
    async def register(user_data: dict):
        try:
            _ = await user_system.register_user(user_data)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.post("/auth/verify-email")
    async def verify_email(data: dict):
        try:
            _ = await user_system.verify_email(data["token"])
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.post("/auth/login")
    async def login(credentials: dict):
        try:
            _ = await user_system.login_user(
                credentials["username"], credentials["password"]
            )
            return result
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e

    @app.get("/auth/me")
    async def get_me(current_user: dict = Depends(get_current_user)):
        return current_user

    @app.post("/auth/refresh")
    async def refresh_token(data: dict):
        try:
            _ = await user_system.refresh_token(data["refresh_token"])
            return result
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e

    @app.put("/users/profile")
    async def update_profile(
        updates: dict, current_user: dict = Depends(get_current_user)
    ):
        try:
            _ = await user_system.update_profile(current_user["id"], updates)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.post("/auth/change-password")
    async def change_password(
        data: dict, current_user: dict = Depends(get_current_user)
    ):
        try:
            _ = await user_system.change_password(
                current_user["id"], data["old_password"], data["new_password"]
            )
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.post("/auth/forgot-password")
    async def forgot_password(data: dict):
        _ = await user_system.request_password_reset(data["email"])
        return result

    @app.post("/auth/reset-password")
    async def reset_password(data: dict):
        try:
            _ = await user_system.reset_password(data["token"], data["new_password"])
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    return app


@pytest.fixture
async def client(mock_app):
    """HTTP client for testing."""
    async with AsyncClient(app=mock_app, base_url="http://test") as ac:
        yield ac


class TestUserRegistration:
    """Test user registration workflow."""

    @pytest.mark.asyncio
    async def test_complete_registration_flow(self, client: AsyncClient):
        """Test complete user registration and verification."""
        # 1. Register user
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "first_name": "New",
            "last_name": "User",
        }

        register_response = await client.post("/auth/register", json=user_data)

        assert register_response.status_code == 200
        register_data = register_response.json()
        assert "user" in register_data
        assert "verification_token" in register_data

        _ = register_data["user"]
        assert user["username"] == "newuser"
        assert user["email"] == "newuser@example.com"
        assert user["is_verified"] is False

        # 2. Verify email
        verification_token = register_data["verification_token"]
        verify_response = await client.post(
            "/auth/verify-email", json={"token": verification_token}
        )

        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        assert "verified successfully" in verify_data["message"]

    @pytest.mark.asyncio
    async def test_duplicate_registration(self, client: AsyncClient):
        """Test registration with duplicate username/email."""
        user_data = {
            "username": "duplicate",
            "email": "duplicate@example.com",
            "password": "password123",
        }

        # First registration should succeed
        first_response = await client.post("/auth/register", json=user_data)
        assert first_response.status_code == 200

        # Second registration should fail
        second_response = await client.post("/auth/register", json=user_data)
        assert second_response.status_code == 400
        assert "already exists" in second_response.json()["detail"]


class TestUserAuthentication:
    """Test user authentication workflow."""

    @pytest.mark.asyncio
    async def test_login_logout_flow(self, client: AsyncClient):
        """Test complete login flow."""
        # 1. Register and verify user
        user_data = {
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpass123",
        }

        register_response = await client.post("/auth/register", json=user_data)
        verification_token = register_response.json()["verification_token"]

        await client.post("/auth/verify-email", json={"token": verification_token})

        # 2. Login
        login_response = await client.post(
            "/auth/login", json={"username": "loginuser", "password": "loginpass123"}
        )

        assert login_response.status_code == 200
        login_data = login_response.json()

        assert "access_token" in login_data
        assert "refresh_token" in login_data
        assert login_data["token_type"] == "bearer"
        assert "user" in login_data

        # 3. Access protected endpoint
        access_token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        me_response = await client.get("/auth/me", headers=headers)

        assert me_response.status_code == 200
        user_info = me_response.json()
        assert user_info["username"] == "loginuser"
        assert user_info["email"] == "login@example.com"

    @pytest.mark.asyncio
    async def test_token_refresh(self, client: AsyncClient):
        """Test token refresh functionality."""
        # Setup: Register and login user
        user_data = {
            "username": "refreshuser",
            "email": "refresh@example.com",
            "password": "pass123",
        }
        register_response = await client.post("/auth/register", json=user_data)
        verification_token = register_response.json()["verification_token"]
        await client.post("/auth/verify-email", json={"token": verification_token})

        login_response = await client.post(
            "/auth/login", json={"username": "refreshuser", "password": "pass123"}
        )

        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        refresh_response = await client.post(
            "/auth/refresh", json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == 200
        refresh_data = refresh_response.json()
        assert "access_token" in refresh_data
        assert refresh_data["token_type"] == "bearer"

        # Use new token
        new_token = refresh_data["access_token"]
        headers = {"Authorization": f"Bearer {new_token}"}
        me_response = await client.get("/auth/me", headers=headers)

        assert me_response.status_code == 200

    @pytest.mark.asyncio
    async def test_invalid_login(self, client: AsyncClient):
        """Test login with invalid credentials."""
        # Try login without registration
        login_response = await client.post(
            "/auth/login", json={"username": "nonexistent", "password": "password"}
        )

        assert login_response.status_code == 401
        assert "not found" in login_response.json()["detail"]

        # Register user but try wrong password
        user_data = {
            "username": "wrongpass",
            "email": "wrong@example.com",
            "password": "correct123",
        }
        await client.post("/auth/register", json=user_data)

        wrong_login_response = await client.post(
            "/auth/login", json={"username": "wrongpass", "password": "wrong123"}
        )

        assert wrong_login_response.status_code == 401
        assert "Invalid password" in wrong_login_response.json()["detail"]


class TestUserProfile:
    """Test user profile management."""

    @pytest.mark.asyncio
    async def test_profile_update(self, client: AsyncClient):
        """Test updating user profile."""
        # Setup: Register and login user
        user_data = {
            "username": "profileuser",
            "email": "profile@example.com",
            "password": "pass123",
        }
        register_response = await client.post("/auth/register", json=user_data)
        verification_token = register_response.json()["verification_token"]
        await client.post("/auth/verify-email", json={"token": verification_token})

        login_response = await client.post(
            "/auth/login", json={"username": "profileuser", "password": "pass123"}
        )

        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Update profile
        updates = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com",
        }

        update_response = await client.put(
            "/users/profile", json=updates, headers=headers
        )

        assert update_response.status_code == 200
        update_response.json()
        assert updated_user["first_name"] == "Updated"
        assert updated_user["last_name"] == "Name"
        assert updated_user["email"] == "updated@example.com"

    @pytest.mark.asyncio
    async def test_password_change(self, client: AsyncClient):
        """Test password change functionality."""
        # Setup: Register and login user
        user_data = {
            "username": "changepass",
            "email": "changepass@example.com",
            "password": "oldpass123",
        }
        register_response = await client.post("/auth/register", json=user_data)
        verification_token = register_response.json()["verification_token"]
        await client.post("/auth/verify-email", json={"token": verification_token})

        login_response = await client.post(
            "/auth/login", json={"username": "changepass", "password": "oldpass123"}
        )

        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Change password
        password_data = {"old_password": "oldpass123", "new_password": "newpass456"}

        change_response = await client.post(
            "/auth/change-password", json=password_data, headers=headers
        )

        assert change_response.status_code == 200
        assert "successfully" in change_response.json()["message"]

        # Verify old password doesn't work
        old_login_response = await client.post(
            "/auth/login", json={"username": "changepass", "password": "oldpass123"}
        )
        assert old_login_response.status_code == 401

        # Verify new password works
        new_login_response = await client.post(
            "/auth/login", json={"username": "changepass", "password": "newpass456"}
        )
        assert new_login_response.status_code == 200


class TestPasswordReset:
    """Test password reset workflow."""

    @pytest.mark.asyncio
    async def test_password_reset_flow(self, client: AsyncClient):
        """Test complete password reset flow."""
        # Setup: Register user
        user_data = {
            "username": "resetuser",
            "email": "reset@example.com",
            "password": "original123",
        }
        await client.post("/auth/register", json=user_data)

        # 1. Request password reset
        reset_request_response = await client.post(
            "/auth/forgot-password", json={"email": "reset@example.com"}
        )

        assert reset_request_response.status_code == 200
        reset_data = reset_request_response.json()
        assert "sent" in reset_data["message"]

        # In real app, token would be sent via email
        # For testing, we get it from the response
        reset_token = reset_data["reset_token"]

        # 2. Reset password with token
        reset_response = await client.post(
            "/auth/reset-password",
            json={"token": reset_token, "new_password": "newpassword456"},
        )

        assert reset_response.status_code == 200
        assert "successfully" in reset_response.json()["message"]

        # 3. Verify new password works
        login_response = await client.post(
            "/auth/login", json={"username": "resetuser", "password": "newpassword456"}
        )

        assert login_response.status_code == 200

        # 4. Verify old password doesn't work
        old_login_response = await client.post(
            "/auth/login", json={"username": "resetuser", "password": "original123"}
        )

        assert old_login_response.status_code == 401


class TestCompleteUserWorkflow:
    """Test complete user workflow from registration to deletion."""

    @pytest.mark.asyncio
    async def test_full_user_lifecycle(self, client: AsyncClient):
        """Test complete user lifecycle."""
        # 1. Register user
        user_data = {
            "username": "fulluser",
            "email": "full@example.com",
            "password": "fullpass123",
            "first_name": "Full",
            "last_name": "User",
        }

        register_response = await client.post("/auth/register", json=user_data)
        verification_token = register_response.json()["verification_token"]

        # 2. Verify email
        await client.post("/auth/verify-email", json={"token": verification_token})

        # 3. Login
        login_response = await client.post(
            "/auth/login", json={"username": "fulluser", "password": "fullpass123"}
        )

        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # 4. Access profile
        profile_response = await client.get("/auth/me", headers=headers)
        assert profile_response.status_code == 200

        # 5. Update profile
        await client.put(
            "/users/profile",
            json={"first_name": "Updated", "last_name": "User"},
            headers=headers,
        )

        # 6. Change password
        await client.post(
            "/auth/change-password",
            json={"old_password": "fullpass123", "new_password": "newpass456"},
            headers=headers,
        )

        # 7. Login with new password
        new_login_response = await client.post(
            "/auth/login", json={"username": "fulluser", "password": "newpass456"}
        )

        assert new_login_response.status_code == 200

        # 8. Use refresh token
        refresh_token = new_login_response.json()["refresh_token"]
        refresh_response = await client.post(
            "/auth/refresh", json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__])
