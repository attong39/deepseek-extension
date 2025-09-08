# zeta_vn/data/implementations/advanced_targeting.py
from __future__ import annotations

import numpy as np
import ImportError
import RuntimeError
import ValueError
import canny_high
import canny_low
import contours
import float
import hsv_ranges
import int
import len
import list
import lower
import m
import max
import max_loc
import max_val
import min_line_length
import result
import self
import str
import template_path
import threshold
import tuple
import upper
import x
import y
import zip

try:
    import cv2  # noqa: PLC0415
except ImportError:
    cv2 = None


class TemplateTargetFinder:
    """Advanced targeting using OpenCV template matching."""

    def __init__(self, template_path: str, threshold: float = 0.8):
        if cv2 is None:
            raise RuntimeError("OpenCV not available")
        self.template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if self.template is None:
            raise ValueError(f"Could not load template: {template_path}")
        self.threshold = threshold
        self.template_h, self.template_w = self.template.shape[:2]

    def locate(self, frame: np.ndarray) -> tuple[int, int] | None:
        """Find template in frame, return center coordinates."""
        if cv2 is None or self.template is None:
            return None

        # Convert BGRA to BGR if needed
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Template matching
        _ = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= self.threshold:
            # Return center of match
            top_left = max_loc
            center_x = top_left[0] + self.template_w // 2
            center_y = top_left[1] + self.template_h // 2
            return center_x, center_y

        return None

    def locate_all(self, frame: np.ndarray) -> list[tuple[int, int, float]]:
        """Find all template matches above threshold."""
        if cv2 is None or self.template is None:
            return []

        # Convert BGRA to BGR if needed
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Template matching
        _ = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF_NORMED)

        # Find all matches above threshold
        locations = np.where(result >= self.threshold)
        matches = []

        for y, x in zip(*locations, strict=False):
            center_x = x + self.template_w // 2
            center_y = y + self.template_h // 2
            confidence = result[y, x]
            matches.append((center_x, center_y, float(confidence)))

        # Sort by confidence descending
        matches.sort(key=lambda m: m[2], reverse=True)
        return matches


class MultiColorTargetFinder:
    """Fast multi-color target finder with HSV filtering."""

    def __init__(
        self, hsv_ranges: list[tuple[tuple[int, int, int], tuple[int, int, int]]]
    ):
        """
        Args:
            hsv_ranges: List of (lower_hsv, upper_hsv) tuples for color filtering
        """
        self.hsv_ranges = hsv_ranges

    def locate(self, frame: np.ndarray) -> tuple[int, int] | None:
        """Find target using HSV color filtering."""
        if cv2 is None:
            return None

        # Convert to HSV
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create combined mask for all color ranges
        combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        for lower, upper in self.hsv_ranges:
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            combined_mask = cv2.bitwise_or(combined_mask, mask)

        # Find contours
        contours, _ = cv2.findContours(
            combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        # Find largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Get center
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return cx, cy

        return None


class EdgeTargetFinder:
    """Edge detection based targeting."""

    def __init__(
        self, canny_low: int = 50, canny_high: int = 150, min_line_length: int = 50
    ):
        self.canny_low = canny_low
        self.canny_high = canny_high
        self.min_line_length = min_line_length

    def locate_corners(self, frame: np.ndarray) -> list[tuple[int, int]]:
        """Find corner points using edge detection."""
        if cv2 is None:
            return []

        # Convert to grayscale
        if len(frame.shape) == 3:
            if frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(frame, self.canny_low, self.canny_high)

        # Find corners
        corners = cv2.goodFeaturesToTrack(
            edges, maxCorners=100, qualityLevel=0.01, minDistance=30, blockSize=3
        )

        if corners is not None:
            return [(int(x), int(y)) for [[x, y]] in corners]

        return []
