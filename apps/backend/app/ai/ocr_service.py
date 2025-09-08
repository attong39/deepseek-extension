# apps/backend/app/ai/ocr_service.py
from __future__ import annotations
from typing import List
import Exception
import bool
import lines
import page
import path
import self
import str
import txt

class OCRService:
    """PaddleOCR wrapper – optional; fallback returns empty string."""
    def __init__(self) -> None:
        self._ok = False
        try:
            from paddleocr import PaddleOCR  # type: ignore
            self._ocr = PaddleOCR(use_angle_cls=True, lang="en")
            self._ok = True
        except Exception:
            self._ocr = None

    def available(self) -> bool:
        return self._ok

    def ocr_image(self, path: str) -> str:
        if not self._ok:
            return ""
        result = self._ocr.ocr(path, cls=True)  # type: ignore
        lines: List[str] = []
        for page in result:
            for _, (txt, _conf) in page:
                lines.append(txt)
        return "\n".join(lines)
