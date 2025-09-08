#!/usr/bin/env python3
"""
🚀 Turbo Ollama Client - High Performance API Client
==================================================

Advanced client for interacting with Turbo Ollama API with:
- Async/await support for better performance
- Connection pooling and reuse
- Automatic fallback between Turbo API and local Ollama
- Streaming responses for real-time output
- Response caching for repeated queries
- Rate limiting and retry logic
- Vietnamese language optimization

Usage Examples:
    # Basic usage
    client = TurboOllamaClient()
    response = await client.chat("Xin chào, bạn có thể giúp tôi không?")

    # Streaming response
    async for chunk in client.stream_chat("Viết code Python"):
        print(chunk, end="")

    # Code completion
    code = await client.complete_code("def fibonacci(n):", language="python")
"""

import asyncio
import json
import os
import time
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from enum import Enum
from typing import Any

import aiohttp
from dotenv import load_dotenv
import Exception
import ValueError
import attempt
import bool
import cache_entry
import chunk
import client
import code_prompt
import dict
import e
import float
import hash
import int
import language
import model
import print
import range
import self
import str

# Load .env and allow local overrides from .env.local
load_dotenv()
load_dotenv(".env.local", override=True)


class APIProvider(Enum):
    """API provider options"""

    TURBO = "turbo"
    OLLAMA = "ollama"
    AUTO = "auto"  # Automatically choose best provider


@dataclass
class ChatMessage:
    """Chat message structure"""

    role: str
    content: str
    timestamp: float | None = None


@dataclass
class CompletionRequest:
    """Completion request configuration"""

    prompt: str
    model: str = "deepseek-coder"
    max_tokens: int = 1000
    temperature: float = 0.7
    stream: bool = False
    provider: APIProvider = APIProvider.AUTO


class TurboOllamaClient:
    """High-performance Turbo Ollama API client"""

    def __init__(self):
        # API Configuration
        self.turbo_api_key = os.getenv("TURBO_API_KEY")
        self.turbo_endpoint = os.getenv("TURBO_API_ENDPOINT", "https://api.turbo.ai/v1")
        self.ollama_endpoint = os.getenv("OLLAMA_ENDPOINT", "http://127.0.0.1:11434")

        # Performance Settings
        self.session: aiohttp.ClientSession | None = None
        self.cache: dict[str, Any] = {}
        self.cache_ttl = 300  # 5 minutes
        self.max_retries = 3
        self.timeout = 30

        # Default models
        self.turbo_model = os.getenv("TURBO_MODEL", "turbo")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "deepseek-coder")

        # Vietnamese optimization prompts
        self.vietnamese_system_prompt = """
Bạn là một AI assistant thông minh, hỗ trợ tiếng Việt tự nhiên.
Luôn trả lời bằng tiếng Việt rõ ràng, chính xác và hữu ích.
Khi viết code, hãy thêm comment tiếng Việt để giải thích.
"""

    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def _ensure_session(self) -> None:
        """Ensure aiohttp session is created"""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(
                limit=100, limit_per_host=10, keepalive_timeout=30, enable_cleanup_closed=True
            )
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

    async def close(self) -> None:
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()

    def _get_cache_key(self, prompt: str, provider: str, model: str) -> str:
        """Generate cache key"""
        return f"{provider}:{model}:{hash(prompt)}"

    def _is_cache_valid(self, cache_entry: dict) -> bool:
        """Check if cache entry is still valid"""
        return time.time() - cache_entry.get("timestamp", 0) < self.cache_ttl

    async def _turbo_chat_request(self, prompt: str, model: str | None = None) -> str:
        """Make non-streaming request to Turbo API"""
        if not self.turbo_api_key:
            raise ValueError("TURBO_API_KEY not configured")

        await self._ensure_session()
        assert self.session is not None

        headers = {"Authorization": f"Bearer {self.turbo_api_key}", "Content-Type": "application/json"}

        data = {
            "model": model or self.turbo_model,
            "messages": [
                {"role": "system", "content": self.vietnamese_system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "max_tokens": 1000,
            "temperature": 0.7,
        }

        url = f"{self.turbo_endpoint}/chat/completions"

        for attempt in range(self.max_retries):
            try:
                async with self.session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        if attempt == self.max_retries - 1:
                            raise Exception(f"Turbo API error {response.status}: {error_text}")

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(2**attempt)

        return ""  # Should never reach here

    async def _turbo_stream_request(self, prompt: str, model: str | None = None) -> AsyncGenerator[str, None]:
        """Make streaming request to Turbo API"""
        if not self.turbo_api_key:
            raise ValueError("TURBO_API_KEY not configured")

        await self._ensure_session()
        assert self.session is not None

        headers = {"Authorization": f"Bearer {self.turbo_api_key}", "Content-Type": "application/json"}

        data = {
            "model": model or self.turbo_model,
            "messages": [
                {"role": "system", "content": self.vietnamese_system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": True,
            "max_tokens": 1000,
            "temperature": 0.7,
        }

        url = f"{self.turbo_endpoint}/chat/completions"

        async with self.session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if "choices" in data and data["choices"]:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue

    async def _ollama_chat_request(self, prompt: str, model: str | None = None) -> str:
        """Make non-streaming request to local Ollama"""
        await self._ensure_session()
        assert self.session is not None

        data = {
            "model": model or self.ollama_model,
            "prompt": f"{self.vietnamese_system_prompt}\n\nUser: {prompt}\nAssistant:",
            "stream": False,
        }

        url = f"{self.ollama_endpoint}/api/generate"

        for attempt in range(self.max_retries):
            try:
                async with self.session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "")
                    else:
                        if attempt == self.max_retries - 1:
                            error_text = await response.text()
                            raise Exception(f"Ollama error {response.status}: {error_text}")

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(1)

        return ""  # Should never reach here

    async def _ollama_stream_request(self, prompt: str, model: str | None = None) -> AsyncGenerator[str, None]:
        """Make streaming request to local Ollama"""
        await self._ensure_session()
        assert self.session is not None

        data = {
            "model": model or self.ollama_model,
            "prompt": f"{self.vietnamese_system_prompt}\n\nUser: {prompt}\nAssistant:",
            "stream": True,
        }

        url = f"{self.ollama_endpoint}/api/generate"

        async with self.session.post(url, json=data) as response:
            if response.status == 200:
                async for line in response.content:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        if "response" in data:
                            yield data["response"]
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue

    async def _choose_provider(self, prompt: str) -> APIProvider:
        """Automatically choose the best provider"""
        # Check if Turbo API is available
        if self.turbo_api_key:
            try:
                # Quick health check for Turbo API
                await self._ensure_session()
                async with self.session.get(
                    f"{self.turbo_endpoint}/models", headers={"Authorization": f"Bearer {self.turbo_api_key}"}
                ) as response:
                    if response.status == 200:
                        return APIProvider.TURBO
            except:
                pass

        # Fall back to Ollama
        try:
            await self._ensure_session()
            async with self.session.get(f"{self.ollama_endpoint}/api/tags") as response:
                if response.status == 200:
                    return APIProvider.OLLAMA
        except:
            pass

        # If both fail, default to Ollama
        return APIProvider.OLLAMA

    async def chat(self, prompt: str, provider: APIProvider = APIProvider.AUTO, model: str = None) -> str:
        """
        Send a chat message and get response

        Args:
            prompt: The message to send
            provider: Which API provider to use
            model: Specific model to use

        Returns:
            The AI response as a string
        """
        # Check cache first
        if provider == APIProvider.AUTO:
            provider = await self._choose_provider(prompt)

        cache_key = self._get_cache_key(prompt, provider.value, model or "default")
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]["response"]

        # Make API request
        try:
            if provider == APIProvider.TURBO:
                response = await self._turbo_request(prompt, model, stream=False)
            else:
                response = await self._ollama_request(prompt, model, stream=False)

            # Cache the response
            self.cache[cache_key] = {"response": response, "timestamp": time.time()}

            return response

        except Exception as e:
            # Fallback to other provider if main one fails
            if provider == APIProvider.TURBO:
                try:
                    return await self._ollama_request(prompt, model, stream=False)
                except:
                    raise e
            else:
                if self.turbo_api_key:
                    try:
                        return await self._turbo_request(prompt, model, stream=False)
                    except:
                        raise e
                else:
                    raise e

    async def stream_chat(
        self, prompt: str, provider: APIProvider = APIProvider.AUTO, model: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Send a chat message and get streaming response

        Args:
            prompt: The message to send
            provider: Which API provider to use
            model: Specific model to use

        Yields:
            Response chunks as they arrive
        """
        if provider == APIProvider.AUTO:
            provider = await self._choose_provider(prompt)

        try:
            if provider == APIProvider.TURBO:
                async for chunk in await self._turbo_request(prompt, model, stream=True):
                    yield chunk
            else:
                async for chunk in await self._ollama_request(prompt, model, stream=True):
                    yield chunk

        except Exception as e:
            # Fallback to other provider
            if provider == APIProvider.TURBO:
                try:
                    async for chunk in await self._ollama_request(prompt, model, stream=True):
                        yield chunk
                except:
                    raise e
            else:
                if self.turbo_api_key:
                    try:
                        async for chunk in await self._turbo_request(prompt, model, stream=True):
                            yield chunk
                    except:
                        raise e
                else:
                    raise e

    async def complete_code(
        self, code_prompt: str, language: str = "python", provider: APIProvider = APIProvider.AUTO
    ) -> str:
        """
        Complete code with AI assistance

        Args:
            code_prompt: The code to complete
            language: Programming language
            provider: Which API provider to use

        Returns:
            Completed code
        """
        prompt = f"""
Hoàn thành đoạn code {language} sau và thêm comment tiếng Việt:

```{language}
{code_prompt}
```

Yêu cầu:
- Viết code chất lượng cao, tuân thủ best practices
- Thêm comment tiếng Việt giải thích logic
- Xử lý lỗi phù hợp
- Tối ưu hiệu suất nếu cần
"""

        return await self.chat(prompt, provider)

    async def review_code(self, code: str, language: str = "python") -> str:
        """
        Review code for improvements

        Args:
            code: Code to review
            language: Programming language

        Returns:
            Code review with suggestions
        """
        prompt = f"""
Hãy review đoạn code {language} sau và đưa ra nhận xét, góp ý cải thiện:

```{language}
{code}
```

Phân tích các khía cạnh:
1. Độ chính xác và logic
2. Hiệu suất và tối ưu hoá
3. Bảo mật
4. Khả năng bảo trì
5. Best practices
6. Đề xuất cải thiện cụ thể

Trả lời bằng tiếng Việt và đưa ra ví dụ code cải thiện nếu cần.
"""

        return await self.chat(prompt)

    async def explain_code(self, code: str, language: str = "python") -> str:
        """
        Explain how code works

        Args:
            code: Code to explain
            language: Programming language

        Returns:
            Detailed explanation in Vietnamese
        """
        prompt = f"""
Hãy giải thích chi tiết cách hoạt động của đoạn code {language} sau:

```{language}
{code}
```

Giải thích:
1. Mục đích và chức năng tổng quát
2. Từng phần code hoạt động như thế nào
3. Luồng thực thi
4. Input và output
5. Các concept hoặc thuật toán được sử dụng

Sử dụng tiếng Việt dễ hiểu, phù hợp cho người mới học.
"""

        return await self.chat(prompt)

    def clear_cache(self):
        """Clear response cache"""
        self.cache.clear()

    async def health_check(self) -> dict[str, bool]:
        """Check health of both API providers"""
        health = {"turbo": False, "ollama": False}

        # Check Turbo API
        if self.turbo_api_key:
            try:
                await self._ensure_session()
                async with self.session.get(
                    f"{self.turbo_endpoint}/models", headers={"Authorization": f"Bearer {self.turbo_api_key}"}
                ) as response:
                    health["turbo"] = response.status == 200
            except:
                pass

        # Check Ollama
        try:
            await self._ensure_session()
            async with self.session.get(f"{self.ollama_endpoint}/api/tags") as response:
                health["ollama"] = response.status == 200
        except:
            pass

        return health


# Convenience functions for quick usage
async def quick_chat(prompt: str) -> str:
    """Quick chat without creating client instance"""
    async with TurboOllamaClient() as client:
        return await client.chat(prompt)


async def quick_code_complete(code: str, language: str = "python") -> str:
    """Quick code completion"""
    async with TurboOllamaClient() as client:
        return await client.complete_code(code, language)


# Example usage
async def main():
    """Example usage of the client"""
    async with TurboOllamaClient() as client:
        # Health check
        health = await client.health_check()
        print("🔍 API Health:", health)

        # Simple chat
        print("\n💬 Chat Example:")
        response = await client.chat("Xin chào! Bạn có thể giúp tôi học Python không?")
        print(response)

        # Streaming chat
        print("\n📡 Streaming Example:")
        async for chunk in client.stream_chat("Viết một hàm Python tính fibonacci"):
            print(chunk, end="", flush=True)
        print()

        # Code completion
        print("\n⚡ Code Completion:")
        code = await client.complete_code("def quicksort(arr):")
        print(code)

        # Code review
        print("\n🔍 Code Review:")
        sample_code = """
def divide(a, b):
    return a / b
"""
        review = await client.review_code(sample_code)
        print(review)


if __name__ == "__main__":
    asyncio.run(main())
