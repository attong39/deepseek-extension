"""RBAC (Role-Based Access Control) utilities - Unified Security Module.

Đồng bộ với core permissions: dùng normalize_scopes để tránh lệch contract,
loại bỏ wildcard '*' trong so khớp thực thi.
"""

from __future__ import annotations

from collections.abc import Callable

from app.security.jwt import JWTPayload, verify_jwt_token
from apps.backend.core.value_objects.permissions import normalize_scopes
from fastapi import HTTPException, Request, status
import action
import all
import any
import bool
import isinstance
import len
import list
import request
import require_all
import require_all_scopes
import required_scope
import resource
import scope
import set
import str
import token
import user_role
import user_scopes


def has_scope(user_scopes: list[str], required_scope: str) -> bool:
    """
    Check if user has required scope.

    Args:
        user_scopes: List of user's scopes/permissions
        required_scope: Required scope to check

    Returns:
        bool: True if user has the scope
    """
    # Chuẩn hoá scopes: loại wildcard, lọc scope lạ, sort
    normalized = set(normalize_scopes(user_scopes))

    # Exact scope match
    if required_scope in normalized:
        return True

    # Hierarchical scope check (e.g., "agents:write" includes "agents:read")
    if ":" in required_scope:
        resource, action = required_scope.split(":", 1)

        # Check for write permission implying read permission
        if action == "read":
            write_scope = f"{resource}:write"
            if write_scope in normalized:
                return True

    return False


# FastAPI dependency helper alias
def require_scopes(required_scopes: str | list[str], require_all: bool = False):
    """Alias tiện dụng để tạo validator dependency cho FastAPI routes.

    Example:
        validate = require_scopes(["agents:read"], require_all=False)
        @router.get("/agents", dependencies=[Depends(validate)])
    """

    return create_permission_validator(
        required_scopes=required_scopes, require_all_scopes=require_all
    )


def check_permissions(
    user_scopes: list[str], required_scopes: str | list[str], require_all: bool = False
) -> bool:
    """
    Check if user has required permissions.

    Args:
        user_scopes: List of user's scopes/permissions
        required_scopes: Required scope(s) - string or list
        require_all: If True, user must have ALL scopes; if False, ANY scope

    Returns:
        bool: True if user has required permissions
    """
    # Normalize to list
    if isinstance(required_scopes, str):
        required_scopes = [required_scopes]

    if require_all:
        # User must have ALL required scopes
        return all(has_scope(user_scopes, scope) for scope in required_scopes)
    else:
        # User must have ANY of the required scopes
        return any(has_scope(user_scopes, scope) for scope in required_scopes)


def require_permissions(
    user_scopes: list[str],
    required_scopes: str | list[str],
    require_all: bool = False,
    error_message: str | None = None,
) -> None:
    """
    Require user to have specific permissions or raise HTTPException.

    Args:
        user_scopes: List of user's scopes/permissions
        required_scopes: Required scope(s) - string or list
        require_all: If True, user must have ALL scopes; if False, ANY scope
        error_message: Custom error message

    Raises:
        HTTPException: If user doesn't have required permissions
    """
    if not check_permissions(user_scopes, required_scopes, require_all):
        if error_message is None:
            if isinstance(required_scopes, str):
                scope_text = required_scopes
            else:
                scope_text = ", ".join(required_scopes)
                if require_all:
                    scope_text = f"all of: {scope_text}"
                else:
                    scope_text = f"any of: {scope_text}"

            error_message = f"Insufficient permissions. Required: {scope_text}"

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)


def require_role(user_role: str, required_roles: str | list[str]) -> None:
    """
    Require user to have specific role(s).

    Args:
        user_role: User's current role
        required_roles: Required role(s) - string or list

    Raises:
        HTTPException: If user doesn't have required role
    """
    # Normalize to list
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    # Admin always has access
    if user_role == "admin":
        return

    if user_role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient role. Required: {', '.join(required_roles)}, current: {user_role}",
        )


def validate_token_and_permissions(
    token: str,
    required_scopes: str | list[str] | None = None,
    required_roles: str | list[str] | None = None,
    require_all_scopes: bool = False,
) -> JWTPayload:
    """
    Validate JWT token and check permissions in one step.

    Args:
        token: JWT token to validate
        required_scopes: Required scope(s) for authorization
        required_roles: Required role(s) for authorization
        require_all_scopes: If True, user must have ALL scopes

    Returns:
        JWTPayload: Validated token payload

    Raises:
        HTTPException: If token is invalid or user lacks permissions
    """
    # Verify token first
    payload = verify_jwt_token(token)

    # Check if user is active
    if not payload.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive"
        )

    # Check role requirements
    if required_roles is not None:
        require_role(payload.role, required_roles)

    # Check scope requirements
    if required_scopes is not None:
        require_permissions(payload.scopes, required_scopes, require_all_scopes)

    return payload


# Utility for creating permission decorators
def _extract_bearer_token(request: Request) -> str | None:
    """Extract Bearer token from Authorization header.

    Args:
        request: FastAPI Request

    Returns:
        Token string or None if not present/invalid format.
    """
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def create_permission_validator(
    required_scopes: str | list[str] | None = None,
    required_roles: str | list[str] | None = None,
    require_all_scopes: bool = False,
) -> Callable[..., JWTPayload]:
    """
    Create a permission validator function.

    Args:
        required_scopes: Required scope(s)
        required_roles: Required role(s)
        require_all_scopes: If True, require all scopes

    Returns:
        function: Validator function that takes a token and returns payload
    """

    def validator(request: Request, token: str | None = None) -> JWTPayload:
        # Priority: explicit token param -> Authorization header -> query param 'token'
        found = (
            token or _extract_bearer_token(request) or request.query_params.get("token")
        )
        if not found:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing bearer token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return validate_token_and_permissions(
            found, required_scopes, required_roles, require_all_scopes
        )

    return validator


# Common permission validators
validate_admin = create_permission_validator(required_roles="admin")
validate_user_or_admin = create_permission_validator(required_roles=["user", "admin"])
validate_agent_read = create_permission_validator(required_scopes="agents:read")
validate_agent_write = create_permission_validator(required_scopes="agents:write")
validate_chat_access = create_permission_validator(
    required_scopes=["chat:read", "chat:create"]
)
validate_training_access = create_permission_validator(required_scopes="training:write")
