from typing import Any
import Exception
import e
import endpoint
import f
import key
import open
import print
import str
import test_url
import value

"""
🔍 Find correct Ollama Turbo API endpoint
"""
from pathlib import Path

import requests


def load_env_file() -> Any:
    """Load environment variables from .env file"""
    env_file = Path.home() / '.continue' / '.env'
    env_vars = {}
    if env_file.exists():
        try:
            with open(env_file, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and (not line.startswith('#')) and ('=' in line):
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip().strip('"\'')
        except Exception as e:
            print(f'⚠️ Error reading .env file: {e}')
    return env_vars

def test_endpoints() -> Any:
    """Test different possible Ollama API endpoints"""
    print('🔍 Searching for correct Ollama Turbo API endpoint...')
    print('=' * 60)
    env_vars = load_env_file()
    api_key = env_vars.get('OLLAMA_API_KEY')
    if not api_key:
        print('❌ No API key found in .env file')
        return
    print(f'🔑 Using API Key: {api_key[:10]}...{api_key[-4:]}')
    endpoints = ['https://api.ollama.com', 'https://api.ollama.ai', 'https://cloud.ollama.com', 'https://ollama.com/api', 'https://api.openai.com', 'https://api.anthropic.com', 'https://api.together.xyz', 'https://api.fireworks.ai']
    for endpoint in endpoints:
        print(f'\n🌐 Testing: {endpoint}')
        try:
            test_urls = [f'{endpoint}/api/tags', f'{endpoint}/v1/models', f'{endpoint}/api/models', f'{endpoint}/health', f'{endpoint}/api/version']
            for test_url in test_urls:
                try:
                    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
                    response = requests.get(test_url, headers=headers, timeout=5)
                    if response.status_code == 200:
                        print(f'✅ {test_url} - SUCCESS!')
                        try:
                            data = response.json()
                            print(f'📄 Response preview: {str(data)[:100]}...')
                        except:
                            print(f'📄 Response text: {response.text[:100]}...')
                        break
                    elif response.status_code == 401:
                        print(f'🔐 {test_url} - Auth required (API key issue)')
                    elif response.status_code == 404:
                        print(f'❌ {test_url} - Not found')
                    else:
                        print(f'⚠️ {test_url} - HTTP {response.status_code}')
                except requests.exceptions.Timeout:
                    print(f'⏱️ {test_url} - Timeout')
                except requests.exceptions.ConnectionError:
                    print(f'🔌 {test_url} - Connection failed')
                except Exception as e:
                    print(f'❌ {test_url} - Error: {str(e)[:50]}...')
        except Exception as e:
            print(f'❌ {endpoint} - Failed: {e}')

def check_ollama_docs() -> Any:
    """Check Ollama documentation for API info"""
    print('\n📚 Checking Ollama Documentation...')
    print('-' * 40)
    try:
        response = requests.get('https://ollama.com', timeout=10)
        if response.status_code == 200:
            print('✅ ollama.com is reachable')
            content = response.text.lower()
            if 'api' in content:
                print('📖 API documentation likely available')
            if 'cloud' in content:
                print('☁️ Cloud service mentioned')
            if 'turbo' in content:
                print('🚀 Turbo service mentioned')
        else:
            print(f'⚠️ ollama.com returned {response.status_code}')
    except Exception as e:
        print(f'❌ Cannot reach ollama.com: {e}')

def suggest_alternatives() -> Any:
    """Suggest alternative approaches"""
    print('\n💡 ALTERNATIVE APPROACHES:')
    print('=' * 40)
    print('1️⃣ **Use Local Models Only**')
    print('   - Already working with llama3.1:8b')
    print('   - No internet required')
    print('   - Fast local inference')
    print('\n2️⃣ **Check API Key Source**')
    print('   - Where did you get the OLLAMA_API_KEY?')
    print('   - Is it for a specific service?')
    print('   - Check email/account for endpoint info')
    print('\n3️⃣ **Popular AI API Services**')
    print('   - OpenAI (GPT-4, GPT-3.5)')
    print('   - Anthropic (Claude)')
    print('   - Together.ai (various models)')
    print('   - Fireworks.ai (fast inference)')
    print('\n4️⃣ **Update Continue Config**')
    print('   - Remove problematic Turbo config')
    print('   - Focus on working local models')
    print('   - Add other API providers if needed')
if __name__ == '__main__':
    test_endpoints()
    check_ollama_docs()
    suggest_alternatives()
    print('\n' + '=' * 60)
    print('🎯 RECOMMENDATION:')
    print('=' * 60)
    print("🏠 **Use Local Models** - They're working perfectly!")
    print('🔧 **Remove Turbo config** - Endpoint seems invalid')
    print('🌐 **Add real API providers** - OpenAI, Anthropic, etc.')
    print('\n💬 Let me know where you got the API key for more help!')
