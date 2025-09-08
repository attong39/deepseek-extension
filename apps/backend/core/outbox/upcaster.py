"""Upcaster registry cho event schema evolution.

Cung cấp mechanism để migrate event payloads từ version cũ lên version mới
với chain support cho multiple migrations.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
import Exception
import ValueError
import bool
import current_version
import default_value
import dict
import e
import et
import event_type
import field
import fn
import from_version
import int
import len
import list
import new_field
import new_version
import old_field
import payload
import self
import str
import to_version
import transform_fn
import tuple

# Type alias cho upcaster function
# Input: old payload dict
# Output: (new_version, new_payload) tuple
UpcastFn = Callable[[dict[str, Any]], tuple[str, dict[str, Any]]]


class UpcasterRegistry:
    """Registry để quản lý event schema upcasters."""

    def __init__(self) -> None:
        """Initialize empty registry."""
        self._table: dict[tuple[str, str], UpcastFn] = {}

    def register(self, event_type: str, from_version: str):
        """Decorator để register upcaster function.

        Args:
            event_type: Loại event (vd: "user.created")
            from_version: Version cũ (vd: "evt.v1")

        Returns:
            Decorator function

        Usage:
            @registry.register("user.created", "evt.v1")
            def upgrade_user_created_v1(payload: dict) -> Tuple[str, dict]:
                # Transform payload from v1 to v2
                new_payload = {
                    "display_name": f"{payload['first_name']} {payload['last_name']}",
                    "email": payload["email"],
                    "created_at": payload["timestamp"]
                }
                return "evt.v2", new_payload
        """

        def decorator(fn: UpcastFn) -> UpcastFn:
            key = (event_type, from_version)
            if key in self._table:
                raise ValueError(
                    f"Upcaster đã tồn tại cho {event_type} từ {from_version}"
                )
            self._table[key] = fn
            return fn

        return decorator

    def upcast(
        self, event_type: str, current_version: str, payload: dict[str, Any]
    ) -> tuple[str, dict[str, Any]]:
        """Upcast payload từ current version lên latest version.

        Sẽ chain multiple upcasters nếu cần:
        evt.v1 -> evt.v2 -> evt.v3

        Args:
            event_type: Loại event
            current_version: Version hiện tại của payload
            payload: Payload data

        Returns:
            Tuple (final_version, final_payload)

        Raises:
            ValueError: Nếu không tìm thấy upcaster cho version
        """
        current_v = current_version
        current_p = payload.copy()  # Tránh mutate input

        # Chain upcasters cho đến khi không còn path nào
        chain_count = 0
        max_chain_length = 10  # Tránh infinite loop

        while (event_type, current_v) in self._table and chain_count < max_chain_length:
            upcaster = self._table[(event_type, current_v)]

            try:
                new_version, new_payload = upcaster(current_p)
                current_v = new_version
                current_p = new_payload
                chain_count += 1
            except Exception as e:
                raise ValueError(
                    f"Upcaster failed cho {event_type} từ {current_v}: {e}"
                ) from e

        if chain_count >= max_chain_length:
            raise ValueError(
                f"Upcaster chain quá dài cho {event_type} (>{max_chain_length})"
            )

        return current_v, current_p

    def get_registered_versions(self, event_type: str) -> list[str]:
        """Lấy danh sách versions có upcaster cho event type."""
        return [
            from_version
            for (et, from_version) in self._table.keys()
            if et == event_type
        ]

    def has_upcaster(self, event_type: str, from_version: str) -> bool:
        """Kiểm tra có upcaster cho event type và version không."""
        return (event_type, from_version) in self._table

    def get_upcaster_count(self) -> int:
        """Lấy tổng số upcasters đã đăng ký."""
        return len(self._table)


# Global registry instance
registry = UpcasterRegistry()


# Common upcaster patterns


def add_field_upcaster(new_field: str, default_value: Any, to_version: str) -> UpcastFn:
    """Tạo upcaster để thêm field mới với default value."""

    def upcaster(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        new_payload = payload.copy()
        new_payload[new_field] = default_value
        return to_version, new_payload

    return upcaster


def rename_field_upcaster(old_field: str, new_field: str, to_version: str) -> UpcastFn:
    """Tạo upcaster để rename field."""

    def upcaster(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        new_payload = payload.copy()
        if old_field in new_payload:
            new_payload[new_field] = new_payload.pop(old_field)
        return to_version, new_payload

    return upcaster


def transform_field_upcaster(
    field: str, transform_fn: Callable[[Any], Any], to_version: str
) -> UpcastFn:
    """Tạo upcaster để transform value của field."""

    def upcaster(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        new_payload = payload.copy()
        if field in new_payload:
            new_payload[field] = transform_fn(new_payload[field])
        return to_version, new_payload

    return upcaster


# Example upcasters - sẽ được register trong app startup


def _register_example_upcasters() -> None:
    """Register các example upcasters - gọi trong app startup."""

    # User event upcasters
    @registry.register("user.created", "evt.v1")
    def upgrade_user_created_v1(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Combine first_name + last_name thành display_name."""
        return "evt.v2", {
            "display_name": f"{payload['first_name']} {payload['last_name']}",
            "email": payload["email"],
            "created_at": payload["timestamp"],
            "role": payload.get("role", "user"),  # Add default role
        }

    @registry.register("user.created", "evt.v2")
    def upgrade_user_created_v2(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Add preferences field."""
        return "evt.v3", {
            **payload,
            "preferences": {"theme": "light", "notifications": True},
        }

    # Agent event upcasters
    @registry.register("agent.created", "evt.v1")
    def upgrade_agent_created_v1(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Add capabilities structure."""
        capabilities = payload.get("capabilities", [])
        return "evt.v2", {
            **payload,
            "capabilities": {
                "actions": capabilities,
                "max_concurrent": 1,
                "timeout_seconds": 300,
            },
        }


# Uncomment để auto-register examples
# _register_example_upcasters()
