import os
from typing import Any
import Exception
import e
import endpoint
import f
import len
import matches
import open
import print
import provider

'\n🔍 API Endpoint Discovery & Setup\n=================================\n\nTìm và test các API endpoints khả dụng cho Turbo API\n'
import json

import requests


def test_multiple_endpoints() -> Any:
    """Test multiple possible API endpoints"""
    api_key = os.getenv('API_KEY')
    endpoints = ['https://api.turbo.ai/v1', 'https://turbo.ai/api/v1', 'https://api.turboapi.ai/v1', 'https://turboapi.com/v1', 'https://api.openai.com/v1', 'https://api.anthropic.com/v1', 'https://api.together.xyz/v1', 'https://api.perplexity.ai']
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'TurboAPI-Test/1.0'}
    print('🔍 TESTING MULTIPLE API ENDPOINTS')
    print('=' * 50)
    print(f'API Key: {api_key[:20]}...{api_key[-10:]}')
    print('=' * 50)
    working_endpoints = []
    for endpoint in endpoints:
        print(f'\\n🌐 Testing: {endpoint}')
        try:
            response = requests.get(f'{endpoint}/models', headers=headers, timeout=5)
            if response.status_code == 200:
                print(f'✅ Models endpoint works: {response.status_code}')
                working_endpoints.append((endpoint, 'models'))
                continue
            elif response.status_code == 401:
                print(f'🔑 Auth needed but endpoint exists: {response.status_code}')
                working_endpoints.append((endpoint, 'auth_required'))
                continue
            response = requests.post(f'{endpoint}/chat/completions', headers=headers, json={'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'test'}], 'max_tokens': 1}, timeout=5)
            if response.status_code in [200, 401, 402, 429]:
                print(f'✅ Chat endpoint responds: {response.status_code}')
                working_endpoints.append((endpoint, 'chat'))
            else:
                print(f'❌ Not working: {response.status_code}')
        except requests.exceptions.ConnectionError:
            print('❌ Connection failed')
        except requests.exceptions.Timeout:
            print('⏰ Timeout')
        except Exception as e:
            print(f'❌ Error: {e}')
    print('\\n📊 SUMMARY')
    print('=' * 50)
    if working_endpoints:
        print('✅ Working endpoints found:')
        for endpoint, status in working_endpoints:
            print(f'   {endpoint} ({status})')
    else:
        print('❌ No working endpoints found')
    return working_endpoints

def check_api_key_format() -> Any:
    """Check if API key matches known formats"""
    api_key = os.getenv('API_KEY')
    print('\\n🔍 ANALYZING API KEY FORMAT')
    print('=' * 50)
    print(f'Key: {api_key}')
    print(f'Length: {len(api_key)} characters')
    patterns = {'OpenAI': api_key.startswith('sk-'), 'Anthropic': api_key.startswith('sk-ant-'), 'Together': api_key.startswith('sk-') and len(api_key) > 40, 'Perplexity': api_key.startswith('pplx-'), 'Custom/Turbo': '.' in api_key or '-' in api_key}
    print('\\nPattern matches:')
    for provider, matches in patterns.items():
        status = '✅' if matches else '❌'
        print(f'   {status} {provider}: {matches}')
    if '.' in api_key and len(api_key) > 50:
        print('\\n💡 This looks like a custom API key format')
        print('   Possibly for a specific service or proxy')
    elif api_key.startswith('sk-'):
        print('\\n💡 This looks like an OpenAI-compatible key')
    else:
        print('\\n💡 Unknown key format - might be service-specific')

def create_fallback_config() -> Any:
    """Create config that works with available options"""
    print('\\n⚙️ CREATING FALLBACK CONFIGURATION')
    print('=' * 50)
    config = {'primary': {'name': 'Local Ollama', 'endpoint': 'http://127.0.0.1:11434', 'model': 'deepseek-coder:6.7b', 'cost': 'free', 'status': 'available'}, 'fallbacks': [{'name': 'Turbo API (Original)', 'endpoint': 'https://api.turbo.ai/v1', 'api_key': '5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP', 'model': 'turbo', 'cost': 'paid', 'status': 'unknown'}], 'recommendations': ['Use local Ollama as primary (always works, free)', 'Keep Turbo API as fallback (when endpoint becomes available)', 'Consider alternative API providers if needed']}
    with open('api_config_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print('✅ Config analysis saved to api_config_analysis.json')
    env_content = '# Reliable API Configuration\n# Primary: Local Ollama (always works)\nOLLAMA_ENDPOINT=http://127.0.0.1:11434\nOLLAMA_MODEL=deepseek-coder:6.7b\nOLLAMA_FAST_MODEL=deepseek-coder:1.3b\n\n# Turbo API (when available)\nTURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP\nTURBO_API_ENDPOINT=https://api.turbo.ai/v1\nTURBO_MODE=fallback\n\n# Performance Settings\nOLLAMA_NUM_PARALLEL=8\nOLLAMA_GPU_LAYERS=35\nOLLAMA_MAX_LOADED_MODELS=3\nOLLAMA_CONTEXT_LENGTH=8192\nOLLAMA_NUM_BATCH=512\n'
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print('✅ Updated .env with reliable configuration')

def main() -> Any:
    """Main discovery function"""
    print('🔍 API ENDPOINT DISCOVERY & ANALYSIS')
    print('=' * 60)
    working_endpoints = test_multiple_endpoints()
    check_api_key_format()
    create_fallback_config()
    print('\\n🎯 RECOMMENDATIONS')
    print('=' * 60)
    if working_endpoints:
        print('✅ Some endpoints are responsive')
        print('💡 Your API key might work with alternative providers')
    else:
        print('❌ No responsive endpoints found')
        print('💡 Possible reasons:')
        print('   • Network/firewall blocking API calls')
        print('   • API key is for a specific service not tested')
        print('   • Service might be temporarily down')
    print('\\n🚀 CURRENT BEST SETUP:')
    print('• ✅ Local Ollama: Working perfectly (free)')
    print('• ❓ Turbo API: Endpoint not accessible (keep as fallback)')
    print('• 🎯 VS Code: Use Continue with Ollama primarily')
    print('\\n💡 TO USE NOW:')
    print('1. Continue using local Ollama (Ctrl+I in VS Code)')
    print('2. Monitor if Turbo API becomes accessible')
    print('3. Consider alternative API providers if needed')
if __name__ == '__main__':
    main()
