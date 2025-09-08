"""
OCR (Optical Character Recognition) - CPU-first with alternatives

Primary: OpenCV for image processing (always available)
Optional: PaddleOCR (good but heavy), Tesseract (lightweight alternative)
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any

import numpy as np
import Exception
import FileNotFoundError
import ImportError
import RuntimeError
import ValueError
import bool
import box
import conf
import confidence
import dict
import e
import enumerate
import i
import int
import language
import line
import preprocess
import print
import self
import str
import use_gpu

logger = logging.getLogger(__name__)

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    logger.warning("OpenCV not available")
    OPENCV_AVAILABLE = False

try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    logger.warning("PaddleOCR not available")
    PADDLEOCR_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    logger.warning("Tesseract not available")
    TESSERACT_AVAILABLE = False


class OCREngine:
    """OCR engine with multiple backends."""
    
    def __init__(
        self,
        backend: str = "auto",
        language: str = "en",
        use_gpu: bool = False,
    ) -> None:
        self.language = language
        self.use_gpu = use_gpu and os.getenv("ZETA_USE_GPU") == "1"
        
        # Select backend
        if backend == "auto":
            backend = self._select_backend()
        
        self.backend = backend
        self._initialize_backend()
        
        logger.info(f"OCR engine initialized with {backend} backend")
    
    def _select_backend(self) -> str:
        """Auto-select the best available backend."""
        if PADDLEOCR_AVAILABLE:
            return "paddleocr"
        elif TESSERACT_AVAILABLE:
            return "tesseract"
        else:
            raise RuntimeError("No OCR backend available. Install paddleocr or pytesseract.")
    
    def _initialize_backend(self) -> None:
        """Initialize the selected backend."""
        if self.backend == "paddleocr":
            if not PADDLEOCR_AVAILABLE:
                raise RuntimeError("PaddleOCR not available")
            
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.language,
                use_gpu=self.use_gpu,
                show_log=False,
            )
            
        elif self.backend == "tesseract":
            if not TESSERACT_AVAILABLE:
                raise RuntimeError("Tesseract not available")
            
            # Tesseract is initialized per-call
            self.ocr = None
            
        else:
            raise ValueError(f"Unknown OCR backend: {self.backend}")
    
    def extract_text(
        self,
        image_path: str | Path,
        preprocess: bool = True,
    ) -> dict[str, Any]:
        """Extract text from image."""
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        logger.info(f"Extracting text from: {image_path}")
        
        try:
            if self.backend == "paddleocr":
                return self._extract_paddleocr(image_path, preprocess)
            elif self.backend == "tesseract":
                return self._extract_tesseract(image_path, preprocess)
            else:
                raise ValueError(f"Unknown backend: {self.backend}")
                
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise
    
    def _extract_paddleocr(
        self,
        image_path: Path,
        preprocess: bool,
    ) -> dict[str, Any]:
        """Extract text using PaddleOCR."""
        if preprocess:
            image = self._preprocess_image(str(image_path))
        else:
            image = str(image_path)
        
        result = self.ocr.ocr(image, cls=True)
        
        # Process results
        texts = []
        boxes = []
        confidences = []
        
        if result and result[0]:
            for line in result[0]:
                box, (text, confidence) = line
                texts.append(text)
                boxes.append(box)
                confidences.append(confidence)
        
        full_text = "\n".join(texts)
        
        return {
            "text": full_text,
            "lines": texts,
            "boxes": boxes,
            "confidences": confidences,
            "backend": "paddleocr",
        }
    
    def _extract_tesseract(
        self,
        image_path: Path,
        preprocess: bool,
    ) -> dict[str, Any]:
        """Extract text using Tesseract."""
        if not OPENCV_AVAILABLE:
            raise RuntimeError("OpenCV required for image preprocessing")
        
        # Load and preprocess image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        if preprocess:
            image = self._preprocess_opencv(image)
        
        # Extract text
        text = pytesseract.image_to_string(image, lang=self.language)
        
        # Get detailed data (boxes, confidences)
        data = pytesseract.image_to_data(
            image,
            lang=self.language,
            output_type=pytesseract.Output.DICT,
        )
        
        # Filter out empty text
        filtered_texts = []
        filtered_confidences = []
        for i, conf in enumerate(data['conf']):
            if int(conf) > 0 and data['text'][i].strip():
                filtered_texts.append(data['text'][i])
                filtered_confidences.append(int(conf))
        
        return {
            "text": text.strip(),
            "lines": filtered_texts,
            "boxes": [],  # Would need to reconstruct from data
            "confidences": filtered_confidences,
            "backend": "tesseract",
        }
    
    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for better OCR."""
        if not OPENCV_AVAILABLE:
            return image_path  # Return path if OpenCV not available
        
        image = cv2.imread(image_path)
        if image is None:
            return image_path
        
        return self._preprocess_opencv(image)
    
    def _preprocess_opencv(self, image: np.ndarray) -> np.ndarray:
        """Apply OpenCV preprocessing."""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        denoised = cv2.medianBlur(gray, 3)
        
        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )
        
        return thresh


# Factory function
def create_ocr_engine(
    backend: str = "auto",
    language: str = "en",
    use_gpu: bool = False,
) -> OCREngine:
    """Create an OCR engine with specified configuration."""
    return OCREngine(backend, language, use_gpu)


# Test function
def _test_ocr():
    """Test the OCR engine."""
    try:
        engine = create_ocr_engine()
        print(f"OCR engine created with {engine.backend} backend")
        
        # This would need an actual image file
        # result = engine.extract_text("sample.png")
        # print(f"Extracted: {result['text']}")
        
    except Exception as e:
        print(f"OCR test failed: {e}")


if __name__ == "__main__":
    _test_ocr()
