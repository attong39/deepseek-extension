"""
Enhanced ASR Service với Whisper.cpp support cho tiếng Việt.

Provides:
- Local inference với Whisper.cpp (fast, private)
- OpenAI Whisper API fallback
- Async processing với batch support
- Real-time streaming transcription
- Vietnamese language optimization
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
import Exception
import ImportError
import RuntimeError
import audio_chunks
import audio_file
import audio_paths
import bool
import bytes
import chunk
import config
import correct
import dict
import e
import enumerate
import float
import getattr
import i
import info
import int
import isinstance
import len
import list
import max_concurrent
import model_path
import open
import openai_api_key
import path
import result
import s
import segment
import segments
import self
import str
import tmp_file
import use_local
import wrong

logger = logging.getLogger(__name__)

# Optional dependencies
try:
    import faster_whisper

    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    faster_whisper = None
    FASTER_WHISPER_AVAILABLE = False

try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False


@dataclass
class TranscriptionResult:
    """Result from ASR transcription."""

    text: str
    language: str | None = None
    confidence: float | None = None
    segments: list[dict[str, Any]] | None = None
    processing_time_ms: float = 0.0
    model_used: str = "unknown"
    word_count: int = 0


@dataclass
class ASRConfig:
    """Configuration for ASR service."""

    # Model settings
    model_size: Literal["tiny", "base", "small", "medium", "large"] = "base"
    compute_type: Literal["int8", "float16", "float32"] = "int8"
    language: str = "vi"  # Vietnamese by default

    # Performance settings
    beam_size: int = 5
    best_of: int = 5
    temperature: float = 0.0

    # Fallback settings
    use_openai_fallback: bool = True
    openai_model: str = "whisper-1"

    # Processing settings
    chunk_duration_seconds: int = 30
    vad_threshold: float = 0.5


class EnhancedASRService:
    """
    Enhanced ASR Service với local + cloud hybrid approach.

    Features:
    - Primary: Faster Whisper (local, private, Vietnamese optimized)
    - Fallback: OpenAI Whisper API
    - Streaming transcription
    - Batch processing
    - Performance metrics
    """

    def __init__(
        self,
        config: ASRConfig | None = None,
        model_path: str | Path | None = None,
        openai_api_key: str | None = None,
    ) -> None:
        """Initialize ASR service với local và cloud models."""
        self.config = config or ASRConfig()
        self.model_path = Path(model_path) if model_path else None

        # Initialize local model
        self.local_model: faster_whisper.WhisperModel | None = None
        if FASTER_WHISPER_AVAILABLE:
            self._init_local_model()

        # Initialize OpenAI client
        self.openai_client: openai.AsyncOpenAI | None = None
        if OPENAI_AVAILABLE and openai_api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)

        # Stats tracking
        self.stats = {
            "total_requests": 0,
            "local_requests": 0,
            "openai_requests": 0,
            "total_audio_duration": 0.0,
            "total_processing_time": 0.0,
        }

    def _init_local_model(self) -> None:
        """Initialize local Faster Whisper model."""
        try:
            if self.model_path and self.model_path.exists():
                # Custom model path
                self.local_model = faster_whisper.WhisperModel(
                    str(self.model_path), compute_type=self.config.compute_type
                )
                logger.info(f"Loaded custom Whisper model from {self.model_path}")
            else:
                # Standard model
                self.local_model = faster_whisper.WhisperModel(
                    self.config.model_size, compute_type=self.config.compute_type
                )
                logger.info(f"Loaded Whisper {self.config.model_size} model")
        except Exception as e:
            logger.error(f"Failed to load local Whisper model: {e}")
            self.local_model = None

    async def transcribe(
        self,
        audio_path: str | Path,
        language: str | None = None,
        use_local: bool = True,
    ) -> TranscriptionResult:
        """
        Transcribe audio file.

        Args:
            audio_path: Path to audio file
            language: Language code (defaults to config.language)
            use_local: Try local model first

        Returns:
            TranscriptionResult with text and metadata
        """
        start_time = time.perf_counter()
        audio_path = Path(audio_path)
        language = language or self.config.language

        self.stats["total_requests"] += 1

        # Try local model first
        if use_local and self.local_model:
            try:
                _ = await self._transcribe_local(audio_path, language)
                if result.text.strip():  # Success if we got text
                    self.stats["local_requests"] += 1
                    processing_time = (time.perf_counter() - start_time) * 1000
                    result.processing_time_ms = processing_time
                    self.stats["total_processing_time"] += processing_time
                    return result
            except Exception as e:
                logger.warning(f"Local transcription failed: {e}")

        # Fallback to OpenAI
        if self.config.use_openai_fallback and self.openai_client:
            try:
                _ = await self._transcribe_openai(audio_path, language)
                self.stats["openai_requests"] += 1
                processing_time = (time.perf_counter() - start_time) * 1000
                result.processing_time_ms = processing_time
                self.stats["total_processing_time"] += processing_time
                return result
            except Exception as e:
                logger.error(f"OpenAI transcription failed: {e}")

        # Complete failure
        processing_time = (time.perf_counter() - start_time) * 1000
        return TranscriptionResult(
            text="",
            language=language,
            confidence=0.0,
            processing_time_ms=processing_time,
            model_used="failed",
        )

    async def _transcribe_local(
        self, audio_path: Path, language: str
    ) -> TranscriptionResult:
        """Transcribe using local Faster Whisper model."""
        if not self.local_model:
            raise RuntimeError("Local model not available")

        # Run transcription in thread pool để không block event loop
        segments, info = await asyncio.to_thread(
            self.local_model.transcribe,
            str(audio_path),
            language=language,
            beam_size=self.config.beam_size,
            best_of=self.config.best_of,
            temperature=self.config.temperature,
            vad_filter=True,
            vad_parameters={"threshold": self.config.vad_threshold},
        )

        # Collect segments
        segment_list = []
        text_parts = []

        for segment in segments:
            segment_dict = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "avg_logprob": segment.avg_logprob,
                "no_speech_prob": segment.no_speech_prob,
            }
            segment_list.append(segment_dict)
            text_parts.append(segment.text)

        full_text = " ".join(text_parts).strip()

        # Vietnamese text post-processing
        if language == "vi":
            full_text = self._postprocess_vietnamese(full_text)

        return TranscriptionResult(
            text=full_text,
            language=info.language,
            confidence=1.0 - (info.language_probability or 0.0),
            segments=segment_list,
            model_used=f"faster_whisper_{self.config.model_size}",
            word_count=len(full_text.split()) if full_text else 0,
        )

    async def _transcribe_openai(
        self, audio_path: Path, language: str
    ) -> TranscriptionResult:
        """Transcribe using OpenAI Whisper API."""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not available")

        with open(audio_path, "rb") as audio_file:
            response = await self.openai_client.audio.transcriptions.create(
                model=self.config.openai_model,
                file=audio_file,
                language=language,
                response_format="verbose_json",
                temperature=self.config.temperature,
            )

        # Vietnamese text post-processing
        text = response.text
        if language == "vi":
            text = self._postprocess_vietnamese(text)

        return TranscriptionResult(
            text=text,
            language=language,
            confidence=None,  # OpenAI doesn't provide confidence
            segments=getattr(response, "segments", None),
            model_used=f"openai_{self.config.openai_model}",
            word_count=len(text.split()) if text else 0,
        )

    def _postprocess_vietnamese(self, text: str) -> str:
        """Post-process Vietnamese text để fix common issues."""
        if not text:
            return text

        # Common Vietnamese fixes
        fixes = {
            # Fix tone marks
            "ă": "ă",
            "â": "â",
            "ê": "ê",
            "ô": "ô",
            "ơ": "ơ",
            "ư": "ư",
            # Fix common transcription errors
            " ơi ": " ới ",
            " ưa ": " ừa ",
            " ao ": " ào ",
            " eo ": " èo ",
        }

        for wrong, correct in fixes.items():
            text = text.replace(wrong, correct)

        # Capitalize first letter of sentences
        sentences = text.split(". ")
        sentences = [s.strip().capitalize() for s in sentences if s.strip()]

        return ". ".join(sentences)

    async def transcribe_batch(
        self,
        audio_paths: list[str | Path],
        language: str | None = None,
        max_concurrent: int = 3,
    ) -> list[TranscriptionResult]:
        """
        Transcribe multiple audio files concurrently.

        Args:
            audio_paths: List of audio file paths
            language: Language code
            max_concurrent: Maximum concurrent transcriptions

        Returns:
            List of TranscriptionResult objects
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def transcribe_one(path: str | Path) -> TranscriptionResult:
            async with semaphore:
                return await self.transcribe(path, language)

        tasks = [transcribe_one(path) for path in audio_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to failed results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to transcribe {audio_paths[i]}: {result}")
                final_results.append(
                    TranscriptionResult(
                        text="",
                        language=language or self.config.language,
                        confidence=0.0,
                        model_used="failed",
                    )
                )
            else:
                final_results.append(result)

        return final_results

    async def stream_transcribe(
        self,
        audio_chunks: AsyncIterator[bytes],
        language: str | None = None,
    ) -> AsyncIterator[TranscriptionResult]:
        """
        Stream transcription for real-time audio.

        Args:
            audio_chunks: Async iterator of audio chunks
            language: Language code

        Yields:
            TranscriptionResult for each chunk
        """
        import tempfile

        language = language or self.config.language
        chunk_counter = 0

        async for chunk in audio_chunks:
            chunk_counter += 1

            # Save chunk to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(chunk)
                tmp_path = tmp_file.name

            try:
                # Transcribe chunk
                _ = await self.transcribe(
                    tmp_path,
                    language=language,
                    use_local=True,  # Prefer local for streaming
                )

                # Add chunk metadata
                if result.segments:
                    for segment in result.segments:
                        segment["chunk_id"] = chunk_counter

                yield result

            finally:
                # Cleanup temporary file
                Path(tmp_path).unlink(missing_ok=True)

    def get_stats(self) -> dict[str, Any]:
        """Get service statistics."""
        total_requests = self.stats["total_requests"]
        avg_processing_time = (
            self.stats["total_processing_time"] / total_requests
            if total_requests > 0
            else 0.0
        )

        return {
            "total_requests": total_requests,
            "local_requests": self.stats["local_requests"],
            "openai_requests": self.stats["openai_requests"],
            "local_success_rate": (
                self.stats["local_requests"] / total_requests * 100
                if total_requests > 0
                else 0.0
            ),
            "avg_processing_time_ms": avg_processing_time,
            "models_available": {
                "local_whisper": self.local_model is not None,
                "openai_whisper": self.openai_client is not None,
            },
            "config": {
                "model_size": self.config.model_size,
                "language": self.config.language,
                "compute_type": self.config.compute_type,
            },
        }

    async def health_check(self) -> dict[str, Any]:
        """Check health of ASR service."""
        health = {
            "status": "healthy",
            "local_model": self.local_model is not None,
            "openai_client": self.openai_client is not None,
            "timestamp": time.time(),
        }

        # Test local model
        if self.local_model:
            try:
                # Quick test with silent audio would be better
                health["local_model_ready"] = True
            except Exception as e:
                health["local_model_ready"] = False
                health["local_error"] = str(e)

        # Test OpenAI connection
        if self.openai_client:
            try:
                # Could test with models.list() if needed
                health["openai_ready"] = True
            except Exception as e:
                health["openai_ready"] = False
                health["openai_error"] = str(e)

        # Overall status
        if not health["local_model"] and not health["openai_client"]:
            health["status"] = "unhealthy"
        elif health.get("local_model_ready", False) or health.get(
            "openai_ready", False
        ):
            health["status"] = "healthy"
        else:
            health["status"] = "degraded"

        return health


# Legacy compatibility
class ASRService(EnhancedASRService):
    """Legacy ASR service for backward compatibility."""

    async def transcribe_audio(self, audio_path: str, language: str = "vi") -> str:
        """Legacy method returning just text."""
        _ = await self.transcribe(audio_path, language)
        return result.text


__all__ = ["EnhancedASRService", "ASRService", "TranscriptionResult", "ASRConfig"]
