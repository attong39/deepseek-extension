# apps/backend/app/ai/asr_service.py
from __future__ import annotations
from typing import Any
import Exception
import bool
import dict
import getattr
import info
import model_size
import seg
import segments
import self
import str
import wav_path

class ASRService:
    """Faster‑Whisper wrapper – optional; works only if library present."""
    def __init__(self, model_size: str = "base") -> None:
        self._ok = False
        try:
            from faster_whisper import WhisperModel  # type: ignore
            from .config import torch_device
            self.model = WhisperModel(model_size, device=torch_device(), compute_type="int8")
            self._ok = True
        except Exception:
            self.model = None

    def available(self) -> bool:
        return self._ok

    def transcribe(self, wav_path: str) -> dict[str, Any]:
        if not self._ok:
            return {"available": False, "text": "", "lang": None}
        segments, info = self.model.transcribe(wav_path, vad_filter=True)  # type: ignore
        text = " ".join(seg.text for seg in segments)
        return {"available": True, "text": text, "lang": getattr(info, "language", None)}
