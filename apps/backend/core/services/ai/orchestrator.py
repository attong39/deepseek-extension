"""
AI Service Orchestrator - Central coordination for all AI capabilities.

Orchestrates interactions between different AI services while maintaining
clean separation of concerns and proper dependency injection.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, TypeVar

from apps.backend.core.common.base_classes import BaseService
from apps.backend.core.observability.logging import get_logger
import Exception
import TimeoutError
import ValueError
import bool
import cap
import capabilities
import capability
import dict
import e
import float
import i
import int
import list
import property
import range
import self
import services
import str
import super
import svc
import task
import worker_id

logger = get_logger(__name__)

T = TypeVar("T")


class AIServiceStatus(Enum):
    """AI service status enumeration."""

    STARTING = "starting"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    STOPPING = "stopping"
    STOPPED = "stopped"


@dataclass
class AIRequest:
    """Base AI request structure."""

    request_id: str
    user_id: str
    tenant_id: str | None = None
    capability: str = ""
    payload: dict[str, Any] = None
    context: dict[str, Any] = None
    priority: int = 1  # 1=highest, 10=lowest

    def __post_init__(self) -> None:
        """Initialize payload and context if None."""
        if self.payload is None:
            self.payload = {}
        if self.context is None:
            self.context = {}


@dataclass
class AIResponse:
    """Base AI response structure."""

    request_id: str
    success: bool
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = None
    processing_time_ms: float = 0.0

    def __post_init__(self) -> None:
        """Initialize metadata if None."""
        if self.metadata is None:
            self.metadata = {}


class AICapability(Protocol):
    """Protocol defining AI capability interface."""

    @property
    def name(self) -> str:
        """Capability name."""
        ...

    @property
    def status(self) -> AIServiceStatus:
        """Current capability status."""
        ...

    async def process(self, request: AIRequest) -> AIResponse:
        """Process AI request."""
        ...

    async def health_check(self) -> bool:
        """Check capability health."""
        ...


class BaseAIService(BaseService, ABC):
    """Base class for AI services."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        self._status = AIServiceStatus.STOPPED
        self._health_check_interval = 30.0  # seconds
        self._health_check_task: asyncio.Task[None] | None = None

    @property
    def name(self) -> str:
        """Service name."""
        return self._name

    @property
    def status(self) -> AIServiceStatus:
        """Current service status."""
        return self._status

    async def start(self) -> None:
        """Start the AI service."""
        logger.info(f"Starting AI service: {self.name}")
        self._status = AIServiceStatus.STARTING

        try:
            await self._start_service()
            self._status = AIServiceStatus.READY
            self._health_check_task = asyncio.create_task(self._health_check_loop())
            logger.info(f"AI service {self.name} started successfully")
        except Exception as e:
            self._status = AIServiceStatus.ERROR
            logger.error(f"Failed to start AI service {self.name}: {e}")
            raise

    async def stop(self) -> None:
        """Stop the AI service."""
        logger.info(f"Stopping AI service: {self.name}")
        self._status = AIServiceStatus.STOPPING

        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass

        try:
            await self._stop_service()
            self._status = AIServiceStatus.STOPPED
            logger.info(f"AI service {self.name} stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping AI service {self.name}: {e}")
            self._status = AIServiceStatus.ERROR
            raise

    @abstractmethod
    async def process(self, request: AIRequest) -> AIResponse:
        """Process AI request."""
        ...

    @abstractmethod
    async def _start_service(self) -> None:
        """Start service implementation."""
        ...

    @abstractmethod
    async def _stop_service(self) -> None:
        """Stop service implementation."""
        ...

    async def health_check(self) -> bool:
        """Check service health."""
        try:
            return await self._health_check_implementation()
        except Exception as e:
            logger.warning(f"Health check failed for {self.name}: {e}")
            return False

    async def _health_check_implementation(self) -> bool:
        """Health check implementation."""
        return self._status == AIServiceStatus.READY

    async def _health_check_loop(self) -> None:
        """Background health check loop."""
        while True:
            try:
                await asyncio.sleep(self._health_check_interval)
                is_healthy = await self.health_check()

                if not is_healthy and self._status == AIServiceStatus.READY:
                    logger.warning(f"AI service {self.name} health check failed")
                    self._status = AIServiceStatus.ERROR
                elif is_healthy and self._status == AIServiceStatus.ERROR:
                    logger.info(f"AI service {self.name} recovered from error")
                    self._status = AIServiceStatus.READY

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in health check loop for {self.name}: {e}")


class AIServiceOrchestrator:
    """
    Central orchestrator for all AI capabilities.

    Manages AI services, routes requests, handles failures, and provides
    unified interface for all AI operations in the application layer.
    """

    def __init__(self) -> None:
        self._services: dict[str, BaseAIService] = {}
        self._capabilities: dict[str, str] = {}  # capability -> service mapping
        self._request_queue: asyncio.Queue[AIRequest] = asyncio.Queue()
        self._worker_tasks: list[asyncio.Task[None]] = []
        self._running = False
        self._max_workers = 4
        self._logger = get_logger(__name__)

    def register_service(self, service: BaseAIService) -> None:
        """Register an AI service."""
        if service.name in self._services:
            raise ValueError(f"Service {service.name} already registered")

        self._services[service.name] = service
        self._logger.info(f"Registered AI service: {service.name}")

    def register_capability(self, capability: str, service_name: str) -> None:
        """Register a capability mapping to a service."""
        if service_name not in self._services:
            raise ValueError(f"Service {service_name} not registered")

        self._capabilities[capability] = service_name
        self._logger.info(f"Registered capability {capability} -> {service_name}")

    async def start(self) -> None:
        """Start the orchestrator and all services."""
        self._logger.info("Starting AI Service Orchestrator")

        # Start all services
        for service in self._services.values():
            await service.start()

        # Start request processing workers
        self._running = True
        self._worker_tasks = [
            asyncio.create_task(self._worker(i)) for i in range(self._max_workers)
        ]

        self._logger.info("AI Service Orchestrator started successfully")

    async def stop(self) -> None:
        """Stop the orchestrator and all services."""
        self._logger.info("Stopping AI Service Orchestrator")

        # Stop workers
        self._running = False
        for task in self._worker_tasks:
            task.cancel()

        await asyncio.gather(*self._worker_tasks, return_exceptions=True)

        # Stop all services
        for service in self._services.values():
            await service.stop()

        self._logger.info("AI Service Orchestrator stopped")

    async def process_request(self, request: AIRequest) -> AIResponse:
        """Process an AI request."""
        start_time = asyncio.get_event_loop().time()

        try:
            # Validate request
            if not request.capability:
                return AIResponse(
                    request_id=request.request_id,
                    success=False,
                    error="No capability specified",
                )

            # Find service for capability
            service_name = self._capabilities.get(request.capability)
            if not service_name:
                return AIResponse(
                    request_id=request.request_id,
                    success=False,
                    error=f"Unknown capability: {request.capability}",
                )

            service = self._services.get(service_name)
            if not service:
                return AIResponse(
                    request_id=request.request_id,
                    success=False,
                    error=f"Service {service_name} not available",
                )

            # Check service health
            if service.status != AIServiceStatus.READY:
                return AIResponse(
                    request_id=request.request_id,
                    success=False,
                    error=f"Service {service_name} not ready (status: {service.status})",
                )

            # Process request
            response = await service.process(request)

            # Calculate processing time
            processing_time = (asyncio.get_event_loop().time() - start_time) * 1000
            response.processing_time_ms = processing_time

            return response

        except Exception as e:
            self._logger.error(f"Error processing AI request {request.request_id}: {e}")
            processing_time = (asyncio.get_event_loop().time() - start_time) * 1000

            return AIResponse(
                request_id=request.request_id,
                success=False,
                error=f"Internal error: {str(e)}",
                processing_time_ms=processing_time,
            )

    async def queue_request(self, request: AIRequest) -> None:
        """Queue a request for background processing."""
        await self._request_queue.put(request)

    async def get_service_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all services."""
        status = {}
        for name, service in self._services.items():
            is_healthy = await service.health_check()
            status[name] = {
                "status": service.status.value,
                "healthy": is_healthy,
                "capabilities": [
                    cap for cap, svc in self._capabilities.items() if svc == name
                ],
            }
        return status

    async def get_capabilities(self) -> list[str]:
        """Get list of available capabilities."""
        return list(self._capabilities.keys())

    @asynccontextmanager
    async def service_context(self):
        """Async context manager for orchestrator lifecycle."""
        await self.start()
        try:
            yield self
        finally:
            await self.stop()

    async def _worker(self, worker_id: int) -> None:
        """Background worker for processing queued requests."""
        self._logger.debug(f"AI worker {worker_id} started")

        while self._running:
            try:
                # Get request from queue with timeout
                request = await asyncio.wait_for(self._request_queue.get(), timeout=1.0)

                # Process request
                response = await self.process_request(request)

                # Log results
                if response.success:
                    self._logger.debug(
                        f"Worker {worker_id} processed request {request.request_id} "
                        f"in {response.processing_time_ms:.2f}ms"
                    )
                else:
                    self._logger.warning(
                        f"Worker {worker_id} failed to process request "
                        f"{request.request_id}: {response.error}"
                    )

                # Mark task done
                self._request_queue.task_done()

            except TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._logger.error(f"Worker {worker_id} error: {e}")

        self._logger.debug(f"AI worker {worker_id} stopped")


# Global orchestrator instance
_orchestrator: AIServiceOrchestrator | None = None


def get_ai_orchestrator() -> AIServiceOrchestrator:
    """Get global AI orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AIServiceOrchestrator()
    return _orchestrator


async def setup_ai_orchestrator(
    services: list[BaseAIService], capabilities: dict[str, str]
) -> AIServiceOrchestrator:
    """Setup and configure AI orchestrator."""
    orchestrator = get_ai_orchestrator()

    # Register services
    for service in services:
        orchestrator.register_service(service)

    # Register capabilities
    for capability, service_name in capabilities.items():
        orchestrator.register_capability(capability, service_name)

    return orchestrator
