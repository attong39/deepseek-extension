"""SQLAlchemy models cho hệ thống phân quyền.

Models này định nghĩa cấu trúc bảng và relationships cho RBAC/ABAC system.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from apps.backend.data.models.base import Base, TimestampMixin
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import bool
import dict
import self
import str


class Role(Base, TimestampMixin):
    """Model cho bảng roles - định nghĩa các vai trò trong hệ thống."""

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="system")
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[str | None] = mapped_column(String(36))

    # Relationships
    permissions = relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )
    user_roles = relationship("UserRole", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role(name={self.name}, scope={self.scope})>"


class Permission(Base):
    """Model cho bảng permissions - định nghĩa quyền hạn cụ thể."""

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    domain: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(10), nullable=False, default="low")
    requires_mfa: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    roles = relationship(
        "Role", secondary="role_permissions", back_populates="permissions"
    )

    def __repr__(self) -> str:
        return f"<Permission(name={self.name}, risk={self.risk_level})>"


class RolePermission(Base):
    """Model cho bảng role_permissions - mapping giữa role và permission."""

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id"), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey("permission.id"), primary_key=True
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    granted_by: Mapped[str | None] = mapped_column(String(36))

    def __repr__(self) -> str:
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"


class UserRole(Base):
    """Model cho bảng user_roles - gán vai trò cho user theo context."""

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, primary_key=True)
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("role.id"), nullable=False, primary_key=True
    )
    tenant_id: Mapped[str | None] = mapped_column(String(36), primary_key=True)
    project_id: Mapped[str | None] = mapped_column(String(36), primary_key=True)
    workspace_id: Mapped[str | None] = mapped_column(String(36), primary_key=True)
    scope_data: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    granted_by: Mapped[str | None] = mapped_column(String(36))

    # Relationships
    role = relationship("Role", back_populates="user_roles")

    def __repr__(self) -> str:
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"


class JITGrant(Base, TimestampMixin):
    """Model cho bảng jit_grants - Just-In-Time grants cho hành động nhạy cảm."""

    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    permission_name: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str | None] = mapped_column(String(50))
    resource_id: Mapped[str | None] = mapped_column(String(36))
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    mfa_required: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=False)
    approved_by: Mapped[str | None] = mapped_column(String(36))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    def is_valid(self) -> bool:
        """Kiểm tra grant có còn hiệu lực không."""
        now = datetime.now(UTC)
        return (
            self.is_active
            and self.expires_at > now
            and (not self.approval_required or self.approved_at is not None)
            and (not self.mfa_required or self.mfa_verified)
        )

    def mark_used(self) -> None:
        """Đánh dấu grant đã được sử dụng."""
        self.used_at = datetime.now(UTC)

    def __repr__(self) -> str:
        return f"<JITGrant(user_id={self.user_id}, permission={self.permission_name})>"


class AuditEvent(Base):
    """Model cho bảng audit_events - ghi lại mọi quyết định phân quyền."""

    user_id: Mapped[str | None] = mapped_column(String(36))
    tenant_id: Mapped[str | None] = mapped_column(String(36))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str | None] = mapped_column(String(50))
    resource_id: Mapped[str | None] = mapped_column(String(36))
    decision: Mapped[str] = mapped_column(String(20), nullable=False)  # allow, deny
    reason: Mapped[str | None] = mapped_column(String(100))
    risk_level: Mapped[str | None] = mapped_column(String(10))
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(Text)
    session_id: Mapped[str | None] = mapped_column(String(36))
    request_id: Mapped[str | None] = mapped_column(String(36))
    context_data: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<AuditEvent(action={self.action}, decision={self.decision})>"
