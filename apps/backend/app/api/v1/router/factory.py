from __future__ import annotations

import time
from collections.abc import Callable
from functools import cached_property
from typing import TYPE_CHECKING

from app.admin import create_admin_router
from app.agents import create_agents_router
from app.auth import create_auth_router
from app.files import create_files_router
from app.health import create_health_router
from app.memory import create_memory_router
from app.rag import create_rag_router
from app.training import create_training_router
from fastapi import APIRouter, Request, Response
import call_next
import dict
import float
import print
import request
import self
import str
import threshold
import time_taken

"""Router Factory implementation for API v1.
Giải quyết missing build_api_v1_router và optimize performance
với lazy loading pattern.
"""
if TYPE_CHECKING:
    pass


class RouterFactory:
    """Centralized router factory với lazy loading cho performance."""

    def __init__(self) -> None:
        """Initialize router factory."""
        self._performance_stats: dict[str, float] = {}

    @cached_property
    def health_router(self) -> APIRouter:
        """Health check router - lazy loaded."""
        return create_health_router()

    @cached_property
    def auth_router(self) -> APIRouter:
        """Authentication router - lazy loaded."""
        return create_auth_router()

    @cached_property
    def agents_router(self) -> APIRouter:
        """Agents router - lazy loaded."""
        return create_agents_router()

    @cached_property
    def memory_router(self) -> APIRouter:
        """Memory router - lazy loaded."""
        return create_memory_router()

    @cached_property
    def rag_router(self) -> APIRouter:
        """RAG router - lazy loaded."""
        return create_rag_router()

    @cached_property
    def training_router(self) -> APIRouter:
        """Training router - lazy loaded."""
        return create_training_router()

    @cached_property
    def admin_router(self) -> APIRouter:
        """Admin router - lazy loaded."""
        return create_admin_router()

    @cached_property
    def files_router(self) -> APIRouter:
        """Files router - lazy loaded."""
        return create_files_router()

    def create_performance_middleware(self) -> Callable[[Request, Callable], Response]:
        """Create performance monitoring middleware."""

        async def performance_middleware(
            request: Request, call_next: Callable
        ) -> Response:
            """Track request performance và log slow requests."""
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = f"{process_time:.4f}"
            endpoint = f"{request.method} {request.url.path}"
            self._performance_stats[endpoint] = process_time
            if process_time > 0.1:
                print(f"🐌 SLOW REQUEST: {endpoint} took {process_time:.4f}s")
            return response

        return performance_middleware

    @cached_property
    def main_router(self) -> APIRouter:
        """Main API v1 router với all endpoints và middleware."""
        router = APIRouter(
            prefix="/api/v1",
            responses={
                404: {"description": "Not found"},
                500: {"description": "Internal server error"},
            },
        )

        @router.middleware("http")
        async def add_performance_middleware(
            request: Request, call_next: Callable
        ) -> Response:
            middleware = self.create_performance_middleware()
            return await middleware(request, call_next)

        router.include_router(
            self.health_router, prefix="/health", tags=["🏥 Health & Monitoring"]
        )
        router.include_router(
            self.auth_router, prefix="/auth", tags=["🔐 Authentication"]
        )
        router.include_router(
            self.agents_router, prefix="/agents", tags=["🤖 AI Agents"]
        )
        router.include_router(
            self.memory_router, prefix="/memory", tags=["🧠 Memory & Knowledge"]
        )
        router.include_router(
            self.rag_router, prefix="/rag", tags=["📚 RAG & Documents"]
        )
        router.include_router(
            self.training_router, prefix="/training", tags=["🎯 Model Training"]
        )
        router.include_router(
            self.admin_router, prefix="/admin", tags=["⚙️ Administration"]
        )
        router.include_router(
            self.files_router, prefix="/files", tags=["📁 File Management"]
        )
        return router

    def get_performance_stats(self) -> dict[str, float]:
        """Get current performance statistics."""
        return self._performance_stats.copy()

    def get_slow_endpoints(self, threshold: float = 0.1) -> dict[str, float]:
        """Get endpoints slower than threshold."""
        return {
            endpoint: time_taken
            for endpoint, time_taken in self._performance_stats.items()
            if time_taken > threshold
        }


_router_factory: RouterFactory | None = None


def get_router_factory() -> RouterFactory:
    """Get global router factory instance (singleton pattern)."""
    global _router_factory
    if _router_factory is None:
        _router_factory = RouterFactory()
    return _router_factory


def build_api_v1_router() -> APIRouter:
    """Main factory function để tạo API v1 router.
    Đây là function được mong đợi bởi các imports khác.
    Giải quyết missing build_api_v1_router error.
    Returns:
        FastAPI router configured với all v1 endpoints
    """
    factory = get_router_factory()
    return factory.main_router


create_api_v1_router = build_api_v1_router
api_v1_router_factory = build_api_v1_router
__all__ = [
    "RouterFactory",
    "api_v1_router_factory",
    "build_api_v1_router",
    "create_api_v1_router",
    "get_router_factory",
]
