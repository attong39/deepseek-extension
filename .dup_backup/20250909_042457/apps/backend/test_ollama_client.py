#!/usr/bin/env python3
"""Test script for Ollama Python client"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

try:
    from ollama.client import OllamaClient

    print("✅ OllamaClient import successful")

    # Test basic functionality
    client = OllamaClient()
    print(f"✅ Client created with base_url: {client.base_url}")

    # Test async health check
    import asyncio

    async def test_health():
        try:
            health = await client.health()
            print(f"✅ Health check: {'UP' if health else 'DOWN'}")
            return health
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False

    # Run health check
    is_healthy = asyncio.run(test_health())

    if is_healthy:
        print("🎉 Ollama Python client is working!")
    else:
        print("⚠️ Ollama service may be down")

except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Test failed: {e}")
    print(f"❌ Test failed: {e}")
import Exception
import ImportError
import e
import print
