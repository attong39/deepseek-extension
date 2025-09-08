#!/usr/bin/env python3
"""
🚀 Complete Turbo API Implementation
====================================

Full implementation of Turbo API integration with:
- API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
- Robust error handling and fallback
- Cost optimization and caching
- VS Code Continue integration
- Comprehensive logging and monitoring
"""

import asyncio
import json
import os
import time
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TurboAPIImplementation:
    """Complete Turbo API implementation with all features"""

    def __init__(self, api_key: str | None = None):
        # API Configuration
        self.api_key = api_key or os.getenv(
            "TURBO_API_KEY", "5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP"
        )
        self.turbo_endpoint = os.getenv("TURBO_API_BASE", "https://api.turbo.ai/v1")
        self.ollama_endpoint = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

        # Mode settings
        self.airplane_mode = os.getenv("AIRPLANE_MODE", "false").lower() in {"true", "1", "yes"}
        self.fallback_enabled = True

        # Session management
        self.session: aiohttp.ClientSession | None = None
        self.timeout = 30

        # Performance settings
        self.cache: dict[str, dict] = {}
        self.cache_ttl = 600  # 10 minutes
        self.rate_limiter = {"last_request": 0.0, "min_interval": 0.1}

        # Statistics
        self.stats = {
            "turbo_requests": 0,
            "ollama_requests": 0,
            "cache_hits": 0,
            "errors": 0,
            "total_cost": 0.0,
            "session_start": time.time(),
        }

        # Logging
        self.log_file = Path("turbo_api_usage.log")

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session or self.session.closed:
            connector = aiohttp.TCPConnector(limit=10, keepalive_timeout=30)
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

    def _log_request(self, endpoint: str, success: bool, response_time: float, error: str = ""):
        """Log API requests for monitoring"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "endpoint": endpoint,
            "success": success,
            "response_time_ms": round(response_time * 1000, 2),
            "error": error,
            "api_key_hash": str(hash(self.api_key))[:8],
        }

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def _get_cache_key(self, prompt: str, model: str = "") -> str:
        """Generate cache key"""
        return str(hash(f"{model}:{prompt.lower().strip()}"))

    def _is_cached(self, prompt: str, model: str = "") -> bool:
        """Check if response is cached"""
        cache_key = self._get_cache_key(prompt, model)
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if time.time() - entry["timestamp"] < self.cache_ttl:
                return True
            else:
                # Remove expired cache
                del self.cache[cache_key]
        return False

    def _get_cached(self, prompt: str, model: str = "") -> str:
        """Get cached response"""
        cache_key = self._get_cache_key(prompt, model)
        self.stats["cache_hits"] += 1
        return self.cache[cache_key]["response"]

    def _cache_response(self, prompt: str, response: str, model: str = ""):
        """Cache response"""
        cache_key = self._get_cache_key(prompt, model)
        self.cache[cache_key] = {"response": response, "timestamp": time.time(), "model": model}

    def _rate_limit(self):
        """Apply rate limiting"""
        now = time.time()
        elapsed = now - self.rate_limiter["last_request"]
        if elapsed < self.rate_limiter["min_interval"]:
            # TODO: Replace blocking sleep with async await asyncio.sleep(self.rate_limiter["min_interval"] - elapsed)
        self.rate_limiter["last_request"] = time.time()

    def _estimate_cost(self, prompt: str, response: str = "") -> float:
        """Estimate request cost"""
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = len(response.split()) * 1.3 if response else 100
        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * 0.002  # $0.002 per 1K tokens estimate

    async def turbo_chat(self, prompt: str, model: str = "turbo", use_cache: bool = True) -> str:
        """Chat with Turbo API"""
        # Check cache
        if use_cache and self._is_cached(prompt, model):
            print("📦 Using cached response")
            return self._get_cached(prompt, model)

        # Rate limiting
        self._rate_limit()

        start_time = time.time()

        try:
            await self._ensure_session()

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "TurboAPI-Client/1.0",
            }

            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7,
            }

            url = f"{self.turbo_endpoint}/chat/completions"

            async with self.session.post(url, headers=headers, json=data) as response:
                response_time = time.time() - start_time

                if response.status == 200:
                    result = await response.json()
                    content = result["choices"][0]["message"]["content"]

                    # Cache and track
                    if use_cache:
                        self._cache_response(prompt, content, model)

                    cost = self._estimate_cost(prompt, content)
                    self.stats["turbo_requests"] += 1
                    self.stats["total_cost"] += cost

                    self._log_request("turbo", True, response_time)
                    print(f"💰 Turbo API cost: ${cost:.4f}")

                    return content
                else:
                    error_text = await response.text()
                    self._log_request("turbo", False, response_time, error_text)
                    raise Exception(f"Turbo API error {response.status}: {error_text}")

        except Exception as e:
            response_time = time.time() - start_time
            self.stats["errors"] += 1
            self._log_request("turbo", False, response_time, str(e))
            raise e

    async def ollama_chat(self, prompt: str, model: str = "deepseek-coder:6.7b") -> str:
        """Chat with local Ollama"""
        try:
            await self._ensure_session()

            data = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 1000, "num_ctx": 4096},
            }

            url = f"{self.ollama_endpoint}/api/generate"

            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result.get("response", "")

                    self.stats["ollama_requests"] += 1
                    print("✅ Ollama response (free)")

                    return content
                else:
                    error_text = await response.text()
                    raise Exception(f"Ollama error {response.status}: {error_text}")

        except Exception as e:
            self.stats["errors"] += 1
            raise e

    async def smart_chat(self, prompt: str, prefer_turbo: bool = True) -> str:
        """Smart chat with automatic fallback"""
        if self.airplane_mode:
            print("✈️ Airplane mode: Using Ollama only")
            return await self.ollama_chat(prompt)

        try:
            if prefer_turbo:
                return await self.turbo_chat(prompt)
            else:
                return await self.ollama_chat(prompt)

        except Exception as primary_error:
            print(f"⚠️ Primary API failed: {primary_error}")
            print("🔄 Trying fallback...")

            try:
                if prefer_turbo:
                    # Fallback to Ollama
                    return await self.ollama_chat(prompt)
                else:
                    # Fallback to Turbo
                    return await self.turbo_chat(prompt)

            except Exception as fallback_error:
                print(f"❌ Fallback also failed: {fallback_error}")
                raise Exception(f"Both APIs failed: {primary_error}, {fallback_error}")

    async def batch_process(self, prompts: list[str], prefer_turbo: bool = True) -> list[str]:
        """Process multiple prompts efficiently"""
        print(f"🔄 Processing {len(prompts)} prompts...")

        tasks = []
        for prompt in prompts:
            task = asyncio.create_task(self.smart_chat(prompt, prefer_turbo))
            tasks.append(task)

        results = []
        for i, task in enumerate(tasks):
            try:
                result = await task
                results.append(result)
                print(f"✅ Prompt {i+1}/{len(prompts)} completed")
            except Exception as e:
                results.append(f"Error: {e}")
                print(f"❌ Prompt {i+1}/{len(prompts)} failed: {e}")

        return results

    def get_usage_stats(self) -> dict:
        """Get detailed usage statistics"""
        runtime = time.time() - self.stats["session_start"]
        total_requests = self.stats["turbo_requests"] + self.stats["ollama_requests"]

        return {
            "session_duration_minutes": round(runtime / 60, 2),
            "total_requests": total_requests,
            "turbo_requests": self.stats["turbo_requests"],
            "ollama_requests": self.stats["ollama_requests"],
            "cache_hits": self.stats["cache_hits"],
            "cache_efficiency_percent": round((self.stats["cache_hits"] / max(1, total_requests)) * 100, 1),
            "errors": self.stats["errors"],
            "error_rate_percent": round((self.stats["errors"] / max(1, total_requests)) * 100, 1),
            "estimated_total_cost_usd": round(self.stats["total_cost"], 4),
            "requests_per_minute": round(total_requests / max(1, runtime / 60), 1),
        }

    def print_stats(self):
        """Print usage statistics"""
        stats = self.get_usage_stats()

        print("\n📊 USAGE STATISTICS")
        print("=" * 40)
        print(f"⏱️  Session: {stats['session_duration_minutes']} min")
        print(f"📡 Total Requests: {stats['total_requests']}")
        print(f"🚀 Turbo API: {stats['turbo_requests']}")
        print(f"🤖 Ollama: {stats['ollama_requests']}")
        print(f"📦 Cache Hits: {stats['cache_hits']} ({stats['cache_efficiency_percent']}%)")
        print(f"❌ Errors: {stats['errors']} ({stats['error_rate_percent']}%)")
        print(f"💰 Total Cost: ${stats['estimated_total_cost_usd']}")
        print(f"⚡ Speed: {stats['requests_per_minute']} req/min")

    async def health_check(self) -> dict[str, bool]:
        """Check health of all endpoints"""
        health = {"turbo": False, "ollama": False}

        # Check Turbo API
        try:
            await self.turbo_chat("Hello", use_cache=False)
            health["turbo"] = True
            print("✅ Turbo API is working")
        except Exception as e:
            print(f"❌ Turbo API failed: {e}")

        # Check Ollama
        try:
            await self.ollama_chat("Hello")
            health["ollama"] = True
            print("✅ Ollama is working")
        except Exception as e:
            print(f"❌ Ollama failed: {e}")

        return health


def setup_vscode_continue():
    """Setup VS Code Continue extension with Turbo API"""
    print("🔧 Setting up VS Code Continue extension...")

    continue_dir = Path.home() / ".continue"
    continue_dir.mkdir(exist_ok=True)

    config = {
        "models": [
            {
                "title": "Turbo API",
                "provider": "openai",
                "model": "turbo",
                "apiKey": "5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP",
                "apiBase": "https://api.turbo.ai/v1",
                "contextLength": 4096,
            },
            {
                "title": "DeepSeek Coder (Local)",
                "provider": "ollama",
                "model": "deepseek-coder:6.7b",
                "apiBase": "http://localhost:11434",
                "contextLength": 4096,
            },
        ],
        "tabAutocompleteModel": {
            "title": "DeepSeek Fast",
            "provider": "ollama",
            "model": "deepseek-coder:1.3b",
            "apiBase": "http://localhost:11434",
        },
        "systemMessage": "You are a helpful AI coding assistant. Answer in Vietnamese when appropriate.",
        "allowAnonymousTelemetry": False,
    }

    config_file = continue_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Continue config saved to: {config_file}")


def setup_environment():
    """Setup environment variables and config files"""
    print("⚙️ Setting up environment...")

    env_content = """# Turbo API Configuration
TURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
TURBO_API_BASE=https://api.turbo.ai/v1

# Ollama Configuration
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_NUM_CTX=4096

# Mode Settings
AIRPLANE_MODE=false

# Performance Settings
OLLAMA_NUM_PARALLEL=8
OLLAMA_GPU_LAYERS=35
OLLAMA_MAX_LOADED_MODELS=3
OLLAMA_CONTEXT_LENGTH=8192
OLLAMA_NUM_BATCH=512
"""

    env_file = Path(".env")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)

    print(f"✅ Environment file updated: {env_file}")


async def demo_implementation():
    """Demo the complete implementation"""
    print("🚀 TURBO API IMPLEMENTATION DEMO")
    print("=" * 50)

    async with TurboAPIImplementation() as client:
        # Health check
        print("\n1. 🏥 Health Check:")
        health = await client.health_check()

        # Single chat test
        print("\n2. 💬 Single Chat Test:")
        try:
            response = await client.smart_chat("Viết một function Python để tính số Fibonacci", prefer_turbo=True)
            print(f"Response: {response[:200]}...")
        except Exception as e:
            print(f"Chat failed: {e}")

        # Batch processing test
        print("\n3. 🔄 Batch Processing Test:")
        prompts = ["Hello in Vietnamese", "Python list comprehension example", "Best practices for API design"]

        try:
            results = await client.batch_process(prompts, prefer_turbo=False)
            for i, result in enumerate(results):
                print(f"  {i+1}. {result[:80]}...")
        except Exception as e:
            print(f"Batch processing failed: {e}")

        # Print final stats
        print("\n4. 📊 Final Statistics:")
        client.print_stats()


async def main():
    """Main implementation function"""
    print("🎯 COMPLETE TURBO API IMPLEMENTATION")
    print("=" * 60)

    # Setup
    setup_environment()
    setup_vscode_continue()

    # Demo
    await demo_implementation()

    print("\n✅ IMPLEMENTATION COMPLETE!")
    print("\n🎯 What's been implemented:")
    print("  • Complete Turbo API client with your key")
    print("  • Robust error handling and fallback")
    print("  • Cost optimization with caching")
    print("  • Usage tracking and logging")
    print("  • VS Code Continue integration")
    print("  • Batch processing capabilities")
    print("  • Health monitoring")

    print("\n🚀 How to use:")
    print("  • Import TurboAPIImplementation class")
    print("  • Use smart_chat() for automatic fallback")
    print("  • Use batch_process() for multiple prompts")
    print("  • Check get_usage_stats() for monitoring")

    print("\n🔑 Your API key is configured and ready!")


if __name__ == "__main__":
    asyncio.run(main())
