from typing import Any
import Exception
import e
import f
import false
import len
import model
import model_name
import open
import print

"""
🔧 Continue Extension Fix
========================

Fix Continue extension configuration
"""
import json
from pathlib import Path

import requests


def test_ollama_connection() -> Any:
    """Test if Ollama is working"""
    print('🔍 Testing Ollama connection...')
    try:
        response = requests.get('http://127.0.0.1:11434/api/version', timeout=5)
        if response.status_code == 200:
            version = response.json()
            print(f"✅ Ollama running: v{version.get('version', 'unknown')}")
            return True
        else:
            print(f'❌ Ollama not responding: {response.status_code}')
            return False
    except Exception as e:
        print(f'❌ Cannot connect to Ollama: {e}')
        return False

def test_models() -> Any:
    """Test available models"""
    print('\n📋 Testing models...')
    try:
        response = requests.get('http://127.0.0.1:11434/api/tags', timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f'✅ Found {len(models)} models:')
            available_models = []
            for model in models:
                name = model.get('name', 'Unknown')
                print(f'   • {name}')
                available_models.append(name)
            return available_models
        else:
            print(f'❌ Cannot get models: {response.status_code}')
            return []
    except Exception as e:
        print(f'❌ Models error: {e}')
        return []

def test_model_generation(model_name: Any) -> Any:
    """Test model generation"""
    print(f'\n🧪 Testing {model_name}...')
    try:
        response = requests.post('http://127.0.0.1:11434/api/generate', json={'model': model_name, 'prompt': 'Hello', 'stream': False}, timeout=30)
        if response.status_code == 200:
            result = response.json()
            output = result.get('response', '')
            print(f'✅ {model_name}: {output[:50]}...')
            return True
        else:
            print(f'❌ {model_name} failed: {response.status_code}')
            return False
    except Exception as e:
        print(f'❌ {model_name} error: {e}')
        return False

def fix_continue_config() -> Any:
    """Fix Continue configuration"""
    print('\n🔧 Fixing Continue configuration...')
    config_path = Path.home() / '.continue' / 'config.json'
    clean_config = {'models': [{'title': 'DeepSeek Coder 6.7B', 'provider': 'ollama', 'model': 'deepseek-coder:6.7b', 'apiBase': 'http://127.0.0.1:11434'}, {'title': 'DeepSeek Coder 1.3B', 'provider': 'ollama', 'model': 'deepseek-coder:1.3b', 'apiBase': 'http://127.0.0.1:11434'}], 'tabAutocompleteModel': {'title': 'DeepSeek Fast', 'provider': 'ollama', 'model': 'deepseek-coder:1.3b', 'apiBase': 'http://127.0.0.1:11434'}, 'systemMessage': 'You are a helpful AI coding assistant. Respond in Vietnamese when appropriate.', 'allowAnonymousTelemetry': false}
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(clean_config, f, indent=2, ensure_ascii=False)
        print(f'✅ Fixed Continue config: {config_path}')
        return True
    except Exception as e:
        print(f'❌ Cannot fix config: {e}')
        return False

def create_simple_test() -> Any:
    """Create simple test for Continue"""
    print('\n🧪 Creating simple test...')
    test_script = 'import requests\nimport json\n\ndef test_continue_api():\n    """Simple test for Continue API"""\n    \n    # Test data\n    data = {\n        "model": "deepseek-coder:1.3b",\n        "prompt": "Write a simple Python hello world function:",\n        "stream": False\n    }\n    \n    try:\n        response = requests.post(\n            "http://127.0.0.1:11434/api/generate",\n            json=data,\n            timeout=30\n        )\n        \n        if response.status_code == 200:\n            result = response.json()\n            print("✅ API Response:")\n            print(result.get("response", "No response"))\n        else:\n            print(f"❌ API Error: {response.status_code}")\n            print(response.text)\n    \n    except Exception as e:\n        print(f"❌ Error: {e}")\n\nif __name__ == "__main__":\n    test_continue_api()\n'
    with open('test_continue_simple.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    print('✅ Created test_continue_simple.py')

def main() -> Any:
    """Main fix function"""
    print('🔧 CONTINUE EXTENSION FIX')
    print('=' * 40)
    if not test_ollama_connection():
        print('\n❌ Ollama not running!')
        print('💡 Start Ollama first: ollama serve')
        return False
    models = test_models()
    if not models:
        print('\n❌ No models available!')
        return False
    working_models = []
    for model in models:
        if test_model_generation(model):
            working_models.append(model)
    if not working_models:
        print('\n❌ No models working!')
        return False
    print(f'\n✅ Working models: {working_models}')
    if fix_continue_config():
        print('\n✅ Continue configuration fixed!')
    create_simple_test()
    print('\n🚀 SOLUTION:')
    print("1. 🔄 Reload VS Code: Ctrl+Shift+P > 'Developer: Reload Window'")
    print('2. 🧪 Test: python test_continue_simple.py')
    print('3. 💬 Try Continue: Ctrl+I in VS Code')
    print('4. ❓ If still not working, restart Continue extension')
    return True
if __name__ == '__main__':
    main()
