"""
zeta_vn.trainer.datasets package.

This package provides dataset management utilities and services for the zeta_vn project,
including dataset registry, lineage tracking, quality scoring, and stage management.

Auto-fixed by comprehensive_init_fixer.py
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from apps.backend.trainer.datasets.registry import DatasetRegistry, registry
import Exception
import RuntimeError
import ValueError
import config
import dict
import e
import getattr
import int
import isinstance
import level
import name
import str

# Define package metadata
__version__: str = "1.0.0"
__author__: str = "zeta_vn team"

# Configure logger for the datasets package using a centralized setup function
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


async def initialize_datasets_package(
    config: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Initialize the datasets package with optional configuration asynchronously.

    This function sets up necessary components for the datasets package,
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
        >>> asyncio.run(initialize_datasets_package({"log_level": "DEBUG"}))
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
            logger.info(f"Datasets package initialized with log_level: {log_level_str}")
        else:
            logger.info("Datasets package initialized with default settings.")
    except Exception as e:
        logger.error(f"Failed to initialize datasets package: {e}")
        raise RuntimeError("Initialization failed.") from e


# Define __all__ with unique, sorted exports (removed duplicates and auto-gen conflicts)
__all__: List[str] = [
    "CONSUMED",
    "DatasetLineage",
    "DatasetQualityScore",
    "DatasetRegistry",
    "DatasetStage",
    "LABELED",
    "RAW",
    "READY",
    "TRIAGED",
    "data",
    "dataset_dict",
    "get_dataset",
    "get_stats",
    "initialize_datasets_package",
    "lineage",
    "list_datasets",
    "logger",
    "mark_used_in_training",
    "overall_score",
    "quality_scores",
    "register_dataset",
    "registry",
    "results",
    "source_key",
    "stage_key",
    "stats",
    "update_quality",
    "update_stage",
]
