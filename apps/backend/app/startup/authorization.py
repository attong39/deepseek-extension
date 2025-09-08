"""App startup configuration cho ZETA authorization system.

Module này khởi tạo và cấu hình dependency injection cho authorization system.
"""

from __future__ import annotations

import logging
import os

from apps.backend.core.security.permission_manager import PermissionManager
from apps.backend.data.external.repositories.jit_grant_repo import MockJitGrantRepo
import Exception
import RuntimeError
import bool
import e
import use_mock_jit

logger = logging.getLogger(__name__)

# Global permission manager instance
_permission_manager: PermissionManager | None = None


def configure_authorization_system(use_mock_jit: bool = False) -> PermissionManager:
    """Cấu hình authorization system với dependency injection.

    Args:
        use_mock_jit: Sử dụng mock JIT repository cho testing/development

    Returns:
        Configured PermissionManager instance
    """
    global _permission_manager

    try:
        # Initialize JIT repository
        if use_mock_jit:
            logger.info("Using mock JIT repository for development/testing")
            jit_repo = MockJitGrantRepo()
        else:
            logger.info("Using mock JIT repository (real DB repo not implemented yet)")
            jit_repo = MockJitGrantRepo()

        # Initialize permission manager with DI
        _permission_manager = PermissionManager(jit_repo=jit_repo, audit_enabled=True)

        logger.info("✅ Authorization system configured successfully")
        return _permission_manager

    except Exception as e:
        logger.error(f"❌ Failed to configure authorization system: {e}")
        raise


def get_permission_manager() -> PermissionManager:
    """Get current permission manager instance.

    Returns:
        PermissionManager instance

    Raises:
        RuntimeError: If authorization system not initialized
    """
    if _permission_manager is None:
        raise RuntimeError(
            "Authorization system not initialized. Call startup_authorization() first."
        )
    return _permission_manager


def startup_authorization() -> None:
    """Startup hook cho authorization system."""
    logger.info("🚀 Starting authorization system...")

    # Determine environment
    environment = os.getenv("ENVIRONMENT", "development")
    use_mock = environment in ["development", "testing"]

    configure_authorization_system(use_mock_jit=use_mock)

    logger.info("🎉 Authorization system started successfully")


def shutdown_authorization() -> None:
    """Shutdown hook cho authorization system."""
    global _permission_manager

    logger.info("🛑 Shutting down authorization system...")

    # Cleanup
    _permission_manager = None

    logger.info("✅ Authorization system shutdown complete")


# FastAPI integration
def get_startup_handler():
    """Get startup handler cho FastAPI app."""

    def startup():
        startup_authorization()

    return startup


def get_shutdown_handler():
    """Get shutdown handler cho FastAPI app."""

    def shutdown():
        shutdown_authorization()

    return shutdown


# FastAPI dependency
def get_permission_manager_dependency() -> PermissionManager:
    """FastAPI dependency để inject PermissionManager."""
    return get_permission_manager()
