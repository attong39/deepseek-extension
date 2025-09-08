import os
from typing import Any
import Exception
import FileNotFoundError
import ImportError
import e
import f
import len
import model
import open
import print

'\n🔍 Quick Ollama VS Code Integration Check\n========================================\n'
import json
import subprocess
from pathlib import Path


def check_ollama_status() -> Any:
    """Check Ollama installation and status"""
    print('🔍 OLLAMA STATUS CHECK')
    print('=' * 40)
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'✅ Ollama installed: {result.stdout.strip()}')
        else:
            print('❌ Ollama not installed')
            return False
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print('✅ Ollama is running')
            print('📋 Available models:')
            print(result.stdout)
        else:
            print('⚠️ Ollama not running - starting it...')
            subprocess.Popen(['ollama', 'serve'])
        return True
    except FileNotFoundError:
        print('❌ Ollama command not found')
        return False
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

def check_vscode_config() -> Any:
    """Check VS Code configuration"""
    print('\n🔧 VS CODE CONFIGURATION')
    print('=' * 40)
    vscode_dir = Path.cwd() / '.vscode'
    settings_file = vscode_dir / 'settings.json'
    if settings_file.exists():
        print('✅ VS Code settings.json exists')
        try:
            with open(settings_file, encoding='utf-8') as f:
                settings = json.load(f)
                if 'ollama.host' in settings:
                    print(f"✅ Ollama host configured: {settings['ollama.host']}")
                else:
                    print('⚠️ Ollama host not configured')
        except Exception as e:
            print(f'⚠️ Error reading settings: {e}')
    else:
        print('❌ VS Code settings.json not found')
    continue_dir = Path.home() / '.continue'
    continue_config = continue_dir / 'config.json'
    if continue_config.exists():
        print('✅ Continue AI config exists')
        try:
            with open(continue_config, encoding='utf-8') as f:
                config = json.load(f)
                models = config.get('models', [])
                print(f'✅ {len(models)} AI models configured')
                for model in models:
                    print(f"   • {model.get('title', 'Unknown')}")
        except Exception as e:
            print(f'⚠️ Error reading Continue config: {e}')
    else:
        print('❌ Continue AI config not found')

def check_api_key() -> Any:
    """Check API key configuration"""
    print('\n🔑 API KEY CONFIGURATION')
    print('=' * 40)
    api_key = os.getenv('API_KEY')
    env_file = Path.cwd() / '.env'
    if env_file.exists():
        with open(env_file, encoding='utf-8') as f:
            content = f.read()
            if 'TURBO_API_KEY' in content:
                print('✅ TURBO_API_KEY found in .env')
            else:
                print('⚠️ TURBO_API_KEY not in .env')
            if api_key in content:
                print('✅ Your API key is configured')
            else:
                print('⚠️ Your specific API key not found')
    else:
        print('❌ .env file not found')
    print(f'🔑 Your API Key: {api_key[:8]}...{api_key[-8:]}')

def test_connection() -> Any:
    """Test connections"""
    print('\n🧪 CONNECTION TESTS')
    print('=' * 40)
    try:
        import requests
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                print('✅ Local Ollama API responding')
            else:
                print(f'⚠️ Local Ollama API error: {response.status_code}')
        except Exception as e:
            print(f'❌ Cannot reach local Ollama: {e}')
        try:
            response = requests.get('https://api.turbo.ai', timeout=5)
            print('✅ Turbo API endpoint reachable')
        except Exception as e:
            print(f'⚠️ Turbo API endpoint issue: {e}')
    except ImportError:
        print('⚠️ requests module not available for testing')

def main() -> Any:
    """Main check function"""
    print('🚀 OLLAMA VS CODE INTEGRATION CHECK')
    print('API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP')
    print('=' * 60)
    ollama_ok = check_ollama_status()
    check_vscode_config()
    check_api_key()
    test_connection()
    print('\n📋 SUMMARY')
    print('=' * 40)
    if ollama_ok:
        print('✅ Ollama is ready')
        print('🎯 Next steps:')
        print('  1. Run: python setup_vscode_ollama.py')
        print('  2. Restart VS Code')
        print('  3. Install Continue extension if needed')
        print('  4. Test with Ctrl+I in VS Code')
    else:
        print('❌ Ollama needs to be installed/started')
        print('🎯 Fix steps:')
        print('  1. Run: reinstall_ollama.bat')
        print('  2. Wait for installation to complete')
        print('  3. Run this check again')
if __name__ == '__main__':
    main()
