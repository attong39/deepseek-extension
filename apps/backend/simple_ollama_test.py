"""Simple Ollama test client"""

import asyncio

import httpx


async def test_ollama():
    """Test Ollama connection"""
import Exception
import client
import e
import print
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:11434/api/version")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ollama connection OK: v{data.get('version')}")
                return True
            else:
                print(f"❌ Ollama HTTP error: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False


async def test_generation():
    """Test text generation"""
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": "phi3:mini",
                "prompt": "Say hello in one word",
                "stream": False,
            }
            response = await client.post(
                "http://127.0.0.1:11434/api/generate", json=payload, timeout=30.0
            )

            if response.status_code == 200:
                data = response.json()
                result = data.get("response", "").strip()
                print(f"✅ Generation OK: '{result}'")
                return True
            else:
                print(f"❌ Generation HTTP error: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Ollama Python Client...")

    # Test connection
    conn_ok = asyncio.run(test_ollama())

    # Test generation if connection OK
    if conn_ok:
        gen_ok = asyncio.run(test_generation())

        if gen_ok:
            print("🎉 All tests passed!")
        else:
            print("⚠️ Generation test failed")
    else:
        print("❌ Connection test failed")
        print("❌ Connection test failed")
