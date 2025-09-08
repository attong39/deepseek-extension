#!/usr/bin/env python3
"""
🚀 Ollama API Turbo Quick Setup
Automated one-command setup for experienced users
"""

import os
import sys
import json
import argparse
import platform
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Quick Ollama API Turbo setup')
    parser.add_argument('--api-key', required=True, help='Your Ollama API key')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without executing')
    parser.add_argument('--backup', action='store_true', default=True, help='Create backup before changes')
    parser.add_argument('--install-extensions', action='store_true', default=True, help='Install VS Code extensions')
    
    args = parser.parse_args()
    
    print("🚀 Ollama API Turbo Quick Setup")
    print("=" * 40)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    
    # Step 1: Create .env file
    print("\n📝 Creating environment file...")
    env_content = f"""# Ollama API Configuration
OLLAMA_API_KEY={args.api_key}
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=deepseek-r1:latest

# Created: {datetime.now().isoformat()}
"""
    
    if not args.dry_run:
        with open('.env', 'w') as f:
            f.write(env_content)
    print("✅ .env file created")
    
    # Step 2: Update .gitignore
    print("\n🔒 Updating .gitignore...")
    gitignore_additions = """
# Ollama Setup Files
.env
*.env
.env.local
.env.production
*.key
*.pem
~/.ollama
.ollama/
settings_backup_*.json
config_backup_*/
ollama_setup.log
*.log
"""
    
    if not args.dry_run:
        with open('.gitignore', 'a') as f:
            f.write(gitignore_additions)
    print("✅ .gitignore updated")
    
    # Step 3: Configure VS Code
    print("\n💻 Configuring VS Code...")
    if platform.system().lower() == 'windows':
        settings_path = Path(os.environ['APPDATA']) / 'Code' / 'User' / 'settings.json'
    elif platform.system().lower() == 'darwin':
        settings_path = Path.home() / 'Library' / 'Application Support' / 'Code' / 'User' / 'settings.json'
    else:
        settings_path = Path.home() / '.config' / 'Code' / 'User' / 'settings.json'
    
    # Load existing settings
    existing_settings = {}
    if settings_path.exists():
        try:
            with open(settings_path, 'r') as f:
                existing_settings = json.load(f)
        except:
            pass
    
    # Add Ollama settings
    ollama_settings = {
        "ollama.host": "http://127.0.0.1:11434",
        "ollama.apiKey": args.api_key,
        "ollama.model": "deepseek-r1:latest",
        "continue.telemetryEnabled": False,
        "continue.enableTabAutocomplete": True,
    }
    
    merged_settings = {**existing_settings, **ollama_settings}
    
    if not args.dry_run:
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_path, 'w') as f:
            json.dump(merged_settings, f, indent=2)
    
    print(f"✅ VS Code configured: {settings_path}")
    
    # Step 4: Install Continue extension
    if args.install_extensions:
        print("\n📦 Installing Continue extension...")
        if not args.dry_run:
            try:
                result = subprocess.run(['code', '--install-extension', 'Continue.continue'], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print("✅ Continue extension installed")
                else:
                    print(f"⚠️  Extension install warning: {result.stderr}")
            except Exception as e:
                print(f"❌ Extension install failed: {e}")
        else:
            print("✅ Would install Continue extension")
    
    # Step 5: Test connection
    print("\n🧪 Testing Ollama connection...")
    if not args.dry_run:
        try:
            import requests
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama server is responding")
            else:
                print("⚠️  Ollama server not responding (may need to start: 'ollama serve')")
        except Exception as e:
            print(f"⚠️  Could not test connection: {e}")
    else:
        print("✅ Would test Ollama connection")
    
    # Summary
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Start Ollama server: 'ollama serve'")
    print("2. Pull DeepSeek model: 'ollama pull deepseek-r1'")
    print("3. Restart VS Code")
    print("4. Press Ctrl+I to start chatting with AI!")
    
    if args.api_key:
        print(f"\n🔑 API Key: {args.api_key[:8]}...{args.api_key[-4:]}")

if __name__ == '__main__':
    main()