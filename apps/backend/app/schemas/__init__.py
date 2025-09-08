"""
Zeta VN App Schemas package initializer.

This module sets up the schemas package, configures logging, and exposes
public schema objects. All imports follow the project structure.

Attributes:
    __all__ (list[str]): List of public objects exported by this package.
    logger (logging.Logger): Configured logger for the schemas package.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

# Import logger from project's standard logging module (assuming zeta_vn.app.logger exists)
from app.logger import get_logger
import Exception
import TypeError
import ValueError
import bool
import data
import dict
import e
import isinstance
import key
import list
import name
import str

__all__: list[str] = [
    "agent",
    "chat",
    "memory",
    "rag",
]


def get_logger(name: str = "zeta.schemas") -> logging.Logger:
    """
    Get a configured logger for the schemas package.

    Args:
        name (str): Logger name. Defaults to "zeta.schemas".

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        ValueError: If logger name is empty or not a string.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Logger name must be a non-empty string.")
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger: logging.Logger = get_logger()


async def validate_schema_input(data: dict[str, Any]) -> bool:
    """
    Validate schema input data asynchronously.

    Args:
        data (Dict[str, Any]): Input data to validate.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        TypeError: If input is not a dictionary.
        ValueError: If data contains invalid keys or values.
    """
    try:
        if not isinstance(data, dict):
            logger.error("Input data must be a dictionary.")
            raise TypeError("Input data must be a dictionary.")
        # Add more validation logic here as needed, e.g., check for required keys
        required_keys = {"type", "content"}  # Example; adjust based on schema
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
        # Additional checks, e.g., type validation
        if not isinstance(data.get("content"), str):
            raise ValueError("Content must be a string.")
        logger.info("Schema input validation successful.")
        return True
    except Exception as e:
        logger.error(f"Schema input validation failed: {e}")
        raise


# Import public schema objects following project structure
from .agent import agent
from .chat import chat
from .memory import memory
from .rag import rag
