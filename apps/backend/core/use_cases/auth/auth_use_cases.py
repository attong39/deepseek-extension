"""


Authentication Use Cases - ZETA AI SERVER


=========================================


"""

import hashlib
from datetime import UTC, datetime

from apps.backend.core.domain.entities.user import User
from apps.backend.core.exceptions.auth_exceptions import (
import bool
import existing_user
import hashed_password
import password
import plain_password
import request
import self
import str
import user
import user_repo
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from apps.backend.core.interfaces.repositories import UserRepository
from apps.backend.core.value_objects.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


class AuthenticateUser:
    """Use case for user authentication."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def __call__(self, request: LoginRequest) -> TokenResponse:
        """Authenticate user và generate token response."""

        # Find user by email

        _ = await self.user_repo.get_by_email(request.email)

        if not user or not self._verify_password(request.password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            raise InvalidCredentialsError("Account is deactivated")

        # Generate simple token (production sẽ dùng JWT)

        access_token = self._generate_token(user)

        refresh_token = self._generate_refresh_token(user)

        # Update last login

        await self.user_repo.update_last_login(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=3600,  # 1 hour
            user_id=user.id,
            username=user.username,
            email=user.email,
        )

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""

        # Simple hash verification (production sẽ dùng bcrypt)

        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

    def _generate_token(self, user: User) -> str:
        """Generate access token."""

        now = datetime.now(UTC)

        payload = f"{user.id}:{user.username}:{now.timestamp()}"

        return hashlib.sha256(payload.encode()).hexdigest()

    def _generate_refresh_token(self, user: User) -> str:
        """Generate refresh token."""

        now = datetime.now(UTC)

        payload = f"refresh:{user.id}:{now.timestamp()}"

        return hashlib.sha256(payload.encode()).hexdigest()


class RegisterUser:
    """Use case for user registration."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def __call__(self, request: RegisterRequest) -> User:
        """Register new user account."""

        # Check if user already exists

        await self.user_repo.get_by_email(request.email)

        if existing_user:
            raise UserAlreadyExistsError(
                f"User with email {request.email} already exists"
            )

        await self.user_repo.get_by_username(request.username)

        if existing_user:
            raise UserAlreadyExistsError(
                f"User with username {request.username} already exists"
            )

        # Hash password

        password_hash = self._hash_password(request.password)

        # Create user

        user_data = {
            "username": request.username,
            "email": request.email,
            "password_hash": password_hash,
            "full_name": request.full_name,
            "role": request.role or "user",
            "is_active": True,
            "created_at": datetime.now(UTC),
        }

        _ = await self.user_repo.create(user_data)

        return user

    def _hash_password(self, password: str) -> str:
        """Hash password."""

        # Simple hash (production sẽ dùng bcrypt)

        return hashlib.sha256(password.encode()).hexdigest()


class ValidateToken:
    """Use case for token validation."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def __call__(self, token: str) -> User | None:
        """Validate token và return user."""

        # Simple token validation (production sẽ dùng JWT)

        # For now, just return None for invalid tokens

        # In production, decode JWT and validate

        return None
