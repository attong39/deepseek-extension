"""Ollama Python Client for Zeta AI Agent

Contract
- All public methods return OllamaResponse with fields: success: bool, data: Any, error: str
- Health check returns data with at least: {"version": str, "model_count": int}
- Errors are mapped to OllamaError subclasses where appropriate
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, cast
import BaseException
import Exception
import ImportError
import attempt
import bool
import config
import data_any
import dict
import e
import endpoint
import exc
import float
import int
import isinstance
import json_data
import kwargs
import len
import list
import messages
import method
import model
import model_count
import ok_t
import ok_v
import options
import payload
import prompt
import property
import range
import sc_t
import sc_v
import self
import str
import stream
import tuple
import type

try:
    import httpx
except ImportError as exc:
    raise ImportError("httpx is required: pip install httpx") from exc


logger = logging.getLogger(__name__)


@dataclass
class OllamaConfig:
    """Configuration for Ollama client"""

    host: str = "http://localhost:11434"
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0


class OllamaError(Exception):
    """Base exception for Ollama errors"""

    pass


class OllamaConnectionError(OllamaError):
    """Connection error"""

    pass


class OllamaTimeoutError(OllamaError):
    """Timeout error"""

    pass


@dataclass
class OllamaResponse:
    """Response wrapper"""

    success: bool
    data: Any = None
    error: str = ""


class OllamaClient:
    """Async Ollama client"""

    def __init__(self, config: OllamaConfig | None = None):
        self.config = config or OllamaConfig()
        self._client: httpx.AsyncClient | None = None
        self._healthy = False

    async def __aenter__(self) -> "OllamaClient":
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: type | None, exc_val: BaseException | None, exc_tb: Any | None
    ) -> None:
        """Async context manager exit"""
        await self.close()

    async def connect(self) -> None:
        """Connect to Ollama service"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.config.host, timeout=self.config.timeout
            )

        # Test connection
        try:
            response = await self._request("GET", "/api/version")
            if response.status_code == 200:
                self._healthy = True
                logger.info("Connected to Ollama service")
            else:
                self._healthy = False
                logger.warning(f"Ollama service returned status {response.status_code}")
        except Exception as e:
            self._healthy = False
            logger.error(f"Failed to connect to Ollama: {e}")
            raise OllamaConnectionError(f"Failed to connect: {e}") from e

    async def close(self) -> None:
        """Close connection"""
        if self._client:
            await self._client.aclose()
            self._client = None
        self._healthy = False

    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make HTTP request with retry logic"""
        if not self._client:
            raise OllamaConnectionError("Client not connected")

        last_error: OllamaError | None = None

        for attempt in range(self.config.max_retries):
            try:
                response = await self._client.request(
                    method, endpoint, json=json_data, **kwargs
                )
                return response

            except httpx.TimeoutException as e:
                last_error = OllamaTimeoutError(f"Request timeout: {e}")
            except httpx.ConnectError as e:
                last_error = OllamaConnectionError(f"Connection failed: {e}")
            except Exception as e:
                last_error = OllamaError(f"Request failed: {e}")

            if attempt < self.config.max_retries - 1:
                await asyncio.sleep(self.config.retry_delay * (attempt + 1))

        if last_error:
            raise last_error
        raise OllamaError("Request failed after all retries")

    def _to_ollama_response(self, response: httpx.Response) -> OllamaResponse:
        """Convert httpx.Response to OllamaResponse"""
        try:
            data = response.json()
        except Exception:
            data = None
        success = 200 <= response.status_code < 300
        error = "" if success else f"HTTP {response.status_code}"
        return OllamaResponse(success=success, data=data, error=error)

    async def generate(
        self, model: str, prompt: str, stream: bool = False, **options: Any
    ) -> OllamaResponse:
        """Generate text completion"""
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **options,
        }

        response = await self._request("POST", "/api/generate", json_data=payload)
        return self._to_ollama_response(response)

    async def chat(
        self,
        model: str,
        messages: list[dict[str, str]],
        stream: bool = False,
        **options: Any,
    ) -> OllamaResponse:
        """Chat completion with messages"""
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **options,
        }

        response = await self._request("POST", "/api/chat", json_data=payload)
        return self._to_ollama_response(response)

    async def list_models(self) -> OllamaResponse:
        """List available models"""
        response = await self._request("GET", "/api/tags")
        return self._to_ollama_response(response)

    async def pull_model(self, model: str, stream: bool = False) -> OllamaResponse:
        """Pull a model by name. Uses Ollama REST API if available.

        Note: In some Ollama versions, pulling is primarily a CLI operation.
        This method attempts REST endpoint '/api/pull'.
        """
        payload: dict[str, Any] = {"name": model, "stream": stream}
        try:
            response = await self._request("POST", "/api/pull", json_data=payload)
            return self._to_ollama_response(response)
        except OllamaError as e:
            # Surface the error in the response wrapper as a failure
            return OllamaResponse(success=False, data=None, error=str(e))

    async def health_check(self) -> OllamaResponse:
        """Check service health and summarize version and model count"""
        try:
            ok_v, version, sc_v = await self._fetch_version()
            ok_t, model_count, sc_t = await self._fetch_model_count()
            overall_success = ok_v and ok_t
            error = "" if overall_success else f"version={sc_v}, tags={sc_t}"
            return OllamaResponse(
                success=overall_success,
                data={"version": version, "model_count": model_count},
                error=error,
            )
        except (OllamaConnectionError, OllamaTimeoutError) as e:
            return OllamaResponse(success=False, data=None, error=str(e))

    async def _fetch_version(self) -> tuple[bool, str | None, int]:
        """Fetch version endpoint and extract version string."""
        resp = await self._request("GET", "/api/version")
        version: str | None = None
        ok = 200 <= resp.status_code < 300
        if ok:
            try:
                data_any: Any = resp.json()
                if isinstance(data_any, dict):
                    data_dict = cast(dict[str, Any], data_any)
                    val = data_dict.get("version")
                    if isinstance(val, str):
                        version = val
                    elif val is not None:
                        version = str(val)
            except Exception:
                version = None
        return ok, version, resp.status_code

    async def _fetch_model_count(self) -> tuple[bool, int, int]:
        """Fetch tags endpoint and count models."""
        resp = await self._request("GET", "/api/tags")
        count = 0
        ok = 200 <= resp.status_code < 300
        if ok:
            try:
                data_any: Any = resp.json()
                if isinstance(data_any, dict):
                    data_dict = cast(dict[str, Any], data_any)
                    models = data_dict.get("models")
                    if isinstance(models, list):
                        models_list = cast(list[dict[str, Any]], models)
                        count = len(models_list)
            except Exception:
                count = 0
        return ok, count, resp.status_code

    @property
    def is_healthy(self) -> bool:
        """Check if service is healthy"""
        return self._healthy


async def create_client(config: OllamaConfig | None = None) -> OllamaClient:
    """Create and initialize Ollama client"""
    client = OllamaClient(config)
    await client.connect()
    return client
