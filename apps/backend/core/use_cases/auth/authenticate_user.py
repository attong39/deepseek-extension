from datetime import datetime
from typing import Any
import BaseException
import Exception
import JWTError
import JWTExpiredSignatureError
import TypeError
import ValueError
import bool
import bytearray
import bytes
import callable
import err
import existing_user
import getattr
import hashed_password
import isinstance
import jwt
import password
import plain_password
import request
import self
import str
import token
import tuple
import type
import user
import user_repo

#!/usr/bin/env python3
# ruff: format

"""Authentication use cases for ZETA AI Server.

Implements JWT-based authentication with user management.
"""

from __future__ import annotations

import importlib
import inspect
from datetime import UTC, timedelta
from typing import TYPE_CHECKING, cast

import bcrypt
from apps.backend.config.settings import get_settings
from apps.backend.core.exceptions.auth_exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
)
from apps.backend.core.value_objects.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

from core.utils.async_utils import _maybe_await

if TYPE_CHECKING:  # pragma: no cover - typing only
    from apps.backend.core.domain.entities.user import User
    from apps.backend.core.interfaces.repositories import UserRepository


def _init_jwt() -> (
    tuple[Any, type[BaseException], type[BaseException], type[BaseException]]
):
    """Resolve a JWT implementation and its common exceptions.

    Returns:
        (jwt_module, ExpiredSignatureError, InvalidTokenError, BaseJWTError)
    """
    try:  # Prefer PyJWT
        jwt_mod = importlib.import_module("jwt")
        e_exp = getattr(jwt_mod, "ExpiredSignatureError", Exception)
        e_inv = getattr(jwt_mod, "InvalidTokenError", Exception)
        e_base = getattr(jwt_mod, "PyJWTError", Exception)
        return jwt_mod, e_exp, e_inv, e_base
    except Exception:
        try:  # Fallback to python-jose
            jose_jwt = importlib.import_module("jose.jwt")
            jose_exc = importlib.import_module("jose.exceptions")
            e_exp = getattr(jose_exc, "ExpiredSignatureError", Exception)
            e_base = getattr(jose_exc, "JWTError", Exception)
            e_inv = e_base
            return jose_jwt, e_exp, e_inv, e_base
        except Exception:
            return None, Exception, Exception, Exception


jwt_mod, JWTExpiredSignatureError, JWTInvalidTokenError, JWTError = _init_jwt()

# Ensure jwt is typed as Any for static analysis while remaining runtime-flexible
jwt: Any = cast("Any", jwt_mod)

settings = get_settings()


class AuthenticateUser:
    """Use case for user authentication with JWT tokens."""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def __call__(self, request: LoginRequest) -> TokenResponse:
        """Authenticate a user and generate JWT tokens.

        Args:
            request: Login credentials (email/username + password).

        Returns:
            TokenResponse containing access/refresh tokens and metadata.

        Raises:
            InvalidCredentialsError: Invalid credentials or disabled account.
        """

        # Find user by email or username
        res = self.user_repo.get_by_email(request.email)
        _ = await _maybe_await(res)
        if not user:
            get_by_username = getattr(self.user_repo, "get_by_username", None)
            if get_by_username is not None:
                _res = get_by_username(request.email)
                _ = await _maybe_await(_res)

        if not user:
            raise InvalidCredentialsError("Invalid email/username or password")

        # Check if user is active BEFORE verifying password (avoid bcrypt with dummy hashes)
        is_active_attr = getattr(user, "is_active", None)
        is_active = bool(
            is_active_attr()
            if callable(is_active_attr)
            else getattr(user, "is_active", False)
        )
        if not is_active:
            raise InvalidCredentialsError("Account is deactivated")

        # hashed_password in tests may be a Mock; coerce to str for bcrypt
        hashed = getattr(user, "password_hash", "")
        if isinstance(hashed, (bytes, bytearray)):
            hashed_bytes = bytes(hashed)
        else:
            try:
                hashed_bytes = str(hashed).encode("utf-8")
            except Exception:
                hashed_bytes = b""

        if not self._verify_password(request.password, hashed_bytes):
            raise InvalidCredentialsError("Invalid email/username or password")

        # Generate tokens
        access_token = self._generate_access_token(user)
        refresh_token = self._generate_refresh_token(user)

        # Update last login (support async or sync)
        update_last_login = getattr(self.user_repo, "update_last_login", None)
        if update_last_login is not None:
            _r = update_last_login(user.id)
            await _maybe_await(_r)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=str(user.id),
            username=user.username,
            email=user.email,
        )

    def _verify_password(
        self, plain_password: str, hashed_password: str | bytes
    ) -> bool:
        """Verify password against hash.

        Accept either `str` or `bytes` for `hashed_password` because unit tests
        may provide Mock objects or bytes. This helper coerces types safely.
        """
        if isinstance(hashed_password, str):
            hashed = hashed_password.encode("utf-8")
        elif isinstance(hashed_password, (bytes, bytearray)):
            hashed = bytes(hashed_password)
        else:
            # Fallback: convert to string then to bytes
            try:
                hashed = str(hashed_password).encode("utf-8")
            except Exception:
                hashed = b""

        try:
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed)
        except (ValueError, TypeError):  # pragma: no cover - defensive
            return False

    def _generate_access_token(self, user: User) -> str:
        """Generate JWT access token."""

        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "access",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def _generate_refresh_token(self, user: User) -> str:
        """Generate JWT refresh token."""

        expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "refresh",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


class RegisterUser:
    """Use case for user registration."""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def __call__(self, request: RegisterRequest) -> User:
        """Register a new user account.

        Args:
            request: Registration data (username, email, password, etc.).

        Returns:
            The created user entity.

        Raises:
            UserAlreadyExistsError: If the user already exists.
        """

        # Check if user already exists
        await self.user_repo.get_by_email(request.email)
        if existing_user:
            raise UserAlreadyExistsError(
                f"User with email {request.email} already exists"
            )

        get_by_username = getattr(self.user_repo, "get_by_username", None)
        existing_user2 = None
        if get_by_username is not None:
            _res = get_by_username(request.username)
            existing_user2 = await _res if inspect.isawaitable(_res) else _res

        if existing_user2:
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

        _ = await self.user_repo.create(user_data)  # type: ignore[arg-type]
        return user

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


class RefreshToken:
    """Use case for token refresh."""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def __call__(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using a refresh token.

        Args:
            refresh_token: A valid refresh token.

        Returns:
            TokenResponse: New access token and refresh token.

        Raises:
            InvalidTokenError: If the refresh token is invalid/expired.
        """

        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )

            if payload.get("type") != "refresh":
                raise InvalidTokenError("Invalid token type")

            user_id = payload.get("sub")
            if not user_id:
                raise InvalidTokenError("Invalid token payload")

            # Get user
            _ = await self.user_repo.get_by_id(user_id)

            active = False
            if user is not None:
                is_active_attr = getattr(user, "is_active", None)
                if callable(is_active_attr):
                    active = bool(is_active_attr())
                else:
                    active = bool(getattr(user, "is_active", False))

            if not user or not active:
                raise InvalidTokenError("User not found or inactive")

            # Generate new tokens
            access_token = self._generate_access_token(user)
            new_refresh_token = self._generate_refresh_token(user)

            return TokenResponse(
                access_token=access_token,
                refresh_token=new_refresh_token,
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user_id=str(user.id),
                username=user.username,
                email=user.email,
            )

        except JWTExpiredSignatureError as err:
            raise InvalidTokenError("Refresh token has expired") from err

        except JWTError as err:
            raise InvalidTokenError("Invalid refresh token") from err

    def _generate_access_token(self, user: User) -> str:
        """Generate JWT access token."""

        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "access",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def _generate_refresh_token(self, user: User) -> str:
        """Generate JWT refresh token."""

        expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "refresh",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


class ValidateToken:
    """Use case for token validation."""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def __call__(self, token: str) -> User:
        """Validate an access token and return the user.

        Args:
            token: JWT access token.

        Returns:
            The authenticated user entity.

        Raises:
            InvalidTokenError: If the token is invalid/expired.
        """

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )

            if payload.get("type") != "access":
                raise InvalidTokenError("Invalid token type")

            user_id = payload.get("sub")
            if not user_id:
                raise InvalidTokenError("Invalid token payload")

            # Get user
            _ = await self.user_repo.get_by_id(user_id)

            active = False
            if user is not None:
                is_active_attr = getattr(user, "is_active", None)
                if callable(is_active_attr):
                    active = bool(is_active_attr())
                else:
                    active = bool(getattr(user, "is_active", False))

            if not user or not active:
                raise InvalidTokenError("User not found or inactive")

            return user

        except JWTExpiredSignatureError as err:
            raise InvalidTokenError("Access token has expired") from err

        except JWTError as err:
            raise InvalidTokenError("Invalid access token") from err
