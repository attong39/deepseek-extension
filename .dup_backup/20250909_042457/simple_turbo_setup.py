#!/usr/bin/env python3
"""
🔧 Simple Turbo Ollama Setup - Local Mode
"""

import json
from pathlib import Path

import requests
import Exception
import e
import f
import len
import model
import open
import print
import round


def setup_local_mode():
    """Setup simple local mode"""
    print("🏠 Setting up Turbo Ollama - Local Mode")
    print("=" * 50)

    # Test local Ollama first
    print("1️⃣ Testing local Ollama...")
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Local Ollama working! {len(models)} models available")

            for model in models:
                name = model.get("name", "Unknown")
                size_gb = round(model.get("size", 0) / (1024**3), 1)
                print(f"   📦 {name} ({size_gb}GB)")
        else:
            print("❌ Local Ollama not responding properly")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to local Ollama: {e}")
        print("💡 Please start Ollama: ollama serve")
        return False

    # Create/update Continue config
    print("\n2️⃣ Updating Continue config...")
    continue_dir = Path.home() / ".continue"
    continue_dir.mkdir(exist_ok=True)

    continue_config = continue_dir / "config.json"

    # Create clean config
    config = {
        "models": [
            {
                "title": "🏠 DeepSeek Coder 6.7B (Primary)",
                "provider": "ollama",
                "model": "deepseek-coder:6.7b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 8192,
                "systemMessage": "You are an expert coding assistant.",
            },
            {
                "title": "🧠 DeepSeek Coder v2 16B (Advanced)",
                "provider": "ollama",
                "model": "MFDoom/deepseek-coder-v2-tool-calling:16b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 16384,
                "systemMessage": "You are an advanced coding assistant with tool calling capabilities.",
            },
            {
                "title": "⚡ DeepSeek Coder 1.3B (Fast)",
                "provider": "ollama",
                "model": "deepseek-coder:1.3b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 4096,
                "systemMessage": "You are a fast code completion assistant.",
            },
            {
                "title": "🦙 Llama 3.1 8B (General)",
                "provider": "ollama",
                "model": "llama3.1:8b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 8192,
                "systemMessage": "You are a helpful assistant.",
            },
        ],
        "tabAutocompleteModel": {
            "title": "⚡ Fast Autocomplete",
            "provider": "ollama",
            "model": "deepseek-coder:1.3b",
            "apiBase": "http://127.0.0.1:11434",
            "contextLength": 2048,
        },
        "chatModel": {
            "title": "🏠 Primary Chat Model",
            "provider": "ollama",
            "model": "deepseek-coder:6.7b",
            "apiBase": "http://127.0.0.1:11434",
            "contextLength": 8192,
        },
        "allowAnonymousTelemetry": False,
        "docs": [],
        "contextProviders": [
            {"name": "code", "params": {}},
            {"name": "docs", "params": {}},
            {"name": "diff", "params": {}},
            {"name": "terminal", "params": {}},
            {"name": "problems", "params": {}},
        ],
        "slashCommands": [
            {"name": "edit", "description": "Edit highlighted code"},
            {"name": "comment", "description": "Write comments for highlighted code"},
            {"name": "share", "description": "Export conversation to markdown"},
            {"name": "cmd", "description": "Generate shell commands"},
            {"name": "commit", "description": "Generate commit message"},
        ],
    }

    # Write clean JSON (no BOM)
    with open(continue_config, "w", encoding="utf-8", newline="\n") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    print(f"✅ Created clean Continue config: {continue_config}")

    # Create .env file
    print("\n3️⃣ Creating .env file...")
    env_content = f"""# Turbo Ollama Configuration - Local Mode
# Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Local Mode Settings
TURBO_MODE=local
OLLAMA_ENDPOINT=http://127.0.0.1:11434
OLLAMA_PRIMARY_MODEL=deepseek-coder:6.7b
OLLAMA_FAST_MODEL=deepseek-coder:1.3b
OLLAMA_ADVANCED_MODEL=MFDoom/deepseek-coder-v2-tool-calling:16b

# Performance Settings
OLLAMA_NUM_PARALLEL=8
OLLAMA_GPU_LAYERS=35
OLLAMA_MAX_LOADED_MODELS=3
OLLAMA_CONTEXT_LENGTH=8192
OLLAMA_NUM_BATCH=512

# VS Code Integration
CONTINUE_CONFIG_PATH={continue_config}
"""

    env_file = Path(".env")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)

    print(f"✅ Created {env_file}")

    # Create auth config
    print("\n4️⃣ Creating authentication config...")
    auth_dir = Path.home() / ".turbo-ollama"
    auth_dir.mkdir(exist_ok=True)

    auth_config = {
        "mode": "local",
        "local_endpoint": "http://127.0.0.1:11434",
        "created_at": __import__("datetime").datetime.now().isoformat(),
        "last_used": __import__("datetime").datetime.now().isoformat(),
        "models_available": len(models),
    }

    auth_file = auth_dir / "auth.json"
    with open(auth_file, "w", encoding="utf-8") as f:
        json.dump(auth_config, f, indent=2, ensure_ascii=False)

    print(f"✅ Created auth config: {auth_file}")

    # Test generation
    print("\n5️⃣ Testing generation...")
    try:
        test_response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "deepseek-coder:6.7b",
                "prompt": "Hello! Please respond with 'Local Turbo Ollama is working!'",
                "stream": False,
            },
            timeout=20,
        )

        if test_response.status_code == 200:
            result = test_response.json()
            ai_response = result.get("response", "").strip()
            print("✅ Generation test successful!")
            print(f"🤖 AI Response: {ai_response}")
        else:
            print(f"⚠️ Generation test failed: {test_response.status_code}")

    except Exception as e:
        print(f"⚠️ Generation test error: {e}")

    print("\n🎉 LOCAL MODE SETUP COMPLETE!")
    print("=" * 50)

    return True


def show_usage_instructions():
    """Show usage instructions"""
    print("\n🚀 USAGE INSTRUCTIONS")
    print("=" * 30)

    print("\n📋 MODELS CONFIGURED:")
    print("🏠 DeepSeek Coder 6.7B (Primary) - Best balance")
    print("🧠 DeepSeek Coder v2 16B (Advanced) - Highest quality")
    print("⚡ DeepSeek Coder 1.3B (Fast) - Quick responses")
    print("🦙 Llama 3.1 8B (General) - General purpose")

    print("\n⌨️ VS CODE SHORTCUTS:")
    print("Ctrl+L       : Open Continue chat")
    print("Ctrl+I       : Inline code edit")
    print("Ctrl+Shift+L : Quick AI commands")
    print("Tab          : Accept AI suggestion")

    print("\n🎯 NEXT STEPS:")
    print("1. 🔄 Restart VS Code completely")
    print("2. 💬 Press Ctrl+L to start Continue chat")
    print("3. 🤖 Select 'DeepSeek Coder 6.7B (Primary)'")
    print("4. 🚀 Start coding with AI assistance!")

    print("\n💡 TIPS:")
    print("• Use 6.7B model for general coding")
    print("• Use 16B model for complex tasks")
    print("• Use 1.3B model for fast completion")
    print("• All models work offline (no internet needed)")


if __name__ == "__main__":
    print("🔧 TURBO OLLAMA SIMPLE SETUP")
    print("=" * 60)

    if setup_local_mode():
        show_usage_instructions()

        print("\n✨ READY TO USE!")
        print("Your Turbo Ollama is configured for local AI coding.")
    else:
        print("\n❌ Setup failed!")
        print("Please check Ollama is running: ollama serve")
