"""
System Controller Module

This module provides the SystemController class for orchestrating core system operations
(version, config, reload, shutdown) via a service interface.

Author: duy_bg_vn
Layer: Controllers (Application Orchestration)
Responsibility:
    - Orchestrate use-cases across services/adapters
    - Keep controllers framework-agnostic (usable by API, CLI, WS)
    - No DB/HTTP here; call services in core/services via DI
"""

from __future__ import annotations

import logging
from typing import Any, Protocol
import Exception
import dict
import exc
import self
import str
import system

logger = logging.getLogger("apps.backend.app.controllers.system_controller")


class SystemService(Protocol):
    """
    Protocol for system service operations.

    Methods:
        version: Get system version information.
        config: Get system configuration.
        reload: Reload system configuration.
        shutdown: Shutdown the system.
    """

    async def version(self) -> dict[str, Any]: ...
    async def config(self) -> dict[str, Any]: ...
    async def reload(self) -> None: ...
    async def shutdown(self) -> None: ...


class SystemController:
    """
    Core system ops: version, config, reload, shutdown.

    Args:
        system (SystemService): The system service implementation.

    Methods:
        version: Get system version information.
        config: Get system configuration.
        reload: Reload system configuration.
        shutdown: Shutdown the system.
    """

    def __init__(self, system: SystemService) -> None:
        """
        Initialize SystemController.

        Args:
            system (SystemService): The system service implementation.
        """
        self._sys = system

    async def version(self) -> dict[str, Any]:
        """
        Get system version information.

        Returns:
            Dict[str, Any]: System version info.

        Raises:
            Exception: If service fails.
        """
        try:
            version_info = await self._sys.version()
            logger.info("Fetched system version info")
            return version_info
        except Exception as exc:
            logger.exception("Failed to fetch system version info: %s", exc)
            raise

    async def config(self) -> dict[str, Any]:
        """
        Get system configuration.

        Returns:
            Dict[str, Any]: System configuration.

        Raises:
            Exception: If service fails.
        """
        try:
            config_info = await self._sys.config()
            logger.info("Fetched system config")
            return config_info
        except Exception as exc:
            logger.exception("Failed to fetch system config: %s", exc)
            raise

    async def reload(self) -> None:
        """
        Reload system configuration.

        Raises:
            Exception: If service fails.
        """
        try:
            await self._sys.reload()
            logger.info("System configuration reloaded")
        except Exception as exc:
            logger.exception("Failed to reload system configuration: %s", exc)
            raise

    async def shutdown(self) -> None:
        """
        Shutdown the system.

        Raises:
            Exception: If service fails.
        """
        try:
            await self._sys.shutdown()
            logger.info("System shutdown initiated")
        except Exception as exc:
            logger.exception("Failed to shutdown system: %s", exc)
            raise
