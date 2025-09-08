from __future__ import annotations

import logging
from typing import Any

from .base_client import BaseAPIClient
import Exception
import api_key
import base_url
import bool
import cat
import dict
import dimensions
import e
import flag
import float
import function_call
import functions
import int
import kwargs
import len
import list
import max_tokens
import messages
import model
import organization
import self
import str
import stream
import super
import temperature
import text

"""
OpenAI API Client - Integration Layer
Handles all interactions with OpenAI's APIs including:
- GPT models for text generation
- Embeddings for vector search
- Moderation for content safety
- Function calling for tool use
"""
logger = logging.getLogger(__name__)


class OpenAIClient(BaseAPIClient):
    """
    OpenAI API client for GPT, embeddings, and moderation.
    Features:
    - Chat completions with streaming
    - Text embeddings generation
    - Content moderation
    - Function calling support
    - Token usage tracking
    """

    def __init__(
        self,
        api_key: str,
        organization: str | None = None,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o-mini",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs,
    ):
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            rate_limit=60,  # OpenAI default tier
            **kwargs,
        )
        self.organization = organization
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tokens_used = 0
        self.requests_made = 0

    def _get_default_headers(self) -> dict[str, str]:
        """Get OpenAI-specific headers."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ZetaVN/1.0",
        }
        if self.organization:
            headers["OpenAI-Organization"] = self.organization
        return headers

    async def _authenticate(self) -> None:
        """Test authentication with OpenAI."""
        try:
            await self.list_models()
            self._is_authenticated = True
            logger.info("✅ OpenAI authentication successful")
        except Exception as e:
            self._is_authenticated = False
            logger.error(f"❌ OpenAI authentication failed: {e}")
            raise

    async def list_models(self) -> dict[str, Any]:
        """List available OpenAI models."""
        return await self.get("/models")

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        stream: bool = False,
        functions: list[dict[str, Any]] | None = None,
        function_call: str | dict[str, str] | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Create a chat completion using OpenAI's GPT models.
        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model to use (defaults to instance model)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-2)
            stream: Whether to stream the response
            functions: List of functions for function calling
            function_call: How to call functions ('auto', 'none', or specific function)
        Returns:
            OpenAI chat completion response
        """
        data = {
            "model": model or self.model,
            "messages": messages,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature if temperature is not None else self.temperature,
            "stream": stream,
            **kwargs,
        }
        if functions:
            data["functions"] = functions
            if function_call:
                data["function_call"] = function_call
        try:
            response = await self.post("/chat/completions", data=data)
            if "usage" in response:
                usage = response["usage"]
                self.tokens_used += usage.get("total_tokens", 0)
            self.requests_made += 1
            logger.debug(
                f"💬 Chat completion: {len(messages)} messages -> {response.get('usage', {}).get('total_tokens', 0)} tokens"
            )
            return response
        except Exception as e:
            logger.error(f"❌ Chat completion failed: {e}")
            raise

    async def generate_embedding(
        self,
        text: str,
        model: str = "text-embedding-3-small",
        dimensions: int | None = None,
    ) -> dict[str, Any]:
        """
        Generate text embedding using OpenAI's embedding models.
        Args:
            text: Text to embed
            model: Embedding model to use
            dimensions: Number of dimensions (for ada-002 compatibility)
        Returns:
            OpenAI embedding response with vector data
        """
        data = {
            "model": model,
            "input": text,
        }
        if dimensions:
            data["dimensions"] = dimensions
        try:
            response = await self.post("/embeddings", data=data)
            if "usage" in response:
                self.tokens_used += response["usage"].get("total_tokens", 0)
            self.requests_made += 1
            logger.debug(
                f"🔍 Generated embedding: {len(text)} chars -> {len(response['data'][0]['embedding'])} dims"
            )
            return response
        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {e}")
            raise

    async def moderate_content(
        self,
        text: str,
        model: str = "text-moderation-latest",
    ) -> dict[str, Any]:
        """
        Check content for policy violations using OpenAI's moderation.
        Args:
            text: Text to moderate
            model: Moderation model to use
        Returns:
            Moderation response with flagged categories
        """
        data = {
            "model": model,
            "input": text,
        }
        try:
            response = await self.post("/moderations", data=data)
            self.requests_made += 1
            result = response["results"][0]
            flagged = result.get("flagged", False)
            if flagged:
                categories = [
                    cat for cat, flag in result.get("categories", {}).items() if flag
                ]
                logger.warning(f"⚠️ Content flagged for: {', '.join(categories)}")
            else:
                logger.debug("✅ Content passed moderation")
            return response
        except Exception as e:
            logger.error(f"❌ Content moderation failed: {e}")
            raise

    async def get_usage_stats(self) -> dict[str, Any]:
        """Get current usage statistics."""
        return {
            "tokens_used": self.tokens_used,
            "requests_made": self.requests_made,
            "model": self.model,
            "authenticated": self._is_authenticated,
        }

    async def health_check(self) -> dict[str, Any]:
        """Check OpenAI API health and authentication."""
        try:
            models_response = await self.list_models()
            available_models = len(models_response.get("data", []))
            return {
                "status": "healthy",
                "authenticated": self._is_authenticated,
                "available_models": available_models,
                "current_model": self.model,
                "usage": await self.get_usage_stats(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "authenticated": self._is_authenticated,
            }


__all__ = [
    "OpenAIClient",
    "available_models",
    "categories",
    "data",
    "flagged",
    "headers",
    "logger",
    "models_response",
    "response",
    "result",
    "usage",
]
