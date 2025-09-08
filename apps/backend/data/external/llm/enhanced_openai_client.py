"""


Enhanced OpenAI Client for ZETA AI Phase 3


Author: Duy BG VN





Advanced OpenAI integration with multi-modal capabilities, streaming,


function calling, and comprehensive error handling.


"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any, Literal
import Exception
import api_key
import audio_data
import audio_size_bytes
import base_url
import bool
import bytes
import chunk
import dict
import e
import embedding
import filename
import float
import func
import getattr
import hasattr
import image
import image_url
import int
import isinstance
import key
import kwargs
import language
import len
import list
import max_tokens
import msg
import organization
import prompt
import request
import request_params
import requested_model
import required_tokens
import result
import s
import self
import str
import stream
import usage

try:
    from openai import AsyncOpenAI  # type: ignore
    from openai.types.chat import ChatCompletion, ChatCompletionChunk  # type: ignore
except Exception:  # pragma: no cover - optional dependency in test env
    AsyncOpenAI = None  # type: ignore
    ChatCompletion = Any  # type: ignore
    ChatCompletionChunk = Any  # type: ignore
from apps.backend.config.ml_config import TOKEN_LIMITS, get_ml_settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class OpenAIConfig(BaseModel):
    """OpenAI configuration."""

    api_key: str

    organization: str | None = None

    base_url: str | None = None

    default_model: str = "gpt-4-turbo"
    # Long-context preferences
    use_long_context: bool = True
    long_context_model: str = "gpt-4o"

    default_embedding_model: str = "text-embedding-ada-002"

    default_image_model: str = "dall-e-3"

    default_audio_model: str = "whisper-1"

    max_retries: int = 3

    timeout: float = 60.0


class ChatMessage(BaseModel):
    """Chat message with enhanced features."""

    role: str

    content: str

    name: str | None = None

    function_call: dict[str, Any] | None = None

    tool_calls: list[dict[str, Any]] | None = None


class FunctionDefinition(BaseModel):
    """Function definition for function calling."""

    name: str

    description: str

    parameters: dict[str, Any]


class ImageGenerationRequest(BaseModel):
    """Image generation request."""

    prompt: str

    model: str = "dall-e-3"

    n: int = 1

    size: Literal[
        "1024x1024",
        "1536x1024",
        "1024x1536",
        "256x256",
        "512x512",
        "1792x1024",
        "1024x1792",
    ] = "1024x1024"

    quality: Literal["standard", "hd"] = "standard"

    style: Literal["vivid", "natural"] = "vivid"


class EnhancedOpenAIClient:
    """Enhanced OpenAI client with advanced features."""

    def __init__(self, config: OpenAIConfig):
        """


        Initialize enhanced OpenAI client.





        Args:


            config: OpenAI configuration


        """

        self.config = config

        # If openai package is not installed, keep client as None and raise when used.
        if AsyncOpenAI is None:  # pragma: no cover - optional dependency
            self._client = None
        else:
            self._client = AsyncOpenAI(
                api_key=config.api_key,
                organization=config.organization,
                base_url=config.base_url,
                max_retries=config.max_retries,
                timeout=config.timeout,
            )

        # Usage tracking

        self.usage_stats = {"requests": 0, "tokens": 0, "cost": 0.0, "errors": 0}

    def _select_model_for_tokens(
        self,
        required_tokens: int | None,
        requested_model: str | None,
    ) -> str:
        """Select a model based on estimated token requirement and ML flags.

        Args:
            required_tokens: Estimated tokens needed for prompt+completion.
            requested_model: Explicit model requested by caller, if any.

        Returns:
            Chosen model name.
        """
        # Respect explicit request if provided
        if requested_model:
            return requested_model

        ml = get_ml_settings()
        default_model = self.config.default_model or ml.default_chat_model
        if not required_tokens:
            return default_model

        # Compare against token limits; prefer long-context if needed and allowed
        default_limit = TOKEN_LIMITS.get(default_model, ml.max_context_tokens)
        if (
            self.config.use_long_context
            and ml.use_long_context_model
            and required_tokens > default_limit
        ):
            return self.config.long_context_model or ml.long_context_model
        return default_model

    async def chat_completion(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        *,
        stream: bool = False,
        opts: dict[str, Any] | None = None,
    ) -> Any:
        """


        Enhanced chat completion with all OpenAI features.





        Args:


            messages: List of chat messages


            model: Model to use


            temperature: Sampling temperature


            max_tokens: Maximum tokens to generate


            top_p: Top-p sampling


            frequency_penalty: Frequency penalty


            presence_penalty: Presence penalty


            stream: Whether to stream response


            functions: Available functions for function calling


            function_call: Function call behavior


            tools: Available tools


            tool_choice: Tool choice behavior


            **kwargs: Additional parameters





        Returns:


            Chat completion or streaming chunks


        """

        try:
            opts = opts or {}
            # Optionally auto-select model for long context
            model = self._select_model_for_tokens(
                opts.get("estimated_prompt_tokens"), model
            )

            # Convert messages to OpenAI format
            openai_messages = self._to_openai_messages(messages)

            # Prepare request parameters

            # Build core params and merge extras
            request_params: dict[str, Any] = {
                "model": model,
                "messages": openai_messages,
                "stream": stream,
            }
            # Map supported optional fields from opts
            for key in (
                "temperature",
                "max_tokens",
                "top_p",
                "frequency_penalty",
                "presence_penalty",
                "functions",
                "function_call",
                "tools",
                "tool_choice",
            ):
                if key in opts and opts[key] is not None:
                    request_params[key] = opts[key]

            # Add function calling parameters if provided

            if request_params.get("functions"):
                request_params["functions"] = [
                    {
                        "name": func.name,
                        "description": func.description,
                        "parameters": func.parameters,
                    }
                    for func in request_params["functions"]
                ]

            # Make API call; if streaming, return an async generator of chunks
            if stream:
                stream_ctx = await self._client.chat.completions.create(
                    **request_params
                )

                async def _gen() -> AsyncGenerator[ChatCompletionChunk, None]:
                    # OpenAI SDK returns an async CM for streams
                    async with stream_ctx as s:  # type: ignore[attr-defined]
                        async for chunk in s:  # type: ignore[misc]
                            yield chunk

                # Usage stats best-effort for streams: increment request count only
                self.usage_stats["requests"] += 1
                return _gen()

            response = await self._client.chat.completions.create(**request_params)

            # Update usage stats for non-stream
            self.usage_stats["requests"] += 1
            if hasattr(response, "usage") and response.usage:
                self.usage_stats["tokens"] += response.usage.total_tokens
                self.usage_stats["cost"] += self._calculate_cost(model, response.usage)
            return response

        except Exception as e:
            self.usage_stats["errors"] += 1

            logger.error(f"Chat completion error: {e}")

            raise

    def _to_openai_messages(self, messages: list[ChatMessage]) -> list[dict[str, Any]]:
        return [
            {
                "role": msg.role,
                "content": msg.content,
                **({"name": msg.name} if msg.name else {}),
                **({"function_call": msg.function_call} if msg.function_call else {}),
                **({"tool_calls": msg.tool_calls} if msg.tool_calls else {}),
            }
            for msg in messages
        ]

    async def generate_embeddings(
        self, texts: str | list[str], model: str | None = None
    ) -> list[list[float]]:
        """


        Generate text embeddings.





        Args:


            texts: Text(s) to embed


            model: Embedding model to use





        Returns:


            List of embedding vectors


        """

        try:
            model = model or self.config.default_embedding_model

            # Ensure texts is a list

            if isinstance(texts, str):
                texts = [texts]

            response = await self._client.embeddings.create(model=model, input=texts)

            # Update usage stats

            self.usage_stats["requests"] += 1

            if response.usage:
                self.usage_stats["tokens"] += response.usage.total_tokens

                self.usage_stats["cost"] += self._calculate_embedding_cost(
                    model, response.usage
                )

            return [embedding.embedding for embedding in response.data]

        except Exception as e:
            self.usage_stats["errors"] += 1

            logger.error(f"Embedding generation error: {e}")

            raise

    async def generate_image(
        self, request: ImageGenerationRequest
    ) -> list[dict[str, Any]]:
        """


        Generate images using DALL-E.





        Args:


            request: Image generation request





        Returns:


            List of generated images


        """

        try:
            response = await self._client.images.generate(
                model=request.model,
                prompt=request.prompt,
                n=request.n,
                size=request.size,
                quality=request.quality,
                style=request.style,
            )

            # Update usage stats

            self.usage_stats["requests"] += 1

            self.usage_stats["cost"] += self._calculate_image_cost(request)

            return [
                {
                    "url": image.url,
                    "b64_json": image.b64_json,
                    "revised_prompt": getattr(image, "revised_prompt", None),
                }
                for image in (response.data or [])
            ]

        except Exception as e:
            self.usage_stats["errors"] += 1

            logger.error(f"Image generation error: {e}")

            raise

    async def analyze_image(
        self,
        image_url: str,
        prompt: str = "What's in this image?",
        model: str = "gpt-4-vision-preview",
        max_tokens: int = 1000,
    ) -> str:
        """


        Analyze image using GPT-4 Vision.





        Args:


            image_url: URL of image to analyze


            prompt: Analysis prompt


            model: Vision model to use


            max_tokens: Maximum tokens for response





        Returns:


            Image analysis result


        """

        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ]

            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,  # type: ignore
                max_tokens=max_tokens,
            )

            # Update usage stats

            self.usage_stats["requests"] += 1

            if response.usage:
                self.usage_stats["tokens"] += response.usage.total_tokens

                self.usage_stats["cost"] += self._calculate_cost(model, response.usage)

            content = response.choices[0].message.content

            return content or ""

        except Exception as e:
            self.usage_stats["errors"] += 1

            logger.error(f"Image analysis error: {e}")

            raise

    async def transcribe_audio(
        self,
        audio_data: bytes,
        filename: str,
        model: str | None = None,
        language: str | None = None,
        prompt: str | None = None,
    ) -> str:
        """


        Transcribe audio using Whisper.





        Args:


            audio_data: Audio file data


            filename: Audio filename


            model: Whisper model to use


            language: Audio language


            prompt: Transcription prompt





        Returns:


            Transcribed text


        """

        try:
            model = model or self.config.default_audio_model

            # Create file-like object

            audio_file = (filename, audio_data, "audio/mpeg")

            # Prepare transcription parameters

            transcription_params = {"model": model, "file": audio_file}

            if language:
                transcription_params["language"] = language

            if prompt:
                transcription_params["prompt"] = prompt

            response = await self._client.audio.transcriptions.create(
                **transcription_params
            )

            # Update usage stats

            self.usage_stats["requests"] += 1

            self.usage_stats["cost"] += self._calculate_audio_cost(len(audio_data))

            return response.text

        except Exception as e:
            self.usage_stats["errors"] += 1

            logger.error(f"Audio transcription error: {e}")

            raise

    async def moderate_content(self, content: str) -> dict[str, Any]:
        """


        Moderate content using OpenAI moderation.





        Args:


            content: Content to moderate





        Returns:


            Moderation result


        """

        try:
            response = await self._client.moderations.create(input=content)

            # Update usage stats

            self.usage_stats["requests"] += 1

            _ = response.results[0]

            return {
                "flagged": result.flagged,
                "categories": result.categories.model_dump(),
                "category_scores": result.category_scores.model_dump(),
            }

        except Exception as e:
            self.usage_stats["errors"] += 1

            logger.error(f"Content moderation error: {e}")

            raise

    async def list_models(self) -> list[dict[str, Any]]:
        """


        List available OpenAI models.





        Returns:


            List of available models


        """

        try:
            response = await self._client.models.list()

            return [
                {
                    "id": model.id,
                    "object": model.object,
                    "created": model.created,
                    "owned_by": model.owned_by,
                }
                for model in response.data
            ]

        except Exception as e:
            logger.error(f"Error listing models: {e}")

            raise

    def _calculate_cost(self, model: str, usage: Any) -> float:
        """Calculate API cost based on usage."""

        # Cost per 1K tokens (input/output)

        costs = {
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gpt-4-vision-preview": {"input": 0.01, "output": 0.03},
        }

        if model not in costs:
            return 0.0

        model_costs = costs[model]

        input_cost = (usage.prompt_tokens / 1000) * model_costs["input"]

        output_cost = (usage.completion_tokens / 1000) * model_costs["output"]

        return input_cost + output_cost

    def _calculate_embedding_cost(self, model: str, usage: Any) -> float:
        """Calculate embedding cost."""

        costs = {
            "text-embedding-ada-002": 0.0001,  # per 1K tokens
            "text-embedding-3-small": 0.00002,
            "text-embedding-3-large": 0.00013,
        }

        if model not in costs:
            return 0.0

        return (usage.total_tokens / 1000) * costs[model]

    def _calculate_image_cost(self, request: ImageGenerationRequest) -> float:
        """Calculate image generation cost."""

        costs = {
            "dall-e-3": {
                "1024x1024": {"standard": 0.04, "hd": 0.08},
                "1024x1792": {"standard": 0.08, "hd": 0.12},
                "1792x1024": {"standard": 0.08, "hd": 0.12},
            },
            "dall-e-2": {
                "1024x1024": {"standard": 0.02},
                "512x512": {"standard": 0.018},
                "256x256": {"standard": 0.016},
            },
        }

        if request.model not in costs:
            return 0.0

        model_costs = costs[request.model]

        size_costs = model_costs.get(request.size, {})

        cost_per_image = size_costs.get(request.quality, 0.0)

        return cost_per_image * request.n

    def _calculate_audio_cost(self, audio_size_bytes: int) -> float:
        """Calculate audio transcription cost."""

        # Whisper costs $0.006 per minute

        # Estimate: 1MB ≈ 1 minute of audio

        estimated_minutes = audio_size_bytes / (1024 * 1024)

        return estimated_minutes * 0.006

    def get_usage_stats(self) -> dict[str, Any]:
        """Get usage statistics."""

        return {**self.usage_stats, "timestamp": datetime.now().isoformat()}

    def reset_usage_stats(self) -> None:
        """Reset usage statistics."""

        self.usage_stats = {"requests": 0, "tokens": 0, "cost": 0.0, "errors": 0}

    async def close(self) -> None:
        """Close the client."""

        await self._client.close()

    async def __aenter__(self) -> EnhancedOpenAIClient:
        """Async context manager entry."""

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""

        await self.close()


# Factory function


def create_enhanced_openai_client(
    api_key: str,
    organization: str | None = None,
    base_url: str | None = None,
    **kwargs: Any,
) -> EnhancedOpenAIClient:
    """


    Create enhanced OpenAI client.





    Args:


        api_key: OpenAI API key


        organization: Organization ID


        base_url: Custom base URL


        **kwargs: Additional configuration





    Returns:


        Enhanced OpenAI client


    """

    config = OpenAIConfig(
        api_key=api_key, organization=organization, base_url=base_url, **kwargs
    )

    return EnhancedOpenAIClient(config)
