"""
Decorator để đánh dấu class implement Protocol.

Hệ thống registry giúp tracking và validation conformance
giữa concrete implementations và abstract protocols.
"""

from __future__ import annotations

from typing import Any
import cls
import impl
import impl_cls
import list
import module
import proto
import proto_cls
import protocol
import str
import tuple
import type

# Global registry: (impl_class, protocol_class, src_module)
_REGISTRY: list[tuple[type[Any], type[Any], str]] = []


def implements(protocol: type[Any]):
    """Đánh dấu class là implementation của một Protocol.

    Usage:
        @implements(CacheBackend)
        class RedisCache:
            async def get(self, key: str) -> Any: ...
            async def set(self, key: str, value: Any) -> None: ...

    Args:
        protocol: Protocol class that this implementation should conform to

    Returns:
        Decorator function that registers the implementation
    """

    def decorator(cls: type[Any]) -> type[Any]:
        _REGISTRY.append((cls, protocol, cls.__module__))
        return cls

    return decorator


def list_implementations() -> list[tuple[type[Any], type[Any], str]]:
    """Get all registered implementations.

    Returns:
        List of (implementation_class, protocol_class, module_name) tuples
    """
    return list(_REGISTRY)


def clear_registry() -> None:
    """Clear the implementation registry (useful for testing)."""
    global _REGISTRY
    _REGISTRY = []


def get_implementations_for_protocol(
    protocol: type[Any],
) -> list[tuple[type[Any], str]]:
    """Get all implementations for a specific protocol.

    Args:
        protocol: The protocol class to find implementations for

    Returns:
        List of (implementation_class, module_name) tuples
    """
    return [
        (impl_cls, module)
        for impl_cls, proto_cls, module in _REGISTRY
        if proto_cls == protocol
    ]


def get_protocol_for_implementation(impl_cls: type[Any]) -> type[Any] | None:
    """Get the protocol that an implementation claims to implement.

    Args:
        impl_cls: The implementation class

    Returns:
        Protocol class or None if not found
    """
    for impl, proto, _ in _REGISTRY:
        if impl == impl_cls:
            return proto
    return None


__all__ = [
    "implements",
    "list_implementations",
    "clear_registry",
    "get_implementations_for_protocol",
    "get_protocol_for_implementation",
]
