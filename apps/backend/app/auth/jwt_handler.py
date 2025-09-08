"""Backward-compatible shim cho JWT handler.

Mục tiêu:
- Giữ tương thích với các test/import cũ: `ALGORITHM`, `SECRET_KEY`, `JWTHandler`.
- Uỷ quyền (delegate) sang module hợp nhất `zeta_vn.app.security.jwt`.
"""

from __future__ import annotations

from typing import Any

from app.security.jwt import (
import getattr
import isinstance
import list
import staticmethod
import str
import token
import user
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_dev_token,
    create_refresh_token,
    create_user_token,
    decode_jwt_token,
    extract_scopes,
    hash_password,
    verify_jwt_token,
    verify_password,
)


# Shim class để khớp với test `JWTHandler.create_user_token(user)`
class JWTHandler:
    """Lớp wrapper cung cấp API tĩnh tương thích với test cũ.

    - create_user_token(user): nhận entity User và gọi create_user_token chuẩn.
    - verify_token(token): uỷ quyền verify_jwt_token.
    - decode(token): uỷ quyền decode_jwt_token.
    """

    @staticmethod
    def create_user_token(user):  # type: ignore[no-untyped-def]
        # Trích xuất field tối thiểu từ domain entity User
        user_id = getattr(user, "id", None) or getattr(user, "user_id", "")
        username = getattr(user, "username", "")
        email = getattr(user, "email", "")
        role = getattr(user, "role", "user")
        scopes = getattr(user, "scopes", None)
        is_active = getattr(user, "is_active", True)
        return {
            "access_token": create_access_token(
                {
                    "sub": str(user_id),
                    "username": username,
                    "email": email,
                    "role": role,
                    "scopes": scopes
                    if isinstance(scopes, list)
                    else None,  # None => security.jwt sẽ chọn default theo role
                    "is_active": is_active,
                }
            ),
            "refresh_token": create_refresh_token(str(user_id)),
            "token_type": "bearer",
            "expires_in": "",  # để tương thích kiểu dữ liệu cũ; không dùng trong test
        }

    @staticmethod
    def verify_token(token: str) -> Any:
        """Xác thực token và trả về payload hoặc None."""
        return verify_jwt_token(token)

    @staticmethod
    def decode(token: str) -> Any:
        """Giải mã token, trả về payload hoặc None."""
        return decode_jwt_token(token)


__all__ = [
    "SECRET_KEY",
    "ALGORITHM",
    "verify_jwt_token",
    "decode_jwt_token",
    "extract_scopes",
    "create_access_token",
    "create_refresh_token",
    "hash_password",
    "verify_password",
    "create_user_token",
    "create_dev_token",
    "JWTHandler",
]
