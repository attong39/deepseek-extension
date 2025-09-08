"""Controllers package for Zeta backend application.

Cung cấp các controller và service cho các module chính của hệ thống:
- Analytics, Batch, CLI, Desktop, Mobile, Monitoring, Stream, System, Voice, Web, Webhook.
- Định nghĩa các controller/service, event bus, context, args, logger.

Nguyên tắc thiết kế:
- Clean Architecture, separation of concerns
- Type-first, đầy đủ type hints
- Tối ưu hiệu năng với lazy loading
- Tích hợp logger chuẩn dự án
- Không hard-code, kiểm tra input và xử lý exception an toàn
- Hỗ trợ async/await cho các controller/service có I/O

"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Dict, List

from apps.backend.core.observability.logging import get_logger
import AttributeError
import Exception
import ImportError
import RuntimeError
import bool
import dict
import e
import globals
import module_name
import name
import str

if TYPE_CHECKING:
    from .analytics_controller import AnalyticsController
    from .batch_controller import BatchController
    from .cli_controller import CLIController
    from .desktop_controller import DesktopController
    from .mobile_controller import MobileController
    from .monitoring_controller import MonitoringController
    from .stream_controller import StreamController
    from .system_controller import SystemController
    from .voice_controller import VoiceController
    from .web_controller import WebController
    from .webhook_controller import WebhookController

# Logger chuẩn của dự án
logger = get_logger(__name__)

__all__ = [
    "AnalyticsController",
    "AnalyticsService",
    "BatchController",
    "BatchService",
    "CLIController",
    "CLIService",
    "DesktopController",
    "DesktopService",
    "EventBus",
    "MobileController",
    "MobilePushService",
    "MonitoringController",
    "MonitoringService",
    "StreamController",
    "SystemController",
    "SystemService",
    "TemplateService",
    "VoiceController",
    "VoiceService",
    "WebController",
    "WebhookController",
    "WebhookService",
    "args",
    "ctx",
    "logger",
    # Internal modules
    "analytics_controller",
    "batch_controller",
    "cli_controller",
    "desktop_controller",
    "mobile_controller",
    "monitoring_controller",
    "stream_controller",
    "system_controller",
    "voice_controller",
    "web_controller",
    "webhook_controller",
]


async def _validate_imports() -> bool:
    """Validate that all required controller modules can be imported.

    Returns:
        bool: True if all imports are valid, False otherwise.

    Raises:
        ImportError: If any required module cannot be imported.
    """
    try:
        from . import (
            analytics_controller,
            batch_controller,
            cli_controller,
            desktop_controller,
            mobile_controller,
            monitoring_controller,
            stream_controller,
            system_controller,
            voice_controller,
            web_controller,
            webhook_controller,
        )
        logger.info("Controllers package imports validated successfully")
        return True
    except ImportError as e:
        logger.error(f"Failed to import controller module: {e}")
        raise ImportError(f"Controllers package initialization failed: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error during controllers package validation: {e}")
        raise RuntimeError(f"Controllers package validation failed: {e}") from e


def _setup_lazy_loading() -> None:
    """Setup lazy loading for controller modules to improve startup performance."""
    _lazy_cache: dict[str, Any] = {}

    def _lazy_import(module_name: str) -> Any:
        """Lazy import helper with caching.

        Args:
            module_name: Name of the module to import.

        Returns:
            The imported module.

        Raises:
            ImportError: If module cannot be imported.
        """
        if module_name not in _lazy_cache:
            try:
                if module_name == "analytics_controller":
                    from . import analytics_controller
                    _lazy_cache[module_name] = analytics_controller
                elif module_name == "batch_controller":
                    from . import batch_controller
                    _lazy_cache[module_name] = batch_controller
                elif module_name == "cli_controller":
                    from . import cli_controller
                    _lazy_cache[module_name] = cli_controller
                elif module_name == "desktop_controller":
                    from . import desktop_controller
                    _lazy_cache[module_name] = desktop_controller
                elif module_name == "mobile_controller":
                    from . import mobile_controller
                    _lazy_cache[module_name] = mobile_controller
                elif module_name == "monitoring_controller":
                    from . import monitoring_controller
                    _lazy_cache[module_name] = monitoring_controller
                elif module_name == "stream_controller":
                    from . import stream_controller
                    _lazy_cache[module_name] = stream_controller
                elif module_name == "system_controller":
                    from . import system_controller
                    _lazy_cache[module_name] = system_controller
                elif module_name == "voice_controller":
                    from . import voice_controller
                    _lazy_cache[module_name] = voice_controller
                elif module_name == "web_controller":
                    from . import web_controller
                    _lazy_cache[module_name] = web_controller
                elif module_name == "webhook_controller":
                    from . import webhook_controller
                    _lazy_cache[module_name] = webhook_controller
                else:
                    raise ImportError(f"Unknown lazy module: {module_name}")

                logger.debug(f"Lazy loaded controller module: {module_name}")

            except ImportError as e:
                logger.error(f"Failed to lazy load {module_name}: {e}")
                raise

        return _lazy_cache[module_name]

    globals()["_lazy_import"] = _lazy_import


def __getattr__(name: str) -> Any:
    """Lazy loading support for controllers package attributes.

    Args:
        name: Name of the attribute to get.

    Returns:
        The requested attribute.

    Raises:
        AttributeError: If attribute is not found.
    """
    lazy_modules = {
        "analytics_controller", "batch_controller", "cli_controller",
        "desktop_controller", "mobile_controller", "monitoring_controller",
        "stream_controller", "system_controller", "voice_controller",
        "web_controller", "webhook_controller"
    }

    if name in lazy_modules:
        try:
            return _lazy_import(name)
        except ImportError:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    # Example: Lazy load controller classes if needed
    if name == "AnalyticsController":
        from .analytics_controller import AnalyticsController
        return AnalyticsController
    elif name == "BatchController":
        from .batch_controller import BatchController
        return BatchController
    elif name == "CLIController":
        from .cli_controller import CLIController
        return CLIController
    elif name == "DesktopController":
        from .desktop_controller import DesktopController
        return DesktopController
    elif name == "MobileController":
        from .mobile_controller import MobileController
        return MobileController
    elif name == "MonitoringController":
        from .monitoring_controller import MonitoringController
        return MonitoringController
    elif name == "StreamController":
        from .stream_controller import StreamController
        return StreamController
    elif name == "SystemController":
        from .system_controller import SystemController
        return SystemController
    elif name == "VoiceController":
        from .voice_controller import VoiceController
        return VoiceController
    elif name == "WebController":
        from .web_controller import WebController
        return WebController
    elif name == "WebhookController":
        from .webhook_controller import WebhookController
        return WebhookController

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


async def _initialize_controllers() -> None:
    """Initialize the controllers package with validation and setup."""
    try:
        await _validate_imports()
        _setup_lazy_loading()
        logger.info("Controllers package initialized successfully")
    except Exception as e:
        logger.critical(f"Failed to initialize controllers package: {e}")
        raise


if __name__ != "__main__":
    try:
        asyncio.run(_initialize_controllers())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(_initialize_controllers())
        else:
            loop.run_until_complete(_initialize_controllers())
