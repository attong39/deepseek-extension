import os
from typing import Any
import Exception
import KeyboardInterrupt
import e
import f
import len
import m
import model
import open
import print
import self

'\n🔐 Ollama Online Authentication Setup\n====================================\n\nSetup for Ollama online service with your account credentials\nAPI Key: 7da59eeb32d8447bbf291f5842bbe3a7.KoeW1XFcpJqaLn7-2LbRjMNY\n'
import json
from pathlib import Path

import requests


class OllamaOnlineAuth:
    """Class xử lý authentication cho Ollama online service"""

    def __init__(self: Any) -> Any:
        self.api_key = os.getenv('API_KEY')
        self.base_url = 'https://api.ollama.com/v1'
        self.auth_header = f'Bearer {self.api_key}'
        self.ssh_keys = ['ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOL6rVMt+Ei5N35MdBIhreieNTiPjubotHD0zB/n98xY', 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJieyliQp85617/ikDTyFTGCM+ZrG+aMLMLoGmqZ5CGq', 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAiDhr0NYsRO6vO0w0C4txzd+xt4x/gMnbcQfH/v6pxU']
        self.headers = {'Authorization': self.auth_header, 'Content-Type': 'application/json', 'User-Agent': 'Ollama-VS-Code-Client/1.0'}

    def test_ollama_online_connection(self: Any) -> Any:
        """Test connection to Ollama online service"""
        print('🌐 Testing Ollama online connection...')
        try:
            response = requests.get(f'{self.base_url}/models', headers=self.headers, timeout=15)
            if response.status_code == 200:
                models = response.json()
                print('✅ Connected to Ollama online!')
                print(f"📋 Available models: {len(models.get('models', []))}")
                for model in models.get('models', [])[:5]:
                    name = model.get('name', 'Unknown')
                    size = model.get('size', 'Unknown')
                    print(f'   • {name} ({size})')
                return True
            elif response.status_code == 401:
                print('❌ Authentication failed - invalid API key')
                return False
            elif response.status_code == 403:
                print('❌ Access forbidden - check API permissions')
                return False
            else:
                print(f'⚠️ Unexpected response {response.status_code}: {response.text}')
                return False
        except requests.exceptions.ConnectionError as e:
            print(f'❌ Connection error: {e}')
            print('💡 Check if api.ollama.com is accessible')
            return False
        except Exception as e:
            print(f'❌ Error: {e}')
            return False

    def test_chat_api(self: Any) -> Any:
        """Test chat completions with Ollama online"""
        print('💬 Testing chat API...')
        try:
            response = requests.post(f'{self.base_url}/chat/completions', headers=self.headers, json={'model': 'llama3.2:3b', 'messages': [{'role': 'user', 'content': 'Hello! Can you help me with Python programming?'}], 'max_tokens': 100}, timeout=30)
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f'✅ Chat API working: {message[:100]}...')
                usage = result.get('usage', {})
                if usage:
                    print(f"📊 Tokens used: {usage.get('total_tokens', 'N/A')}")
                return True
            else:
                print(f'❌ Chat API failed: {response.status_code}')
                print(f'Response: {response.text}')
                return False
        except Exception as e:
            print(f'❌ Chat test error: {e}')
            return False

    def get_account_info(self: Any) -> Any:
        """Get account information"""
        print('👤 Getting account information...')
        try:
            response = requests.get(f'{self.base_url}/account', headers=self.headers, timeout=10)
            if response.status_code == 200:
                account = response.json()
                print('✅ Account info:')
                print(f"   Username: {account.get('username', 'USDT239')}")
                print(f"   Plan: {account.get('plan', 'N/A')}")
                print(f"   Usage: {account.get('usage', 'N/A')}")
                return account
            else:
                print('⚠️ Account info not available via API')
                return None
        except Exception as e:
            print(f'⚠️ Cannot get account info: {e}')
            return None

    def setup_ollama_online_config(self: Any) -> Any:
        """Setup configuration for Ollama online"""
        print('⚙️ Setting up Ollama online configuration...')
        env_content = f'# Ollama Online Configuration\nOLLAMA_ONLINE_API_KEY={self.api_key}\nOLLAMA_ONLINE_ENDPOINT={self.base_url}\nOLLAMA_MODE=hybrid\n\n# Local Ollama (Fallback)\nOLLAMA_LOCAL_ENDPOINT=http://127.0.0.1:11434\nOLLAMA_LOCAL_MODEL=deepseek-coder:6.7b\nOLLAMA_FAST_MODEL=deepseek-coder:1.3b\n\n# Performance Settings\nOLLAMA_NUM_PARALLEL=8\nOLLAMA_GPU_LAYERS=35\nOLLAMA_MAX_LOADED_MODELS=3\nOLLAMA_CONTEXT_LENGTH=8192\nOLLAMA_NUM_BATCH=512\n\n# API Settings\nOLLAMA_TIMEOUT=30\nOLLAMA_MAX_TOKENS=2000\nOLLAMA_TEMPERATURE=0.7\n'
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print('✅ Updated .env file')
        continue_dir = Path.home() / '.continue'
        continue_config_path = continue_dir / 'config.json'
        if continue_config_path.exists():
            with open(continue_config_path, encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {'models': []}
        online_models = [{'title': 'Llama 3.2 3B (Online)', 'provider': 'ollama', 'model': 'llama3.2:3b', 'apiKey': self.api_key, 'apiBase': self.base_url, 'contextLength': 8192, 'priority': 1}, {'title': 'DeepSeek Coder (Online)', 'provider': 'ollama', 'model': 'deepseek-coder:6.7b', 'apiKey': self.api_key, 'apiBase': self.base_url, 'contextLength': 8192, 'priority': 2}, {'title': 'Local DeepSeek (Fallback)', 'provider': 'ollama', 'model': 'deepseek-coder:6.7b', 'apiBase': 'http://127.0.0.1:11434', 'contextLength': 8192, 'priority': 3}]
        config['models'] = [m for m in config['models'] if 'ollama' not in m.get('provider', '').lower()]
        config['models'].extend(online_models)
        config['tabAutocompleteModel'] = {'title': 'Fast Autocomplete', 'provider': 'ollama', 'model': 'deepseek-coder:1.3b', 'apiBase': 'http://127.0.0.1:11434'}
        with open(continue_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f'✅ Updated Continue config: {continue_config_path}')

    def update_vscode_settings(self: Any) -> Any:
        """Update VS Code settings for Ollama online"""
        print('🔧 Updating VS Code settings...')
        vscode_dir = Path('.vscode')
        settings_file = vscode_dir / 'settings.json'
        if settings_file.exists():
            with open(settings_file, encoding='utf-8') as f:
                settings = json.load(f)
        else:
            settings = {}
        ollama_settings = {'ollama.endpoint': self.base_url, 'ollama.apiKey': self.api_key, 'ollama.model': 'llama3.2:3b', 'ollama.fallbackEndpoint': 'http://127.0.0.1:11434', 'ollama.mode': 'hybrid'}
        settings.update(ollama_settings)
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print(f'✅ Updated VS Code settings: {settings_file}')

    def create_test_script(self: Any) -> Any:
        """Create test script for Ollama online"""
        print('🧪 Creating Ollama online test script...')
        test_script = f'''#!/usr/bin/env python3\n"""\n🌐 Ollama Online API Test\n=========================\n\nTest script for Ollama online service\nAPI Key: {self.api_key[:20]}...\n"""\n\nimport requests\nimport json\nimport time\n\n\ndef test_ollama_online():\n    """Test Ollama online service"""\n    api_key=os.getenv("API_KEY")\n    base_url = "{self.base_url}"\n    \n    headers = {{\n        "Authorization": f"Bearer {{api_key}}",\n        "Content-Type": "application/json"\n    }}\n    \n    print("🌐 OLLAMA ONLINE API TEST")\n    print("=" * 40)\n    print(f"Endpoint: {{base_url}}")\n    print("=" * 40)\n    \n    # Test 1: List models\n    print("\\n1. 📋 Available Models:")\n    try:\n        response = requests.get(f"{{base_url}}/models", headers=headers, timeout=10)\n        if response.status_code == 200:\n            models = response.json()\n            print(f"✅ Found {{len(models.get('models', []))}} models")\n            for model in models.get('models', [])[:5]:\n                print(f"   • {{model.get('name', 'Unknown')}}")\n        else:\n            print(f"❌ Failed: {{response.status_code}}")\n    except Exception as e:\n        print(f"❌ Error: {{e}}")\n    \n    # Test 2: Chat completion\n    print("\\n2. 💬 Chat Test:")\n    try:\n        response = requests.post(\n            f"{{base_url}}/chat/completions",\n            headers=headers,\n            json={{\n                "model": "llama3.2:3b",\n                "messages": [\n                    {{"role": "user", "content": "Write a simple Python hello world function"}}\n                ],\n                "max_tokens": 150\n            }},\n            timeout=30\n        )\n        \n        if response.status_code == 200:\n            result = response.json()\n            message = result["choices"][0]["message"]["content"]\n            print(f"✅ Chat response: {{message[:100]}}...")\n            \n            usage = result.get("usage", {{}})\n            if usage:\n                print(f"📊 Tokens: {{usage.get('total_tokens', 'N/A')}}")\n        else:\n            print(f"❌ Chat failed: {{response.status_code}}")\n            print(f"Response: {{response.text}}")\n    except Exception as e:\n        print(f"❌ Chat error: {{e}}")\n    \n    # Test 3: Vietnamese\n    print("\\n3. 🇻🇳 Vietnamese Test:")\n    try:\n        response = requests.post(\n            f"{{base_url}}/chat/completions",\n            headers=headers,\n            json={{\n                "model": "llama3.2:3b",\n                "messages": [\n                    {{"role": "user", "content": "Viết một function Python tính số Fibonacci"}}\n                ],\n                "max_tokens": 200\n            }},\n            timeout=30\n        )\n        \n        if response.status_code == 200:\n            result = response.json()\n            message = result["choices"][0]["message"]["content"]\n            print(f"✅ Vietnamese: {{message[:100]}}...")\n        else:\n            print(f"❌ Failed: {{response.status_code}}")\n    except Exception as e:\n        print(f"❌ Error: {{e}}")\n    \n    print("\\n🎯 Ollama online test completed!")\n\n\nif __name__ == "__main__":\n    test_ollama_online()\n'''
        test_file = Path('test_ollama_online.py')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_script)
        print(f'✅ Created test script: {test_file}')
        return test_file

def main() -> Any:
    """Main setup function"""
    print('🚀 OLLAMA ONLINE AUTHENTICATION SETUP')
    print('=' * 60)
    print('Account: USDT239')
    print('API Key: 7da59eeb32d8447bbf291f5842bbe3a7.KoeW1XFcpJqaLn7-2LbRjMNY')
    print('=' * 60)
    auth = OllamaOnlineAuth()
    if not auth.test_ollama_online_connection():
        print('\\n⚠️ Cannot connect to Ollama online')
        print('💡 Will setup hybrid mode (online + local fallback)')
    auth.test_chat_api()
    auth.get_account_info()
    auth.setup_ollama_online_config()
    auth.update_vscode_settings()
    test_file = auth.create_test_script()
    print('\\n🎉 OLLAMA ONLINE SETUP COMPLETED!')
    print('=' * 60)
    print('✅ API key configured')
    print('✅ Hybrid mode setup (online + local)')
    print('✅ Continue extension configured')
    print('✅ VS Code settings updated')
    print('✅ Test script created')
    print('\\n🚀 NEXT STEPS:')
    print("1. 🔄 Reload VS Code: Ctrl+Shift+P > 'Developer: Reload Window'")
    print('2. 🧪 Test online: python test_ollama_online.py')
    print('3. 💬 Use Continue: Ctrl+I (will try online first)')
    print('4. 🏠 Fallback: Local Ollama if online fails')
    print('\\n💡 USAGE MODES:')
    print('• 🌐 Primary: Ollama online (your account)')
    print('• 🏠 Fallback: Local Ollama (when offline)')
    print('• ⚡ Tab completion: Local (for speed)')
    print('• 🔄 Auto-switch: Best of both worlds')
    return True
if __name__ == '__main__':
    try:
        success = main()
        if success:
            print('\\n🎯 Ollama online authentication ready!')
        else:
            print('\\n❌ Setup incomplete')
    except KeyboardInterrupt:
        print('\\n👋 Setup cancelled')
    except Exception as e:
        print(f'\\n❌ Setup error: {e}')
