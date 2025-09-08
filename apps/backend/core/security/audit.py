"""Audit logging cho hệ thống phân quyền ZETA.

Module này ghi lại tất cả các quyết định phân quyền để:
- Compliance và regulatory requirements
- Security monitoring và forensics
- Performance tuning cho policy engine
- Debugging permission issues
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from apps.backend.core.security.context import SecurityContext
import allowed
import audit_data
import bool
import context
import created_by
import dict
import expires_at
import grant_id
import logger_name
import permission_name
import policy_name
import reason
import resource_id
import self
import str
import user_id
import violation_details

logger = logging.getLogger(__name__)


class AuditLogger:
    """Logger chuyên dụng cho audit events."""

    def __init__(self, logger_name: str = "security.audit") -> None:
        self.audit_logger = logging.getLogger(logger_name)

    def log_permission_check(
        self,
        context: SecurityContext,
        allowed: bool,
        reason: str,
    ) -> None:
        """Ghi log cho permission check.

        Args:
            context: SecurityContext được kiểm tra
            allowed: Kết quả cho phép hay không
            reason: Lý do quyết định
        """
        audit_data: dict[str, Any] = {
            "event_type": "permission_check",
            "timestamp": datetime.now(UTC).isoformat(),
            "decision": "ALLOW" if allowed else "DENY",
            "reason": reason,
            "user_id": context.subject.user_id,
            "tenant_id": context.subject.tenant_id,
            "roles": context.subject.roles,
            "action": context.action.name,
            "action_risk": context.action.risk,
            "resource_type": context.resource.type,
            "resource_id": context.resource.id,
            "resource_sensitivity": context.resource.sensitivity,
            "ip_address": context.environment.ip,
            "user_agent": context.environment.user_agent,
            "request_id": context.environment.request_id,
        }

        # Log với level khác nhau tùy theo decision
        if allowed:
            self.audit_logger.info("Permission granted", extra={"audit": audit_data})
        else:
            self.audit_logger.warning("Permission denied", extra={"audit": audit_data})

    def log_jit_grant_created(
        self,
        user_id: str,
        permission_name: str,
        reason: str,
        expires_at: datetime,
        created_by: str,
    ) -> None:
        """Ghi log khi tạo JIT grant."""
        audit_data: dict[str, Any] = {
            "event_type": "jit_grant_created",
            "timestamp": datetime.now(UTC).isoformat(),
            "user_id": user_id,
            "permission_name": permission_name,
            "reason": reason,
            "expires_at": expires_at.isoformat(),
            "created_by": created_by,
        }

        self.audit_logger.info("JIT grant created", extra={"audit": audit_data})

    def log_jit_grant_used(
        self,
        grant_id: str,
        user_id: str,
        permission_name: str,
        resource_id: str | None = None,
    ) -> None:
        """Ghi log khi sử dụng JIT grant."""
        audit_data: dict[str, Any] = {
            "event_type": "jit_grant_used",
            "timestamp": datetime.now(UTC).isoformat(),
            "grant_id": grant_id,
            "user_id": user_id,
            "permission_name": permission_name,
            "resource_id": resource_id,
        }

        self.audit_logger.info("JIT grant used", extra={"audit": audit_data})

    def log_policy_violation(
        self,
        context: SecurityContext,
        policy_name: str,
        violation_details: dict[str, Any],
    ) -> None:
        """Ghi log khi vi phạm policy."""
        audit_data: dict[str, Any] = {
            "event_type": "policy_violation",
            "timestamp": datetime.now(UTC).isoformat(),
            "user_id": context.subject.user_id,
            "action": context.action.name,
            "resource_type": context.resource.type,
            "resource_id": context.resource.id,
            "policy_name": policy_name,
            "violation_details": violation_details,
            "ip_address": context.environment.ip,
            "request_id": context.environment.request_id,
        }

        self.audit_logger.error("Policy violation", extra={"audit": audit_data})


# Global audit logger instance
_global_audit_logger: AuditLogger | None = None


def get_audit_logger() -> AuditLogger:
    """Lấy global audit logger instance."""
    if _global_audit_logger is None:
        return AuditLogger()
    return _global_audit_logger


def set_audit_logger(audit_logger: AuditLogger) -> None:
    """Đặt global audit logger instance."""
    global _global_audit_logger  # noqa: PLW0603
    _global_audit_logger = audit_logger


# Convenience functions
def audit_permission_check(
    context: SecurityContext,
    allowed: bool,
    reason: str,
) -> None:
    """Shortcut function để ghi audit log cho permission check."""
    audit_logger = get_audit_logger()
    audit_logger.log_permission_check(context, allowed, reason)


def audit_jit_grant_created(
    user_id: str,
    permission_name: str,
    reason: str,
    expires_at: datetime,
    created_by: str,
) -> None:
    """Shortcut function để ghi audit log cho JIT grant creation."""
    audit_logger = get_audit_logger()
    audit_logger.log_jit_grant_created(
        user_id, permission_name, reason, expires_at, created_by
    )


def audit_policy_violation(
    context: SecurityContext,
    policy_name: str,
    violation_details: dict[str, Any],
) -> None:
    """Shortcut function để ghi audit log cho policy violation."""
    audit_logger = get_audit_logger()
    audit_logger.log_policy_violation(context, policy_name, violation_details)
