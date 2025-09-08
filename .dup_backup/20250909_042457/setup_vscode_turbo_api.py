#!/usr/bin/env python3
"""
🔧 VS Code Turbo API Setup
==========================

Script to configure Ollama API Turbo for VS Code
API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
"""

import json
from pathlib import Path
import Exception
import e
import f
import open
import print


def setup_vscode_settings():
    """Configure VS Code settings for Turbo API"""
    print("🔧 Configuring VS Code settings...")

    # VS Code settings directory
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    settings_file = vscode_dir / "settings.json"

    # Load existing settings or create new
    if settings_file.exists():
        with open(settings_file, encoding="utf-8") as f:
            settings = json.load(f)
    else:
        settings = {}

    # Turbo API configuration
    turbo_config = {
        # Ollama Configuration
        "ollama.endpoint": "http://127.0.0.1:11434",
        "ollama.model": "deepseek-coder:6.7b",
        "ollama.apiKey": "5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP",
        # GitHub Copilot fallback
        "github.copilot.enable": {"*": True, "yaml": False, "plaintext": False, "markdown": True},
        # Continue extension (Ollama integration)
        "continue.telemetryEnabled": False,
        "continue.enableTabAutocomplete": True,
        "continue.models": [
            {
                "title": "DeepSeek Coder",
                "provider": "ollama",
                "model": "deepseek-coder:6.7b",
                "apiBase": "http://127.0.0.1:11434",
            },
            {
                "title": "DeepSeek Fast",
                "provider": "ollama",
                "model": "deepseek-coder:1.3b",
                "apiBase": "http://127.0.0.1:11434",
            },
        ],
        "continue.tabAutocompleteModel": {
            "title": "DeepSeek Fast",
            "provider": "ollama",
            "model": "deepseek-coder:1.3b",
            "apiBase": "http://127.0.0.1:11434",
        },
        # Python settings
        "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
        # Editor settings for AI assistance
        "editor.inlineSuggest.enabled": True,
        "editor.quickSuggestions": {"other": True, "comments": True, "strings": True},
        "editor.suggestOnTriggerCharacters": True,
        "editor.acceptSuggestionOnCommitCharacter": True,
        "editor.acceptSuggestionOnEnter": "on",
        "editor.tabCompletion": "on",
        # File associations
        "files.associations": {"*.py": "python", "*.md": "markdown", "*.json": "jsonc"},
    }

    # Merge configurations
    settings.update(turbo_config)

    # Save settings
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    print(f"✅ VS Code settings saved to: {settings_file}")
    return settings_file


def create_continue_config():
    """Create Continue extension config"""
    print("🔧 Creating Continue extension config...")

    config_dir = Path.home() / ".continue"
    config_dir.mkdir(exist_ok=True)

    config = {
        "models": [
            {
                "title": "DeepSeek Coder 6.7B",
                "provider": "ollama",
                "model": "deepseek-coder:6.7b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 8192,
            },
            {
                "title": "DeepSeek Coder 1.3B (Fast)",
                "provider": "ollama",
                "model": "deepseek-coder:1.3b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 4096,
            },
            {
                "title": "Turbo API",
                "provider": "openai",
                "model": "turbo",
                "apiKey": "5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP",
                "apiBase": "https://api.turbo.ai/v1",
            },
        ],
        "tabAutocompleteModel": {
            "title": "DeepSeek Fast Tab",
            "provider": "ollama",
            "model": "deepseek-coder:1.3b",
            "apiBase": "http://127.0.0.1:11434",
        },
        "systemMessage": "You are a helpful AI coding assistant. Respond in Vietnamese when appropriate.",
        "completionOptions": {"temperature": 0.2, "topP": 1, "presencePenalty": 0, "frequencyPenalty": 0},
        "allowAnonymousTelemetry": False,
        "docs": [],
        "contextProviders": [
            {"name": "code", "params": {}},
            {"name": "docs", "params": {}},
            {"name": "diff", "params": {}},
            {"name": "terminal", "params": {}},
            {"name": "problems", "params": {}},
            {"name": "folder", "params": {}},
            {"name": "codebase", "params": {}},
        ],
        "slashCommands": [
            {"name": "edit", "description": "Edit code in current file"},
            {"name": "comment", "description": "Write comments for code"},
            {"name": "share", "description": "Export conversation"},
            {"name": "commit", "description": "Generate commit message"},
        ],
    }

    config_file = config_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Continue config saved to: {config_file}")
    return config_file


def create_env_file():
    """Create environment file with API key"""
    print("🔐 Creating environment file...")

    env_content = """# Turbo API Configuration
TURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
TURBO_API_ENDPOINT=https://api.turbo.ai/v1

# Ollama Configuration  
OLLAMA_ENDPOINT=http://127.0.0.1:11434
OLLAMA_MODEL=deepseek-coder:6.7b
OLLAMA_FAST_MODEL=deepseek-coder:1.3b

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

    print(f"✅ Environment file created: {env_file}")
    print("⚠️  Đừng commit file .env vào git!")

    # Add to .gitignore
    gitignore_file = Path(".gitignore")
    if gitignore_file.exists():
        with open(gitignore_file) as f:
            content = f.read()
    else:
        content = ""

    if ".env" not in content:
        with open(gitignore_file, "a") as f:
            f.write("\n# Environment files\n.env\n.env.local\n")
        print("✅ Added .env to .gitignore")

    return env_file


def create_launch_config():
    """Create VS Code launch configuration"""
    print("🚀 Creating launch configuration...")

    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Test Turbo API",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/optimized_turbo_client.py",
                "console": "integratedTerminal",
                "envFile": "${workspaceFolder}/.env",
                "justMyCode": True,
            },
            {
                "name": "Quick Turbo Test",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/quick_start_turbo.py",
                "console": "integratedTerminal",
                "envFile": "${workspaceFolder}/.env",
            },
            {
                "name": "Setup Ollama",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/configure_turbo_ollama.py",
                "args": ["all"],
                "console": "integratedTerminal",
            },
        ],
    }

    launch_file = vscode_dir / "launch.json"
    with open(launch_file, "w", encoding="utf-8") as f:
        json.dump(launch_config, f, indent=2)

    print(f"✅ Launch config saved to: {launch_file}")
    return launch_file


def create_tasks_config():
    """Create VS Code tasks configuration"""
    print("⚙️ Creating tasks configuration...")

    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Start Ollama Server",
                "type": "shell",
                "command": "ollama",
                "args": ["serve"],
                "group": "build",
                "isBackground": True,
                "presentation": {"echo": True, "reveal": "always", "focus": False, "panel": "new"},
                "problemMatcher": [],
            },
            {
                "label": "Test Turbo API",
                "type": "shell",
                "command": "python",
                "args": ["${workspaceFolder}/optimized_turbo_client.py"],
                "group": "test",
                "presentation": {"echo": True, "reveal": "always", "focus": True, "panel": "new"},
            },
            {
                "label": "Configure Turbo Ollama",
                "type": "shell",
                "command": "python",
                "args": ["${workspaceFolder}/configure_turbo_ollama.py", "all"],
                "group": "build",
                "presentation": {"echo": True, "reveal": "always", "focus": True, "panel": "new"},
            },
            {
                "label": "Pull DeepSeek Models",
                "type": "shell",
                "command": "ollama",
                "args": ["pull", "deepseek-coder:6.7b"],
                "group": "build",
                "presentation": {"echo": True, "reveal": "always", "focus": True, "panel": "new"},
            },
        ],
    }

    tasks_file = vscode_dir / "tasks.json"
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks_config, f, indent=2)

    print(f"✅ Tasks config saved to: {tasks_file}")
    return tasks_file


def create_quick_start_script():
    """Create quick start script for testing"""
    print("🚀 Creating quick start script...")

    script_content = '''#!/usr/bin/env python3
"""
🚀 Quick Start Turbo API Test
============================

Quick test script for Turbo API with key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
"""

import asyncio
import os
import sys
from pathlib import Path

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
            print("\\n1. 🇻🇳 Vietnamese Test:")
            response = await client.chat_optimized("Xin chào! Tôi cần giúp đỡ về lập trình Python.")
            print(f"Response: {response[:200]}...")
            
            # Test code generation
            print("\\n2. 💻 Code Generation Test:")
            response = await client.chat_optimized("Write a Python function to calculate factorial")
            print(f"Code: {response[:300]}...")
            
            # Print stats
            print("\\n3. 📊 Quick Stats:")
            stats = client.get_usage_stats()
            print(f"   Requests: {stats['total_requests']}")
            print(f"   Cache hits: {stats['cache_hits']}")
            print(f"   Cost: ${stats['estimated_total_cost_usd']}")
            
            print("\\n✅ Quick test completed successfully!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("💡 Make sure Ollama is running as fallback")


if __name__ == "__main__":
    asyncio.run(quick_test())
'''

    script_file = Path("quick_start_turbo.py")
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_content)

    print(f"✅ Quick start script created: {script_file}")
    return script_file


def create_extensions_list():
    """Create recommended extensions list"""
    print("📦 Creating extensions recommendations...")

    extensions = {
        "recommendations": [
            "continue.continue",  # Continue - AI coding assistant
            "ms-python.python",  # Python
            "ms-python.vscode-pylance",  # Pylance
            "ms-toolsai.jupyter",  # Jupyter
            "github.copilot",  # GitHub Copilot (backup)
            "ms-vscode.vscode-json",  # JSON
            "redhat.vscode-yaml",  # YAML
            "bradlc.vscode-tailwindcss",  # Tailwind (if needed)
            "esbenp.prettier-vscode",  # Prettier
            "ms-vscode.powershell",  # PowerShell
        ]
    }

    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    extensions_file = vscode_dir / "extensions.json"
    with open(extensions_file, "w", encoding="utf-8") as f:
        json.dump(extensions, f, indent=2)

    print(f"✅ Extensions recommendations saved to: {extensions_file}")
    print("💡 VS Code will suggest installing these extensions")
    return extensions_file


def main():
    """Main setup function"""
    print("🎯 VS CODE TURBO API SETUP")
    print("=" * 50)
    print("Setting up VS Code for Ollama API Turbo")
    print("API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP")
    print("=" * 50)

    try:
        # Create all configuration files
        setup_vscode_settings()
        create_continue_config()
        create_env_file()
        create_launch_config()
        create_tasks_config()
        create_quick_start_script()
        create_extensions_list()

        print("\\n🎉 SETUP COMPLETED!")
        print("=" * 50)
        print("✅ VS Code settings configured")
        print("✅ Continue extension configured")
        print("✅ Environment variables set")
        print("✅ Launch configurations created")
        print("✅ Tasks configured")
        print("✅ Quick start script ready")
        print("✅ Extensions recommendations added")

        print("\\n🚀 NEXT STEPS:")
        print("1. 📦 Install recommended extensions (VS Code will prompt)")
        print("2. 🔄 Reload VS Code (Ctrl+Shift+P > 'Developer: Reload Window')")
        print("3. ▶️  Start Ollama: Ctrl+Shift+P > 'Tasks: Run Task' > 'Start Ollama Server'")
        print("4. 🧪 Test API: F5 > Select 'Test Turbo API'")
        print("5. 💬 Use Continue: Ctrl+I or click Continue icon in sidebar")

        print("\\n💡 USAGE TIPS:")
        print("• Use Ctrl+I for inline chat with Continue")
        print("• Tab autocomplete will use DeepSeek models")
        print("• Primary API will try Turbo first, fallback to Ollama")
        print("• Check .env file for API configuration")

    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎯 Ready to code with AI assistance!")
    else:
        print("\\n❌ Setup incomplete, please check errors above")
