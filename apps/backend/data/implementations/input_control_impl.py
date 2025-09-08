"""Input control implementation for mouse and keyboard automation.





This module provides concrete implementations for controlling mouse


and keyboard inputs using PyAutoGUI.


"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

import pyautogui
import Exception
import RuntimeError
import ValueError
import bool
import button
import clicks
import direction
import double
import duration
import e
import end
import float
import int
import interval
import k
import key
import position
import self
import start
import str
import text
import x
import y

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import Point


logger = logging.getLogger(__name__)


# Configure PyAutoGUI safety settings


pyautogui.FAILSAFE = True  # Move mouse to corner to abort


pyautogui.PAUSE = 0.1  # Default pause between actions


class InputControllerImpl:
    """Implementation of input controller using PyAutoGUI."""

    def __init__(self) -> None:
        """Initialize the input controller implementation."""

        logger.info("InputControllerImpl initialized")

    async def click(
        self, position: Point, button: str = "left", double: bool = False
    ) -> None:
        """Click at a specific position.





        Args:


            position: Point to click at


            button: Mouse button ("left", "right", "middle")


            double: Whether to double-click


        """

        try:
            logger.debug(
                f"Clicking at {position} with {button} button (double: {double})"
            )

            # Validate button type

            if button not in ["left", "right", "middle"]:
                raise ValueError(f"Invalid button: {button}")

            # Perform click in thread pool to avoid blocking

            await asyncio.get_event_loop().run_in_executor(
                None, self._perform_click, position.x, position.y, button, double
            )

        except Exception as e:
            logger.error(f"Click failed at {position}: {e}")

            raise RuntimeError(f"Click failed: {e}") from e

    def _perform_click(self, x: int, y: int, button: str, double: bool) -> None:
        """Perform the actual click operation."""

        if double:
            pyautogui.doubleClick(x, y, button=button)

        else:
            pyautogui.click(x, y, button=button)

    async def drag(self, start: Point, end: Point, duration: float = 1.0) -> None:
        """Drag from start to end position.





        Args:


            start: Starting point


            end: Ending point


            duration: Duration in seconds


        """

        try:
            logger.debug(f"Dragging from {start} to {end} over {duration}s")

            await asyncio.get_event_loop().run_in_executor(
                None,
                pyautogui.drag,
                end.x - start.x,  # relative movement
                end.y - start.y,
                duration,
                button="left",
            )

        except Exception as e:
            logger.error(f"Drag failed from {start} to {end}: {e}")

            raise RuntimeError(f"Drag failed: {e}") from e

    async def type_text(self, text: str, interval: float = 0.1) -> None:
        """Type text with specified interval between characters.





        Args:


            text: Text to type


            interval: Delay between characters in seconds


        """

        try:
            logger.debug(f"Typing text: '{text[:50]}...' with interval {interval}s")

            await asyncio.get_event_loop().run_in_executor(
                None, pyautogui.typewrite, text, interval
            )

        except Exception as e:
            logger.error(f"Type text failed: {e}")

            raise RuntimeError(f"Type text failed: {e}") from e

    async def key_press(self, key: str) -> None:
        """Press a specific key.





        Args:


            key: Key to press (e.g., "enter", "ctrl+c")


        """

        try:
            logger.debug(f"Pressing key: {key}")

            # Handle key combinations

            if "+" in key:
                keys = [k.strip() for k in key.split("+")]

                await asyncio.get_event_loop().run_in_executor(
                    None, pyautogui.hotkey, *keys
                )

            else:
                await asyncio.get_event_loop().run_in_executor(
                    None, pyautogui.press, key
                )

        except Exception as e:
            logger.error(f"Key press failed for '{key}': {e}")

            raise RuntimeError(f"Key press failed: {e}") from e

    async def scroll(
        self, position: Point, direction: str = "down", clicks: int = 3
    ) -> None:
        """Scroll at a specific position.





        Args:


            position: Position to scroll at


            direction: Scroll direction ("up", "down")


            clicks: Number of scroll clicks


        """

        try:
            logger.debug(f"Scrolling {direction} at {position} for {clicks} clicks")

            # Move to position first

            await self.move_to(position, duration=0.5)

            # Determine scroll direction

            scroll_clicks = clicks if direction == "up" else -clicks

            await asyncio.get_event_loop().run_in_executor(
                None, pyautogui.scroll, scroll_clicks, position.x, position.y
            )

        except Exception as e:
            logger.error(f"Scroll failed at {position}: {e}")

            raise RuntimeError(f"Scroll failed: {e}") from e

    async def move_to(self, position: Point, duration: float = 1.0) -> None:
        """Move mouse to a specific position.





        Args:


            position: Target position


            duration: Duration in seconds


        """

        try:
            logger.debug(f"Moving to {position} over {duration}s")

            await asyncio.get_event_loop().run_in_executor(
                None, pyautogui.moveTo, position.x, position.y, duration
            )

        except Exception as e:
            logger.error(f"Move to failed for {position}: {e}")

            raise RuntimeError(f"Move to failed: {e}") from e
