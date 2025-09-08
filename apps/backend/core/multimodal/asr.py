"""
Vietnamese ASR using Whisper.
"""

from __future__ import annotations
import ImportError
import audio_path
import model_size
import result
import self
import str

try:
    import whisper

    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


class VietASR:
    """Vietnamese speech recognition."""

    def __init__(self, model_size: str = "small"):
        if not WHISPER_AVAILABLE:
            raise ImportError(
                "Whisper not available. Install with: pip install openai-whisper"
            )

        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio to Vietnamese text."""
        _ = self.model.transcribe(audio_path, language="vi")
        return result["text"].strip()
