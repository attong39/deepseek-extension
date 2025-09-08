"""Permission manager located in security layer.

This module provides the PermissionManager wrapper which delegates to the
low-level RBAC implementation. Placing it under `security/` keeps the
cross-cutting authorization concern separate from service implementations.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.core.security.authorization.rbac import AccessControlManager
import Exception
import PermissionError
import acm
import action
import allowed
import bool
import dict
import hasattr
import pid
import resource
import scope
import self
import str
import user

logger = logging.getLogger(__name__)


class PermissionManager:
    """Thin wrapper trên AccessControlManager để dùng trong use-cases.

    Methods
    -------
    has_scope(user, scope) -> bool
    require_scope(user, scope) -> None | raises PermissionError
    audit_decision(user, resource, action, allowed) -> None
    """

    def __init__(self, acm: AccessControlManager | None = None) -> None:
        self._acm = acm or AccessControlManager()

    def has_scope(self, user: dict[str, Any] | None, scope: str) -> bool:
        """Return True if user has a coarse-grained scope/permission.

        Args:
            user: dict containing at least 'id' or 'sub'.
            scope: scope string, e.g. 'automation:plan:create'
        """
        if not user:
            return False
        user_id = user.get("id") or user.get("sub")
        if not user_id:
            return False
        try:
            # call check_permission in a permissive way; exact signature may vary
            decision = self._acm.check_permission(user_id)  # type: ignore[arg-type]
            for pid in (
                decision.applied_permissions
                if hasattr(decision, "applied_permissions")
                else []
            ):
                if scope in str(pid):
                    return True
        except Exception:
            logger.debug("RBAC unavailable, denying scope check")
            return False
        return False

    def require_scope(self, user: dict[str, Any] | None, scope: str) -> None:
        """Raise PermissionError if user lacks scope."""
        if not self.has_scope(user, scope):
            logger.info("Permission denied for user %s on scope %s", user, scope)
            raise PermissionError(f"Missing required scope: {scope}")

    def audit_decision(
        self, user: dict[str, Any] | None, resource: str, action: str, allowed: bool
    ) -> None:
        uid = (user.get("id") or user.get("sub")) if user else "anonymous"
        logger.info(
            "audit: user=%s resource=%s action=%s allowed=%s",
            uid,
            resource,
            action,
            allowed,
        )
