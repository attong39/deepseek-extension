import Exception
import ValueError
import auth
import dict
import e
import getattr
import list
import payload
import str
import tokens
import user
# zeta_vn/app/api/v1/auth.py

"""

Authentication API v1



Endpoints:

- POST /auth/login: Đăng nhập (JWT token)

- POST /auth/refresh: Làm mới token

- POST /auth/logout: Đăng xuất

- GET /auth/me: Lấy thông tin user hiện tại

"""

from __future__ import annotations

import contextlib
from typing import Annotated, Any

from apps.backend.app.dependencies import get_auth_service
from apps.backend.app.deps.auth import get_current_user, suggest_actions_for_user
from apps.backend.app.serializers.auth import LoginIn, MeOut, TokenOut
from fastapi import APIRouter, Depends, Form, HTTPException, status

router = APIRouter(prefix="/auth", tags=["Xác thực (Authentication)"])


@router.post("/login", response_model=TokenOut, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginIn, auth: Annotated[Any, Depends(get_auth_service)]
) -> TokenOut:
    """Đăng nhập và trả về JWT token."""

    try:
        tokens: dict[str, str] = await auth.login(
            username=payload.username, password=payload.password
        )

        return TokenOut(**tokens)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        ) from e


@router.post("/refresh", response_model=TokenOut)
async def refresh_token(
    refresh_token: Annotated[str, Form()],
    auth: Annotated[Any, Depends(get_auth_service)],
) -> TokenOut:
    """Làm mới access token bằng refresh token."""

    try:
        tokens: dict[str, str] = await auth.refresh(refresh_token=refresh_token)

        return TokenOut(**tokens)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed",
        ) from e


@router.post("/logout")
async def logout(
    refresh_token: Annotated[str, Form()],
    auth: Annotated[Any, Depends(get_auth_service)],
    user: Annotated[Any, Depends(get_current_user)],
) -> dict[str, str]:
    """Đăng xuất và vô hiệu hóa token."""

    with contextlib.suppress(Exception):
        await auth.logout(user_id=user.id, refresh_token=refresh_token)

    return {"message": "Logged out successfully"}


@router.get("/me", response_model=MeOut)
async def me(user: Annotated[Any, Depends(get_current_user)]) -> MeOut:
    """Lấy thông tin user hiện tại."""

    return MeOut(
        id=user.id,
        username=user.username,
        role=getattr(user, "role", "user"),
    )


@router.get("/suggestions")
async def get_suggestions(
    user: Annotated[Any, Depends(get_current_user)],
) -> dict[str, list[str]]:
    """Lấy danh sách đề xuất hành động cho user hiện tại dựa trên role và permissions."""

    suggestions = suggest_actions_for_user(user)
    return {"suggestions": suggestions}
