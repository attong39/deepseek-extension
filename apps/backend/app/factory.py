"""Application factory for ZETA_VN FastAPI app."""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from app.api.v1.router import build_api_v1_router
from app.middleware import (
    AuthenticationMiddleware,
    CompressionMiddleware,
    PerformanceMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)
from apps.backend.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    logger.info("Starting ZETA_VN application...")

    # Initialize database connections
    # Initialize Redis connections
    # Initialize model registry
    # Start background tasks

    yield

    # Shutdown
    logger.info("Shutting down ZETA_VN application...")

    # Close database connections
    # Close Redis connections
    # Cleanup background tasks


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="ZETA_VN API",
        description="AI-powered Vietnamese assistant with advanced capabilities",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middleware stack
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CompressionMiddleware)
    app.add_middleware(PerformanceMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(AuthenticationMiddleware)

    # Include API routers
    app.include_router(build_api_v1_router())

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "zeta_vn"}

    return app


__all__ = ["create_app", "lifespan"]
