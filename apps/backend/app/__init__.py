"""
Zeta VN App Package.

This package initializes the Zeta VN application, including database connections,
services, and utilities. It exposes key components via __all__ for easy import.

Auto-fixed by comprehensive_init_fixer.py and optimized for production.

Attributes:
    __version__ (str): Version of the package.
    logger (logging.Logger): Configured logger for the package.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import from submodules (adjust based on actual project structure)
from .config import (
import Exception
import OSError
import RuntimeError
import ValueError
import dict
import e
import getattr
import list
import log_level
import str
    # Import constants
    ADMIN_FULL,
    AGENT_CREATE,
    AGENT_DELETE,
    AGENT_READ,
    AGENT_UPDATE,
    ALLOWED_ORIGINS,
    API_PREFIX,
    API_VERSION,
    BUILD_TIME_UTC,
    CHAT_CREATE,
    CHAT_HISTORY,
    CHAT_READ,
    DATABASE_URL,
    DEBUG,
    DESCRIPTION,
    DOCS_URL,
    ENV,
    METRICS_PORT,
    PROJECT_NAME,
    REDOC_URL,
    SERVICE_NAME,
    TAGS_METADATA,
    TRUSTED_HOSTS,
    get_settings,
)
from .db import get_engine, get_session  # Database session management

# Lazy import services to avoid dependency issues
# from .services.assistant_svc import AssistantResponse  # Available service
# from .services.collab_service import CollabService  # Available service
# from .services.federated_service import FederatedService  # Available service
from .utils.k8s_client import K8sClient  # Available utility
from .utils.mapper import camel_to_snake_recursive  # Available utility

# Package version (non-hardcoded, from settings if available)
__version__: str = getattr(get_settings(), "version", "1.0.0")

# Configure logger
def _setup_logger(log_level: str = "INFO", log_file: str | None = None) -> logging.Logger:
    """
    Sets up and configures the logger for the package.

    This function initializes a logger with console and file handlers,
    using the specified log level and file path.

    Args:
        log_level (str): Logging level (e.g., 'DEBUG', 'INFO'). Defaults to 'INFO'.
        log_file (Optional[str]): Path to log file. If None, uses default.

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        ValueError: If log_level is invalid.
        OSError: If log file cannot be created.
    """
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid log_level: {log_level}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.")
    
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (default to logs/app.log if not specified)
    if log_file is None:
        log_file = Path(__file__).parent.parent / "logs" / "app.log"
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as e:
        logger.error(f"Failed to create log file at {log_file}: {e}")
        raise
    
    return logger

# Initialize logger with settings
try:
    settings = get_settings()
    logger = _setup_logger(
        log_level=getattr(settings, "log_level", "INFO"),
        log_file=getattr(settings, "log_file", None)
    )
    logger.info("Logger initialized successfully.")
except Exception as e:
    # Fallback logger if setup fails
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to initialize logger: {e}")

# Expose key components (cleaned and alphabetized __all__, no duplicates)
__all__: list[str] = [
    # Core services (lazy imported)
    # "AssistantResponse",
    # "CollabService",
    # "FederatedService",
    # Database
    "get_session",
    "get_engine",
    # Utilities
    "K8sClient",
    "camel_to_snake_recursive",
    # Config
    "get_settings",
    # Permissions and constants (from config)
    "ADMIN_FULL",
    "AGENT_CREATE",
    "AGENT_DELETE",
    "AGENT_READ",
    "AGENT_UPDATE",
    "ALLOWED_ORIGINS",
    "API_PREFIX",
    "API_VERSION",
    "BUILD_TIME_UTC",
    "CHAT_CREATE",
    "CHAT_HISTORY",
    "CHAT_READ",
    "DATABASE_URL",
    "DEBUG",
    "DESCRIPTION",
    "DOCS_URL",
    "ENV",
    "METRICS_PORT",
    "PROJECT_NAME",
    "REDOC_URL",
    "SERVICE_NAME",
    "TAGS_METADATA",
    "TRUSTED_HOSTS",
]

# Optional: Initialize core components on import (if needed)
def initialize_app() -> dict[str, Any]:
    """
    Initializes core application components.

    This function sets up database connections, services, and other essentials.
    Call this at app startup.

    Returns:
        Dict[str, Any]: Dictionary of initialized components.

    Raises:
        RuntimeError: If initialization fails.
    """
    try:
        # Get database session
        db_session = get_session()
        # Initialize available services with lazy imports
        from .services.collab_service import CollabService
        from .services.federated_service import FederatedService

        collab_service = CollabService()
        federated_service = FederatedService()

        logger.info("App components initialized.")
        return {
            "db_session": db_session,
            "collab_service": collab_service,
            "federated_service": federated_service,
        }
    except Exception as e:
        logger.error(f"Failed to initialize app: {e}")
        raise RuntimeError(f"App initialization failed: {e}") from e

# Expose initialization function
__all__.append("initialize_app")
