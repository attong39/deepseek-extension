"""Dependency injection providers.

Cung cấp factory functions cho tạo và configure services.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import KeyError
import bool
import callable
import dict
import name
import provider_func
import self
import str


@dataclass(frozen=True)
class Providers:
    """Container cho shared providers/dependencies."""

    # Database & Storage
    db_session: Any  # AsyncSession factory
    cache: Any | None = None  # Redis, memcached, etc.
    vector_store: Any | None = None  # Pinecone, Chroma, etc.

    # External Services
    llm_router: Any | None = None  # MoE router, single provider
    outbox_emitter: Any | None = None  # Event emitter

    # Configuration
    config: Any | None = None  # App config

    # Observability
    logger: Any | None = None
    metrics: Any | None = None  # Prometheus, etc.
    tracer: Any | None = None  # OpenTelemetry, etc.

    # Security & Rules
    rule_engine: Any | None = None
    auth_service: Any | None = None


class DIContainer:
    """Simple dependency injection container.

    Alternative to heavy DI frameworks, cung cấp basic service location.
    """

    def __init__(self):
        self._providers: dict[str, Any] = {}
        self._singletons: dict[str, Any] = {}

    def register_provider(self, name: str, provider_func: Any) -> None:
        """Register provider function cho dependency."""
        self._providers[name] = provider_func

    def register_singleton(self, name: str, instance: Any) -> None:
        """Register singleton instance."""
        self._singletons[name] = instance

    def get(self, name: str) -> Any:
        """Get dependency by name."""
        # Check singletons first
        if name in self._singletons:
            return self._singletons[name]

        # Check providers
        if name in self._providers:
            provider = self._providers[name]
            # Call provider function
            if callable(provider):
                instance = provider()
                # Cache as singleton if provider returns same type
                self._singletons[name] = instance
                return instance
            return provider

        raise KeyError(f"Dependency '{name}' not found")

    def get_optional(self, name: str) -> Any | None:
        """Get dependency, return None if not found."""
        try:
            return self.get(name)
        except KeyError:
            return None

    def has(self, name: str) -> bool:
        """Check if dependency exists."""
        return name in self._providers or name in self._singletons

    def clear(self) -> None:
        """Clear all providers và singletons."""
        self._providers.clear()
        self._singletons.clear()


# Default container instance
container = DIContainer()
