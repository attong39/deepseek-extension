"""
ASR (Automatic Speech Recognition) - CPU-first, GPU-ready

Uses Faster-Whisper for transcription with automatic device detection.
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any
import Exception
import FileNotFoundError
import ImportError
import RuntimeError
import beam_size
import bool
import chunk_length
import compute_type
import dict
import e
import hasattr
import info
import int
import language
import len
import list
import model_size
import print
import segment
import segments
import self
import str
import vad_filter

logger = logging.getLogger(__name__)

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    logger.warning("faster-whisper not available")
    WHISPER_AVAILABLE = False


class ASREngine:
    """Automatic Speech Recognition engine."""
    
    def __init__(
        self,
        model_size: str = "base",
        device: str | None = None,
        compute_type: str = "int8",
    ) -> None:
        if not WHISPER_AVAILABLE:
            raise RuntimeError("faster-whisper not installed. Install with: uv add faster-whisper")
        
        self.model_size = model_size
        self.compute_type = compute_type
        
        # Auto-detect device
        if device is None:
            device = self._get_device()
        
        self.device = device
        logger.info(f"Initializing ASR engine on {device}")
        
        try:
            self.model = WhisperModel(
                model_size,
                device=device,
                compute_type=compute_type,
            )
            logger.info(f"Loaded Whisper model: {model_size}")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def _get_device(self) -> str:
        """Auto-detect optimal device."""
        if os.getenv("ZETA_USE_GPU") == "1":
            try:
                import torch
                if torch.cuda.is_available():
                    logger.info("GPU detected and enabled for ASR")
                    return "cuda"
                else:
                    logger.warning("ZETA_USE_GPU=1 but no CUDA available for ASR")
            except ImportError:
                logger.warning("PyTorch not available for ASR")
        
        return "cpu"
    
    def transcribe(
        self,
        audio_path: str | Path,
        language: str | None = None,
        vad_filter: bool = True,
        beam_size: int = 5,
    ) -> dict[str, Any]:
        """Transcribe audio file to text."""
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        logger.info(f"Transcribing audio: {audio_path}")
        
        try:
            segments, info = self.model.transcribe(
                str(audio_path),
                language=language,
                vad_filter=vad_filter,
                beam_size=beam_size,
            )
            
            # Process segments
            segments_list = []
            full_text = []
            
            for segment in segments:
                segment_data = {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                    "avg_logprob": segment.avg_logprob,
                    "no_speech_prob": segment.no_speech_prob,
                }
                segments_list.append(segment_data)
                full_text.append(segment.text.strip())
            
            result = {
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "text": " ".join(full_text),
                "segments": segments_list,
                "vad_options": {
                    "onset": info.vad_options.onset if hasattr(info, 'vad_options') else None,
                    "offset": info.vad_options.offset if hasattr(info, 'vad_options') else None,
                } if hasattr(info, 'vad_options') else None,
            }
            
            logger.info(f"Transcription completed: {len(segments_list)} segments, {info.duration:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    def transcribe_stream(
        self,
        audio_path: str | Path,
        chunk_length: int = 30,
    ) -> list[dict[str, Any]]:
        """Transcribe audio in chunks (for long files)."""
        audio_path = Path(audio_path)
        
        logger.info(f"Stream transcribing audio: {audio_path}")
        
        try:
            segments, _ = self.model.transcribe(
                str(audio_path),
                chunk_length=chunk_length,
            )
            
            results = []
            for segment in segments:
                results.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                })
            
            logger.info(f"Stream transcription completed: {len(results)} chunks")
            return results
            
        except Exception as e:
            logger.error(f"Stream transcription failed: {e}")
            raise


# Factory function
def create_asr_engine(
    model_size: str = "base",
    device: str | None = None,
    compute_type: str = "int8",
) -> ASREngine:
    """Create an ASR engine with specified configuration."""
    return ASREngine(model_size, device, compute_type)


# Test function
def _test_asr():
    """Test the ASR engine with a sample file."""
    if not WHISPER_AVAILABLE:
        print("Whisper not available for testing")
        return
    
    engine = create_asr_engine()
    
    # This would need an actual audio file
    # result = engine.transcribe("sample.wav")
    # print(f"Transcribed: {result['text']}")
    
    print("ASR engine created successfully")


if __name__ == "__main__":
    _test_asr()
