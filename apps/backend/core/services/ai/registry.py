"""AI Capability Registry - Service discovery and management for AI capabilities.

Provides centralized registration, discovery, and health monitoring of AI
capabilities across the application. Supports dynamic capability loading
and runtime service management.

Includes simple registry for One-Click Learning.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from apps.backend.core.observability.logging import get_logger
import Exception
import ValueError
import any
import available_only
import bool
import c
import dep
import dependencies
import description
import dict
import e
import event_type
import float
import handler
import health_check_interval
import include_description
import include_tags
import item
import len
import list
import max
import metadata
import name
import property
import query
import self
import service_name
import status
import str
import sum
import tag
import tags
import version

logger = get_logger(__name__)


# === Simple Registry for One-Click Learning ===


class Registry:
    """Simple service registry for plugins and components."""

    def __init__(self):
        self._items: dict[str, Any] = {}

    def register(self, name: str, item: Any) -> None:
        """Register a service or component."""
        if name in self._items:
            raise ValueError(f"Duplicate registry key: {name}")
        self._items[name] = item

    def get(self, name: str) -> Any:
        """Get a registered service or component."""
        return self._items[name]


registry = Registry()


# === Existing Complex Registry (Backwards Compatibility) ===


class CapabilityStatus(Enum):
    """Capability status enumeration."""

    REGISTERED = "registered"
    INITIALIZING = "initializing"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"
    DEPRECATED = "deprecated"


@dataclass
class CapabilityInfo:
    """Information about a registered capability."""

    name: str
    description: str
    version: str
    service_name: str
    status: CapabilityStatus
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    last_health_check: datetime | None = None
    health_status: bool = False
    dependencies: list[str] = field(default_factory=list)

    @property
    def is_available(self) -> bool:
        """Check if capability is available for use."""
        return self.status == CapabilityStatus.AVAILABLE and self.health_status


@runtime_checkable
class CapabilityProvider(Protocol):
    """Protocol for capability providers."""

    @property
    def capability_name(self) -> str:
        """Name of the capability."""
        ...

    @property
    def capability_version(self) -> str:
        """Version of the capability."""
        ...

    async def initialize(self) -> None:
        """Initialize the capability."""
        ...

    async def health_check(self) -> bool:
        """Perform health check."""
        ...

    async def shutdown(self) -> None:
        """Shutdown the capability."""
        ...


@dataclass
class HealthCheckResult:
    """Result of a health check operation."""

    capability_name: str
    healthy: bool
    response_time_ms: float
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class AICapabilityRegistry:
    """
    Registry for AI capabilities with service discovery and health monitoring.

    Manages registration, discovery, and lifecycle of AI capabilities.
    Provides health monitoring and dependency resolution.
    """

    def __init__(self, health_check_interval: float = 30.0) -> None:
        self._capabilities: dict[str, CapabilityInfo] = {}
        self._providers: dict[str, CapabilityProvider] = {}
        self._health_check_interval = health_check_interval
        self._health_check_task: asyncio.Task[None] | None = None
        self._running = False
        self._logger = get_logger(__name__)
        self._event_handlers: dict[str, list[Callable[[CapabilityInfo], None]]] = {
            "registered": [],
            "status_changed": [],
            "health_changed": [],
            "unregistered": [],
        }

    def register_capability(
        self,
        name: str,
        description: str,
        version: str,
        service_name: str,
        provider: CapabilityProvider | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        dependencies: list[str] | None = None,
    ) -> None:
        """Register a new AI capability."""
        if name in self._capabilities:
            raise ValueError(f"Capability '{name}' already registered")

        capability = CapabilityInfo(
            name=name,
            description=description,
            version=version,
            service_name=service_name,
            status=CapabilityStatus.REGISTERED,
            tags=tags or [],
            metadata=metadata or {},
            dependencies=dependencies or [],
        )

        self._capabilities[name] = capability

        if provider:
            self._providers[name] = provider

        self._logger.info(f"Registered capability: {name} v{version}")
        self._notify_event("registered", capability)

    def unregister_capability(self, name: str) -> None:
        """Unregister a capability."""
        if name not in self._capabilities:
            raise ValueError(f"Capability '{name}' not found")

        capability = self._capabilities[name]

        # Remove from providers if present
        if name in self._providers:
            del self._providers[name]

        del self._capabilities[name]

        self._logger.info(f"Unregistered capability: {name}")
        self._notify_event("unregistered", capability)

    def get_capability(self, name: str) -> CapabilityInfo | None:
        """Get capability information by name."""
        return self._capabilities.get(name)

    def list_capabilities(
        self,
        status: CapabilityStatus | None = None,
        tags: list[str] | None = None,
        available_only: bool = False,
    ) -> list[CapabilityInfo]:
        """List capabilities with optional filtering."""
        capabilities = list(self._capabilities.values())

        if status:
            capabilities = [c for c in capabilities if c.status == status]

        if tags:
            capabilities = [
                c for c in capabilities if any(tag in c.tags for tag in tags)
            ]

        if available_only:
            capabilities = [c for c in capabilities if c.is_available]

        return capabilities

    def find_capabilities(
        self, query: str, include_description: bool = True, include_tags: bool = True
    ) -> list[CapabilityInfo]:
        """Find capabilities by text query."""
        query_lower = query.lower()
        results = []

        for capability in self._capabilities.values():
            # Search in name
            if query_lower in capability.name.lower():
                results.append(capability)
                continue

            # Search in description
            if include_description and query_lower in capability.description.lower():
                results.append(capability)
                continue

            # Search in tags
            if include_tags and any(
                query_lower in tag.lower() for tag in capability.tags
            ):
                results.append(capability)
                continue

        return results

    def get_dependencies(self, capability_name: str) -> list[str]:
        """Get dependencies for a capability."""
        capability = self.get_capability(capability_name)
        if not capability:
            return []
        return capability.dependencies

    def get_dependents(self, capability_name: str) -> list[str]:
        """Get capabilities that depend on this capability."""
        dependents = []
        for name, capability in self._capabilities.items():
            if capability_name in capability.dependencies:
                dependents.append(name)
        return dependents

    def validate_dependencies(self, capability_name: str) -> dict[str, bool]:
        """Validate all dependencies for a capability."""
        capability = self.get_capability(capability_name)
        if not capability:
            return {}

        validation_results = {}
        for dep in capability.dependencies:
            dep_capability = self.get_capability(dep)
            validation_results[dep] = (
                dep_capability is not None and dep_capability.is_available
            )

        return validation_results

    async def start_health_monitoring(self) -> None:
        """Start background health monitoring."""
        if self._running:
            return

        self._running = True
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        self._logger.info("Started capability health monitoring")

    async def stop_health_monitoring(self) -> None:
        """Stop background health monitoring."""
        if not self._running:
            return

        self._running = False

        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass

        self._logger.info("Stopped capability health monitoring")

    async def health_check(
        self, capability_name: str | None = None
    ) -> dict[str, HealthCheckResult]:
        """Perform health check on capabilities."""
        results = {}

        capabilities_to_check = (
            [capability_name] if capability_name else list(self._capabilities.keys())
        )

        for name in capabilities_to_check:
            if name not in self._capabilities:
                continue

            capability = self._capabilities[name]
            provider = self._providers.get(name)

            start_time = asyncio.get_event_loop().time()

            try:
                if provider:
                    is_healthy = await provider.health_check()
                else:
                    # Basic health check - just check if status is available
                    is_healthy = capability.status == CapabilityStatus.AVAILABLE

                response_time = (asyncio.get_event_loop().time() - start_time) * 1000

                results[name] = HealthCheckResult(
                    capability_name=name,
                    healthy=is_healthy,
                    response_time_ms=response_time,
                )

                # Update capability health status
                old_health = capability.health_status
                capability.health_status = is_healthy
                capability.last_health_check = datetime.utcnow()

                if old_health != is_healthy:
                    self._notify_event("health_changed", capability)

            except Exception as e:
                response_time = (asyncio.get_event_loop().time() - start_time) * 1000

                results[name] = HealthCheckResult(
                    capability_name=name,
                    healthy=False,
                    response_time_ms=response_time,
                    error_message=str(e),
                )

                # Update capability health status
                old_health = capability.health_status
                capability.health_status = False
                capability.last_health_check = datetime.utcnow()

                if old_health:
                    self._notify_event("health_changed", capability)

                self._logger.warning(f"Health check failed for {name}: {e}")

        return results

    def update_capability_status(
        self, capability_name: str, status: CapabilityStatus
    ) -> None:
        """Update capability status."""
        capability = self.get_capability(capability_name)
        if not capability:
            raise ValueError(f"Capability '{capability_name}' not found")

        old_status = capability.status
        capability.status = status

        if old_status != status:
            self._logger.info(
                f"Capability {capability_name} status: {old_status} -> {status}"
            )
            self._notify_event("status_changed", capability)

    def add_event_handler(
        self, event_type: str, handler: Callable[[CapabilityInfo], None]
    ) -> None:
        """Add event handler for capability events."""
        if event_type not in self._event_handlers:
            raise ValueError(f"Unknown event type: {event_type}")

        self._event_handlers[event_type].append(handler)

    def remove_event_handler(
        self, event_type: str, handler: Callable[[CapabilityInfo], None]
    ) -> None:
        """Remove event handler."""
        if event_type in self._event_handlers:
            try:
                self._event_handlers[event_type].remove(handler)
            except ValueError:
                pass

    def get_registry_stats(self) -> dict[str, Any]:
        """Get registry statistics."""
        capabilities = list(self._capabilities.values())

        status_counts = {}
        for status in CapabilityStatus:
            status_counts[status.value] = sum(
                1 for c in capabilities if c.status == status
            )

        return {
            "total_capabilities": len(capabilities),
            "available_capabilities": sum(1 for c in capabilities if c.is_available),
            "status_distribution": status_counts,
            "health_check_interval": self._health_check_interval,
            "monitoring_active": self._running,
            "last_full_health_check": max(
                (c.last_health_check for c in capabilities if c.last_health_check),
                default=None,
            ),
        }

    def _notify_event(self, event_type: str, capability: CapabilityInfo) -> None:
        """Notify event handlers."""
        handlers = self._event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(capability)
            except Exception as e:
                self._logger.error(f"Error in event handler for {event_type}: {e}")

    async def _health_check_loop(self) -> None:
        """Background health check loop."""
        while self._running:
            try:
                await asyncio.sleep(self._health_check_interval)
                await self.health_check()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._logger.error(f"Error in health check loop: {e}")


# Global registry instance
_registry: AICapabilityRegistry | None = None


def get_capability_registry() -> AICapabilityRegistry:
    """Get global capability registry instance."""
    global _registry
    if _registry is None:
        _registry = AICapabilityRegistry()
    return _registry
