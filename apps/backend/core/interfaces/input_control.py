"""Input control interfaces for mouse and keyboard automation.

This module defines the protocols for controlling mouse and keyboard
inputs in the automation system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol
import bool
import float
import int
import str

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import Point


class InputController(Protocol):
    """Protocol for mouse and keyboard input control."""

    async def click(
        self, position: Point, button: str = "left", double: bool = False
    ) -> None:
        """Click at a specific position.

        Args:
            position: Point to click at
            button: Mouse button ("left", "right", "middle")
            double: Whether to double-click
        """
        ...

    async def drag(self, start: Point, end: Point, duration: float = 1.0) -> None:
        """Drag from start to end position.

        Args:
            start: Starting point
            end: Ending point
            duration: Duration in seconds
        """
        ...

    async def type_text(self, text: str, interval: float = 0.1) -> None:
        """Type text with specified interval between characters.

        Args:
            text: Text to type
            interval: Delay between characters in seconds
        """
        ...

    async def key_press(self, key: str) -> None:
        """Press a specific key.

        Args:
            key: Key to press (e.g., "enter", "ctrl+c")
        """
        ...

    async def scroll(
        self, position: Point, direction: str = "down", clicks: int = 3
    ) -> None:
        """Scroll at a specific position.

        Args:
            position: Position to scroll at
            direction: Scroll direction ("up", "down")
            clicks: Number of scroll clicks
        """
        ...

    async def move_to(self, position: Point, duration: float = 1.0) -> None:
        """Move mouse to a specific position.

        Args:
            position: Target position
            duration: Duration in seconds
        """
        ...
