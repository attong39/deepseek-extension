"""
Desktop Controller Module

This module provides the DesktopController class for orchestrating desktop control
operations (mouse, keyboard, screenshot, heartbeat) via a service interface.

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
import action
import all
import button
import bytes
import desktop
import dict
import exc
import int
import isinstance
import k
import len
import list
import self
import str
import user_id
import x
import y

logger = logging.getLogger("apps.backend.app.controllers.desktop_controller")


class DesktopService(Protocol):
    """
    Protocol for desktop service operations.

    Methods:
        start_session: Start a desktop session for a user.
        stop_session: Stop a desktop session.
        mouse: Perform mouse actions.
        keyboard: Perform keyboard actions.
        screenshot: Capture a screenshot.
        heartbeat: Get session heartbeat.
    """

    async def start_session(self, *, user_id: str) -> str: ...
    async def stop_session(self, *, session_id: str) -> None: ...
    async def mouse(
        self, *, session_id: str, action: str, x: int, y: int, button: str = "left"
    ) -> None: ...
    async def keyboard(self, *, session_id: str, keys: list[str]) -> None: ...
    async def screenshot(self, *, session_id: str) -> bytes: ...
    async def heartbeat(self, *, session_id: str) -> dict[str, Any]: ...


class DesktopController:
    """
    Coordinate desktop control (mouse, keyboard, screen).

    Args:
        desktop (DesktopService): The desktop service implementation.

    Methods:
        start: Start a desktop session for a user.
        stop: Stop a desktop session.
        send_mouse: Send mouse action to the desktop.
        send_keyboard: Send keyboard action to the desktop.
        grab_screen: Capture a screenshot from the desktop.
        keepalive: Get heartbeat info for a session.
    """

    def __init__(self, desktop: DesktopService) -> None:
        """
        Initialize DesktopController.

        Args:
            desktop (DesktopService): The desktop service implementation.
        """
        self._desktop = desktop

    async def start(self, user_id: str) -> str:
        """
        Start a desktop session for a user.

        Args:
            user_id (str): The user ID.

        Returns:
            str: The session ID.

        Raises:
            ValueError: If user_id is invalid.
            Exception: If service fails.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            logger.error("Invalid user_id: %r", user_id)
            raise ValueError("user_id must be a non-empty string")
        try:
            session_id = await self._desktop.start_session(user_id=user_id)
            logger.info("Started session for user_id=%s, session_id=%s", user_id, session_id)
            return session_id
        except Exception as exc:
            logger.exception("Failed to start session for user_id=%s: %s", user_id, exc)
            raise

    async def stop(self, session_id: str) -> None:
        """
        Stop a desktop session.

        Args:
            session_id (str): The session ID.

        Raises:
            ValueError: If session_id is invalid.
            Exception: If service fails.
        """
        if not isinstance(session_id, str) or not session_id.strip():
            logger.error("Invalid session_id: %r", session_id)
            raise ValueError("session_id must be a non-empty string")
        try:
            await self._desktop.stop_session(session_id=session_id)
            logger.info("Stopped session_id=%s", session_id)
        except Exception as exc:
            logger.exception("Failed to stop session_id=%s: %s", session_id, exc)
            raise

    async def send_mouse(
        self, session_id: str, action: str, x: int, y: int, button: str = "left"
    ) -> None:
        """
        Send mouse action to the desktop.

        Args:
            session_id (str): The session ID.
            action (str): Mouse action (e.g., "move", "click").
            x (int): X coordinate.
            y (int): Y coordinate.
            button (str, optional): Mouse button. Defaults to "left".

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not isinstance(session_id, str) or not session_id.strip():
            logger.error("Invalid session_id: %r", session_id)
            raise ValueError("session_id must be a non-empty string")
        if not isinstance(action, str) or not action.strip():
            logger.error("Invalid action: %r", action)
            raise ValueError("action must be a non-empty string")
        if not isinstance(x, int) or not isinstance(y, int):
            logger.error("Invalid coordinates: x=%r, y=%r", x, y)
            raise ValueError("x and y must be integers")
        if button not in {"left", "right", "middle"}:
            logger.error("Invalid button: %r", button)
            raise ValueError("button must be 'left', 'right', or 'middle'")
        try:
            await self._desktop.mouse(
                session_id=session_id, action=action, x=x, y=y, button=button
            )
            logger.info(
                "Mouse action sent: session_id=%s, action=%s, x=%d, y=%d, button=%s",
                session_id, action, x, y, button
            )
        except Exception as exc:
            logger.exception(
                "Failed mouse action: session_id=%s, action=%s, x=%d, y=%d, button=%s: %s",
                session_id, action, x, y, button, exc
            )
            raise

    async def send_keyboard(self, session_id: str, keys: list[str]) -> None:
        """
        Send keyboard action to the desktop.

        Args:
            session_id (str): The session ID.
            keys (List[str]): List of keys to send.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not isinstance(session_id, str) or not session_id.strip():
            logger.error("Invalid session_id: %r", session_id)
            raise ValueError("session_id must be a non-empty string")
        if not isinstance(keys, list) or not all(isinstance(k, str) and k for k in keys):
            logger.error("Invalid keys: %r", keys)
            raise ValueError("keys must be a non-empty list of strings")
        try:
            await self._desktop.keyboard(session_id=session_id, keys=keys)
            logger.info("Keyboard action sent: session_id=%s, keys=%r", session_id, keys)
        except Exception as exc:
            logger.exception("Failed keyboard action: session_id=%s, keys=%r: %s", session_id, keys, exc)
            raise

    async def grab_screen(self, session_id: str) -> bytes:
        """
        Capture a screenshot from the desktop.

        Args:
            session_id (str): The session ID.

        Returns:
            bytes: Screenshot image bytes.

        Raises:
            ValueError: If session_id is invalid.
            Exception: If service fails.
        """
        if not isinstance(session_id, str) or not session_id.strip():
            logger.error("Invalid session_id: %r", session_id)
            raise ValueError("session_id must be a non-empty string")
        try:
            image_bytes = await self._desktop.screenshot(session_id=session_id)
            logger.info("Screenshot captured: session_id=%s, bytes=%d", session_id, len(image_bytes))
            return image_bytes
        except Exception as exc:
            logger.exception("Failed to capture screenshot: session_id=%s: %s", session_id, exc)
            raise

    async def keepalive(self, session_id: str) -> dict[str, Any]:
        """
        Get heartbeat info for a session.

        Args:
            session_id (str): The session ID.

        Returns:
            Dict[str, Any]: Heartbeat information.

        Raises:
            ValueError: If session_id is invalid.
            Exception: If service fails.
        """
        if not isinstance(session_id, str) or not session_id.strip():
            logger.error("Invalid session_id: %r", session_id)
            raise ValueError("session_id must be a non-empty string")
        try:
            heartbeat = await self._desktop.heartbeat(session_id=session_id)
            logger.info("Heartbeat received: session_id=%s, data=%r", session_id, heartbeat)
            return heartbeat
        except Exception as exc:
            logger.exception("Failed to get heartbeat: session_id=%s: %s", session_id, exc)
            raise
