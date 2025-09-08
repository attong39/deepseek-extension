"""Compression middleware for ZETA AI system.





This middleware provides response compression using gzip to reduce


bandwidth usage and improve API response times.


"""

from __future__ import annotations

import gzip
import io
import logging
import zlib
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Callable
from typing import TYPE_CHECKING, Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import Exception
import any
import app
import bool
import bytes
import call_next
import chunk
import compression_level
import dict
import e
import exclude_path
import exclude_paths
import gz_file
import hasattr
import int
import isinstance
import len
import list
import max
import memoryview
import min
import minimum_size
import path
import request
import round
import self
import set
import str
import stream
import super

if TYPE_CHECKING:
    from fastapi import FastAPI

from starlette.responses import StreamingResponse

# Setup


logger = logging.getLogger(__name__)


class CompressionMiddleware(BaseHTTPMiddleware):
    """Middleware for compressing HTTP responses."""

    # Minimum response size to compress (bytes)

    MIN_COMPRESSION_SIZE = 1024  # 1KB

    # Content types that should be compressed

    COMPRESSIBLE_TYPES = {
        "application/json",
        "application/javascript",
        "application/xml",
        "application/rss+xml",
        "application/atom+xml",
        "text/html",
        "text/css",
        "text/javascript",
        "text/xml",
        "text/plain",
        "text/csv",
        "image/svg+xml",
    }

    # Content types that should never be compressed

    NON_COMPRESSIBLE_TYPES = {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "image/bmp",
        "image/ico",
        "video/mp4",
        "video/webm",
        "audio/mp3",
        "audio/wav",
        "audio/ogg",
        "application/pdf",
        "application/zip",
        "application/gzip",
        "application/x-gzip",
        "application/x-compressed",
        "application/octet-stream",
    }

    def __init__(
        self,
        app: Any,
        minimum_size: int | None = None,
        compression_level: int = 6,
        exclude_paths: set[str] | None = None,
    ) -> None:
        super().__init__(app)

        self.minimum_size = minimum_size or self.MIN_COMPRESSION_SIZE

        self.compression_level = max(1, min(9, compression_level))

        self.exclude_paths = exclude_paths or {
            "/health",
            "/metrics",
            "/static/",
            "/assets/",
            "/favicon.ico",
        }

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request and compress response if applicable.





        Args:


            request: FastAPI request object.


            call_next: Next middleware/endpoint in chain.





        Returns:


            HTTP response (potentially compressed).


        """

        # Skip compression for excluded paths
        if self._should_exclude_path(request.url.path):
            return await call_next(request)

        # Check if client accepts gzip encoding
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding.lower():
            return await call_next(request)

        # Get response from next middleware/endpoint
        response = await call_next(request)

        # Check if response should be compressed
        if not self._should_compress_response(response):
            return response

        # Compress the response (sync helper)
        compressed_response = self._compress_response(response)

        if compressed_response:
            # Add compression headers
            compressed_response.headers["content-encoding"] = "gzip"
            compressed_response.headers["vary"] = "Accept-Encoding"

            # Remove content-length as it will change
            if "content-length" in compressed_response.headers:
                del compressed_response.headers["content-length"]

            logger.debug("Response compressed with gzip")
            return compressed_response

        return response

    def _should_exclude_path(self, path: str) -> bool:
        """Check if path should be excluded from compression.





        Args:


            path: Request path.





        Returns:


            True if path should be excluded.


        """

        return any(path.startswith(exclude_path) for exclude_path in self.exclude_paths)

    def _should_compress_response(self, response: Response) -> bool:
        """Check if response should be compressed.





        Args:


            response: HTTP response object.





        Returns:


            True if response should be compressed.


        """

        # Skip if already compressed

        if response.headers.get("content-encoding"):
            return False

        # Skip if no content

        if not hasattr(response, "body") or not response.body:
            return False

        # Check content type

        content_type = response.headers.get("content-type", "").split(";")[0].strip()

        # Skip non-compressible types

        if content_type in self.NON_COMPRESSIBLE_TYPES:
            return False

        # Only compress known compressible types

        if content_type not in self.COMPRESSIBLE_TYPES:
            # Allow compression for unknown text types

            if not content_type.startswith("text/"):
                return False

        # Check minimum size

        content_length = len(response.body) if response.body else 0

        if content_length < self.minimum_size:
            return False

        return True

    def _compress_response(self, response: Response) -> Response | None:
        """Compress response body using gzip.





        Args:


            response: HTTP response object.





        Returns:


            Compressed response or None if compression failed.


        """

        try:
            # Get response body

            if hasattr(response, "body") and response.body:
                body_content = response.body

            else:
                return None

            # Compress the content

            compressed_content = self._compress_content(body_content)

            if not compressed_content:
                return None

            # Calculate compression ratio

            original_size = len(body_content)

            compressed_size = len(compressed_content)

            compression_ratio = (1 - compressed_size / original_size) * 100

            # Only use compression if it provides significant savings

            if compression_ratio < 10:  # Less than 10% savings
                logger.debug(f"Compression savings too low: {compression_ratio:.1f}%")

                return None

            # Create new response with compressed content

            compressed_response = Response(
                content=compressed_content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type"),
            )

            # Add compression info header

            compressed_response.headers["x-compression-ratio"] = (
                f"{compression_ratio:.1f}%"
            )

            compressed_response.headers["x-original-size"] = str(original_size)

            compressed_response.headers["x-compressed-size"] = str(compressed_size)

            logger.debug(
                "Compressed response: %d -> %d bytes (%.1f%% reduction)",
                original_size,
                compressed_size,
                compression_ratio,
            )

            return compressed_response

        except Exception as e:
            logger.error(f"Compression failed: {e}")

            return None

    def _compress_content(self, content: bytes | memoryview) -> bytes | None:
        """Compress content using gzip.





        Args:


            content: Content to compress.





        Returns:


            Compressed content or None if compression failed.


        """

        try:
            # Allow memoryview or bytes; coerce to bytes for gzip
            if isinstance(content, memoryview):
                content = bytes(content)

            # Use BytesIO buffer for gzip compression
            buffer = io.BytesIO()

            with gzip.GzipFile(
                fileobj=buffer, mode="wb", compresslevel=self.compression_level
            ) as gz_file:
                gz_file.write(content)

            compressed_content = buffer.getvalue()

            return compressed_content

        except Exception as e:
            logger.error(f"Gzip compression failed: {e}")

            return None

    def get_compression_stats(self) -> dict[str, Any]:
        """Get compression statistics.





        Returns:


            Compression statistics.


        """

        return {
            "minimum_size": self.minimum_size,
            "compression_level": self.compression_level,
            "compressible_types": list(self.COMPRESSIBLE_TYPES),
            "excluded_paths": list(self.exclude_paths),
        }


class StreamingCompressionMiddleware(BaseHTTPMiddleware):
    """Middleware for compressing streaming responses."""

    def __init__(self, app: Any, compression_level: int = 6) -> None:
        super().__init__(app)

        self.compression_level = compression_level

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request and handle streaming compression.





        Args:


            request: FastAPI request object.


            call_next: Next middleware/endpoint in chain.





        Returns:


            HTTP response (potentially compressed).


        """

        # Check if client accepts gzip

        accept_encoding = request.headers.get("accept-encoding", "")

        if "gzip" not in accept_encoding.lower():
            return await call_next(request)

        response = await call_next(request)

        # Only handle streaming responses

        if not isinstance(response, StreamingResponse):
            return response

        # Check content type

        content_type = response.headers.get("content-type", "")

        if not self._is_compressible_stream(content_type):
            return response

        # Create compressed streaming response

        compressed_response = StreamingResponse(
            self._compress_stream(response.body_iterator),
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=content_type,
        )

        # Add compression headers

        compressed_response.headers["content-encoding"] = "gzip"

        compressed_response.headers["vary"] = "Accept-Encoding"

        # Remove content-length for streaming

        if "content-length" in compressed_response.headers:
            del compressed_response.headers["content-length"]

        return compressed_response

    def _is_compressible_stream(self, content_type: str) -> bool:
        """Check if streaming content type is compressible.





        Args:


            content_type: Response content type.





        Returns:


            True if content type is compressible.


        """

        compressible_stream_types = {
            "application/json",
            "text/plain",
            "text/csv",
            "application/x-ndjson",
            "text/event-stream",
        }

        base_type = content_type.split(";")[0].strip()

        return base_type in compressible_stream_types

    async def _compress_stream(
        self, stream: AsyncIterable[Any]
    ) -> AsyncIterator[bytes]:
        """Compress streaming content.





        Args:


            stream: Content stream iterator.





        Yields:


            Compressed content chunks.


        """

        # Use zlib.compressobj to stream gzip-compatible data without
        # relying on private GzipFile internals. This produces a valid
        # gzip stream: write header, compress chunks, then flush trailer.

        # Gzip header
        def _gzip_header() -> bytes:
            return b"\x1f\x8b\x08\x00" + (b"\x00" * 4) + b"\x02\xff"

        compressor = zlib.compressobj(
            level=self.compression_level,
            method=zlib.DEFLATED,
            wbits=16 + zlib.MAX_WBITS,
        )

        try:
            # Emit gzip header
            yield _gzip_header()

            async for chunk in stream:
                if not chunk:
                    continue

                # Normalize chunk types to bytes
                if isinstance(chunk, memoryview):
                    chunk_bytes = bytes(chunk)
                elif isinstance(chunk, str):
                    chunk_bytes = chunk.encode("utf8")
                elif isinstance(chunk, bytes):
                    chunk_bytes = chunk
                else:
                    try:
                        chunk_bytes = bytes(chunk)
                    except Exception:
                        # Skip unknown chunk types
                        continue

                compressed_chunk = compressor.compress(chunk_bytes)

                if compressed_chunk:
                    yield compressed_chunk

            # Finish compression
            final_chunk = compressor.flush()

            if final_chunk:
                yield final_chunk

        except Exception as e:
            logger.error(f"Stream compression failed: {e}")

            # Fall back to uncompressed if compression fails
            async for chunk in stream:
                yield chunk


def attach(app: FastAPI) -> None:
    """Attach compression middleware to FastAPI app (compat helper)."""
    app.add_middleware(CompressionMiddleware)


# Utility functions


def is_content_compressible(content_type: str, content_length: int = 0) -> bool:
    """Check if content is suitable for compression.





    Args:


        content_type: Content MIME type.


        content_length: Content size in bytes.





    Returns:


        True if content should be compressed.


    """

    # Check minimum size

    if (
        content_length > 0
        and content_length < CompressionMiddleware.MIN_COMPRESSION_SIZE
    ):
        return False

    # Check content type

    base_type = content_type.split(";")[0].strip()

    if base_type in CompressionMiddleware.NON_COMPRESSIBLE_TYPES:
        return False

    return (
        base_type in CompressionMiddleware.COMPRESSIBLE_TYPES
        or base_type.startswith("text/")
    )


def calculate_compression_savings(
    original_size: int, compressed_size: int
) -> dict[str, Any]:
    """Calculate compression savings statistics.





    Args:


        original_size: Original content size.


        compressed_size: Compressed content size.





    Returns:


        Compression statistics.


    """

    if original_size == 0:
        return {"ratio": 0, "savings_percent": 0, "savings_bytes": 0}

    savings_bytes = original_size - compressed_size

    savings_percent = (savings_bytes / original_size) * 100

    compression_ratio = compressed_size / original_size

    return {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "savings_bytes": savings_bytes,
        "savings_percent": round(savings_percent, 2),
        "compression_ratio": round(compression_ratio, 3),
    }
