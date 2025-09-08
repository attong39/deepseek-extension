import os
import result
import user

"""
Tests for Authentication Use Cases - ZETA AI
===========================================
"""

import pytest

from core.domain.value_objects.auth import LoginRequest, RegisterRequest
from core.exceptions.auth_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from core.use_cases.auth.auth_use_cases import AuthenticateUser, RegisterUser
from data.repositories.user_repository import InMemoryUserRepository


class TestAuthenticateUser:
    """Test cases for AuthenticateUser use case."""

    @pytest.fixture
    async def user_repo(self):
        """Setup user repository with test data."""
        repo = InMemoryUserRepository()
        # Pre-create a test user
        await repo.create(
            {
                "username": "testuser",
                "email": "test@example.com",
                "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # 'password'
                "full_name": "Test User",
                "role": "user",
                "is_active": True,
            }
        )
        return repo

    @pytest.fixture
    def auth_use_case(self, user_repo):
        """Setup AuthenticateUser use case."""
        return AuthenticateUser(user_repo)

    @pytest.mark.asyncio
    async def test_authenticate_valid_user(self, auth_use_case):
        """Test successful authentication."""
        request = LoginRequest(email="test@example.com", password=os.getenv("PASSWORD"))
        _ = await auth_use_case(request)

        assert result.user_id == "1"
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.token_type == "bearer"
        assert result.access_token is not None
        assert result.refresh_token is not None

    @pytest.mark.asyncio
    async def test_authenticate_invalid_email(self, auth_use_case):
        """Test authentication with invalid email."""
        request = LoginRequest(
            email="invalid@example.com", password=os.getenv("PASSWORD")
        )

        with pytest.raises(InvalidCredentialsError):
            await auth_use_case(request)

    @pytest.mark.asyncio
    async def test_authenticate_invalid_password(self, auth_use_case):
        """Test authentication with invalid password."""
        request = LoginRequest(email="test@example.com", password=os.getenv("PASSWORD"))

        with pytest.raises(InvalidCredentialsError):
            await auth_use_case(request)


class TestRegisterUser:
    """Test cases for RegisterUser use case."""

    @pytest.fixture
    def user_repo(self):
        """Setup empty user repository."""
        return InMemoryUserRepository()

    @pytest.fixture
    def register_use_case(self, user_repo):
        """Setup RegisterUser use case."""
        return RegisterUser(user_repo)

    @pytest.mark.asyncio
    async def test_register_new_user(self, register_use_case):
        """Test successful user registration."""
        request = RegisterRequest(
            username="newuser",
            email="new@example.com",
            password=os.getenv("PASSWORD"),
            full_name="New User",
        )

        _ = await register_use_case(request)

        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.full_name == "New User"
        assert user.role == "user"
        assert user.is_active is True

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, register_use_case, user_repo):
        """Test registration with duplicate email."""
        # Create first user
        await user_repo.create(
            {
                "username": "existinguser",
                "email": "existing@example.com",
                "password_hash": "hash",
                "role": "user",
                "is_active": True,
            }
        )

        # Try to register with same email
        request = RegisterRequest(
            username="newuser",
            email="existing@example.com",
            password=os.getenv("PASSWORD"),
        )

        with pytest.raises(UserAlreadyExistsError):
            await register_use_case(request)

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, register_use_case, user_repo):
        """Test registration with duplicate username."""
        # Create first user
        await user_repo.create(
            {
                "username": "existinguser",
                "email": "existing@example.com",
                "password_hash": "hash",
                "role": "user",
                "is_active": True,
            }
        )

        # Try to register with same username
        request = RegisterRequest(
            username="existinguser",
            email="new@example.com",
            password=os.getenv("PASSWORD"),
        )

        with pytest.raises(UserAlreadyExistsError):
            await register_use_case(request)
