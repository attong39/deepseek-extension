"""Policy Engine cho hệ thống phân quyền ZETA - Production Ready.

Module này thực hiện quyết định phân quyền theo mô hình nhiều lớp:
1. Safety rules (deny-by-default cho hành động rủi ro)
2. RBAC (role-based permissions)
3. ABAC (attribute-based: tenant, ownership, sensitivity)
4. Risk gates + JIT grants
5. Rate limiting

Có thể thay thế bằng OPA/Casbin mà không đổi interface.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Protocol

from apps.backend.core.security.context import SecurityContext
from apps.backend.core.security.permissions import (
import abac_result
import any
import bool
import ctx
import dict
import int
import jit_repo
import list
import permission
import rate_limit_result
import rbac_result
import reason
import requires_mfa
import resource_id
import risk_result
import role
import roles
import safety_result
import self
import set
import str
import tuple
import user_id
import user_permissions
    DEFAULT_ROLE_PERMS,
    PERMISSIONS,
    get_permission_risk,
)


class JITGrantRepository(Protocol):
    """Interface cho repository quản lý JIT grants."""

    def find_valid_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
        now: datetime | None = None,
    ) -> dict[str, Any] | None:
        """Tìm JIT grant hợp lệ cho user."""
        ...

    def create_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
        reason: str = "",
        expires_in_minutes: int = 15,
        requires_mfa: bool = True,
    ) -> dict[str, Any]:
        """Tạo JIT grant mới."""
        ...


class PolicyEngine(Protocol):
    """Protocol cho Policy Engine để đưa ra quyết định phân quyền."""

    def decide(self, ctx: SecurityContext) -> tuple[bool, str]:
        """Đưa ra quyết định allow/deny cho một SecurityContext."""
        ...


class InlinePolicyEngine:
    """Policy Engine inline không phụ thuộc dịch vụ ngoài.

    Thực hiện quyết định theo thứ tự:
    1. Safety rules → 2. RBAC → 3. ABAC → 4. Risk gates → 5. Rate limits
    """

    def __init__(self, jit_repo: JITGrantRepository | None = None):
        """Initialize policy engine.

        Args:
            jit_repo: Repository cho JIT grants (optional)
        """
        self.jit_repo = jit_repo

    def decide(self, ctx: SecurityContext) -> tuple[bool, str]:
        """Đưa ra quyết định phân quyền theo pipeline nhiều lớp."""

        # 0. Deny-by-default - kiểm tra action có được đăng ký không
        if ctx.action.name not in PERMISSIONS:
            return (False, f"unknown_action: {ctx.action.name}")

        # 1. Safety rules - luôn kiểm tra đầu tiên
        self._check_safety_rules(ctx)
        if not safety_result[0]:
            return safety_result

        # 2. RBAC - kiểm tra role có permission không
        self._check_rbac(ctx)
        if not rbac_result[0]:
            return rbac_result

        # 3. ABAC - kiểm tra attributes (tenant, ownership, sensitivity)
        self._check_abac(ctx)
        if not abac_result[0]:
            return abac_result

        # 4. Risk gates - JIT grants cho high-risk actions
        self._check_risk_gates(ctx)
        if not risk_result[0]:
            return risk_result

        # 5. Rate limiting rules (placeholder)
        self._check_rate_limits(ctx)
        if not rate_limit_result[0]:
            return rate_limit_result

        return (True, "allow")

    def _check_safety_rules(self, ctx: SecurityContext) -> tuple[bool, str]:
        """Kiểm tra safety rules cứng - deny-by-default cho critical actions."""

        # Chặn xóa dữ liệu restricted/secret
        if ctx.action.name in [
            "files:delete",
            "memory:purge",
            "training:delete",
        ] and ctx.resource.sensitivity in ["restricted", "secret"]:
            return (False, "safety_blocked_sensitive_data")

        # Chặn operations critical ngoài giờ làm việc (8-18h)
        if (
            ctx.action.risk == "critical"
            and ctx.environment.time_of_day is not None
            and not (8 <= ctx.environment.time_of_day <= 18)
            and "emergency" not in ctx.action.context
        ):
            return (False, "safety_blocked_off_hours")

        # Chặn operations từ thiết bị không tin cậy
        if (
            ctx.action.risk in ["high", "critical"]
            and ctx.environment.device_trust == "low"
        ):
            return (False, "safety_blocked_untrusted_device")

        # Yêu cầu MFA cho critical operations
        if ctx.action.risk == "critical" and ctx.subject.mfa_level < 2:
            return (False, "safety_requires_strong_mfa")

        return (True, "safety_passed")

    def _check_rbac(self, ctx: SecurityContext) -> tuple[bool, str]:
        """Kiểm tra role-based access control."""

        # Lấy tất cả permissions từ roles của user
        user_permissions: set[str] = set()
        for role in ctx.subject.roles:
            role_perms = DEFAULT_ROLE_PERMS.get(role, [])
            user_permissions.update(role_perms)

        # Thêm permissions trực tiếp (JIT grants)
        user_permissions.update(ctx.subject.permissions)

        # Kiểm tra permission cần thiết
        if ctx.action.name not in user_permissions:
            return (False, f"rbac_denied_missing_permission_{ctx.action.name}")

        return (True, "rbac_passed")

    def _check_abac(self, ctx: SecurityContext) -> tuple[bool, str]:
        """Kiểm tra attribute-based access control."""

        # Kiểm tra tenant isolation
        if (
            ctx.resource.tenant_id
            and ctx.subject.tenant_id
            and ctx.resource.tenant_id != ctx.subject.tenant_id
        ):
            return (False, "abac_tenant_mismatch")

        # Kiểm tra ownership cho resource cá nhân
        if (
            ctx.resource.owner_id
            and ctx.resource.owner_id != ctx.subject.user_id
            and not self._has_admin_override(ctx.subject.roles)
        ):
            return (False, "abac_ownership_denied")

        # Kiểm tra sensitivity level vs user clearance
        if ctx.resource.sensitivity == "secret" and not self._has_secret_clearance(
            ctx.subject.roles
        ):
            return (False, "abac_insufficient_clearance")

        return (True, "abac_passed")

    def _check_risk_gates(self, ctx: SecurityContext) -> tuple[bool, str]:
        """Kiểm tra risk gates và JIT grants cho high-risk actions."""

        risk = get_permission_risk(ctx.action.name)

        # High/critical risk actions cần JIT grant
        if risk in ["high", "critical"] and self.jit_repo:
            grant = self.jit_repo.find_valid_grant(
                user_id=ctx.subject.user_id,
                permission=ctx.action.name,
                resource_id=ctx.resource.id,
                now=datetime.now(UTC),
            )

            if grant is None:
                return (False, f"risk_gate_jit_required_{risk}")

        return (True, "risk_gate_passed")

    def _check_rate_limits(self, ctx: SecurityContext) -> tuple[bool, str]:
        """Kiểm tra rate limiting rules."""
        # TODO: Implement rate limiting với Redis
        return (True, "rate_limit_passed")

    def _has_admin_override(self, roles: list[str]) -> bool:
        """Kiểm tra user có quyền admin để override ownership."""
        return any(role in ["admin", "superadmin", "power_user"] for role in roles)

    def _has_secret_clearance(self, roles: list[str]) -> bool:
        """Kiểm tra user có clearance để truy cập dữ liệu secret."""
        return any(role in ["admin", "superadmin"] for role in roles)


class MockJITGrantRepository:
    """Mock implementation cho testing."""

    def __init__(self):
        self.grants: dict[str, dict[str, Any]] = {}

    def find_valid_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
        now: datetime | None = None,
    ) -> dict[str, Any] | None:
        """Mock implementation - return None (no grants)."""
        return None

    def create_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
        reason: str = "",
        expires_in_minutes: int = 15,
        requires_mfa: bool = True,
    ) -> dict[str, Any]:
        """Mock implementation."""
        grant_id = f"{user_id}_{permission}_{resource_id or 'global'}"
        grant: dict[str, Any] = {
            "id": grant_id,
            "user_id": user_id,
            "permission": permission,
            "resource_id": resource_id,
            "reason": reason,
            "expires_at": datetime.now(UTC),
            "requires_mfa": requires_mfa,
        }
        self.grants[grant_id] = grant
        return grant
