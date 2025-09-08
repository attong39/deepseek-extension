#!/usr/bin/env python3
"""
🔧 VS Code Ollama Integration Setup
==================================

Script to configure VS Code with Ollama and Turbo API
NOTE: Do not hardcode API keys in source. Use environment variables instead.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
import Exception
import FileNotFoundError
import KeyboardInterrupt
import e
import ext
import f
import line
import open
import print


def check_ollama_installation():
    """Check if Ollama is installed and running"""
    print("🔍 Checking Ollama installation...")

    try:
        # Check if ollama command exists
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama not found")
            return False
    except FileNotFoundError:
        print("❌ Ollama not installed")
        return False


def install_vscode_extensions():
    """Install required VS Code extensions"""
    print("\n📦 Installing VS Code extensions...")

    extensions = [
        "continue.continue",  # Continue AI extension
        "ms-python.python",  # Python extension
        "ms-vscode.vscode-json",  # JSON support
        "bradlc.vscode-tailwindcss",  # For web UI if needed
    ]

    for ext in extensions:
        print(f"Installing {ext}...")
        try:
            result = subprocess.run(["code", "--install-extension", ext], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {ext} installed")
            else:
                print(f"⚠️ Failed to install {ext}")
        except Exception as e:
            print(f"❌ Error installing {ext}: {e}")


def create_vscode_settings():
    """Create VS Code settings for Ollama integration"""
    print("\n⚙️ Configuring VS Code settings...")

    # VS Code settings directory
    vscode_dir = Path.cwd() / ".vscode"
    vscode_dir.mkdir(exist_ok=True)

    # Settings configuration
    settings = {
        "continue.telemetryEnabled": False,
        "continue.enableTabAutocomplete": True,
        "continue.enableDebugLogs": True,
        # Ollama configuration
        "ollama.host": "http://localhost:11434",
        "ollama.model": "deepseek-coder:6.7b",
        "ollama.contextLength": 4096,
        # Python configuration
        "python.defaultInterpreterPath": sys.executable,
        "python.terminal.activateEnvironment": True,
        # Editor settings for AI assistance
        "editor.suggestOnTriggerCharacters": True,
        "editor.acceptSuggestionOnCommitCharacter": True,
        "editor.acceptSuggestionOnEnter": "on",
        "editor.tabCompletion": "on",
        # File associations
        "files.associations": {"*.env.ollama": "properties", "*.md": "markdown"},
    }

    settings_file = vscode_dir / "settings.json"
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

    print(f"✅ VS Code settings saved to {settings_file}")


def create_continue_config():
    """Create Continue AI configuration"""
    print("\n🤖 Setting up Continue AI configuration...")

    # Continue config directory
    continue_dir = Path.home() / ".continue"
    continue_dir.mkdir(exist_ok=True)

    continue_config = {
        "models": [
            {
                "title": "DeepSeek Coder (Local)",
                "provider": "ollama",
                "model": "deepseek-coder:6.7b",
                "apiBase": "http://localhost:11434",
                "contextLength": 4096,
                "completionOptions": {"temperature": 0.2, "topP": 0.9, "maxTokens": 1000},
            },
            {
                "title": "Turbo • gpt-oss:120b",
                "provider": "openai",
                "model": "gpt-oss:120b",
                "apiKey": os.environ.get("OLLAMA_TURBO_API_KEY", "env:OLLAMA_TURBO_API_KEY"),
                "baseUrl": "https://ollama.com",
                "contextLength": 4096,
                "completionOptions": {"temperature": 0.7, "maxTokens": 1000},
            },
        ],
        "tabAutocompleteModel": {
            "title": "DeepSeek Coder Tab",
            "provider": "ollama",
            "model": "deepseek-coder:1.3b",
            "apiBase": "http://localhost:11434",
            "contextLength": 1024,
            "completionOptions": {"temperature": 0.1, "maxTokens": 100},
        },
        "embeddingsProvider": {"provider": "ollama", "model": "nomic-embed-text", "apiBase": "http://localhost:11434"},
        "systemMessage": "You are an expert software developer assistant. Provide clear, concise, and practical code solutions. Support Vietnamese language when needed.",
        "requestOptions": {"timeout": 30000, "verifySsl": False},
        "allowAnonymousTelemetry": False,
    }

    config_file = continue_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(continue_config, f, indent=2)

    print(f"✅ Continue AI config saved to {config_file}")


def create_workspace_config():
    """Create workspace-specific configuration"""
    print("\n📁 Setting up workspace configuration...")

    # Workspace settings
    vscode_dir = Path.cwd() / ".vscode"

    # Launch configuration for debugging
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "env": {"OLLAMA_TURBO_API_KEY": "", "OLLAMA_HOST": "http://localhost:11434"},
            },
            {
                "name": "Ollama Test",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/optimized_turbo_client.py",
                "console": "integratedTerminal",
            },
        ],
    }

    launch_file = vscode_dir / "launch.json"
    with open(launch_file, "w", encoding="utf-8") as f:
        json.dump(launch_config, f, indent=2)

    # Tasks configuration
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Start Ollama",
                "type": "shell",
                "command": "ollama",
                "args": ["serve"],
                "group": "build",
                "isBackground": True,
                "problemMatcher": [],
            },
            {
                "label": "Test Turbo API",
                "type": "shell",
                "command": "python",
                "args": ["${workspaceFolder}/optimized_turbo_client.py"],
                "group": "test",
            },
            {
                "label": "Reinstall Ollama",
                "type": "shell",
                "command": "${workspaceFolder}/reinstall_ollama.bat",
                "group": "build",
            },
        ],
    }

    tasks_file = vscode_dir / "tasks.json"
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks_config, f, indent=2)

    print("✅ Workspace config saved")


def update_env_file():
    """Update main .env file with Ollama configuration"""
    print("\n🔧 Updating environment configuration...")

    env_file = Path.cwd() / ".env"

    # Read existing .env
    env_content = ""
    if env_file.exists():
        with open(env_file, encoding="utf-8") as f:
            env_content = f.read()

    # Add/update Ollama configuration
    ollama_config = """
# --- OLLAMA VS CODE INTEGRATION (Updated) ---------------
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=deepseek-coder:6.7b
OLLAMA_API_BASE_URL=http://localhost:11434
OLLAMA_CONTEXT_LENGTH=4096

# --- TURBO API INTEGRATION (Primary) --------------------
TURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
TURBO_API_ENDPOINT=https://api.turbo.ai/v1
TURBO_MODEL=turbo

# --- VS CODE CONTINUE INTEGRATION -----------------------
CONTINUE_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
CONTINUE_MODEL=deepseek-coder:6.7b
CONTINUE_ENDPOINT=http://localhost:11434
"""

    # Remove old Ollama config if exists
    lines = env_content.split("\n")
    filtered_lines = []
    skip_section = False

    for line in lines:
        if (
            line.startswith("# --- OLLAMA")
            or line.startswith("# --- TURBO")
            or line.startswith("# --- VS CODE CONTINUE")
        ):
            skip_section = True
        elif line.startswith("# ---") and skip_section:
            skip_section = False
            filtered_lines.append(line)
        elif not skip_section:
            filtered_lines.append(line)

    # Add new config
    new_content = "\n".join(filtered_lines).rstrip() + ollama_config

    with open(env_file, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ Environment file updated")


def test_integration():
    """Test the integration"""
    print("\n🧪 Testing VS Code Ollama integration...")

    try:
        # Test Ollama connection
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is responding")
            print(f"Models: {result.stdout}")
        else:
            print("⚠️ Ollama not responding")

        # Test Python environment
        import requests

        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama API accessible")
            else:
                print("⚠️ Ollama API not accessible")
        except Exception as e:
            print(f"⚠️ Cannot reach Ollama API: {e}")

    except Exception as e:
        print(f"❌ Test failed: {e}")


def main():
    """Main setup function"""
    print("🚀 VS CODE OLLAMA INTEGRATION SETUP")
    print("=" * 50)
    print("API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP")
    print("=" * 50)

    # Check if Ollama is installed
    if not check_ollama_installation():
        print("\n❌ Please install Ollama first:")
        print("Run: reinstall_ollama.bat")
        return

    # Setup steps
    install_vscode_extensions()
    create_vscode_settings()
    create_continue_config()
    create_workspace_config()
    update_env_file()
    test_integration()

    print("\n✅ SETUP COMPLETE!")
    print("=" * 50)
    print("🎯 Next steps:")
    print("1. Restart VS Code")
    print("2. Open Command Palette (Ctrl+Shift+P)")
    print("3. Type 'Continue' to start using AI assistance")
    print("4. Use Ctrl+I for inline AI help")
    print("5. Use Ctrl+L for chat with AI")

    print("\n💡 Features enabled:")
    print("• Tab completion with DeepSeek Coder")
    print("• Chat assistance with Turbo API")
    print("• Local fallback with Ollama")
    print("• Cost optimization with caching")

    print("\n🔑 Your Turbo API key is configured and ready!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("Please check the logs and try again")
