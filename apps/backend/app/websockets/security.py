"""WebSocket security guard cho ZETA authorization system.

Module này cung cấp authentication và authorization cho WebSocket connections,
đồng nhất với HTTP security pipeline.
"""

from __future__ import annotations

import logging
from typing import Any

from app.startup.authorization import get_permission_manager
from apps.backend.core.security.context import (
import Exception
import action_name
import allowed
import bool
import dict
import e
import getattr
import hash
import permission
import reason
import resource_id
import resource_type
import self
import str
import user_agent
import websocket
    Action,
    Environment,
    Resource,
    SecurityContext,
    Subject,
)
from fastapi import WebSocket, WebSocketException, status

logger = logging.getLogger(__name__)


class WebSocketSecurityGuard:
    """Security guard cho WebSocket connections."""

    def __init__(self):
        self.permission_manager = get_permission_manager()

    async def authenticate_websocket(self, websocket: WebSocket) -> Subject:
        """Authenticate WebSocket connection và extract Subject.

        Args:
            websocket: WebSocket connection

        Returns:
            Subject object nếu authentication thành công

        Raises:
            WebSocketException: Nếu authentication thất bại
        """
        try:
            # Extract token từ query parameters hoặc headers
            token = self._extract_token(websocket)
            if not token:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Missing authentication token",
                )

            # Validate token và extract user info
            user_info = await self._validate_token(token)
            if not user_info:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Invalid authentication token",
                )

            # Create Subject
            subject = Subject(
                user_id=user_info["user_id"],
                tenant_id=user_info.get("tenant_id"),
                roles=user_info.get("roles", []),
                mfa_level=user_info.get("mfa_level", 0),
                session_id=user_info.get("session_id"),
                last_activity=None,  # Will be updated by middleware
            )

            return subject

        except WebSocketException:
            raise
        except Exception as e:
            logger.error(f"WebSocket authentication error: {e}")
            raise WebSocketException(
                code=status.WS_1011_INTERNAL_ERROR, reason="Authentication failed"
            )

    async def authorize_websocket_action(
        self,
        websocket: WebSocket,
        subject: Subject,
        action_name: str,
        resource_type: str = "websocket",
        resource_id: str | None = None,
    ) -> bool:
        """Authorize WebSocket action.

        Args:
            websocket: WebSocket connection
            subject: Authenticated subject
            action_name: Action được request
            resource_type: Loại resource
            resource_id: ID của resource

        Returns:
            True nếu được phép, False nếu không
        """
        try:
            # Build SecurityContext
            context = self._build_security_context(
                websocket, subject, action_name, resource_type, resource_id
            )

            # Check permission - sử dụng sync method
            allowed, reason = self.permission_manager.check_permission(
                context, action_name
            )

            if not allowed:
                logger.warning(
                    f"WebSocket action denied: {action_name} for user {subject.user_id}, reason: {reason}"
                )

            return allowed

        except Exception as e:
            logger.error(f"WebSocket authorization error: {e}")
            return False

    def _extract_token(self, websocket: WebSocket) -> str | None:
        """Extract authentication token từ WebSocket."""
        # Try query parameters first
        token = websocket.query_params.get("token")
        if token:
            return token

        # Try headers
        auth_header = websocket.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix

        return None

    async def _validate_token(self, token: str) -> dict[str, Any] | None:
        """Validate authentication token và extract user info.

        Args:
            token: JWT token

        Returns:
            User info dict nếu valid, None nếu invalid
        """
        # NOTE: Mock implementation - replace với JWT validation thực tế
        if not token or token == "invalid":
            return None

        # Mock user cho testing
        return {
            "user_id": "ws_user_123",
            "tenant_id": "tenant_abc",
            "roles": ["user"],
            "mfa_level": 1,
            "session_id": f"ws_session_{token[:8]}",
        }

    def _build_security_context(
        self,
        websocket: WebSocket,
        subject: Subject,
        action_name: str,
        resource_type: str,
        resource_id: str | None,
    ) -> SecurityContext:
        """Build SecurityContext cho WebSocket request."""

        # Extract client info
        client_host = (
            getattr(websocket.client, "host", "unknown")
            if websocket.client
            else "unknown"
        )
        websocket.headers.get("user-agent", "websocket-client")

        # Build components
        action = Action(
            name=action_name,
            risk="low",  # Default, sẽ được lookup trong permissions
            requires_mfa=False,
            rate_limit_key=f"ws:{client_host}:{action_name}",
        )

        resource = Resource(
            type=resource_type,
            id=resource_id or f"ws://{client_host}",
            sensitivity="internal",
            owner_id=subject.user_id,
            tenant_id=subject.tenant_id,
        )

        environment = Environment(
            ip=client_host,
            user_agent=user_agent,
            time_of_day=None,  # Will be set by policy engine
            device_trust="medium",  # WebSocket from web app
            location=None,
            is_vpn=False,
            request_id=f"ws_req_{hash(websocket)}",
        )

        return SecurityContext(
            subject=subject,
            action=action,
            resource=resource,
            environment=environment,
        )


# Global instance
_ws_guard: WebSocketSecurityGuard | None = None


def get_websocket_guard() -> WebSocketSecurityGuard:
    """Get global WebSocket security guard instance."""
    global _ws_guard  # noqa: PLW0603
    if _ws_guard is None:
        _ws_guard = WebSocketSecurityGuard()
    return _ws_guard


# Convenience functions cho WebSocket endpoints
async def ws_authenticate(websocket: WebSocket) -> Subject:
    """Authenticate WebSocket connection."""
    guard = get_websocket_guard()
    return await guard.authenticate_websocket(websocket)


async def ws_authorize(
    websocket: WebSocket,
    subject: Subject,
    action: str,
    resource_type: str = "websocket",
    resource_id: str | None = None,
) -> bool:
    """Authorize WebSocket action."""
    guard = get_websocket_guard()
    return await guard.authorize_websocket_action(
        websocket, subject, action, resource_type, resource_id
    )


async def ws_require_permission(
    websocket: WebSocket,
    subject: Subject,
    permission: str,
    resource_type: str = "websocket",
    resource_id: str | None = None,
) -> None:
    """Require permission cho WebSocket action, raise exception nếu denied.

    Args:
        websocket: WebSocket connection
        subject: Authenticated subject
        permission: Permission name
        resource_type: Loại resource
        resource_id: ID của resource

    Raises:
        WebSocketException: Nếu không có quyền
    """
    is_allowed = await ws_authorize(
        websocket, subject, permission, resource_type, resource_id
    )

    if not is_allowed:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason=f"Permission denied: {permission}",
        )
