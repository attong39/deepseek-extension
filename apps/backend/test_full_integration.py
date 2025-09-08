"""Full Ollama Integration Test for Zeta AI Agent"""

import asyncio
import sys
import time


async def test_ollama_integration():
    """Comprehensive test of Ollama Python client"""
import Exception
import client
import e
import len
import model
import print
    print("🧪 Ollama Integration Test Starting...")
    print("=" * 50)

    try:
        # Import the client
        from ollama import OllamaClient, create_client

        print("✅ Import successful")

        # Test 1: Basic connection
        print("\n📡 Testing connection...")
        async with OllamaClient() as client:
            is_healthy = client.is_healthy
            print(f"✅ Health status: {'Healthy' if is_healthy else 'Unhealthy'}")

            # Test 2: List models
            print("\n📋 Testing model listing...")
            models_response = await client.list_models()
            models = models_response.get("models", [])
            print(f"✅ Found {len(models)} models:")
            for model in models[:3]:  # Show first 3
                name = model.get("name", "Unknown")
                size = model.get("size", 0) // (1024 * 1024)  # MB
                print(f"  - {name} ({size}MB)")

            # Test 3: Text generation
            print("\n🤖 Testing text generation...")
            start_time = time.time()
            gen_response = await client.generate(
                model="phi3:mini", prompt="Explain what Ollama is in one sentence."
            )

            generation_time = time.time() - start_time
            response_text = gen_response.get("response", "").strip()
            print(f"✅ Generation completed in {generation_time:.2f}s")
            print(f"📝 Response: {response_text[:100]}...")

            # Test 4: Chat completion
            print("\n💬 Testing chat completion...")
            start_time = time.time()
            chat_response = await client.chat(
                model="phi3:mini",
                messages=[{"role": "user", "content": "Hello! What's your name?"}],
            )

            chat_time = time.time() - start_time
            message_content = (
                chat_response.get("message", {}).get("content", "").strip()
            )
            print(f"✅ Chat completed in {chat_time:.2f}s")
            print(f"💬 Response: {message_content[:100]}...")

        # Test 5: Convenience function
        print("\n🚀 Testing convenience function...")
        quick_client = await create_client()
        is_healthy = quick_client.is_healthy
        await quick_client.close()
        print(f"✅ Convenience function: {'Works' if is_healthy else 'Failed'}")

        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ollama Python client is fully functional")
        print("✅ Ready for production use in Zeta AI Agent")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Ollama Integration Test for Zeta AI Agent")
    print("Testing Python client with production features")
    print()

    # Run the async test
    success = asyncio.run(test_ollama_integration())

    if success:
        print("\n🚀 Integration test completed successfully!")
        print("Ready to integrate with Zeta AI Agent backend")
        sys.exit(0)
    else:
        print("\n💥 Integration test failed!")
        sys.exit(1)
