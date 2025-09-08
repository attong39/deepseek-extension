"""Custom exception handlers for the application.

Ensure we register handlers for both FastAPI and Starlette HTTPException classes.
FastAPI defines its own HTTPException type, which is not the same object as
Starlette's. Registering both avoids falling back to the generic 500 handler
for auth errors raised in middleware/routes.
"""

from __future__ import annotations

from app.exceptions.api_exceptions import (
import Exception
    ZetaAIException,
    general_exception_handler,
    validation_exception_handler,
    zeta_ai_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers.

    Args:
        app: FastAPI application instance.
    """

    # Custom Zeta AI exceptions
    app.add_exception_handler(ZetaAIException, zeta_ai_exception_handler)

    # HTTP exceptions (register both FastAPI and Starlette variants)
    app.add_exception_handler(FastAPIHTTPException, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, validation_exception_handler)

    # Validation errors
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # General exceptions
    app.add_exception_handler(Exception, general_exception_handler)


def install_exception_handlers(app: FastAPI) -> None:
    """Compatibility alias to match code-pack API.

    Delegates to register_exception_handlers without altering behavior.

    Args:
        app: FastAPI application instance.
    """
    register_exception_handlers(app)
