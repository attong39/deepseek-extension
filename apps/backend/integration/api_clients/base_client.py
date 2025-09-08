from __future__ import annotations

import asyncio
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

import aiohttp
import Exception
import ImportError
import TimeoutError
import ValueError
import api_key
import attempt
import base_url
import data
import dict
import e
import endpoint
import headers
import int
import max_retries
import method
import params
import range
import rate_limit
import self
import str
import timeout

try:
    from core.observability.logging import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

"""
Base API Client - Integration Layer
Provides the foundation for all external API integrations with:
- Authentication handling
- Rate limiting and retry logic
- Request/response validation
- Error handling and logging
- Performance monitoring
"""


class APIClientError(Exception):
    """Base exception for API client errors."""


class RateLimitError(APIClientError):
    """Raised when rate limit is exceeded."""


class AuthenticationError(APIClientError):
    """Raised when authentication fails."""


class BaseAPIClient(ABC):
    """
    Base class for all external API clients.
    Provides common functionality for:
    - HTTP session management
    - Authentication
    - Rate limiting
    - Error handling
    - Request/response logging
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        rate_limit: int = 60,  # requests per minute
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        """Khởi tạo BaseAPIClient.

        Args:
            base_url: Base URL của API.
            api_key: API key (từ env hoặc param).
            rate_limit: Giới hạn request per minute.
            timeout: Timeout cho requests (giây).
            max_retries: Số lần retry tối đa.

        Raises:
            ValueError: Nếu config không hợp lệ.
        """
        if not base_url:
            raise ValueError("base_url không được rỗng")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("API_KEY")
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.max_retries = max_retries
        self._requests_made = 0
        self._rate_limit_reset = datetime.now() + timedelta(minutes=1)
        self._session: aiohttp.ClientSession | None = None
        self._is_authenticated = False

    async def __aenter__(self) -> BaseAPIClient:
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.cleanup()

    async def initialize(self) -> None:
        """Initialize the API client and authenticate."""
        try:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=self._get_default_headers(),
            )
            if self.api_key:
                await self._authenticate()
            logger.info(f"✅ {self.__class__.__name__} initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize {self.__class__.__name__}: {e}")
            raise APIClientError(f"Initialization failed: {e}") from e

    async def cleanup(self) -> None:
        """Clean up resources."""
        if self._session:
            await self._session.close()

    @abstractmethod
    async def _authenticate(self) -> None:
        """Implement authentication logic for specific API."""

    @abstractmethod
    def _get_default_headers(self) -> dict[str, str]:
        """Get default headers for requests."""

    async def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        now = datetime.now()
        if now >= self._rate_limit_reset:
            self._requests_made = 0
            self._rate_limit_reset = now + timedelta(minutes=1)
        if self._requests_made >= self.rate_limit:
            wait_time = (self._rate_limit_reset - now).total_seconds()
            logger.warning(f"⏳ Rate limit reached, waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
        self._requests_made += 1

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Make HTTP request with retry logic and error handling.
        """
        if not self._session:
            raise APIClientError("Client not initialized. Use async context manager.")
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = self._get_default_headers()
        if headers:
            request_headers.update(headers)
        for attempt in range(self.max_retries + 1):
            try:
                await self._check_rate_limit()
                async with self._session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=request_headers,
                ) as response:
                    logger.debug(f"🌐 {method} {url} -> {response.status}")
                    if response.status == 429:  # Rate limited
                        if attempt < self.max_retries:
                            wait_time = 2**attempt  # Exponential backoff
                            logger.warning(f"⏳ Rate limited, retrying in {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                        raise RateLimitError("Rate limit exceeded")
                    if response.status == 401:
                        raise AuthenticationError("Authentication failed")
                    if response.status >= 400:
                        error_text = await response.text()
                        raise APIClientError(
                            f"API error {response.status}: {error_text}"
                        )
                    try:
                        return await response.json()
                    except json.JSONDecodeError:
                        return {"text": await response.text()}
            except (TimeoutError, aiohttp.ClientError) as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    logger.warning(f"🔄 Request failed, retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                    continue
                raise APIClientError(
                    f"Request failed after {self.max_retries} retries: {e}"
                )
        raise APIClientError("Max retries exceeded")

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make GET request."""
        return await self._make_request("GET", endpoint, params=params, headers=headers)

    async def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make POST request."""
        return await self._make_request("POST", endpoint, data=data, headers=headers)

    async def put(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make PUT request."""
        return await self._make_request("PUT", endpoint, data=data, headers=headers)

    async def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make DELETE request."""
        return await self._make_request("DELETE", endpoint, headers=headers)

    async def health_check(self) -> dict[str, Any]:
        """Check if the API is healthy and accessible."""
        try:
            response = await self.get("/health")
            return {
                "status": "healthy",
                "authenticated": self._is_authenticated,
                "base_url": self.base_url,
                "response": response,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "base_url": self.base_url,
            }


__all__ = [
    "APIClientError",
    "AuthenticationError",
    "BaseAPIClient",
    "RateLimitError",
    "error_text",
    "logger",
    "now",
    "request_headers",
    "response",
    "url",
    "wait_time",
]
