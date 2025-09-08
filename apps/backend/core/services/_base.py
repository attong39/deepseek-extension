"""Base service class và ServiceContext.

Cung cấp common foundation cho tất cả services trong ZETA_VN.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from apps.backend.core.services.types import Startable
import Exception
import bool
import context
import ctx
import dict
import error
import operation
import property
import self
import str
import type


@dataclass(slots=True)
class ServiceContext:
    """Context chứa shared dependencies cho services."""

    logger: Any
    tracer: Any | None = None
    metrics: Any | None = None
    config: Any | None = None
    di_container: Any | None = None  # dependency injection container
    cache: Any | None = None
    event_emitter: Any | None = None


class BaseService(Startable):
    """Base class cho tất cả services.

    Cung cấp:
    - Lifecycle management (start/stop)
    - Access đến shared resources qua context
    - Common logging và metrics
    - Error handling patterns
    """

    def __init__(self, ctx: ServiceContext):
        self.ctx = ctx
        self.log = ctx.logger
        self.tracer = ctx.tracer
        self.metrics = ctx.metrics
        self.config = ctx.config
        self.di = ctx.di_container
        self.cache = ctx.cache
        self.emitter = ctx.event_emitter

        # Service state
        self._started = False

    async def start(self) -> None:
        """Start service. Override để thêm logic khởi tạo."""
        if self._started:
            self.log.warning(f"{self.__class__.__name__} already started")
            return

        self.log.info(f"Starting {self.__class__.__name__}")
        await self._start_impl()
        self._started = True
        self.log.info(f"{self.__class__.__name__} started successfully")

    async def stop(self) -> None:
        """Stop service. Override để thêm logic cleanup."""
        if not self._started:
            return

        self.log.info(f"Stopping {self.__class__.__name__}")
        await self._stop_impl()
        self._started = False
        self.log.info(f"{self.__class__.__name__} stopped")

    async def _start_impl(self) -> None:
        """Override để implement start logic. Default no-op."""

    async def _stop_impl(self) -> None:
        """Override để implement stop logic. Default no-op."""

    @property
    def is_started(self) -> bool:
        """Check if service đã started."""
        return self._started

    def _log_operation(self, operation: str, **context: Any) -> None:
        """Helper để log operations với context."""
        self.log.info(
            f"{self.__class__.__name__}.{operation}",
            extra={
                "service": self.__class__.__name__,
                "operation": operation,
                **context,
            },
        )

    def _log_error(self, operation: str, error: Exception, **context: Any) -> None:
        """Helper để log errors với context."""
        self.log.error(
            f"{self.__class__.__name__}.{operation} failed: {error}",
            exc_info=True,
            extra={
                "service": self.__class__.__name__,
                "operation": operation,
                "error_type": type(error).__name__,
                "error_msg": str(error),
                **context,
            },
        )

    async def health_check(self) -> dict[str, Any]:
        """Health check cho service. Override để custom logic."""
        return {
            "service": self.__class__.__name__,
            "status": "healthy" if self._started else "stopped",
            "started": self._started,
        }
