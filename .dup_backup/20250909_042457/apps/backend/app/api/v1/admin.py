import Exception
import active
import audit
import bool
import cursor
import dict
import f
import getattr
import hasattr
import int
import isinstance
import key
import limit
import list
import me
import next_cursor
import object
import payload
import q
import r
import role
import str
import svc
import target_user_id
import tuple
import u
import user
import user_id
# zeta_vn/app/api/v1/admin.py
"""
Admin API (v1)
- Quản trị người dùng (CRUD, gán/bỏ vai trò), feature-flags, audit log, impersonate, stats.
- Router MỎNG: chỉ parse/validate + RBAC + DI, toàn bộ logic nằm ở Service/Use-case.
- RBAC scopes gợi ý:
    admin:*                           (quyền admin tổng)
    admin:users:read|write|delete
    admin:roles:read|write
    admin:flags:read|write|delete
    admin:audit:read
    admin:impersonate:run
    admin:stats:read

Phụ thuộc (DI) kỳ vọng có trong `zeta_vn.app.dependencies`:
    - require_permissions(scope: str)
    - get_current_user() -> User
    - get_admin_service() -> AdminService facade (hoặc SecurityManager + UserRepository gộp)
    - get_audit_service() -> AuditService

Schema kỳ vọng có trong `zeta_vn.app.serializers.admin`:
    - UserCreateIn, UserUpdateIn, UserOut
    - RoleAssignIn
    - FeatureFlagIn, FeatureFlagOut
    - AuditQuery, AuditRecord
    - PageCursor
    - (tuỳ chọn) UsersPage / FlagsPage ... nếu muốn response_model cụ thể

Service kỳ vọng:
    - AdminService (nếu chưa có, tạm dùng SecurityManager như facade) có các method:
        create_user(data) -> User
        get_user(user_id) -> User|None
        list_users(filters, cursor, limit) -> tuple[list[User], str|None]
        update_user(user_id, data) -> User
        delete_user(user_id) -> None
        assign_roles(user_id, roles: list[str]) -> User
        revoke_role(user_id, role: str) -> None
        list_roles() -> list[str]
        get_feature_flags() -> list[FeatureFlagOut] | list[dict]
        set_feature_flag(flag: FeatureFlagIn) -> FeatureFlagOut | dict
        delete_feature_flag(key: str) -> None
        impersonate(actor_id: str, target_user_id: str) -> str (JWT)
        get_stats() -> dict

    - AuditService:
        query(AuditQuery) -> list[AuditRecord]
"""

from __future__ import annotations

from typing import Annotated, Any, Protocol

from apps.backend.app.dependencies import get_admin_service, get_audit_service
from apps.backend.app.deps.auth import get_current_user, require_permissions
from apps.backend.app.serializers.admin import (
    AuditQuery,
    AuditRecord,
    FeatureFlagIn,
    FeatureFlagOut,
    PageCursor,
    RoleAssignIn,
    UserCreateIn,
    UserOut,
    UserUpdateIn,
)
from apps.backend.core.domain.entities.user import User
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel


# (tuỳ chọn) TokenOut: phục vụ impersonate
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminServiceProtocol(Protocol):
    async def create_user(self, data: dict[str, Any], **kwargs) -> object: ...

    async def get_user(self, user_id: str) -> object | None: ...

    async def list_users(
        self, filters: dict[str, Any], cursor: str | None, limit: int
    ) -> tuple[list[object], str | None]: ...

    async def update_user(self, user_id: str, data: dict[str, Any]) -> object: ...

    async def delete_user(self, user_id: str) -> None: ...

    async def assign_roles(self, user_id: str, roles: list[str]) -> object: ...

    async def revoke_role(self, user_id: str, role: str) -> None: ...

    async def list_roles(self) -> list[str]: ...

    async def get_feature_flags(
        self,
    ) -> list[FeatureFlagOut] | list[dict[str, Any]]: ...

    async def set_feature_flag(
        self, flag: dict[str, Any]
    ) -> FeatureFlagOut | dict[str, Any]: ...

    async def delete_feature_flag(self, key: str) -> None: ...

    async def impersonate(self, actor_id: str, target_user_id: str) -> str | None: ...

    async def get_stats(self) -> dict[str, Any]: ...


router = APIRouter(prefix="/admin", tags=["v1", "admin"])

Me = Annotated[User, Depends(get_current_user)]
AdminSvc = Annotated[AdminServiceProtocol, Depends(get_admin_service)]


class AuditServiceProtocol(Protocol):
    async def query(self, payload: AuditQuery) -> list[AuditRecord] | list[dict]: ...


AuditSvc = Annotated[AuditServiceProtocol, Depends(get_audit_service)]

# ---------------------------------------------------------------------
# Users Management
# ---------------------------------------------------------------------


@router.post(
    "/users",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("admin:users:write"))],
)
async def create_user(payload: UserCreateIn, svc: AdminSvc, me: Me) -> UserOut:
    """
    Tạo user mới.
    - RBAC: admin:users:write
    - Logic: uỷ quyền sang AdminService.create_user()
    """
    # mark "me" as used for audit/owner context
    _actor = str(getattr(me, "id", ""))
    _ = await svc.create_user(payload.model_dump(), actor_id=_actor)
    return (
        UserOut.from_entity(user)
        if hasattr(UserOut, "from_entity")
        else UserOut(**user)
    )  # type: ignore


@router.get(
    "/users/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(require_permissions("admin:users:read"))],
)
async def get_user(user_id: str, svc: AdminSvc, me: Me) -> UserOut:
    _ = me  # mark used
    _ = await svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return (
        UserOut.from_entity(user)
        if hasattr(UserOut, "from_entity")
        else UserOut(**user)
    )  # type: ignore


@router.get(
    "/users",
    dependencies=[Depends(require_permissions("admin:users:read"))],
)
async def list_users(
    svc: AdminSvc,
    me: Me,
    q: str | None = Query(default=None, description="free-text search"),
    role: str | None = Query(default=None, description="filter by role"),
    active: bool | None = Query(default=None, description="filter by active"),
    cursor: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    """
    Liệt kê người dùng với filter/pagination. Trả về dạng `{items, cursor}`.
    - RBAC: admin:users:read
    - Service trả `(items, next_cursor)`.
    """
    _ = me
    items, next_cursor = await svc.list_users(
        {"q": q, "role": role, "active": active}, cursor, limit
    )
    # Nếu có UsersPage model: return UsersPage(items=[...], cursor=PageCursor(next_cursor=...))
    if hasattr(UserOut, "from_entity"):
        items = [UserOut.from_entity(u) for u in items]  # type: ignore
    else:
        items = [UserOut(**u) for u in items]  # type: ignore
    return {"items": items, "cursor": PageCursor(next_cursor=next_cursor)}


@router.patch(
    "/users/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(require_permissions("admin:users:write"))],
)
async def update_user(
    user_id: str, payload: UserUpdateIn, svc: AdminSvc, me: Me
) -> UserOut:
    _ = me
    _ = await svc.update_user(user_id, payload.model_dump(exclude_unset=True))
    return (
        UserOut.from_entity(user)
        if hasattr(UserOut, "from_entity")
        else UserOut(**user)
    )  # type: ignore


@router.delete(
    "/users/{user_id}",
    response_class=Response,
    dependencies=[Depends(require_permissions("admin:users:delete"))],
)
async def delete_user(user_id: str, svc: AdminSvc, me: Me) -> None:
    _ = me
    await svc.delete_user(user_id)


# ---------------------------------------------------------------------
# Roles Management
# ---------------------------------------------------------------------


@router.get(
    "/roles",
    response_model=list[str],
    dependencies=[Depends(require_permissions("admin:roles:read"))],
)
async def list_roles(svc: AdminSvc, me: Me) -> list[str]:
    _ = me
    """Danh sách các role hiện có (RBAC)."""
    return await svc.list_roles()


@router.post(
    "/users/{user_id}/roles",
    response_model=UserOut,
    dependencies=[Depends(require_permissions("admin:roles:write"))],
)
async def assign_roles(
    user_id: str, payload: RoleAssignIn, svc: AdminSvc, me: Me
) -> UserOut:
    """
    Gán nhiều role cho user.
    RoleAssignIn: { roles: list[str] }
    """
    _ = me
    _ = await svc.assign_roles(user_id, list(payload.roles))
    return (
        UserOut.from_entity(user)
        if hasattr(UserOut, "from_entity")
        else UserOut(**user)
    )  # type: ignore


@router.delete(
    "/users/{user_id}/roles/{role}",
    response_class=Response,
    dependencies=[Depends(require_permissions("admin:roles:write"))],
)
async def revoke_role(user_id: str, role: str, svc: AdminSvc, me: Me) -> None:
    """Thu hồi 1 role khỏi user."""
    _ = me
    await svc.revoke_role(user_id, role)


# ---------------------------------------------------------------------
# Feature Flags
# ---------------------------------------------------------------------


@router.get(
    "/feature-flags",
    response_model=list[FeatureFlagOut],
    dependencies=[Depends(require_permissions("admin:flags:read"))],
)
async def list_feature_flags(svc: AdminSvc, me: Me) -> list[FeatureFlagOut]:
    _ = me
    flags = await svc.get_feature_flags()
    # Nếu service trả dict, Copilot sẽ map qua FeatureFlagOut(**x)
    if isinstance(flags, list) and flags and not isinstance(flags[0], FeatureFlagOut):
        return [FeatureFlagOut(**f) for f in flags]  # type: ignore
    return flags  # type: ignore


@router.post(
    "/feature-flags",
    response_model=FeatureFlagOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("admin:flags:write"))],
)
async def set_feature_flag(
    payload: FeatureFlagIn, svc: AdminSvc, me: Me
) -> FeatureFlagOut:
    _ = me
    flag = await svc.set_feature_flag(payload.model_dump())
    return FeatureFlagOut(**flag) if not isinstance(flag, FeatureFlagOut) else flag  # type: ignore


@router.delete(
    "/feature-flags/{key}",
    response_class=Response,
    dependencies=[Depends(require_permissions("admin:flags:delete"))],
)
async def delete_feature_flag(key: str, svc: AdminSvc, me: Me) -> None:
    _ = me
    await svc.delete_feature_flag(key)


# ---------------------------------------------------------------------
# Audit Log
# ---------------------------------------------------------------------


@router.post(
    "/audit",
    response_model=list[AuditRecord],
    dependencies=[Depends(require_permissions("admin:audit:read"))],
)
async def query_audit(
    payload: AuditQuery, audit: AuditSvc, me: Me
) -> list[AuditRecord]:
    """
    Truy vấn audit logs theo filter thời gian/actor/action/resource.
    """
    _ = me
    # Expect audit service facade to support `query` method
    records = await audit.query(payload)
    # Nếu AuditService trả dict list — Copilot sẽ map thành AuditRecord(**x)
    if records and not isinstance(records[0], AuditRecord):
        return [AuditRecord(**r) for r in records]  # type: ignore
    return records  # type: ignore


# ---------------------------------------------------------------------
# Impersonate & Stats
# ---------------------------------------------------------------------


@router.post(
    "/impersonate/{target_user_id}",
    response_model=TokenOut,
    dependencies=[Depends(require_permissions("admin:impersonate:run"))],
)
async def impersonate_user(target_user_id: str, svc: AdminSvc, me: Me) -> TokenOut:
    """
    Phát hành token impersonate để debug/hỗ trợ (ghi audit rõ actor->target).
    Cực kỳ nhạy cảm: RBAC bắt buộc 'admin:impersonate:run'.
    """
    token = await svc.impersonate(
        actor_id=str(getattr(me, "id", "")), target_user_id=target_user_id
    )
    if not token:
        raise HTTPException(status_code=400, detail="Cannot impersonate target")
    return TokenOut(access_token=token)


@router.get(
    "/stats",
    response_model=dict,
    dependencies=[Depends(require_permissions("admin:stats:read"))],
)
async def admin_stats(svc: AdminSvc, me: Me) -> dict:
    """
    Thống kê hệ thống cho dashboard quản trị (read-only).
    """
    _ = me
    return await svc.get_stats()


# Import optional sub-routers (e.g., updater) so they are included in the admin namespace
try:
    from apps.backend.app.api.v1.admin import updater as _updater_module

    if hasattr(_updater_module, "router"):
        router.include_router(_updater_module.router)
except Exception:
    # optional module; ignore errors to keep app startup robust
    pass
