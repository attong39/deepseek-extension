"""
OpenAI Whisper ASR Adapter Implementation.

Provides concrete implementation of ASRPort using OpenAI Whisper API.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import Any

from apps.backend.core.domain.ports.asr import ASRPort
import Exception
import ImportError
import api_key
import audio_chunk
import audio_data
import audio_stream
import base_url
import bytearray
import bytes
import dict
import e
import float
import format
import hasattr
import isinstance
import language
import len
import list
import message
import model
import original_error
import self
import str
import super
import timeout
import transcription_id

logger = logging.getLogger(__name__)


class ASRError(Exception):
    """ASR-specific error."""

    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(message)
        self.original_error = original_error


class WhisperASRAdapter(ASRPort):
    """
    OpenAI Whisper implementation của ASRPort.

    Features:
    - High-quality transcription
    - Multi-language support
    - Real-time streaming (via chunking)
    - Automatic language detection
    """

    def __init__(
        self,
        api_key: str,
        model: str = "whisper-1",
        base_url: str | None = None,
        timeout: float = 30.0,
    ):
        """
        Initialize Whisper ASR adapter.

        Args:
            api_key: OpenAI API key
            model: Whisper model name (whisper-1)
            base_url: Custom API base URL (optional)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.timeout = timeout
        self._client: Any = None  # Lazy-loaded OpenAI client

    async def _get_client(self) -> Any:
        """Lazy load OpenAI client."""
        if self._client is None:
            try:
                import openai

                self._client = openai.AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    timeout=self.timeout,
                )
            except ImportError as e:
                raise ASRError(
                    "OpenAI package not installed. Run: pip install openai"
                ) from e
        return self._client

    async def transcribe_audio(
        self, audio_data: bytes, language: str | None = None, format: str = "wav"
    ) -> str:
        """
        Transcribe audio data to text using Whisper.

        Args:
            audio_data: Raw audio bytes
            language: Language code (en, vi, ja, etc.) or None for auto-detect
            format: Audio format (wav, mp3, m4a, webm, mp4)

        Returns:
            Transcribed text

        Raises:
            ASRError: When transcription fails
        """
        try:
            client = await self._get_client()

            # Create file-like object from bytes
            import io

            audio_file = io.BytesIO(audio_data)
            audio_file.name = f"audio.{format}"  # Required by OpenAI API

            # Prepare API parameters
            params = {
                "file": audio_file,
                "model": self.model,
                "response_format": "text",
            }

            if language:
                params["language"] = language

            # Call Whisper API
            response = await client.audio.transcriptions.create(**params)

            # Handle different response formats
            if isinstance(response, str):
                return response.strip()
            else:
                return str(response).strip()

        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            raise ASRError(f"Transcription failed: {e}", e) from e

    async def transcribe_streaming(
        self, audio_stream: AsyncIterator[bytes], language: str | None = None
    ) -> AsyncIterator[str]:
        """
        Streaming transcription by batching audio chunks.

        Note: OpenAI Whisper doesn't support true streaming, so we batch chunks
        and transcribe when we have sufficient data.

        Args:
            audio_stream: Stream of audio chunks
            language: Language code or None for auto-detect

        Yields:
            Partial transcription results
        """
        buffer = bytearray()
        chunk_size = 1024 * 1024  # 1MB chunks for processing

        try:
            async for audio_chunk in audio_stream:
                buffer.extend(audio_chunk)

                # Process when buffer is large enough
                if len(buffer) >= chunk_size:
                    try:
                        # Transcribe current buffer
                        transcription = await self.transcribe_audio(
                            bytes(buffer), language=language, format="wav"
                        )

                        if transcription.strip():
                            yield transcription

                        # Clear buffer (or keep overlap for continuity)
                        buffer = bytearray()

                    except ASRError as e:
                        logger.warning(f"Streaming chunk transcription failed: {e}")
                        # Continue with next chunk
                        buffer = bytearray()

            # Process remaining buffer
            if buffer:
                try:
                    transcription = await self.transcribe_audio(
                        bytes(buffer), language=language, format="wav"
                    )
                    if transcription.strip():
                        yield transcription
                except ASRError as e:
                    logger.warning(f"Final chunk transcription failed: {e}")

        except Exception as e:
            logger.error(f"Streaming transcription failed: {e}")
            raise ASRError(f"Streaming transcription failed: {e}", e) from e

    async def get_supported_languages(self) -> list[str]:
        """
        Get supported language codes for Whisper.

        Returns:
            List of ISO language codes supported by Whisper
        """
        # Whisper supports 99 languages - major ones listed here
        return [
            "en",  # English
            "zh",  # Chinese
            "de",  # German
            "es",  # Spanish
            "ru",  # Russian
            "ko",  # Korean
            "fr",  # French
            "ja",  # Japanese
            "pt",  # Portuguese
            "tr",  # Turkish
            "pl",  # Polish
            "ca",  # Catalan
            "nl",  # Dutch
            "ar",  # Arabic
            "sv",  # Swedish
            "it",  # Italian
            "id",  # Indonesian
            "hi",  # Hindi
            "fi",  # Finnish
            "vi",  # Vietnamese
            "he",  # Hebrew
            "uk",  # Ukrainian
            "el",  # Greek
            "ms",  # Malay
            "cs",  # Czech
            "ro",  # Romanian
            "da",  # Danish
            "hu",  # Hungarian
            "ta",  # Tamil
            "no",  # Norwegian
            "th",  # Thai
            "ur",  # Urdu
            "hr",  # Croatian
            "bg",  # Bulgarian
            "lt",  # Lithuanian
            "la",  # Latin
            "mi",  # Maori
            "ml",  # Malayalam
            "cy",  # Welsh
            "sk",  # Slovak
            "te",  # Telugu
            "fa",  # Persian
            "lv",  # Latvian
            "bn",  # Bengali
            "sr",  # Serbian
            "az",  # Azerbaijani
            "sl",  # Slovenian
            "kn",  # Kannada
            "et",  # Estonian
            "mk",  # Macedonian
            "br",  # Breton
            "eu",  # Basque
            "is",  # Icelandic
            "hy",  # Armenian
            "ne",  # Nepali
            "mn",  # Mongolian
            "bs",  # Bosnian
            "kk",  # Kazakh
            "sq",  # Albanian
            "sw",  # Swahili
            "gl",  # Galician
            "mr",  # Marathi
            "pa",  # Punjabi
            "si",  # Sinhala
            "km",  # Khmer
            "sn",  # Shona
            "yo",  # Yoruba
            "so",  # Somali
            "af",  # Afrikaans
            "oc",  # Occitan
            "ka",  # Georgian
            "be",  # Belarusian
            "tg",  # Tajik
            "sd",  # Sindhi
            "gu",  # Gujarati
            "am",  # Amharic
            "yi",  # Yiddish
            "lo",  # Lao
            "uz",  # Uzbek
            "fo",  # Faroese
            "ht",  # Haitian Creole
            "ps",  # Pashto
            "tk",  # Turkmen
            "nn",  # Nynorsk
            "mt",  # Maltese
            "sa",  # Sanskrit
            "lb",  # Luxembourgish
            "my",  # Myanmar
            "bo",  # Tibetan
            "tl",  # Tagalog
            "mg",  # Malagasy
            "as",  # Assamese
            "tt",  # Tatar
            "haw",  # Hawaiian
            "ln",  # Lingala
            "ha",  # Hausa
            "ba",  # Bashkir
            "jw",  # Javanese
            "su",  # Sundanese
        ]

    async def detect_language(self, audio_data: bytes) -> str:
        """
        Detect language from audio using Whisper.

        Args:
            audio_data: Raw audio bytes

        Returns:
            Detected language code (ISO 639-1)
        """
        try:
            client = await self._get_client()

            # Create file-like object
            import io

            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"

            # Use Whisper API for language detection
            response = await client.audio.transcriptions.create(
                file=audio_file,
                model=self.model,
                response_format="verbose_json",  # Include language detection
            )

            # Extract language from response
            if hasattr(response, "language"):
                return response.language
            elif isinstance(response, dict) and "language" in response:
                return response["language"]
            else:
                # Fallback: try transcription with language detection
                return "en"  # Default to English if detection fails

        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            raise ASRError(f"Language detection failed: {e}", e) from e

    async def reduce_noise(self, audio_data: bytes) -> bytes:
        """
        Basic noise reduction preprocessing.

        Note: OpenAI Whisper has built-in noise robustness, but we can add
        basic preprocessing here if needed.

        Args:
            audio_data: Raw audio with potential noise

        Returns:
            Processed audio bytes (currently pass-through)
        """
        # For OpenAI Whisper, we rely on its built-in noise robustness
        # Advanced noise reduction would require additional audio processing libraries
        logger.debug("Noise reduction: Using Whisper's built-in noise handling")
        return audio_data

    async def get_confidence_score(self, transcription_id: str) -> float:
        """
        Get confidence score for transcription.

        Note: OpenAI Whisper API doesn't directly provide confidence scores.
        This is a placeholder for future implementation or alternative providers.

        Args:
            transcription_id: Identifier for transcription request

        Returns:
            Confidence score (0.0 - 1.0), currently returns 0.8 as default
        """
        # OpenAI Whisper doesn't provide confidence scores via API
        # For now, return a reasonable default
        logger.debug(
            f"Confidence score requested for {transcription_id}: using default 0.8"
        )
        return 0.8
