"""Perception interfaces for computer vision and screen analysis.





This module defines the protocols for screen perception, OCR, and visual


element detection used in the automation system.


"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol
import dict
import float
import int
import list
import str
import tuple

if TYPE_CHECKING:
    import numpy as np
    from apps.backend.core.domain.value_objects.automation import BBox, Point


class ScreenPerception(Protocol):
    """Protocol for screen perception and visual analysis."""

    async def screenshot(self, save_path: str | None = None) -> np.ndarray:
        """Capture a screenshot of the current screen.





        Args:


            save_path: Optional path to save the screenshot





        Returns:


            Screenshot as BGR numpy array (OpenCV format)


        """

        ...

    async def find_template(
        self, template_path: str, region: BBox | None = None, threshold: float = 0.85
    ) -> Point | None:
        """Find template image on screen using template matching.





        Args:


            template_path: Path to template image file


            region: Optional region to search within


            threshold: Confidence threshold (0.0 to 1.0)





        Returns:


            Center point of matched template, or None if not found


        """

        ...

    async def find_text(self, text: str, region: BBox | None = None) -> Point | None:
        """Find text on screen using OCR.





        Args:


            text: Text to find


            region: Optional region to search within





        Returns:


            Center point of found text, or None if not found


        """

        ...

    async def get_screen_size(self) -> tuple[int, int]:
        """Get the screen resolution.





        Returns:


            Tuple of (width, height)


        """

        ...


class OcrEngine(Protocol):
    """Protocol for Optical Character Recognition (OCR)."""

    async def detect_text(self, image: np.ndarray) -> list[dict[str, Any]]:
        """Detect all text in an image.





        Args:


            image: Input image as numpy array





        Returns:


            List of detected text with bounding boxes and confidence


        """

        ...

    async def find_text_location(
        self, image: np.ndarray, target_text: str
    ) -> Point | None:
        """Find the location of specific text in an image.





        Args:


            image: Input image as numpy array


            target_text: Text to search for





        Returns:


            Center point of found text, or None if not found


        """

        ...
