"""Authentication dependencies and small helpers used by routers.

File này giữ các dependency nhẹ (stubs) để phục vụ môi trường phát triển
và test. Không đặt logic domain nặng ở đây; module cung cấp một helper
"auto đề xuất" đơn giản `suggest_actions_for_user` dựa trên role/scopes.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Annotated, Any, TypeAlias
from uuid import UUID

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import Exception
import any
import authorization
import bool
import credentials
import current_user
import data
import details
import dict
import e
import event_type
import exc
import getattr
import i
import isinstance
import len
import list
import range
import refresh_token
import request
import required_scope
import resource
import resource_owner_id
import s
import scheme
import self
import set
import str
import suggestions
import user

security = HTTPBearer()

logger = logging.getLogger(__name__)


def log_security_event(
    user_id: str | UUID, event_type: str, resource: str, details: dict | None = None
) -> None:
    """Ghi sự kiện bảo mật (đơn giản, dùng logging).

    Args:
        user_id: ID người dùng gây ra event (UUID hoặc str).
        event_type: Tên loại event.
        resource: Tên resource liên quan.
        details: Thông tin thêm.
    """
    try:
        audit_data = {
            "user_id": str(user_id),
            "event_type": event_type,
            "resource": resource,
        }
        if details:
            audit_data.update(details)
        logger.info("security_audit", extra={"audit": audit_data})
    except Exception as e:  # pragma: no cover - logging must not break flow
        logger.debug("Failed to log security event: %s", e)


def get_current_permissions(
    authorization: str | None = Header(default=None),
) -> list[str]:
    """Trích permissions/scopes từ header Authorization (nếu có).

    Hàm đơn giản: nếu header không có, trả về rỗng. Nếu có bearer token, cố
    gắng đọc claim 'permissions' hoặc 'scopes' qua JWT handler nếu tồn tại.
    """
    if not authorization:
        return []
    scheme, _, token = authorization.partition(" ")
    if not token or scheme.lower() != "bearer":
        return []
    try:
        # Sử dụng JWTHandler nếu có (module bên ngoài có thể override)
        from app.auth.jwt_handler import JWTHandler  # type: ignore

        payload = JWTHandler.verify_token(token)
        return payload.get("permissions") or payload.get("scopes") or []
    except Exception:
        return []


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Any:
    """Lấy current user từ token JWT.

    Đây là phiên bản nhẹ: trả về một object/dict có các thuộc tính tối thiểu:
    `id`, `username`, `role`, `scopes` để các dependency khác dùng.
    """
    token = credentials.credentials
    # Dev/test shortcuts
    if token in {"dev", "test"}:
        return {
            "id": "test-user-id",
            "username": "dev",
            "role": "admin",
            "scopes": ["*"],
        }
    try:
        from app.auth.jwt_handler import JWTHandler  # type: ignore

        payload = JWTHandler.verify_token(token)
        return {
            "id": payload.get("sub") or payload.get("user_id") or "unknown",
            "username": payload.get("username", "unknown"),
            "role": payload.get("role", "user"),
            "scopes": payload.get("scopes", []) or payload.get("permissions", []),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc


def get_current_admin_user(current_user: Any = Depends(get_current_user)) -> Any:
    """Dependency trả về user khi user là admin; ngược lại raise 403."""
    if getattr(current_user, "role", None) != "admin" and (
        isinstance(current_user, dict) and current_user.get("role") != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin required"
        )
    return current_user


def get_current_user_id(current_user: Any = Depends(get_current_user)) -> str:
    """Trả lại user id dạng chuỗi từ current_user."""
    return str(
        getattr(current_user, "id", None)
        or (current_user.get("id") if isinstance(current_user, dict) else "")
    )


def get_optional_current_user_id(request: Request) -> str | None:
    """Cố gắng trích user id từ header Authorization nếu có, không raise."""
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or " " not in auth:
        return None
    scheme, token = auth.split(" ", 1)
    if scheme.lower() != "bearer" or not token:
        return None
    if token in {"dev", "test"}:
        return "test-user-id"
    try:
        from app.auth.jwt_handler import JWTHandler  # type: ignore

        payload = JWTHandler.verify_token(token)
        return payload.get("sub") or payload.get("user_id")
    except Exception:
        return None


def _has_scope_permission(user_scopes: list[str], required_scope: str) -> bool:
    """Kiểm tra scope hỗ trợ wildcard và parent scope nhỏ gọn."""
    if required_scope in user_scopes:
        return True
    if "*" in user_scopes:
        return True
    # agent:* matches agent:read
    if ":" in required_scope:
        prefix = required_scope.split(":", 1)[0]
        if f"{prefix}:*" in user_scopes:
            return True
    # parent scope e.g. admin covers admin:users
    parts = required_scope.split(":")
    for i in range(1, len(parts)):
        parent = ":".join(parts[:i])
        if parent in user_scopes:
            return True
    return False


def require_permissions(scopes: str | Iterable[str]):
    """Factory trả dependency kiểm tra permission.

    Args:
        scopes: scope hoặc iterable các scope cần có.
    Returns:
        Dependency function dùng trong Depends(...)
    """

    required = [scopes] if isinstance(scopes, str) else list(scopes)

    def _check_permissions(current_user: Any = Depends(get_current_user)) -> Any:
        user_scopes = getattr(current_user, "scopes", None) or (
            current_user.get("scopes") if isinstance(current_user, dict) else []
        )
        # admin or wildcard grants all
        role = getattr(current_user, "role", None) or (
            current_user.get("role") if isinstance(current_user, dict) else None
        )
        if role == "admin" or "*" in user_scopes:
            return current_user
        missing = [s for s in required if not _has_scope_permission(user_scopes, s)]
        if missing:
            log_security_event(
                getattr(current_user, "id", "unknown"),
                "authorization_failed",
                ",".join(missing),
                {"user_scopes": user_scopes},
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Missing: {', '.join(missing)}",
            )
        log_security_event(
            getattr(current_user, "id", "unknown"),
            "authorization_success",
            ",".join(required),
            {"user_scopes": user_scopes},
        )
        return current_user

    return _check_permissions


def get_auth_service():  # pragma: no cover - simple stub
    """Trả về auth service stub dùng cho demo/tests."""

    class _Auth:
        async def login(self, _username: str, _password: str) -> dict[str, str]:
            return {
                "access_token": "mock_access",
                "refresh_token": "mock_refresh",
                "token_type": "bearer",
            }

        async def refresh(self, refresh_token: str) -> dict[str, str]:
            return {
                "access_token": "mock_access_refreshed",
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

    return _Auth()


def get_user_service():  # pragma: no cover - simple stub
    """Minimal user service facade cho tests/demo."""

    class _User:
        def __init__(self) -> None:
            self._users: dict[str, dict] = {}

        async def create_user(self, data: dict, **_kwargs) -> dict:
            user_id = data.get("id") or "u_demo"
            _ = {
                "id": user_id,
                "username": data.get("username", f"user_{user_id[:6]}"),
                "email": data.get("email", "noreply@example.com"),
                "role": data.get("role", "user"),
            }
            self._users[user_id] = user
            return user

        async def get_user(self, user_id: str) -> dict | None:
            return self._users.get(user_id)


def validate_user_access(user_id: str, resource_owner_id: str) -> None:
    """Raise HTTPException nếu user_id không khớp owner_id."""
    if str(user_id) != str(resource_owner_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: insufficient permissions",
        )


# Type aliases for DI (lightweight)
UserService: TypeAlias = Annotated[Any, Depends(get_user_service)]
CurrentUserId: TypeAlias = Annotated[str, Depends(get_current_user_id)]


def get_permission_manager() -> Any:  # pragma: no cover - thin wrapper
    """Trả về một PermissionManager nếu có, else đơn giản None.

    Implementation nên được cung cấp ở core/security nếu cần.
    """
    try:
        from apps.backend.core.security.permission_manager import (
            PermissionManager,  # type: ignore
        )

        return PermissionManager()
    except Exception:
        return None


def suggest_actions_for_user(current_user: Any) -> list[str]:
    """Auto đề xuất hành động dựa trên role và scopes của user.

    Mục tiêu: helper nhỏ để router hoặc UI backend có thể gọi để gợi ý hành động.

    Trả về list các action (string) sắp xếp theo mức ưu tiên.
    """
    role = getattr(current_user, "role", None) or (
        current_user.get("role") if isinstance(current_user, dict) else "user"
    )
    scopes = (
        getattr(current_user, "scopes", None)
        or (current_user.get("scopes") if isinstance(current_user, dict) else [])
        or []
    )

    suggestions: list[str] = []
    # Admin gets management suggestions
    if role == "admin":
        suggestions.extend(["manage_users", "view_audit_logs", "configure_system"])

    # Scope based suggestions
    if any(_has_scope_permission(scopes, s) for s in ["agent:write", "agent:create"]):
        suggestions.append("create_agent")
    if any(_has_scope_permission(scopes, s) for s in ["agent:read", "agent:list"]):
        suggestions.append("list_agents")
    if any(_has_scope_permission(scopes, s) for s in ["automation:plan:create"]):
        suggestions.append("create_automation_plan")

    # Generic suggestions for users
    if role == "user" and not suggestions:
        suggestions.extend(["view_profile", "update_settings"])

    # Remove duplicates but keep order
    seen = set()
    ordered = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    return ordered
