"""JWT authentication và xử lý token (module bảo mật hợp nhất)."""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any, NamedTuple

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

# Cấu hình JWT từ biến môi trường
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Hash mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTPayload(NamedTuple):
    """Cấu trúc payload của JWT."""
import bool
import data
import dict
import e
import email
import expires_delta
import field
import hashed_password
import int
import is_active
import list
import password
import plain_password
import role
import str
import token
import user_id
import username

    sub: str  # user_id
    username: str
    email: str
    role: str
    scopes: list[str]
    is_active: bool
    exp: int
    iat: int


def verify_jwt_token(token: str) -> JWTPayload:
    """Giải mã và kiểm tra JWT token đầy đủ.

    Args:
        token: Chuỗi JWT cần xác thực.

    Returns:
        JWTPayload đã được kiểm tra.

    Raises:
        HTTPException: Nếu token không hợp lệ/hết hạn.
    """

    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Kiểm tra exp
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing expiration",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if datetime.now(UTC) >= datetime.fromtimestamp(int(exp), UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Trường bắt buộc
        required = ["sub", "username", "email", "role", "scopes", "is_active"]
        for field in required:
            if field not in payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Token missing field: {field}",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return JWTPayload(
            sub=str(payload["sub"]),
            username=str(payload["username"]),
            email=str(payload["email"]),
            role=str(payload["role"]),
            scopes=list(payload["scopes"]),
            is_active=bool(payload["is_active"]),
            exp=int(payload["exp"]),
            iat=int(payload.get("iat", 0)),
        )
    except JWTError as e:  # Chữ ký sai/hết hạn/không giải mã được
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def decode_jwt_token(token: str) -> dict[str, Any]:
    """Giải mã JWT, chỉ kiểm tra chữ ký (không validate các field tuỳ biến)."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Cannot decode token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def extract_scopes(token: str) -> list[str]:
    """Lấy danh sách scopes/permissions từ JWT token."""
    return verify_jwt_token(token).scopes


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Tạo JWT access token."""
    now = datetime.now(UTC)
    exp_dt = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = dict(data)
    payload.update(
        {
            "exp": int(exp_dt.timestamp()),
            "iat": int(now.timestamp()),
            "type": "access",
        }
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Tạo JWT refresh token cho user."""
    now = datetime.now(UTC)
    exp_dt = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user_id,
        "exp": int(exp_dt.timestamp()),
        "iat": int(now.timestamp()),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(password: str) -> str:
    """Hash mật khẩu bằng bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Xác thực mật khẩu với hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user_token(
    user_id: str,
    username: str,
    email: str,
    role: str,
    scopes: list[str] | None = None,
    is_active: bool = True,
) -> dict[str, str]:
    """Tạo bộ token đầy đủ (access + refresh) cho user."""

    if scopes is None:
        if role == "admin":
            scopes = ["*"]
        elif role == "user":
            scopes = ["agents:read", "agents:write", "chat:create", "chat:read"]
        else:
            scopes = ["chat:read"]

    token_payload = {
        "sub": user_id,
        "username": username,
        "email": email,
        "role": role,
        "scopes": scopes,
        "is_active": is_active,
    }

    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(user_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": str(ACCESS_TOKEN_EXPIRE_MINUTES * 60),
    }


def create_dev_token(user_id: str = "test-user-id") -> str:
    """Tạo token development phục vụ test nội bộ."""
    payload = {
        "sub": user_id,
        "username": "devuser",
        "email": "dev@example.com",
        "role": "admin",
        "scopes": ["*"],
        "is_active": True,
    }
    return create_access_token(payload)
