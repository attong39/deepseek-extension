#!/usr/bin/env python3
"""
🚀 Turbo Ollama API Usage Examples
=================================

Comprehensive examples showing how to use the Turbo Ollama API effectively.
"""

import asyncio
import time

from turbo_ollama_client import APIProvider, TurboOllamaClient
import Exception
import KeyboardInterrupt
import chunk
import client
import e
import enumerate
import example
import i
import len
import print
import q
import question
import size
import zip


async def example_basic_chat():
    """Example 1: Basic chat interaction"""
    print("=" * 50)
    print("🗣️  Example 1: Basic Chat")
    print("=" * 50)

    async with TurboOllamaClient() as client:
        # Simple Vietnamese chat
        response = await client.chat("Xin chào! Bạn có thể giúp tôi viết code Python không?")
        print(f"AI: {response}")

        # Follow-up question
        response = await client.chat("Viết một function tính số Fibonacci")
        print(f"AI: {response}")


async def example_streaming_chat():
    """Example 2: Streaming chat for real-time responses"""
    print("\n" + "=" * 50)
    print("🌊 Example 2: Streaming Chat")
    print("=" * 50)

    async with TurboOllamaClient() as client:
        print("AI: ", end="", flush=True)

        async for chunk in client.stream_chat("Giải thích chi tiết về Machine Learning bằng tiếng Việt"):
            print(chunk, end="", flush=True)
        print("\n")


async def example_code_completion():
    """Example 3: Code completion and generation"""
    print("\n" + "=" * 50)
    print("💻 Example 3: Code Completion")
    print("=" * 50)

    async with TurboOllamaClient() as client:
        # Python code completion
        code_prompt = """
def calculate_prime_numbers(limit):
    # Viết code để tìm tất cả số nguyên tố nhỏ hơn limit
"""

        result = await client.complete_code(code_prompt, language="python")
        print("Generated Code:")
        print(result)


async def example_provider_comparison():
    """Example 4: Compare different API providers"""
    print("\n" + "=" * 50)
    print("⚡ Example 4: Provider Comparison")
    print("=" * 50)

    prompt = "Viết một function Python để sắp xếp mảng"

    async with TurboOllamaClient() as client:
        # Test Turbo API (if available)
        try:
            start_time = time.time()
            turbo_response = await client.chat(prompt, provider=APIProvider.TURBO)
            turbo_time = time.time() - start_time
            print(f"🚀 Turbo API ({turbo_time:.2f}s): {turbo_response[:100]}...")
        except Exception as e:
            print(f"❌ Turbo API không khả dụng: {e}")

        # Test local Ollama
        try:
            start_time = time.time()
            ollama_response = await client.chat(prompt, provider=APIProvider.OLLAMA)
            ollama_time = time.time() - start_time
            print(f"🏠 Local Ollama ({ollama_time:.2f}s): {ollama_response[:100]}...")
        except Exception as e:
            print(f"❌ Local Ollama không khả dụng: {e}")


async def example_advanced_features():
    """Example 5: Advanced features - caching, retries, etc."""
    print("\n" + "=" * 50)
    print("🔧 Example 5: Advanced Features")
    print("=" * 50)

    async with TurboOllamaClient() as client:
        # Test caching
        prompt = "Giải thích về async/await trong Python"

        # First request (will be cached)
        start_time = time.time()
        response1 = await client.chat(prompt)
        first_time = time.time() - start_time
        print(f"🔍 First request ({first_time:.2f}s): {response1[:50]}...")

        # Second request (should use cache)
        start_time = time.time()
        response2 = await client.chat(prompt)
        cached_time = time.time() - start_time
        print(f"⚡ Cached request ({cached_time:.2f}s): {response2[:50]}...")

        print(f"📊 Cache speedup: {first_time/cached_time:.1f}x faster")


async def example_batch_processing():
    """Example 6: Batch processing multiple requests"""
    print("\n" + "=" * 50)
    print("📦 Example 6: Batch Processing")
    print("=" * 50)

    questions = [
        "Giải thích về list comprehension trong Python",
        "Sự khác biệt giữa tuple và list",
        "Cách sử dụng decorator trong Python",
        "Giải thích về context manager",
        "Async programming trong Python",
    ]

    async with TurboOllamaClient() as client:
        # Process all questions concurrently
        start_time = time.time()
        tasks = [client.chat(q) for q in questions]
        responses = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        print(f"⚡ Processed {len(questions)} questions in {total_time:.2f}s")
        for i, (question, response) in enumerate(zip(questions, responses, strict=True)):
            print(f"\n{i+1}. Q: {question}")
            print(f"   A: {response[:80]}...")


async def example_error_handling():
    """Example 7: Error handling and fallback"""
    print("\n" + "=" * 50)
    print("🛡️  Example 7: Error Handling")
    print("=" * 50)

    async with TurboOllamaClient() as client:
        try:
            # This might fail if model is not available
            response = await client.chat("Test message", model="non-existent-model", provider=APIProvider.OLLAMA)
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error occurred: {e}")

            # Automatic fallback with AUTO provider
            print("🔄 Trying with AUTO provider...")
            response = await client.chat("Test message", provider=APIProvider.AUTO)
            print(f"✅ Fallback successful: {response[:50]}...")


async def example_performance_monitoring():
    """Example 8: Performance monitoring"""
    print("\n" + "=" * 50)
    print("📈 Example 8: Performance Monitoring")
    print("=" * 50)

    async with TurboOllamaClient() as client:
        # Test different request sizes
        small_prompt = "Xin chào"
        medium_prompt = "Viết một function Python để tính giai thừa với giải thích chi tiết"
        large_prompt = """
        Tạo một ứng dụng web hoàn chỉnh sử dụng FastAPI với các tính năng:
        1. Authentication với JWT
        2. CRUD operations cho User model
        3. Database integration với SQLAlchemy
        4. API documentation với Swagger
        5. Error handling và logging
        6. Unit tests
        Bao gồm code chi tiết và giải thích từng phần.
        """

        prompts = [("Small", small_prompt), ("Medium", medium_prompt), ("Large", large_prompt)]

        for size, prompt in prompts:
            start_time = time.time()
            response = await client.chat(prompt)
            elapsed = time.time() - start_time

            print(f"📊 {size} prompt:")
            print(f"   ⏱️  Time: {elapsed:.2f}s")
            print(f"   📝 Response length: {len(response)} chars")
            print(f"   🚀 Speed: {len(response)/elapsed:.0f} chars/sec")


async def main():
    """Run all examples"""
    print("🚀 Turbo Ollama API Usage Examples")
    print("=" * 60)

    examples = [
        example_basic_chat,
        example_streaming_chat,
        example_code_completion,
        example_provider_comparison,
        example_advanced_features,
        example_batch_processing,
        example_error_handling,
        example_performance_monitoring,
    ]

    for example in examples:
        try:
            await example()
            await asyncio.sleep(1)  # Brief pause between examples
        except KeyboardInterrupt:
            print("\n❌ Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error in {example.__name__}: {e}")

    print("\n✅ All examples completed!")


if __name__ == "__main__":
    # Configure environment if needed
    import os

    # Set default values if not configured
    if not os.getenv("OLLAMA_ENDPOINT"):
        os.environ["OLLAMA_ENDPOINT"] = "http://127.0.0.1:11434"

    if not os.getenv("OLLAMA_MODEL"):
        os.environ["OLLAMA_MODEL"] = "deepseek-coder"

    # Run examples
    asyncio.run(main())
