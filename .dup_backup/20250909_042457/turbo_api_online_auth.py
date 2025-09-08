import os
import Exception
import KeyboardInterrupt
import e
import f
import len
import m
import open
import print
import self

#!/usr/bin/env python3
"""
🔐 Turbo API Authentication & Online Setup
==========================================

Script để đăng nhập và sử dụng Turbo API online
API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
"""

import json
from pathlib import Path

import requests


class TurboAPIAuth:
    """Class xử lý authentication cho Turbo API"""

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://api.turbo.ai/v1"
        self.auth_url = "https://api.turbo.ai/auth"
        self.session = requests.Session()

        # Headers cho authentication
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "VS-Code-Turbo-Client/1.0",
        }

    def test_api_connection(self):
        """Test kết nối với Turbo API"""
        print("🔍 Testing Turbo API connection...")

        try:
            # Test endpoint đơn giản
            response = self.session.get(f"{self.base_url}/models", headers=self.headers, timeout=10)

            if response.status_code == 200:
                print("✅ API connection successful!")
                models = response.json()
                print(f"📋 Available models: {len(models.get('data', []))}")
                return True
            elif response.status_code == 401:
                print("❌ Authentication failed - invalid API key")
                return False
            elif response.status_code == 403:
                print("❌ Access forbidden - check API permissions")
                return False
            else:
                print(f"⚠️ API returned status {response.status_code}: {response.text}")
                return False

        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Turbo API - check internet connection")
            return False
        except requests.exceptions.Timeout:
            print("❌ API request timeout")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def validate_api_key(self):
        """Validate API key format và permissions"""
        print("🔑 Validating API key...")

        if not self.api_key or len(self.api_key) < 20:
            print("❌ Invalid API key format")
            return False

        try:
            # Test với một request đơn giản
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={"model": "turbo", "messages": [{"role": "user", "content": "test"}], "max_tokens": 1},
                timeout=15,
            )

            if response.status_code == 200:
                print("✅ API key is valid and has chat permissions")
                return True
            elif response.status_code == 401:
                print("❌ API key is invalid or expired")
                return False
            elif response.status_code == 429:
                print("⚠️ Rate limit exceeded - API key valid but limited")
                return True
            else:
                print(f"⚠️ Unexpected response {response.status_code}: {response.text[:200]}")
                return False

        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False

    def get_account_info(self):
        """Lấy thông tin tài khoản"""
        print("📊 Getting account information...")

        try:
            # Thử endpoint account info
            response = self.session.get(f"{self.base_url}/account", headers=self.headers, timeout=10)

            if response.status_code == 200:
                account_info = response.json()
                print("✅ Account info retrieved:")
                print(f"   User: {account_info.get('email', 'N/A')}")
                print(f"   Plan: {account_info.get('plan', 'N/A')}")
                print(f"   Credits: {account_info.get('credits', 'N/A')}")
                return account_info
            else:
                print("⚠️ Account info not available")
                return None

        except Exception as e:
            print(f"⚠️ Cannot get account info: {e}")
            return None

    def setup_online_config(self):
        """Cài đặt config cho sử dụng online"""
        print("⚙️ Setting up online configuration...")

        # Update .env file
        env_path = Path(".env")
        env_content = f"""# Turbo API Configuration (Online)
TURBO_API_KEY={self.api_key}
TURBO_API_ENDPOINT={self.base_url}
TURBO_MODE=online

# Ollama Configuration (Fallback)
OLLAMA_ENDPOINT=http://127.0.0.1:11434
OLLAMA_MODEL=deepseek-coder:6.7b
OLLAMA_FAST_MODEL=deepseek-coder:1.3b

# Performance Settings
OLLAMA_NUM_PARALLEL=8
OLLAMA_GPU_LAYERS=35
OLLAMA_MAX_LOADED_MODELS=3
OLLAMA_CONTEXT_LENGTH=8192
OLLAMA_NUM_BATCH=512

# Online API Settings
TURBO_MAX_TOKENS=2000
TURBO_TEMPERATURE=0.7
TURBO_TIMEOUT=30
"""

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_content)

        print(f"✅ Updated {env_path}")

        # Update Continue config for online usage
        continue_dir = Path.home() / ".continue"
        continue_config_path = continue_dir / "config.json"

        if continue_config_path.exists():
            with open(continue_config_path, encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {"models": []}

        # Add/update Turbo API model as primary
        turbo_model = {
            "title": "Turbo API (Online)",
            "provider": "openai",
            "model": "turbo",
            "apiKey": self.api_key,
            "apiBase": self.base_url,
            "contextLength": 8192,
            "priority": 1,  # Highest priority
        }

        # Remove existing Turbo API model if exists
        config["models"] = [m for m in config["models"] if m.get("title") != "Turbo API (Online)"]

        # Add as first model (highest priority)
        config["models"].insert(0, turbo_model)

        with open(continue_config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ Updated Continue config: {continue_config_path}")

    def create_online_test_script(self):
        """Tạo script test cho online mode"""
        print("🧪 Creating online test script...")

        test_script = '''#!/usr/bin/env python3
"""
🌐 Turbo API Online Test
========================

Test script để kiểm tra Turbo API online
"""

import requests
import json
import time
from datetime import datetime


def test_turbo_online():
    """Test Turbo API online"""
    api_key=os.getenv("API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🌐 TURBO API ONLINE TEST")
    print("=" * 40)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    
    # Test 1: Simple chat
    print("\\n1. 💬 Simple Chat Test:")
    try:
        response = requests.post(
            "https://api.turbo.ai/v1/chat/completions",
            headers=headers,
            json={
                "model": "turbo",
                "messages": [
                    {"role": "user", "content": "Hello! Can you help me with Python?"}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ Success: {message[:100]}...")
            
            # Calculate cost estimate
            usage = result.get("usage", {})
            tokens = usage.get("total_tokens", 0)
            cost = (tokens / 1000) * 0.002  # Estimate
            print(f"💰 Estimated cost: ${cost:.4f}")
            
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Vietnamese
    print("\\n2. 🇻🇳 Vietnamese Test:")
    try:
        response = requests.post(
            "https://api.turbo.ai/v1/chat/completions",
            headers=headers,
            json={
                "model": "turbo",
                "messages": [
                    {"role": "user", "content": "Viết một function Python để tính số Fibonacci"}
                ],
                "max_tokens": 200,
                "temperature": 0.5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ Vietnamese response: {message[:150]}...")
        else:
            print(f"❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\\n🎯 Online test completed!")


if __name__ == "__main__":
    test_turbo_online()
'''

        test_file = Path("test_turbo_online.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_script)

        print(f"✅ Created {test_file}")
        return test_file


def main():
    """Main authentication setup"""
    print("🔐 TURBO API ONLINE AUTHENTICATION SETUP")
    print("=" * 60)
    print("API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP")
    print("=" * 60)

    auth = TurboAPIAuth()

    # Step 1: Test connection
    if not auth.test_api_connection():
        print("\n❌ Cannot connect to Turbo API")
        print("💡 Check your internet connection or API endpoint")
        return False

    # Step 2: Validate API key
    if not auth.validate_api_key():
        print("\n❌ API key validation failed")
        print("💡 Check if your API key is correct and active")
        return False

    # Step 3: Get account info
    auth.get_account_info()

    # Step 4: Setup online configuration
    auth.setup_online_config()

    # Step 5: Create test script
    test_file = auth.create_online_test_script()

    print("\n🎉 ONLINE SETUP COMPLETED!")
    print("=" * 60)
    print("✅ API connection verified")
    print("✅ API key validated")
    print("✅ Online configuration updated")
    print("✅ Continue extension configured for online use")
    print("✅ Test script created")

    print("\n🚀 NEXT STEPS:")
    print("1. 🔄 Reload VS Code: Ctrl+Shift+P > 'Developer: Reload Window'")
    print("2. 🧪 Test online: python test_turbo_online.py")
    print("3. 💬 Use Continue: Ctrl+I (will use online Turbo API first)")
    print("4. 📊 Monitor usage and costs")

    print("\n💡 USAGE MODES:")
    print("• 🌐 Online: Turbo API (costs apply, high quality)")
    print("• 🏠 Fallback: Local Ollama (free, when API fails)")
    print("• 🔄 Auto-switch: Tries online first, falls back to local")

    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Ready for online AI coding!")
        else:
            print("\n❌ Setup incomplete, please check above")
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
