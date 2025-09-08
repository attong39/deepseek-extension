"""Permission Manager for ZETA authorization system."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any, Protocol

from apps.backend.core.security.context import SecurityContext
from apps.backend.core.security.permissions import (
    DEFAULT_ROLE_PERMISSIONS,
    PERMISSIONS,
    get_permission_risk,
)

logger = logging.getLogger(__name__)


class JITGrantRepository(Protocol):
    """Interface cho JIT Grant Repository."""
import Exception
import allowed
import audit_enabled
import bool
import context
import dict
import e
import getattr
import jit_repo
import permission_name
import role
import self
import set
import str
import tuple

    def find_valid_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
        now: datetime | None = None,
    ) -> dict[str, Any] | None:
        """Find valid JIT grant."""
        ...


class PermissionManager:
    """Central permission manager với DI và deny-by-default policy."""

    def __init__(
        self, jit_repo: JITGrantRepository | None = None, audit_enabled: bool = True
    ) -> None:
        """Initialize permission manager.

        Args:
            jit_repo: JIT Grant repository để check JIT grants
            audit_enabled: Enable audit logging
        """
        self._jit_repo = jit_repo
        self._audit_enabled = audit_enabled

    def check_permission(
        self,
        context: SecurityContext,
        permission_name: str,
    ) -> tuple[bool, str]:
        """Check permission với security context.

        Args:
            context: Security context
            permission_name: Tên permission cần kiểm tra

        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        try:
            # 0. Deny-by-default - kiểm tra permission có được đăng ký không
            if permission_name not in PERMISSIONS:
                reason = f"unknown_permission: {permission_name}"
                if self._audit_enabled:
                    logger.warning(f"Permission denied: {reason}")
                return False, reason

            # 1. RBAC check - convert roles to permissions first
            user_permissions = set()
            for role in context.subject.roles:
                role_perms = DEFAULT_ROLE_PERMISSIONS.get(role, [])
                user_permissions.update(role_perms)

            # Add direct permissions if any
            user_permissions.update(getattr(context.subject, "permissions", []))

            # Check if user has this permission
            if permission_name not in user_permissions:
                reason = f"rbac_denied: {permission_name}"
                if self._audit_enabled:
                    logger.warning(f"Permission denied: {reason}")
                return False, reason

            # 2. ABAC checks - tenant isolation
            if context.resource and context.resource.tenant_id:
                if context.subject.tenant_id != context.resource.tenant_id:
                    reason = "tenant_isolation: access denied to resource from different tenant"
                    if self._audit_enabled:
                        logger.warning(f"Permission denied: {reason}")
                    return False, reason

            # 3. Risk gates - JIT check for high/critical permissions
            risk = get_permission_risk(permission_name)
            if risk in ["high", "critical"] and self._jit_repo:
                grant = self._jit_repo.find_valid_grant(
                    user_id=context.subject.user_id,
                    permission=permission_name,
                    resource_id=context.resource.id if context.resource else None,
                    now=datetime.now(UTC),
                )
                if grant is None:
                    reason = f"jit_required: {permission_name} requires JIT grant"
                    if self._audit_enabled:
                        logger.warning(f"Permission denied: {reason}")
                    return False, reason

            # All checks passed
            reason = f"allowed: {permission_name}"
            if self._audit_enabled:
                logger.info(f"Permission granted: {permission_name}")

            return True, reason

        except Exception as e:
            reason = f"error: {str(e)}"
            logger.error(f"Permission check error: {e}")
            return False, reason

    def ensure_permission(
        self,
        context: SecurityContext,
        permission_name: str,
    ) -> None:
        """Check permission and raise exception if denied."""
        allowed, reason = self.check_permission(context, permission_name)
        if not allowed:
            raise PermissionDeniedError(f"Access denied: {reason}")


class PermissionDeniedError(Exception):
    """Exception for permission denied cases."""
