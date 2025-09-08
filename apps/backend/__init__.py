"""
Backend package for zeta-monorepo.

This module initializes the backend application, including logging, configuration,
and core components. It provides a centralized entry point for backend operations.

Auto-fixed by comprehensive_init_fixer.py
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

# Imports from project structure (adjust paths if needed)
from .core.observability.logging import get_logger  # Standard logger
import APIHandler
import DatabaseManager
import Exception
import KeyboardInterrupt
import RuntimeError
import ValueError
import config_override
import dict
import e
import float
import get_config
import isinstance
import key
import list
import logger
import self
import str
import value

# Expose key components for external use
__all__: list[str] = ["BackendApp", "initialize_backend"]

# Global logger instance
logger: logging.Logger = get_logger(__name__)


class BackendApp:
    """
    Main backend application class for zeta-monorepo.

    This class handles initialization of core components like database and API,
    with async support for I/O operations. It ensures safe startup and shutdown.

    Attributes:
        config (Dict[str, Any]): Application configuration loaded from core.config.
        db_manager (Optional[DatabaseManager]): Database manager instance.
        api_handler (Optional[APIHandler]): API handler instance.
    """

    def __init__(self, config_override: dict[str, Any] | None = None) -> None:
        """
        Initialize the BackendApp.

        Args:
            config_override (Optional[Dict[str, Any]]): Optional config overrides.
                Must be a dict with valid keys; invalid keys are ignored with a warning.

        Raises:
            ValueError: If config_override contains invalid types.
        """
        self.config: dict[str, Any] = get_config()
        if config_override:
            if not isinstance(config_override, dict):
                raise ValueError("config_override must be a dictionary.")
            for key, value in config_override.items():
                if key in self.config:
                    self.config[key] = value
                else:
                    logger.warning(f"Ignoring unknown config key: {key}")
        
        self.db_manager: DatabaseManager | None = None
        self.api_handler: APIHandler | None = None
        logger.info("BackendApp initialized with config.")

    async def initialize_components(self) -> None:
        """
        Asynchronously initialize core components (database and API).

        This method handles I/O operations safely with exception handling.

        Raises:
            RuntimeError: If initialization of any component fails.
        """
        try:
            logger.info("Initializing database manager...")
            self.db_manager = DatabaseManager(self.config["database_url"])
            await self.db_manager.connect()
            
            logger.info("Initializing API handler...")
            self.api_handler = APIHandler(self.config["api_port"])
            await self.api_handler.start()
            
            logger.info("All components initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            await self.shutdown()
            raise RuntimeError(f"Component initialization failed: {e}") from e

    async def shutdown(self) -> None:
        """
        Asynchronously shut down core components.

        Ensures graceful cleanup of resources.
        """
        try:
            if self.db_manager:
                await self.db_manager.disconnect()
                logger.info("Database manager shut down.")
            if self.api_handler:
                await self.api_handler.stop()
                logger.info("API handler shut down.")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    async def run(self) -> None:
        """
        Run the backend application.

        Initializes components and keeps the app running until interrupted.
        """
        await self.initialize_components()
        try:
            # Simulate running (replace with actual event loop or server logic)
            await asyncio.sleep(float('inf'))
        except KeyboardInterrupt:
            logger.info("Received shutdown signal.")
        finally:
            await self.shutdown()


async def initialize_backend(config_override: dict[str, Any] | None = None) -> BackendApp:
    """
    Initialize and return a BackendApp instance.

    This is a convenience function for quick setup.

    Args:
        config_override (Optional[Dict[str, Any]]): Optional config overrides.

    Returns:
        BackendApp: The initialized backend app instance.

    Raises:
        RuntimeError: If initialization fails.
    """
    app = BackendApp(config_override)
    await app.initialize_components()
    return app
