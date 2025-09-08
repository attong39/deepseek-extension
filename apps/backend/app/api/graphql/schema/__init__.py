"""
zeta_vn.app.api.graphql.schema package.

This package provides GraphQL schema definitions with performance optimization for the zeta_vn project,
including agent, memory, training, and base schemas.

Auto-fixed by comprehensive_init_fixer.py
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from . import agent, base, memory, training
import AttributeError
import Exception
import RuntimeError
import ValueError
import bool
import config
import dict
import e
import getattr
import hasattr
import int
import isinstance
import level
import list
import module
import name
import str

# Define package metadata
__version__: str = "1.0.0"
__author__: str = "zeta_vn team"
__layer__: str = "application"
__clean_architecture__: bool = True

# Configure logger for the schema package using a centralized setup function
def _setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with standardized configuration.

    Args:
        name (str): The name of the logger.
        level (int): The logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# Initialize the package logger
logger: logging.Logger = _setup_logger(__name__)


async def initialize_graphql_schema_package(
    config: dict[str, Any] | None = None,
) -> None:
    """
    Initialize the GraphQL schema package with optional configuration asynchronously.

    This function sets up necessary components for the GraphQL schema package,
    such as logging levels or external dependencies. It ensures safe
    initialization with input validation and exception handling.

    Args:
        config (Optional[Dict[str, Any]]): Optional configuration dictionary.
            Expected keys include 'log_level' (str), etc. Defaults to None.

    Raises:
        ValueError: If config contains invalid keys or values.
        RuntimeError: If initialization fails due to external issues.

    Example:
        >>> import asyncio
        >>> asyncio.run(initialize_graphql_schema_package({"log_level": "DEBUG"}))
        # Sets logger level to DEBUG asynchronously.
    """
    try:
        if config is not None:
            if not isinstance(config, dict):
                raise ValueError("Config must be a dictionary.")
            log_level_str = config.get("log_level", "INFO").upper()
            if log_level_str not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                raise ValueError(f"Invalid log_level: {log_level_str}")
            log_level = getattr(logging, log_level_str)
            logger.setLevel(log_level)
            logger.info(f"GraphQL schema package initialized with log_level: {log_level_str}")
        else:
            logger.info("GraphQL schema package initialized with default settings.")
    except Exception as e:
        logger.error(f"Failed to initialize GraphQL schema package: {e}")
        raise RuntimeError("Initialization failed.") from e


def __getattr__(name: str) -> Any:
    """Lazy import for GraphQL schema components.

    Supported lazy imports:
    - AgentType, ChatType, MemoryType, MessageType, UserType, TrainingType: GraphQL types.
    - CreateAgentInput, UpdateAgentInput, CreateChatInput, SendMessageInput, CreateMemoryInput: Input types.
    - Query, Mutation, Subscription: Root operations.
    - AgentQuery, AgentMutation, MemoryQuery, MemoryMutation, TrainingQuery, TrainingMutation: Sub-queries/mutations.
    - SCHEMA_VERSION, SCHEMA_DESCRIPTION, schema: Schema metadata and object.

    Args:
        name (str): Name of the attribute to import.

    Returns:
        Any: The imported attribute.

    Raises:
        AttributeError: If the attribute is not available.
    """
    strawberry_items = {
        "AgentType",
        "ChatType",
        "MemoryType",
        "MessageType",
        "UserType",
        "TrainingType",
        "CreateAgentInput",
        "UpdateAgentInput",
        "CreateChatInput",
        "SendMessageInput",
        "CreateMemoryInput",
        "Query",
        "Mutation",
        "Subscription",
        "AgentQuery",
        "AgentMutation",
        "MemoryQuery",
        "MemoryMutation",
        "TrainingQuery",
        "TrainingMutation",
        "SCHEMA_VERSION",
        "SCHEMA_DESCRIPTION",
        "schema",
    }
    if name in strawberry_items:
        try:
            if hasattr(base, name):
                return getattr(base, name)
            for module in [agent, memory, training]:
                if hasattr(module, name):
                    return getattr(module, name)
        except AttributeError:
            pass
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Combine manual and auto-generated exports carefully
_manual_exports: list[str] = [
    "AgentMutation",
    "AgentQuery",
    "AgentType",
    "ChatType",
    "CreateAgentInput",
    "CreateChatInput",
    "CreateMemoryInput",
    "MemoryMutation",
    "MemoryQuery",
    "MemoryType",
    "MessageType",
    "Mutation",
    "Query",
    "SCHEMA_DESCRIPTION",
    "SCHEMA_SDL",
    "SCHEMA_VERSION",
    "SendMessageInput",
    "Subscription",
    "TrainingMutation",
    "TrainingQuery",
    "TrainingType",
    "UpdateAgentInput",
    "UserType",
    "schema",
]

_auto_exports: list[str] = [
    "agent",
    "base",
    "memory",
    "simple",
    "training",
]

__all__: list[str] = _manual_exports + _auto_exports  # Combine both lists explicitly
