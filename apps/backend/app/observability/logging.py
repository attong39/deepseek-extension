from __future__ import annotations

import logging
from typing import Literal
import Exception
import level
import str

# Structured logging setup.


# Provides a single configure_logging() used at app startup.


# Falls back gracefully if python-json-logger is unavailable.


def configure_logging(
    level: str | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
) -> None:
    """Configure root logger with JSON formatter when available.





    Args:


        level: Logging level name.


    """

    logger = logging.getLogger()

    logger.setLevel(level.upper())

    handler = logging.StreamHandler()

    try:
        from pythonjsonlogger import jsonlogger

        fmt = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")

        handler.setFormatter(fmt)

    except Exception:
        # Plain formatter fallback

        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )

    logger.handlers = [handler]
