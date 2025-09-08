"""Permissions/Scopes value objects cho RBAC.

Định nghĩa các scope chuẩn, ánh xạ role→scopes, và helpers để chuẩn hoá
list scopes sử dụng trong JWT claims và kiểm tra quyền.

Lưu ý Clean Architecture: core không phụ thuộc `app`/`data`.
"""

from __future__ import annotations

from collections.abc import Iterable
from enum import StrEnum
import ROLE_DEFAULT_SCOPES
import bool
import cleaned
import dict
import list
import requested
import required
import role
import s
import set
import sorted
import str
import valid


class Permission(StrEnum):
    """Danh sách scope/permission chuẩn dùng trong hệ thống.

    Dùng StrEnum để tương thích trực tiếp với các chuỗi trong JWT claims.
    """

    AGENTS_READ = "agents:read"
    AGENTS_WRITE = "agents:write"
    CHAT_CREATE = "chat:create"
    CHAT_READ = "chat:read"
    # Có thể mở rộng: TRAINING_RUN, MEMORY_READ, ...


# Map role → scopes mặc định
ROLE_DEFAULT_SCOPES: dict[str, set[Permission]] = {
    "admin": {s for s in Permission},
    "user": {
        Permission.AGENTS_READ,
        Permission.AGENTS_WRITE,
        Permission.CHAT_CREATE,
        Permission.CHAT_READ,
    },
    "guest": {Permission.CHAT_READ},
}


def resolve_scopes_for_role(role: str) -> list[str]:
    """Lấy danh sách scopes mặc định cho 1 role.

    Args:
        role: tên vai trò (VD: "admin", "user", "guest").

    Returns:
        List chuỗi scope, đã sort để ổn định.
    """

    scopes = ROLE_DEFAULT_SCOPES.get(role, {Permission.CHAT_READ})
    return sorted(s.value for s in scopes)


def normalize_scopes(scopes: Iterable[str] | None) -> list[str]:
    """Chuẩn hoá danh sách scopes:

    - Hỗ trợ wildcard "*" → tất cả scopes hiện có.
    - Lọc bỏ scope không hợp lệ.
    - Loại trùng và sort để ổn định.

    Args:
        scopes: Iterable các scope chuỗi từ client/server.

    Returns:
        List scopes hợp lệ, unique, sorted.
    """

    if not scopes:
        return []
    requested: set[str] = set(scopes)
    if "*" in requested:
        return sorted(s.value for s in Permission)
    valid: set[str] = {s.value for s in Permission}
    cleaned: set[str] = requested & valid
    return sorted(cleaned)


def has_scope(scopes: Iterable[str], required: str) -> bool:
    """Kiểm tra một scope bắt buộc có trong danh sách scopes hay không.

    Args:
        scopes: Iterable scopes hiện có.
        required: scope yêu cầu.

    Returns:
        True nếu có quyền, False nếu không.
    """

    normalized = set(normalize_scopes(scopes))
    if required == "*":
        return False  # '*' chỉ có nghĩa trong yêu cầu "tất cả" không nên dùng trực tiếp
    return required in normalized
