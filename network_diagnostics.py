from typing import Any
import Exception
import FileNotFoundError
import all
import any
import bool
import dict
import domain
import e
import endpoint
import ep
import len
import m
import model
import name
import print
import self
import str
import success
import url

"""
🔧 Network Diagnostics and Ollama Setup
=======================================

Diagnose network connectivity issues and set up Ollama for local fallback
"""
import asyncio
import os
import subprocess
from pathlib import Path

import requests


class NetworkDiagnostics:
    """Network diagnostics and connectivity testing"""

    def __init__(self: Any) -> Any:
        self.api_key = os.getenv('TURBO_API_KEY', '5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP')
        self.turbo_endpoints = ['https://api.turbo.ai/v1', 'https://turbo.ai/api/v1', 'https://api.turboapi.ai/v1', 'https://api.openai.com/v1', 'https://api.anthropic.com/v1']
        self.ollama_endpoint = 'http://127.0.0.1:11434'

    def test_dns_resolution(self: Any) -> dict[str, bool]:
        """Test DNS resolution for various endpoints"""
        print('🌐 Testing DNS Resolution...')
        results = {}
        domains = ['api.turbo.ai', 'turbo.ai', 'api.openai.com', 'google.com']
        for domain in domains:
            try:
                import socket
                socket.gethostbyname(domain)
                results[domain] = True
                print(f'✅ {domain}: Resolved')
            except socket.gaierror:
                results[domain] = False
                print(f'❌ {domain}: DNS resolution failed')
        return results

    def test_network_connectivity(self: Any) -> dict[str, dict]:
        """Test basic network connectivity"""
        print('\n🔗 Testing Network Connectivity...')
        results = {}
        test_urls = [('Google', 'https://google.com'), ('CloudFlare DNS', 'https://1.1.1.1'), ('GitHub', 'https://github.com'), ('OpenAI', 'https://api.openai.com')]
        for name, url in test_urls:
            try:
                response = requests.get(url, timeout=5)
                results[name] = {'status': response.status_code, 'success': response.status_code < 400, 'response_time': response.elapsed.total_seconds()}
                status = '✅' if results[name]['success'] else '⚠️'
                print(f"{status} {name}: {response.status_code} ({results[name]['response_time']:.2f}s)")
            except Exception as e:
                results[name] = {'success': False, 'error': str(e)}
                print(f'❌ {name}: {e}')
        return results

    def test_turbo_endpoints(self: Any) -> dict[str, dict]:
        """Test various Turbo API endpoints"""
        print('\n🚀 Testing Turbo API Endpoints...')
        results = {}
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json', 'User-Agent': 'TurboAPI-Diagnostics/1.0'}
        for endpoint in self.turbo_endpoints:
            print(f'\n🔍 Testing: {endpoint}')
            try:
                models_url = f'{endpoint}/models'
                response = requests.get(models_url, headers=headers, timeout=10)
                results[endpoint] = {'models_status': response.status_code, 'models_success': response.status_code == 200, 'models_response': response.text[:200] if response.text else ''}
                if response.status_code == 200:
                    print(f'✅ Models endpoint working: {response.status_code}')
                    chat_url = f'{endpoint}/chat/completions'
                    chat_data = {'model': 'gpt-3.5-turbo' if 'openai' in endpoint else 'turbo', 'messages': [{'role': 'user', 'content': 'Hello'}], 'max_tokens': 10}
                    chat_response = requests.post(chat_url, headers=headers, json=chat_data, timeout=10)
                    results[endpoint]['chat_status'] = chat_response.status_code
                    results[endpoint]['chat_success'] = chat_response.status_code == 200
                    if chat_response.status_code == 200:
                        print(f'✅ Chat endpoint working: {chat_response.status_code}')
                        results[endpoint]['working'] = True
                    else:
                        print(f'⚠️ Chat endpoint failed: {chat_response.status_code}')
                        results[endpoint]['working'] = False
                else:
                    print(f'❌ Models endpoint failed: {response.status_code}')
                    results[endpoint]['working'] = False
            except Exception as e:
                results[endpoint] = {'working': False, 'error': str(e)}
                print(f'❌ Connection failed: {e}')
        return results

    def test_ollama_connectivity(self: Any) -> dict[str, any]:
        """Test Ollama local connectivity"""
        print('\n🤖 Testing Ollama Connectivity...')
        try:
            response = requests.get(f'{self.ollama_endpoint}/api/tags', timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f'✅ Ollama is running with {len(models)} models')
                for model in models:
                    print(f"   - {model.get('name', 'Unknown')}")
                return {'running': True, 'models': [m.get('name') for m in models], 'model_count': len(models)}
            else:
                print(f'⚠️ Ollama responded with status: {response.status_code}')
                return {'running': False, 'status': response.status_code}
        except requests.ConnectionError:
            print('❌ Ollama is not running or not accessible')
            return {'running': False, 'error': 'Connection refused'}
        except Exception as e:
            print(f'❌ Ollama test failed: {e}')
            return {'running': False, 'error': str(e)}

    def suggest_solutions(self: Any, dns_results: dict, network_results: dict, turbo_results: dict, ollama_results: dict) -> Any:
        """Suggest solutions based on test results"""
        print('\n💡 DIAGNOSTIC RESULTS & SOLUTIONS')
        print('=' * 50)
        if not all(dns_results.values()):
            print('\n🔧 DNS Resolution Issues:')
            print('  1. Check your internet connection')
            print('  2. Try switching DNS servers (8.8.8.8, 1.1.1.1)')
            print('  3. Check firewall/antivirus settings')
            print('  4. Try using VPN if geo-blocked')
        network_working = any(result.get('success', False) for result in network_results.values())
        if not network_working:
            print('\n🔧 Network Connectivity Issues:')
            print('  1. Check internet connection')
            print('  2. Check proxy settings')
            print('  3. Verify firewall allows HTTPS traffic')
            print('  4. Try mobile hotspot to test ISP issues')
        turbo_working = any(result.get('working', False) for result in turbo_results.values())
        if not turbo_working:
            print('\n🔧 Turbo API Issues:')
            print('  1. The api.turbo.ai domain may not exist or be accessible')
            print('  2. Your API key might be for a different service')
            print('  3. Try alternative endpoints:')
            for endpoint, result in turbo_results.items():
                if result.get('working'):
                    print(f'     ✅ Working: {endpoint}')
                else:
                    print(f'     ❌ Failed: {endpoint}')
            print('  4. Consider using local Ollama as primary solution')
        if not ollama_results.get('running', False):
            print('\n🔧 Ollama Setup Required:')
            print('  1. Download Ollama from: https://ollama.ai')
            print('  2. Install and start Ollama service')
            print('  3. Pull a model: ollama pull deepseek-coder:6.7b')
            print('  4. Verify with: ollama list')
        print('\n🎯 RECOMMENDATIONS:')
        if turbo_working:
            print('  ✅ Use working Turbo API endpoint')
        elif ollama_results.get('running'):
            print('  ✅ Use local Ollama (working and free)')
        else:
            print('  🔧 Set up local Ollama as primary solution')
        print('\n📋 Action Plan:')
        print('  1. Set up Ollama for reliable local AI')
        print('  2. Configure environment for local-first approach')
        print('  3. Keep Turbo API as fallback when available')
        print('  4. Monitor for Turbo API accessibility')

class OllamaSetup:
    """Automated Ollama setup and configuration"""

    def __init__(self: Any) -> Any:
        self.ollama_endpoint = 'http://127.0.0.1:11434'
        self.recommended_models = ['deepseek-coder:6.7b', 'deepseek-coder:1.3b', 'llama3.2:3b', 'codellama:7b']

    def check_ollama_installation(self: Any) -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f'✅ Ollama installed: {result.stdout.strip()}')
                return True
            else:
                print('❌ Ollama not found in PATH')
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print('❌ Ollama not installed or not in PATH')
            return False

    def start_ollama_service(self: Any) -> bool:
        """Start Ollama service"""
        try:
            print('🔄 Starting Ollama service...')
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            response = requests.get(f'{self.ollama_endpoint}/api/tags', timeout=5)
            if response.status_code == 200:
                print('✅ Ollama service started successfully')
                return True
            else:
                print('⚠️ Ollama service may not be fully ready')
                return False
        except Exception as e:
            print(f'❌ Failed to start Ollama service: {e}')
            return False

    def pull_recommended_models(self: Any) -> dict[str, bool]:
        """Pull recommended models"""
        results = {}
        for model in self.recommended_models:
            print(f'\n📥 Pulling {model}...')
            try:
                result = subprocess.run(['ollama', 'pull', model], capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    print(f'✅ {model} downloaded successfully')
                    results[model] = True
                else:
                    print(f'❌ Failed to download {model}: {result.stderr}')
                    results[model] = False
            except subprocess.TimeoutExpired:
                print(f'⏰ {model} download timed out')
                results[model] = False
            except Exception as e:
                print(f'❌ Error downloading {model}: {e}')
                results[model] = False
        return results

    def configure_environment_for_local(self: Any) -> Any:
        """Configure environment for local-first approach without clobbering .env.

        This now writes to `.env.local` so that user edits in `.env` aren't overwritten
        by diagnostics tooling. Consumers should load `.env` first and let `.env.local`
        override where supported.
        """
        print('\n⚙️ Configuring for local-first approach...')
        env_content = '# Turbo API Configuration (Fallback)\nTURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP\nTURBO_API_BASE=https://api.turbo.ai/v1\n\n# Ollama Configuration (Primary)\nOLLAMA_HOST=http://127.0.0.1:11434\nOLLAMA_NUM_CTX=8192\nOLLAMA_NUM_PARALLEL=8\nOLLAMA_GPU_LAYERS=35\nOLLAMA_MAX_LOADED_MODELS=3\n\n# Mode Settings - LOCAL FIRST\nAIRPLANE_MODE=false\nTURBO_MODE=local_first\nPREFER_LOCAL=true\n\n# Performance Optimization\nOLLAMA_CONTEXT_LENGTH=8192\nOLLAMA_NUM_BATCH=512\n\n# Logging and Monitoring\nTURBO_LOG_LEVEL=INFO\nTURBO_CACHE_ENABLED=true\nTURBO_RATE_LIMIT_RPM=60\n\n# VS Code Integration\nCONTINUE_CONFIG_PATH=%USERPROFILE%\\.continue\\config.json\nVSCODE_SETTINGS_PATH=.vscode\\settings.json\n'
        env_local = Path('.env.local')
        try:
            existing = env_local.read_text(encoding='utf-8') if env_local.exists() else None
        except Exception:
            existing = None
        if existing == env_content:
            print('✅ .env.local already up to date (no changes written)')
        else:
            try:
                if env_local.exists():
                    env_local.with_suffix('.local.bak').write_text(existing or '', encoding='utf-8')
                env_local.write_text(env_content, encoding='utf-8')
                print('✅ Wrote local-first configuration to .env.local')
            except Exception as e:
                print(f'❌ Failed to write .env.local: {e}')

async def main() -> Any:
    """Main diagnostic and setup function"""
    print('🔧 NETWORK DIAGNOSTICS & OLLAMA SETUP')
    print('=' * 60)
    diagnostics = NetworkDiagnostics()
    print('Phase 1: Network Diagnostics')
    print('-' * 30)
    dns_results = diagnostics.test_dns_resolution()
    network_results = diagnostics.test_network_connectivity()
    turbo_results = diagnostics.test_turbo_endpoints()
    ollama_results = diagnostics.test_ollama_connectivity()
    diagnostics.suggest_solutions(dns_results, network_results, turbo_results, ollama_results)
    print('\n' + '=' * 60)
    print('Phase 2: Ollama Setup')
    print('-' * 30)
    setup = OllamaSetup()
    if not ollama_results.get('running', False):
        print('\n🤖 Setting up Ollama for local AI...')
        if not setup.check_ollama_installation():
            print('\n💡 Ollama Installation Required:')
            print('  1. Download from: https://ollama.ai')
            print('  2. Run the installer')
            print('  3. Restart this script')
            return
        if setup.start_ollama_service():
            print('\n📥 Downloading recommended models...')
            model_results = setup.pull_recommended_models()
            successful_models = [model for model, success in model_results.items() if success]
            if successful_models:
                print(f'\n✅ Successfully set up {len(successful_models)} models:')
                for model in successful_models:
                    print(f'   - {model}')
        setup.configure_environment_for_local()
    else:
        print('✅ Ollama is already running and configured')
    print('\n' + '=' * 60)
    print('🎯 FINAL RECOMMENDATIONS')
    print('=' * 60)
    if ollama_results.get('running', False):
        print('✅ RECOMMENDED APPROACH: Use Local Ollama')
        print('  • Fast, reliable, and completely free')
        print('  • No network dependencies')
        print('  • Full privacy and control')
        print('  • Use: python -c "from turbo_api_implementation import TurboAPIImplementation; import asyncio; asyncio.run(TurboAPIImplementation().smart_chat(\'Hello\', prefer_turbo=False))"')
    turbo_working = any(result.get('working', False) for result in turbo_results.values())
    if turbo_working:
        working_endpoints = [ep for ep, result in turbo_results.items() if result.get('working')]
        print('\n✅ TURBO API ALTERNATIVE: Use working endpoint')
        print(f'  • Working endpoints: {working_endpoints[0]}')
        print('  • Update TURBO_API_BASE in .env')
    else:
        print('\n⚠️ TURBO API STATUS: Currently not accessible')
        print('  • api.turbo.ai domain not found')
        print('  • May be a beta/private service')
        print('  • Keep API key for future use')
    print('\n🚀 NEXT STEPS:')
    print('  1. Use local Ollama for immediate AI assistance')
    print('  2. Configure VS Code Continue extension')
    print('  3. Monitor for Turbo API service availability')
    print('  4. Test the implementation with: python turbo_api_implementation.py')
if __name__ == '__main__':
    asyncio.run(main())
