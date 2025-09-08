"""Auth API endpoints với validate input và handle exception."""

from __future__ import annotations

from app.dependencies import get_auth_service, get_current_user
from app.schemas.auth import AuthCreate, AuthLogin, AuthResponse
from apps.backend.core.domain.entities.user import User
from apps.backend.core.services.auth_service import AuthService
from fastapi import APIRouter, Depends, HTTPException, status

from core.observability.logging import get_logger  # Logger chuẩn dự án với trace-id

logger = get_logger(__name__)

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register_user(
    user_data: AuthCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    """Register a new user.

    Args:
        user_data: Dữ liệu đăng ký (validated qua Pydantic).
        auth_service: Service xử lý auth.

    Returns:
        AuthResponse: Thông tin user đã đăng ký.

    Raises:
        HTTPException: Nếu đăng ký thất bại.
    """
import Exception
import auth_service
import current_user
import dict
import e
import login_data
import str
import user_data
    try:
        user = await auth_service.register_user(user_data)
        logger.info(f"User registered successfully: {user.id}")
        return AuthResponse.from_entity(user)
    except Exception as e:
        logger.error(f"Failed to register user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user",
        )


@router.post("/login", response_model=AuthResponse)
async def login_user(
    login_data: AuthLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    """Login user và trả token.

    Args:
        login_data: Dữ liệu đăng nhập (validated qua Pydantic).
        auth_service: Service xử lý auth.

    Returns:
        AuthResponse: Thông tin user và token.

    Raises:
        HTTPException: Nếu đăng nhập thất bại.
    """
    try:
        user, token = await auth_service.login_user(login_data)
        logger.info(f"User logged in successfully: {user.id}")
        return AuthResponse.from_entity(user, token=token)
    except Exception as e:
        logger.error(f"Failed to login user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


@router.post("/logout")
async def logout_user(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    """Logout user.

    Args:
        current_user: Người dùng hiện tại.
        auth_service: Service xử lý auth.

    Returns:
        dict: Thông báo logout thành công.

    Raises:
        HTTPException: Nếu logout thất bại.
    """
    try:
        await auth_service.logout_user(current_user.id)
        logger.info(f"User logged out successfully: {current_user.id}")
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Failed to logout user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to logout"
        )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    """Refresh access token.

    Args:
        current_user: Người dùng hiện tại.
        auth_service: Service xử lý auth.

    Returns:
        AuthResponse: Thông tin user và token mới.

    Raises:
        HTTPException: Nếu refresh thất bại.
    """
    try:
        token = await auth_service.refresh_token(current_user.id)
        logger.info(f"Token refreshed successfully for user: {current_user.id}")
        return AuthResponse.from_entity(current_user, token=token)
    except Exception as e:
        logger.error(f"Failed to refresh token for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token",
        )


__all__ = [
    "router",
]
