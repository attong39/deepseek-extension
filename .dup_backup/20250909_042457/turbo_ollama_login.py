#!/usr/bin/env python3
"""
🔐 Turbo Ollama Login & Authentication System
=============================================

Hệ thống đăng nhập và xác thực cho Turbo Ollama
Hỗ trợ cả online API và local models
"""

import getpass
import json
import sys
from datetime import datetime
from pathlib import Path

import requests
import Exception
import bool
import dict
import f
import input
import len
import m
import new_mode
import open
import print
import self
import str
import url


class TurboOllamaAuth:
    """Class xử lý authentication và login cho Turbo Ollama"""

    def __init__(self):
        self.config_dir = Path.home() / ".turbo-ollama"
        self.config_file = self.config_dir / "auth.json"
        self.env_file = Path(".env")

        # Tạo thư mục config nếu chưa có
        self.config_dir.mkdir(exist_ok=True)

        # Load existing config
        self.config = self.load_config()

        # API endpoints to try
        self.api_endpoints = [
            "https://api.turbo.ai/v1",
            "https://api.ollama.com/v1",
            "https://cloud.ollama.com/api",
            "https://api.together.xyz/v1",
            "https://api.fireworks.ai/inference/v1",
        ]

        self.local_ollama = "http://127.0.0.1:11434"

    def load_config(self) -> dict:
        """Load existing authentication config"""
        if self.config_file.exists():
            try:
                with open(self.config_file, encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {}

    def save_config(self):
        """Save authentication config"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def login_interactive(self):
        """Interactive login process"""
        print("🔐 TURBO OLLAMA LOGIN")
        print("=" * 40)

        # Option 1: Use existing API key
        if self.config.get("api_key"):
            print(f"✅ Found existing API key: {self.config['api_key'][:10]}...{self.config['api_key'][-4:]}")
            use_existing = input("Use existing API key? (y/n): ").lower().strip()

            if use_existing == "y":
                return self.validate_existing_auth()

        # Option 2: Enter new API key
        print("\n📝 Enter your API key:")
        print("💡 You can get this from:")
        print("   - https://ollama.com/account (if using Ollama Cloud)")
        print("   - https://api.turbo.ai/account (if using Turbo API)")
        print("   - Or use 'local' for local-only mode")

        api_key = getpass.getpass("🔑 API Key (or 'local'): ").strip()

        if api_key.lower() == "local":
            return self.setup_local_only()

        if len(api_key) < 10:
            print("❌ API key too short")
            return False

        # Test the API key
        return self.test_and_save_auth(api_key)

    def setup_local_only(self):
        """Setup for local-only mode"""
        print("🏠 Setting up local-only mode...")

        # Test local Ollama
        if not self.test_local_ollama():
            print("❌ Local Ollama not available")
            print("💡 Please start Ollama: ollama serve")
            return False

        self.config = {
            "mode": "local",
            "local_endpoint": self.local_ollama,
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat(),
        }

        self.save_config()
        self.update_continue_config_local()
        self.create_env_file()

        print("✅ Local-only mode configured!")
        return True

    def test_and_save_auth(self, api_key: str) -> bool:
        """Test API key and save if valid"""
        print("🧪 Testing API key...")

        for endpoint in self.api_endpoints:
            print(f"   Trying {endpoint}...")

            if self.test_api_endpoint(api_key, endpoint):
                # Success! Save config
                self.config = {
                    "api_key": api_key,
                    "endpoint": endpoint,
                    "mode": "online",
                    "created_at": datetime.now().isoformat(),
                    "last_used": datetime.now().isoformat(),
                }

                self.save_config()
                self.update_continue_config_online()
                self.create_env_file()

                print(f"✅ Successfully authenticated with {endpoint}")
                return True

        print("❌ API key failed on all endpoints")
        return False

    def test_api_endpoint(self, api_key: str, endpoint: str) -> bool:
        """Test API key on specific endpoint"""
        try:
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

            # Try different endpoint patterns
            test_urls = [f"{endpoint}/models", f"{endpoint}/chat/completions", f"{endpoint}/api/tags"]

            for url in test_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code in [200, 401]:  # 401 means endpoint exists but auth issue
                        # Try a simple completion
                        completion_response = requests.post(
                            f"{endpoint}/chat/completions",
                            headers=headers,
                            json={
                                "model": "gpt-3.5-turbo",  # Common model name
                                "messages": [{"role": "user", "content": "test"}],
                                "max_tokens": 1,
                            },
                            timeout=15,
                        )

                        if completion_response.status_code == 200:
                            return True

                except requests.exceptions.RequestException:
                    continue

            return False

        except Exception:
            return False

    def test_local_ollama(self) -> bool:
        """Test local Ollama connection"""
        try:
            response = requests.get(f"{self.local_ollama}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def validate_existing_auth(self) -> bool:
        """Validate existing authentication"""
        if self.config.get("mode") == "local":
            return self.test_local_ollama()

        api_key = self.config.get("api_key")
        endpoint = self.config.get("endpoint")

        if not api_key or not endpoint:
            return False

        return self.test_api_endpoint(api_key, endpoint)

    def update_continue_config_online(self):
        """Update Continue config for online mode"""
        continue_dir = Path.home() / ".continue"
        continue_config = continue_dir / "config.json"

        if continue_config.exists():
            with open(continue_config, encoding="utf-8-sig") as f:
                config = json.load(f)
        else:
            config = {"models": []}

        # Add online model as primary
        online_model = {
            "title": "🚀 Turbo Online (Primary)",
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "apiKey": self.config["api_key"],
            "apiBase": self.config["endpoint"],
            "contextLength": 8192,
            "priority": 1,
        }

        # Remove existing online models
        config["models"] = [m for m in config["models"] if "Turbo Online" not in m.get("title", "")]

        # Add as first model
        config["models"].insert(0, online_model)

        with open(continue_config, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print("✅ Updated Continue config for online mode")

    def update_continue_config_local(self):
        """Update Continue config for local mode"""
        continue_dir = Path.home() / ".continue"
        continue_config = continue_dir / "config.json"

        if continue_config.exists():
            with open(continue_config, encoding="utf-8-sig") as f:
                config = json.load(f)
        else:
            config = {"models": []}

        # Ensure local models are properly configured
        local_models = [
            {
                "title": "🏠 DeepSeek Coder 6.7B (Primary)",
                "provider": "ollama",
                "model": "deepseek-coder:6.7b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 8192,
                "priority": 1,
            },
            {
                "title": "⚡ DeepSeek Coder 1.3B (Fast)",
                "provider": "ollama",
                "model": "deepseek-coder:1.3b",
                "apiBase": "http://127.0.0.1:11434",
                "contextLength": 4096,
                "priority": 2,
            },
        ]

        # Remove existing local models and add new ones
        config["models"] = [m for m in config["models"] if not m.get("apiBase", "").startswith("http://127.0.0.1")]
        config["models"] = local_models + config["models"]

        with open(continue_config, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print("✅ Updated Continue config for local mode")

    def create_env_file(self):
        """Create/update .env file"""
        env_content = f"""# Turbo Ollama Configuration
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

        if self.config.get("mode") == "online":
            env_content += f"""# Online Mode Configuration
TURBO_MODE=online
TURBO_API_KEY={self.config['api_key']}
TURBO_ENDPOINT={self.config['endpoint']}
TURBO_MODEL=gpt-3.5-turbo
TURBO_MAX_TOKENS=2000
TURBO_TEMPERATURE=0.7

# Local Ollama (Fallback)
OLLAMA_ENDPOINT=http://127.0.0.1:11434
OLLAMA_MODEL=deepseek-coder:6.7b
"""
        else:
            env_content += """# Local Mode Configuration
TURBO_MODE=local
OLLAMA_ENDPOINT=http://127.0.0.1:11434
OLLAMA_MODEL=deepseek-coder:6.7b
OLLAMA_FAST_MODEL=deepseek-coder:1.3b

# Performance Settings
OLLAMA_NUM_PARALLEL=8
OLLAMA_GPU_LAYERS=35
OLLAMA_MAX_LOADED_MODELS=3
"""

        with open(self.env_file, "w", encoding="utf-8") as f:
            f.write(env_content)

        print(f"✅ Updated {self.env_file}")

    def get_status(self) -> dict:
        """Get current authentication status"""
        if not self.config:
            return {"status": "not_configured"}

        mode = self.config.get("mode", "unknown")

        if mode == "local":
            local_available = self.test_local_ollama()
            return {"status": "local", "local_available": local_available, "last_used": self.config.get("last_used")}

        elif mode == "online":
            api_valid = self.validate_existing_auth()
            local_available = self.test_local_ollama()

            return {
                "status": "online",
                "api_valid": api_valid,
                "local_available": local_available,
                "endpoint": self.config.get("endpoint"),
                "last_used": self.config.get("last_used"),
            }

        return {"status": "unknown"}

    def logout(self):
        """Logout and clear authentication"""
        if self.config_file.exists():
            self.config_file.unlink()

        self.config = {}
        print("✅ Logged out successfully")

    def switch_mode(self, new_mode: str):
        """Switch between online and local mode"""
        if new_mode == "local":
            if self.test_local_ollama():
                self.config["mode"] = "local"
                self.save_config()
                self.update_continue_config_local()
                print("✅ Switched to local mode")
                return True
            else:
                print("❌ Local Ollama not available")
                return False

        elif new_mode == "online":
            if self.config.get("api_key") and self.validate_existing_auth():
                self.config["mode"] = "online"
                self.save_config()
                self.update_continue_config_online()
                print("✅ Switched to online mode")
                return True
            else:
                print("❌ No valid online authentication")
                return False

        return False


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Turbo Ollama Authentication")
    parser.add_argument("action", choices=["login", "logout", "status", "switch"], help="Action to perform")
    parser.add_argument("--mode", choices=["local", "online"], help="Mode to switch to (for switch action)")

    args = parser.parse_args()

    auth = TurboOllamaAuth()

    if args.action == "login":
        print("🔐 TURBO OLLAMA LOGIN")
        print("=" * 50)

        if auth.login_interactive():
            print("\n🎉 Login successful!")

            # Show status
            status = auth.get_status()
            print(f"\n📊 Status: {status['status']}")

            if status["status"] == "online":
                print(f"🌐 Endpoint: {status.get('endpoint')}")
                print(f"✅ API Valid: {status.get('api_valid')}")

            print(f"🏠 Local Available: {status.get('local_available', False)}")

            print("\n🚀 Next steps:")
            print("1. Restart VS Code")
            print("2. Use Ctrl+L for Continue chat")
            print("3. Select your preferred model")

        else:
            print("\n❌ Login failed")
            sys.exit(1)

    elif args.action == "logout":
        auth.logout()

    elif args.action == "status":
        status = auth.get_status()
        print("📊 TURBO OLLAMA STATUS")
        print("=" * 30)
        print(f"Status: {status['status']}")

        if status["status"] == "online":
            print(f"🌐 Endpoint: {status.get('endpoint')}")
            print(f"✅ API Valid: {status.get('api_valid')}")

        print(f"🏠 Local Available: {status.get('local_available', False)}")

        if status.get("last_used"):
            print(f"🕒 Last Used: {status['last_used']}")

    elif args.action == "switch":
        if not args.mode:
            print("❌ Please specify --mode (local or online)")
            sys.exit(1)

        auth.switch_mode(args.mode)


if __name__ == "__main__":
    main()
