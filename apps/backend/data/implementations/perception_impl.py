"""Computer vision implementation for screen perception.





This module provides concrete implementations for screen capture,


template matching, and OCR functionality.


"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

import cv2
import easyocr
import mss
import numpy as np
import Exception
import FileNotFoundError
import RuntimeError
import ValueError
import confidence
import detection
import dict
import e
import float
import h
import image
import int
import languages
import len
import list
import max
import max_loc
import max_val
import min
import offset_x
import offset_y
import point
import region
import result
import save_path
import self
import str
import target_text
import template_path
import text
import threshold
import tuple
import w

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import BBox, Point


logger = logging.getLogger(__name__)


class ScreenPerceptionImpl:
    """Implementation of screen perception using OpenCV and MSS."""

    def __init__(self) -> None:
        """Initialize the screen perception implementation."""

        self._mss = mss.mss()

        logger.info("ScreenPerceptionImpl initialized")

    async def screenshot(self, save_path: str | None = None) -> np.ndarray:
        """Capture a screenshot of the current screen.





        Args:


            save_path: Optional path to save the screenshot





        Returns:


            Screenshot as BGR numpy array (OpenCV format)


        """

        try:
            # Capture the primary monitor

            monitor = self._mss.monitors[1]  # 0 is all monitors, 1 is primary

            screenshot = self._mss.grab(monitor)

            # Convert to numpy array and BGR format for OpenCV

            img_array = np.array(screenshot)

            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)

            # Save if path provided

            if save_path:
                cv2.imwrite(save_path, img_bgr)

                logger.debug(f"Screenshot saved to: {save_path}")

            return img_bgr

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")

            raise RuntimeError(f"Screenshot capture failed: {e}") from e

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

        try:
            # Load template image

            if not Path(template_path).exists():
                raise FileNotFoundError(f"Template not found: {template_path}")

            template = cv2.imread(template_path, cv2.IMREAD_COLOR)

            if template is None:
                raise ValueError(f"Could not load template: {template_path}")

            # Capture screenshot

            screenshot = await self.screenshot()

            # Crop to region if specified

            if region:
                x1, y1, x2, y2 = region.x1, region.y1, region.x2, region.y2

                screenshot = screenshot[y1:y2, x1:x2]

                offset_x, offset_y = x1, y1

            else:
                offset_x, offset_y = 0, 0

            # Perform template matching

            _ = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Check if match meets threshold

            if max_val >= threshold:
                # Calculate center point of template

                h, w = template.shape[:2]

                center_x = max_loc[0] + w // 2 + offset_x

                center_y = max_loc[1] + h // 2 + offset_y

                from apps.backend.core.domain.value_objects.automation import Point

                result_point = Point(x=center_x, y=center_y)

                logger.debug(
                    f"Template found at {result_point} with confidence {max_val:.3f}"
                )

                return result_point

            logger.debug(
                f"Template not found (confidence: {max_val:.3f}, threshold: {threshold})"
            )

            return None

        except Exception as e:
            logger.error(f"Template matching failed: {e}")

            raise RuntimeError(f"Template matching failed: {e}") from e

    async def find_text(self, text: str, region: BBox | None = None) -> Point | None:
        """Find text on screen using OCR.





        Args:


            text: Text to find


            region: Optional region to search within





        Returns:


            Center point of found text, or None if not found


        """

        try:
            # Capture screenshot

            screenshot = await self.screenshot()

            # Crop to region if specified

            if region:
                x1, y1, x2, y2 = region.x1, region.y1, region.x2, region.y2

                screenshot = screenshot[y1:y2, x1:x2]

                offset_x, offset_y = x1, y1

            else:
                offset_x, offset_y = 0, 0

            # Use OCR engine to find text

            ocr_impl = OcrEngineImpl()

            detections = await ocr_impl.detect_text(screenshot)

            # Search for matching text

            target_text_lower = text.lower().strip()

            for detection in detections:
                detected_text = detection.get("text", "").lower().strip()

                if target_text_lower in detected_text:
                    bbox = detection.get("bbox")

                    if bbox:
                        # Calculate center point

                        center_x = int((bbox[0] + bbox[2]) / 2) + offset_x

                        center_y = int((bbox[1] + bbox[3]) / 2) + offset_y

                        from apps.backend.core.domain.value_objects.automation import (
                            Point,
                        )

                        result_point = Point(x=center_x, y=center_y)

                        logger.debug(f"Text '{text}' found at {result_point}")

                        return result_point

            logger.debug(f"Text '{text}' not found on screen")

            return None

        except Exception as e:
            logger.error(f"Text search failed: {e}")

            raise RuntimeError(f"Text search failed: {e}") from e

    async def get_screen_size(self) -> tuple[int, int]:
        """Get the screen resolution.





        Returns:


            Tuple of (width, height)


        """

        try:
            monitor = self._mss.monitors[1]  # Primary monitor

            width = monitor["width"]

            height = monitor["height"]

            logger.debug(f"Screen size: {width}x{height}")

            return width, height

        except Exception as e:
            logger.error(f"Failed to get screen size: {e}")

            raise RuntimeError(f"Could not determine screen size: {e}") from e


class OcrEngineImpl:
    """Implementation of OCR engine using EasyOCR."""

    def __init__(self, languages: list[str] | None = None) -> None:
        """Initialize the OCR engine.





        Args:


            languages: List of language codes (default: ['en'])


        """

        self._languages = languages or ["en"]

        self._reader = easyocr.Reader(self._languages)

        logger.info(f"OcrEngineImpl initialized with languages: {self._languages}")

    async def detect_text(self, image: np.ndarray) -> list[dict[str, Any]]:
        """Detect all text in an image.





        Args:


            image: Input image as numpy array





        Returns:


            List of detected text with bounding boxes and confidence


        """

        try:
            # EasyOCR expects RGB format

            if len(image.shape) == 3 and image.shape[2] == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            else:
                image_rgb = image

            # Perform OCR

            results = self._reader.readtext(image_rgb)

            # Convert to our format

            detections = []

            for result in results:
                bbox, text, confidence = result

                # Convert bbox to [x1, y1, x2, y2] format

                x1 = int(min(point[0] for point in bbox))

                y1 = int(min(point[1] for point in bbox))

                x2 = int(max(point[0] for point in bbox))

                y2 = int(max(point[1] for point in bbox))

                detections.append(
                    {
                        "text": text,
                        "bbox": [x1, y1, x2, y2],
                        "confidence": float(confidence),
                    }
                )

            logger.debug(f"OCR detected {len(detections)} text regions")

            return detections

        except Exception as e:
            logger.error(f"OCR detection failed: {e}")

            raise RuntimeError(f"OCR detection failed: {e}") from e

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

        try:
            detections = await self.detect_text(image)

            target_text_lower = target_text.lower().strip()

            for detection in detections:
                detected_text = detection["text"].lower().strip()

                if target_text_lower in detected_text:
                    bbox = detection["bbox"]

                    center_x = int((bbox[0] + bbox[2]) / 2)

                    center_y = int((bbox[1] + bbox[3]) / 2)

                    from apps.backend.core.domain.value_objects.automation import Point

                    result_point = Point(x=center_x, y=center_y)

                    logger.debug(f"Text '{target_text}' found at {result_point}")

                    return result_point

            logger.debug(f"Text '{target_text}' not found in image")

            return None

        except Exception as e:
            logger.error(f"Text location search failed: {e}")

            raise RuntimeError(f"Text location search failed: {e}") from e
