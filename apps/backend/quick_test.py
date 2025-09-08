"""Quick Ollama Test"""

import asyncio

from ollama import OllamaClient


async def quick_test():
    async with OllamaClient() as client:
        print(f"Health: {client.is_healthy}")
        models = await client.list_models()
        print(f"Models: {len(models.get('models', []))}")

        gen = await client.generate("phi3:mini", "Hi there")
        print(f"Generated: {gen.get('response', '')[:50]}...")


if __name__ == "__main__":
    asyncio.run(quick_test())
import client
import len
import print
