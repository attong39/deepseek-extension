"""
Vietnamese OCR using PaddleOCR.
"""

from __future__ import annotations
import ImportError
import conf
import confidence_threshold
import float
import image_path
import len
import line
import page
import result
import self
import str
import text

try:
    from paddleocr import PaddleOCR

    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False


class VietOCR:
    """Vietnamese OCR processor."""

    def __init__(self):
        if not PADDLEOCR_AVAILABLE:
            raise ImportError(
                "PaddleOCR not available. Install with: pip install paddleocr"
            )

        self.ocr = PaddleOCR(lang="vi", use_angle_cls=True, show_log=False)

    def recognize(self, image_path: str, confidence_threshold: float = 0.6) -> str:
        """Extract text from image."""
        _ = self.ocr.ocr(image_path, cls=True)
        lines = []

        for page in result:
            if page is None:
                continue
            for line in page:
                if len(line) >= 2:
                    text, conf = line[1]
                    if conf >= confidence_threshold:
                        lines.append(text)

        return "\n".join(lines)
