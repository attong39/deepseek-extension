"""
Ollama Prometheus Monitoring for Zeta Backend
"""

import asyncio
import logging
import time
from collections.abc import AsyncGenerator
from typing import Any
import Exception
import ImportError
import app
import args
import bool
import check_interval
import count
import dict
import e
import enabled
import exc
import float
import health_data
import health_response
import int
import isinstance
import kwargs
import len
import method
import ollama_client
import raw_count
import self
import str
import success
import super
import token_count

try:
    from prometheus_client import Counter, Gauge, Histogram
except ImportError as exc:
    raise ImportError(
        "prometheus_client is required: pip install prometheus-client"
    ) from exc

from .client import OllamaClient, OllamaResponse

logger = logging.getLogger(__name__)

# Prometheus metrics
OLLAMA_UP = Gauge("zeta_ollama_up", "Is Ollama service reachable (1=up, 0=down)")
OLLAMA_MODEL_COUNT = Gauge(
    "zeta_ollama_model_count", "Number of models loaded in Ollama"
)
OLLAMA_REQUEST_DURATION = Histogram(
    "zeta_ollama_request_duration_seconds",
    "Time spent on Ollama requests",
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)
OLLAMA_REQUEST_TOTAL = Counter(
    "zeta_ollama_requests_total",
    "Total number of Ollama requests",
    ["method", "status"],
)
OLLAMA_GENERATION_TOKENS = Histogram(
    "zeta_ollama_generation_tokens",
    "Number of tokens generated",
    buckets=[1, 10, 50, 100, 500, 1000, 5000],
)
OLLAMA_LATENCY = Gauge(
    "zeta_ollama_latency_seconds", "Current Ollama API latency in seconds"
)


class OllamaMonitor:
    """Background monitor for Ollama service health and metrics"""

    # Attribute type declarations for static analysis
    client: OllamaClient
    check_interval: float
    enabled: bool
    _monitoring_task: asyncio.Task[None] | None
    _running: bool

    def __init__(
        self,
        ollama_client: OllamaClient | None = None,
        check_interval: float = 30.0,
        enabled: bool = True,
    ) -> None:
        self.client = ollama_client or OllamaClient()
        self.check_interval = check_interval
        self.enabled = enabled
        # Background task handle
        self._monitoring_task = None
        self._running = False

    async def start(self) -> None:
        """Start background monitoring"""
        if not self.enabled:
            logger.info("Ollama monitoring disabled")
            return
        if self._running:
            logger.warning("Ollama monitoring already running")
            return
        self._running = True
        self._monitoring_task = asyncio.create_task(self._monitor_loop())
        logger.info(f"Started Ollama monitoring (interval: {self.check_interval}s)")
        # Yield control to ensure task is scheduled (satisfy async usage linters)
        await asyncio.sleep(0)

    async def stop(self) -> None:
        """Stop background monitoring"""
        if not self._running:
            return
        self._running = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                logger.info("Ollama monitoring task cancellation acknowledged")
                raise
        logger.info("Stopped Ollama monitoring")

    async def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self._running:
            try:
                await self._perform_health_check()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                logger.info("Ollama monitoring loop cancelled")
                raise
            except Exception as e:
                logger.error(f"Error in Ollama monitoring loop: {e}")
                await asyncio.sleep(self.check_interval)

    async def _perform_health_check(self) -> None:
        """Perform health check and update metrics"""
        start_time = time.time()
        try:
            health_response: OllamaResponse = await self.client.health_check()
            latency = time.time() - start_time
            OLLAMA_LATENCY.set(latency)
            if health_response.success:
                OLLAMA_UP.set(1)
                health_data: dict[str, Any] = health_response.data or {}
                raw_count: Any = health_data.get("model_count", 0)
                count: float = (
                    float(raw_count) if isinstance(raw_count, int | float) else 0.0
                )
                OLLAMA_MODEL_COUNT.set(count)
                OLLAMA_REQUEST_TOTAL.labels(
                    method="health_check", status="success"
                ).inc()
                logger.debug(
                    f"Ollama health check: OK (latency: {latency:.3f}s, models: {count})"
                )
            else:
                OLLAMA_UP.set(0)
                OLLAMA_MODEL_COUNT.set(0)
                OLLAMA_REQUEST_TOTAL.labels(
                    method="health_check", status="failure"
                ).inc()
                logger.warning(f"Ollama health check failed: {health_response.error}")
        except Exception as e:
            OLLAMA_UP.set(0)
            OLLAMA_MODEL_COUNT.set(0)
            OLLAMA_REQUEST_TOTAL.labels(method="health_check", status="error").inc()
            logger.error(f"Ollama health check error: {e}")

    def record_request(self, method: str, duration: float, success: bool) -> None:
        """Record a request metric"""
        OLLAMA_REQUEST_DURATION.observe(duration)
        status = "success" if success else "failure"
        OLLAMA_REQUEST_TOTAL.labels(method=method, status=status).inc()

    def record_generation(self, token_count: int) -> None:
        """Record token generation metrics"""
        OLLAMA_GENERATION_TOKENS.observe(token_count)


class MetricsOllamaClient(OllamaClient):
    """OllamaClient wrapper that automatically records Prometheus metrics"""

    def __init__(
        self, monitor: OllamaMonitor | None = None, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.monitor = monitor or OllamaMonitor()

    async def generate(self, *args: Any, **kwargs: Any) -> OllamaResponse:
        start_time = time.time()
        try:
            response = await super().generate(*args, **kwargs)
            duration = time.time() - start_time
            self.monitor.record_request("generate", duration, response.success)
            if response.success and response.data is not None:
                estimated_tokens = len(str(response.data)) // 4
                self.monitor.record_generation(estimated_tokens)
            return response
        except Exception:
            duration = time.time() - start_time
            self.monitor.record_request("generate", duration, False)
            raise

    async def chat(self, *args: Any, **kwargs: Any) -> OllamaResponse:
        start_time = time.time()
        try:
            response = await super().chat(*args, **kwargs)
            duration = time.time() - start_time
            self.monitor.record_request("chat", duration, response.success)
            if response.success and response.data is not None:
                estimated_tokens = len(str(response.data)) // 4
                self.monitor.record_generation(estimated_tokens)
            return response
        except Exception:
            duration = time.time() - start_time
            self.monitor.record_request("chat", duration, False)
            raise

    async def list_models(self, *args: Any, **kwargs: Any) -> OllamaResponse:
        start_time = time.time()
        try:
            response = await super().list_models(*args, **kwargs)
            duration = time.time() - start_time
            self.monitor.record_request("list_models", duration, response.success)
            return response
        except Exception:
            duration = time.time() - start_time
            self.monitor.record_request("list_models", duration, False)
            raise

    async def pull_model(self, *args: Any, **kwargs: Any) -> OllamaResponse:
        start_time = time.time()
        try:
            response = await super().pull_model(*args, **kwargs)
            duration = time.time() - start_time
            self.monitor.record_request("pull_model", duration, response.success)
            return response
        except Exception:
            duration = time.time() - start_time
            self.monitor.record_request("pull_model", duration, False)
            raise


# Singleton monitor instance
_global_monitor: OllamaMonitor | None = None


def get_monitor() -> OllamaMonitor:
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = OllamaMonitor()
    return _global_monitor


async def start_monitoring(
    client: OllamaClient | None = None,
    check_interval: float = 30.0,
    enabled: bool = True,
) -> OllamaMonitor:
    monitor = get_monitor()
    monitor.client = client or OllamaClient()
    monitor.check_interval = check_interval
    monitor.enabled = enabled
    await monitor.start()
    return monitor


async def stop_monitoring() -> None:
    global _global_monitor
    if _global_monitor:
        await _global_monitor.stop()


async def ollama_monitoring_lifespan(_app: Any) -> AsyncGenerator[None, None]:
    await start_monitoring()
    logger.info("Ollama monitoring started")
    yield
    await stop_monitoring()
    logger.info("Ollama monitoring stopped")


def setup_ollama_monitoring(app: Any, **kwargs: Any) -> None:
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def lifespan(app: Any) -> AsyncGenerator[None, None]:
        await start_monitoring(**kwargs)
        yield
        await stop_monitoring()

    app.router.lifespan_context = lifespan
