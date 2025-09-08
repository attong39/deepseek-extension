#!/usr/bin/env python3
"""
🚀 Quick Start Turbo API Test
============================

Quick test script for Turbo API with key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
"""

import asyncio
import sys
from pathlib import Path
import Exception
import ImportError
import client
import e
import print
import str

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from optimized_turbo_client import OptimizedTurboClient
except ImportError:
    print("❌ optimized_turbo_client.py not found!")
    sys.exit(1)


async def quick_test():
    """Quick test function"""
    print("🚀 QUICK TURBO API TEST")
    print("=" * 40)
    print("API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP")
    print("=" * 40)

    async with OptimizedTurboClient() as client:
        try:
            # Test Vietnamese
            print("\n1. 🇻🇳 Vietnamese Test:")
            response = await client.chat_optimized("Xin chào! Tôi cần giúp đỡ về lập trình Python.")
            print(f"Response: {response[:200]}...")

            # Test code generation
            print("\n2. 💻 Code Generation Test:")
            response = await client.chat_optimized("Write a Python function to calculate factorial")
            print(f"Code: {response[:300]}...")

            # Print stats
            print("\n3. 📊 Quick Stats:")
            stats = client.get_usage_stats()
            print(f"   Requests: {stats['total_requests']}")
            print(f"   Cache hits: {stats['cache_hits']}")
            print(f"   Cost: ${stats['estimated_total_cost_usd']}")

            print("\n✅ Quick test completed successfully!")

        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("💡 Make sure Ollama is running as fallback")


if __name__ == "__main__":
    asyncio.run(quick_test())
