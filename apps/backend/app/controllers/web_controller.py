"""
Web Controller Module

This module provides the WebController class for orchestrating server-side rendering
using a template engine (e.g., Jinja2).

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
import ValueError
import context
import dict
import exc
import isinstance
import name
import self
import str
import template

logger = logging.getLogger("apps.backend.app.controllers.web_controller")


class TemplateService(Protocol):
    """
    Protocol for template service operations.

    Methods:
        render: Render a template with context.
    """

    async def render(self, *, name: str, context: dict[str, Any]) -> str: ...


class WebController:
    """
    Server-side rendering controller (Jinja2/Any template engine).

    Args:
        template (TemplateService): The template service implementation.

    Methods:
        render: Render a template with context.
    """

    def __init__(self, template: TemplateService) -> None:
        """
        Initialize WebController.

        Args:
            template (TemplateService): The template service implementation.
        """
        self._tpl = template

    async def render(self, name: str, context: dict[str, Any] | None = None) -> str:
        """
        Render a template with context.

        Args:
            name (str): Template name.
            context (Optional[Dict[str, Any]]): Template context.

        Returns:
            str: Rendered template string.

        Raises:
            ValueError: If name is invalid.
            Exception: If service fails.
        """
        if not isinstance(name, str) or not name.strip():
            logger.error("Invalid template name for render: %r", name)
            raise ValueError("name must be a non-empty string")
        if context is not None and not isinstance(context, dict):
            logger.error("Invalid context for render: %r", context)
            raise ValueError("context must be a dict or None")
        try:
            ctx = context or {}
            logger.debug("Rendering template: name=%s, context=%r", name, ctx)
            result = await self._tpl.render(name=name, context=ctx)
            logger.info("Rendered template: name=%s", name)
            return result
        except Exception as exc:
            logger.exception("Failed to render template: name=%s: %s", name, exc)
            raise
