#!/usr/bin/env python3
"""
Zeta AI Models Verification Script
Tests all available AI models in the development environment
"""

import json
import os
import subprocess
from datetime import datetime
import Exception
import available_models
import e
import error
import f
import len
import line
import model
import ollama_running
import open
import output
import print
import success
import test_prompt
import var


def run_ollama_command(command):
    """Run an Ollama command and return the result"""
    try:
        result = subprocess.run(command, shell=False, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"


def test_model(model_name, test_prompt="def fibonacci(n):"):
    """Test a specific model with a simple prompt"""
    print(f"\n🧪 Testing {model_name}...")
    command = f'ollama run {model_name} "{test_prompt}"'
    success, output, error = run_ollama_command(command)

    if success and output.strip():
        print(f"✅ {model_name}: Working")
        return True
    else:
        print(f"❌ {model_name}: Failed - {error}")
        return False


def check_ollama_status():
    """Check if Ollama is running"""
    print("🔍 Checking Ollama status...")
    success, output, error = run_ollama_command("ollama list")

    if success:
        print("✅ Ollama is running")
        print("\n📋 Available models:")
        lines = output.strip().split("\n")
        models = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                model_name = line.split()[0]
                models.append(model_name)
                print(f"   • {model_name}")
        return True, models
    else:
        print(f"❌ Ollama not running: {error}")
        return False, []


def check_continue_config():
    """Check Continue extension configuration"""
    config_path = os.path.expanduser("~/.continue/config.json")

    if os.path.exists(config_path):
        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)

            print("✅ Continue config found")
            print(f"   • Models configured: {len(config.get('models', []))}")

            for model in config.get("models", []):
                title = model.get("title", "Unknown")
                provider = model.get("provider", "Unknown")
                model_name = model.get("model", "Unknown")
                print(f"   • {title} ({provider}: {model_name})")

            return True
        except Exception as e:
            print(f"❌ Continue config error: {e}")
            return False
    else:
        print("❌ Continue config not found")
        return False


def check_environment_variables():
    """Check required environment variables"""
    print("\n🔧 Checking environment variables...")

    required_vars = ["TURBO_API_KEY"]
    all_good = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✅ {var}: {masked}")
        else:
            print(f"❌ {var}: Not set")
            all_good = False

    return all_good


def main():
    """Main verification function"""
    print("🚀 Zeta AI Models Verification")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check Ollama status
    ollama_running, available_models = check_ollama_status()

    if not ollama_running:
        print("\n❌ Cannot proceed without Ollama running")
        return

    # Test key models
    print("\n🧪 Testing AI Models")
    print("-" * 30)

    key_models = ["MFDoom/deepseek-coder-v2-tool-calling:16b", "deepseek-coder:6.7b", "deepseek-coder:1.3b"]

    working_models = []
    for model in key_models:
        if model in available_models:
            if test_model(model):
                working_models.append(model)
        else:
            print(f"⚠️  {model}: Not downloaded")

    # Check Continue configuration
    print("\n⚙️  Checking VS Code Integration")
    print("-" * 30)
    continue_ok = check_continue_config()

    # Check environment
    env_ok = check_environment_variables()

    # Summary
    print("\n📊 Summary")
    print("=" * 50)
    print(f"✅ Working AI models: {len(working_models)}/{len(key_models)}")
    print(f"✅ Continue extension: {'OK' if continue_ok else 'Issues'}")
    print(f"✅ Environment vars: {'OK' if env_ok else 'Issues'}")

    if len(working_models) == len(key_models) and continue_ok and env_ok:
        print("\n🎉 All systems are GO! Your AI development environment is ready.")
    else:
        print("\n⚠️  Some issues detected. Check the details above.")

    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
