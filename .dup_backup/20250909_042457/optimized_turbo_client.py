#!/usr/bin/env python3
"""
Optimized Turbo + Ollama Client (env-driven)

Environment variables:
- TURBO_API_KEY: API key for Turbo (empty => Airplane Mode)
- TURBO_API_BASE: Default https://api.turbo.ai/v1
- AIRPLANE_MODE: "1"/"true"/"yes"/"on" => force local Ollama
- OLLAMA_HOST: Default http://127.0.0.1:11434 (use http://0.0.0.0:11434 to expose)
- OLLAMA_NUM_CTX: Context length for Ollama (e.g., 4096, 8192, ...)
"""

from __future__ import annotations

import asyncio
import os
import time

import aiohttp
from dotenv import load_dotenv

# Load environment (.env first, then optional .env.local overrides)
load_dotenv()
load_dotenv(".env.local", override=True)


class OptimizedTurboClient:
    """Client for Turbo API and local Ollama with smart fallback and caching."""

    def __init__(self, api_key: str | None = None):
        # Env-driven configuration
        self.api_key = api_key or os.getenv("TURBO_API_KEY", "")
        self.primary_endpoint = os.getenv("TURBO_API_BASE", "https://api.turbo.ai/v1").rstrip("/")
        self.ollama_endpoint = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
        self.airplane_mode = os.getenv("AIRPLANE_MODE", "").lower() in {"1", "true", "yes", "on"} or not bool(
            self.api_key
        )

        # Ollama settings
        self.ollama_models = [
            "llama2",
            "mistral",
            "codellama",
            "deepseek-coder:6.7b",
        ]
        self.default_ollama_model = "deepseek-coder:6.7b"

        # Client-side options for Ollama requests
        self.ollama_num_ctx = int(os.getenv("OLLAMA_NUM_CTX", os.getenv("OLLAMA_CONTEXT_LENGTH", "4096")))
        self.ollama_num_batch = int(os.getenv("OLLAMA_NUM_BATCH", "0"))  # 0 => let server default

        # Local-first mode preference
        self.prefer_local = os.getenv("PREFER_LOCAL", "false").lower() in {"true", "1", "yes"}

        # Performance settings
        self.session = None
        self.timeout = 30
        self.max_retries = 3

        # Cost optimization
        self.cache = {}
        self.cache_ttl = 600  # 10 minutes
        self.rate_limiter = {"last_request": 0.0, "min_interval": 0.1}

        # Usage tracking
        self.stats = {
            "requests": 0,
            "cache_hits": 0,
            "errors": 0,
            "total_cost": 0.0,
            "start_time": time.time(),
        }

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            # Yield control briefly to satisfy async function usage and keep event loop responsive
            await asyncio.sleep(0)
            connector = aiohttp.TCPConnector(limit=10, keepalive_timeout=30)
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            # Creating ClientSession isn't awaitable; keep function async to match call sites
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

    def _get_cache_key(self, prompt: str, model: str = "") -> str:
        return str(hash(f"{model}:{prompt.lower().strip()}"))

    def _is_cached(self, prompt: str, model: str = "") -> bool:
        key = self._get_cache_key(prompt, model)
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.cache_ttl:
                return True
        return False

    def _get_cached(self, prompt: str, model: str = "") -> str:
        key = self._get_cache_key(prompt, model)
        self.stats["cache_hits"] += 1
        return self.cache[key]["response"]

    def _cache_response(self, prompt: str, response: str, model: str = "") -> None:
        key = self._get_cache_key(prompt, model)
        self.cache[key] = {"response": response, "timestamp": time.time(), "model": model}

    def _rate_limit(self) -> None:
        now = time.time()
        elapsed = now - self.rate_limiter["last_request"]
        if elapsed < self.rate_limiter["min_interval"]:
            # TODO: Replace blocking sleep with async await asyncio.sleep(self.rate_limiter["min_interval"] - elapsed)
        self.rate_limiter["last_request"] = time.time()

    def _estimate_cost(self, prompt: str, response: str = "") -> float:
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = len(response.split()) * 1.3 if response else 100
        return ((input_tokens + output_tokens) / 1000.0) * 0.002

    async def chat_optimized(
        self,
        prompt: str,
        use_turbo: bool = True,
        ollama_model: str | None = None,
    ) -> str:
        """Chat with selected backend; fallback on failure.
        - If Airplane Mode is ON or API key missing, forces Ollama.
        - Caches by (model, prompt).
        """
        effective_use_turbo = use_turbo and not self.airplane_mode
        model_ctx = "turbo" if effective_use_turbo else (ollama_model or self.default_ollama_model)

        if self._is_cached(prompt, model_ctx):
            print("📦 Using cached response")
            return self._get_cached(prompt, model_ctx)

        self._rate_limit()

        try:
            if effective_use_turbo:
                response = await self._turbo_request(prompt)
                self._cache_response(prompt, response, model_ctx)
                cost = self._estimate_cost(prompt, response)
                self.stats["total_cost"] += cost
                self.stats["requests"] += 1
                print(f"💰 Estimated cost: ${cost:.4f}")
                return response
            else:
                response = await self._ollama_request(prompt, ollama_model)
                self._cache_response(prompt, response, model_ctx)
                self.stats["requests"] += 1
                print("✅ Ollama request (no cost)")
                return response
        except Exception as primary_err:
            print(f"⚠️ Primary API failed: {primary_err}")
            self.stats["errors"] += 1
            print("🔄 Trying fallback...")

            try:
                if effective_use_turbo:
                    # Fallback to Ollama
                    response = await self._ollama_request(prompt, ollama_model)
                    self._cache_response(prompt, response, model_ctx)
                    self.stats["requests"] += 1
                    print("✅ Fallback to Ollama successful (no cost)")
                    return response
                else:
                    # Fallback to Turbo (only if not in airplane mode)
                    if self.airplane_mode:
                        raise RuntimeError("Airplane mode is ON; Turbo disabled")
                    response = await self._turbo_request(prompt)
                    self._cache_response(prompt, response, model_ctx)
                    cost = self._estimate_cost(prompt, response)
                    self.stats["total_cost"] += cost
                    self.stats["requests"] += 1
                    print(f"💰 Fallback cost: ${cost:.4f}")
                    return response
            except Exception as fallback_err:
                print(f"❌ Fallback also failed: {fallback_err}")
                raise RuntimeError(
                    f"Both primary and fallback backends failed: {primary_err}, {fallback_err}"
                ) from fallback_err

    async def _turbo_request(self, prompt: str) -> str:
        await self._ensure_session()
        if not self.api_key:
            raise RuntimeError("Missing TURBO_API_KEY; set env or enable Airplane Mode")

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "model": "turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7,
        }
        url = f"{self.primary_endpoint}/chat/completions"

        assert self.session is not None
        async with self.session.post(url, headers=headers, json=data) as resp:
            if resp.status == 200:
                body = await resp.json()
                return body["choices"][0]["message"]["content"]
            text = await resp.text()
            raise RuntimeError(f"API error {resp.status}: {text}")

    async def _ollama_request(self, prompt: str, model: str | None = None) -> str:
        await self._ensure_session()
        model = model or self.default_ollama_model
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 1000,
                "num_ctx": self.ollama_num_ctx,
                **({"num_batch": self.ollama_num_batch} if self.ollama_num_batch > 0 else {}),
            },
        }
        url = f"{self.ollama_endpoint}/api/generate"

        assert self.session is not None
        async with self.session.post(url, json=data) as resp:
            if resp.status == 200:
                body = await resp.json()
                return body.get("response", "")
            text = await resp.text()
            raise RuntimeError(f"Ollama error {resp.status}: {text}")

    async def list_ollama_models(self) -> list[str]:
        try:
            await self._ensure_session()
            url = f"{self.ollama_endpoint}/api/tags"
            assert self.session is not None
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    body = await resp.json()
                    return [m.get("name", "") for m in body.get("models", []) if m.get("name")]
                return self.ollama_models
        except Exception:
            return self.ollama_models

    async def pull_ollama_model(self, model_name: str) -> bool:
        try:
            await self._ensure_session()
            url = f"{self.ollama_endpoint}/api/pull"
            payload = {"name": model_name, "stream": False}
            assert self.session is not None
            async with self.session.post(url, json=payload) as resp:
                return resp.status == 200
        except Exception:
            return False

    def batch_optimize(
        self,
        prompts: list[str],
        use_turbo: bool = True,
        ollama_model: str | None = None,
    ) -> list[str]:
        print(f"🔄 Processing {len(prompts)} prompts...")
        model_ctx = "turbo" if (use_turbo and not self.airplane_mode) else (ollama_model or self.default_ollama_model)

        cached: list[tuple[str, str]] = []
        uncached: list[str] = []
        for p in prompts:
            if self._is_cached(p, model_ctx):
                cached.append((p, self._get_cached(p, model_ctx)))
            else:
                uncached.append(p)
        print(f"📦 {len(cached)} cached, {len(uncached)} new requests")

        async def process_batch():
            tasks: list[tuple[str, asyncio.Task[str]]] = []
            for p in uncached:
                t = asyncio.create_task(self.chat_optimized(p, use_turbo=use_turbo, ollama_model=ollama_model))
                tasks.append((p, t))
            results: list[tuple[str, str]] = []
            for p, t in tasks:
                try:
                    r = await t
                    results.append((p, r))
                except Exception as e:  # keep going
                    results.append((p, f"Error: {e}"))
            return results

        new_responses = asyncio.run(process_batch())
        all_responses = dict(cached + new_responses)
        return [all_responses[p] for p in prompts]

    def get_usage_stats(self) -> dict:
        runtime = time.time() - self.stats["start_time"]
        return {
            "session_duration_minutes": round(runtime / 60, 1),
            "total_requests": self.stats["requests"],
            "cache_hits": self.stats["cache_hits"],
            "cache_efficiency_percent": round((self.stats["cache_hits"] / max(1, self.stats["requests"])) * 100, 1),
            "errors": self.stats["errors"],
            "error_rate_percent": round((self.stats["errors"] / max(1, self.stats["requests"])) * 100, 1),
            "estimated_total_cost_usd": round(self.stats["total_cost"], 4),
            "avg_cost_per_request": round(self.stats["total_cost"] / max(1, self.stats["requests"]), 4),
            "requests_per_minute": round(self.stats["requests"] / max(1, runtime / 60), 1),
        }

    def print_cost_breakdown(self) -> None:
        s = self.get_usage_stats()
        print("\n💰 CHI PHÍ VÀ HIỆU SUẤT")
        print("=" * 40)
        print(f"💸 Total Cost: ${s['estimated_total_cost_usd']}")
        print(f"📊 Requests: {s['total_requests']}")
        print(f"📦 Cache Hits: {s['cache_hits']} ({s['cache_efficiency_percent']}%)")
        print(f"❌ Errors: {s['errors']} ({s['error_rate_percent']}%)")
        print(f"⏱️ Session: {s['session_duration_minutes']} min")
        print(f"⚡ Speed: {s['requests_per_minute']} req/min")
        if s["cache_efficiency_percent"] < 30:
            print("\n💡 TIP: Cache efficiency thấp, hãy reuse các câu hỏi tương tự")
        if s["estimated_total_cost_usd"] > 1.0:
            print("⚠️ WARNING: Chi phí cao, cân nhắc sử dụng Ollama nhiều hơn")


# Demo functions
async def demo_ollama_integration() -> None:
    print("🤖 DEMO: Ollama Integration")
    print("=" * 50)

    async with OptimizedTurboClient() as client:
        print(f"AIRPLANE_MODE: {client.airplane_mode}")
        print(f"OLLAMA_HOST: {client.ollama_endpoint}")
        print(f"OLLAMA_NUM_CTX: {client.ollama_num_ctx}")

        try:
            models = await client.list_ollama_models()
            print(f"Available models: {', '.join(models) if models else 'n/a'}")
        except Exception:
            pass

        print("\n1. 💬 Ollama Chat Test:")
        resp1 = await client.chat_optimized(
            "Xin chào! Bạn có thể giúp tôi không?", use_turbo=False, ollama_model=client.default_ollama_model
        )
        print(f"Response: {resp1[:120]}...")

        if not client.airplane_mode:
            print("\n2. 🚀 Turbo Chat Test:")
            resp2 = await client.chat_optimized("Viết function Python tính số Fibonacci", use_turbo=True)
            print(f"Turbo: {resp2[:120]}...")

        print("\n3. 📊 Usage Statistics:")
        client.print_cost_breakdown()


def demo_batch_processing() -> None:
    print("\n\n🔄 DEMO: Batch Processing")
    print("=" * 50)

    prompts = [
        "Tạo function hello world",
        "Giải thích về Python decorators",
        "Viết code để đọc file CSV",
        "Tạo function hello world",
        "Làm thế nào để tối ưu Python code?",
    ]

    client = OptimizedTurboClient()
    responses = client.batch_optimize(prompts, use_turbo=not client.airplane_mode)

    print("\nKết quả:")
    for i, (p, r) in enumerate(zip(prompts, responses, strict=True), 1):
        print(f"{i}. {p}")
        print(f"   -> {r[:80]}...")
        print()


async def main() -> None:
    print("🎯 TURBO + OLLAMA INTEGRATION DEMO")
    print("=" * 60)

    try:
        await demo_ollama_integration()
        demo_batch_processing()
        print("\n\n✅ DEMO COMPLETED!")
        print("💡 Key Benefits:")
        print("  • Seamless Turbo/Ollama integration (env-driven)")
        print("  • Airplane Mode + OLLAMA_NUM_CTX support")
        print("  • Intelligent caching + detailed cost tracking")
        print("  • Automatic fallback between backends")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("💡 Tip: Ensure Ollama is running locally (or set OLLAMA_HOST)")


if __name__ == "__main__":
    asyncio.run(main())
