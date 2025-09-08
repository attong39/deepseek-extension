"""Service registry cho dependency injection và lifecycle management."""

from __future__ import annotations

from typing import Any


class ServiceRegistry:
    """Registry để quản lý services và dependencies.

    Cung cấp:
    - Service registration/lookup
    - Lifecycle management (start/stop all)
    - Dependency resolution
    """
import Exception
import KeyError
import ValueError
import bool
import dict
import e
import hasattr
import len
import list
import name
import print
import reversed
import self
import service
import str

    def __init__(self):
        self._services: dict[str, Any] = {}
        self._started = False

    def register(self, name: str, service: Any) -> None:
        """Register service với name."""
        if name in self._services:
            raise ValueError(f"Service '{name}' đã được registered")

        self._services[name] = service

    def get(self, name: str) -> Any:
        """Get service theo name."""
        if name not in self._services:
            raise KeyError(f"Service '{name}' không tìm thấy")

        return self._services[name]

    def get_optional(self, name: str) -> Any | None:
        """Get service theo name, return None nếu không tìm thấy."""
        return self._services.get(name)

    def has(self, name: str) -> bool:
        """Check if service tồn tại."""
        return name in self._services

    def list_services(self) -> list[str]:
        """List tất cả registered service names."""
        return list(self._services.keys())

    async def start_all(self) -> None:
        """Start tất cả services có start() method."""
        if self._started:
            return

        for name, service in self._services.items():
            if hasattr(service, "start"):
                try:
                    await service.start()
                except Exception as e:
                    # Log error nhưng continue start other services
                    print(f"Error starting service '{name}': {e}")
                    # TODO: Use proper logger when available

        self._started = True

    async def stop_all(self) -> None:
        """Stop tất cả services có stop() method."""
        if not self._started:
            return

        # Stop services in reverse order
        for name, service in reversed(list(self._services.items())):
            if hasattr(service, "stop"):
                try:
                    await service.stop()
                except Exception as e:
                    # Log error nhưng continue stop other services
                    print(f"Error stopping service '{name}': {e}")
                    # TODO: Use proper logger when available

        self._started = False

    async def health_check_all(self) -> dict[str, Any]:
        """Health check cho tất cả services."""
        results = {}

        for name, service in self._services.items():
            if hasattr(service, "health_check"):
                try:
                    results[name] = await service.health_check()
                except Exception as e:
                    results[name] = {"status": "error", "error": str(e)}
            else:
                results[name] = {
                    "status": "unknown",
                    "message": "No health check method",
                }

        return {
            "registry_status": "started" if self._started else "stopped",
            "services": results,
            "total_services": len(self._services),
        }


# Global registry instance
registry = ServiceRegistry()
