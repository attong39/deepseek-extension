"""
Zeta VN App Minimal RAG Package.

This package provides minimal Retrieval-Augmented Generation (RAG) components,
including embedding, retrieval, caching, and pipeline functionality.
It exposes key components via __all__ for easy import.

Auto-fixed by comprehensive_init_fixer.py and optimized for production.

Attributes:
    __version__ (str): Version of the package.
    logger (logging.Logger): Configured logger for the package.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import from parent package for settings (adjust if needed)
from app.config import get_settings  # Assumes config module in parent

# Import from submodules (adjust based on actual project structure)
from .core import (
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
    AutoEmbedder,
    InMemoryRetriever,
    RAGCache,
    RAGPipeline,
    SimpleReranker,
)

# Package version (non-hardcoded, from settings if available)
__version__: str = get_settings().get("version", "1.0.0")

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
    
    # File handler (default to logs/minimal_rag.log if not specified)
    if log_file is None:
        log_file = Path(__file__).parent.parent.parent / "logs" / "minimal_rag.log"
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
        log_level=settings.get("log_level", "INFO"),
        log_file=settings.get("log_file")
    )
    logger.info("Minimal RAG logger initialized successfully.")
except Exception as e:
    # Fallback logger if setup fails
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to initialize logger: {e}")

# Expose key components (cleaned and alphabetized __all__, no duplicates)
__all__: list[str] = [
    # Core RAG components
    "AutoEmbedder",
    "InMemoryRetriever",
    "RAGCache",
    "RAGPipeline",
    "SimpleReranker",
    # Utility functions (from original, cleaned)
    "add_document",
    "answer",
    "cached",
    "doc",
    "docs",
    "embed",
    "get",
    "h",
    "hash_int",
    "key",
    "query",
    "query_emb",
    "rerank",
    "result",
    "results",
    "score",
    "search",
    "set",
    "sources",
]

# Optional: Async initialization for RAG components (if needed for I/O)
async def initialize_rag_components() -> dict[str, Any]:
    """
    Asynchronously initializes RAG components.

    This function sets up embedders, retrievers, and caches with async support
    for I/O operations like loading models or data.

    Returns:
        Dict[str, Any]: Dictionary of initialized RAG components.

    Raises:
        RuntimeError: If initialization fails.
    """
    try:
        # Example async setup (adjust based on actual core implementations)
        embedder = AutoEmbedder()
        retriever = InMemoryRetriever()
        cache = RAGCache()
        pipeline = RAGPipeline(embedder=embedder, retriever=retriever, cache=cache)
        
        # Simulate async I/O (e.g., loading embeddings)
        await asyncio.sleep(0.1)  # Placeholder for real async work
        
        logger.info("RAG components initialized asynchronously.")
        return {
            "embedder": embedder,
            "retriever": retriever,
            "cache": cache,
            "pipeline": pipeline,
        }
    except Exception as e:
        logger.error(f"Failed to initialize RAG components: {e}")
        raise RuntimeError(f"RAG initialization failed: {e}") from e

# Expose async initialization function
__all__.append("initialize_rag_components")
