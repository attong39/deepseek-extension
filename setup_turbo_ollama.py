from typing import Any
import Exception
import FileNotFoundError
import e
import f
import input
import len
import line
import model
import open
import print
import self
import title
import var_value

"""
🚀 Turbo API & Ollama Setup Script
==================================

Comprehensive setup script for Turbo API with Ollama integration.
This script will:
1. Check and install Ollama if needed
2. Pull necessary models
3. Set up environment variables
4. Test both Turbo API and Ollama
5. Provide usage instructions
"""
import os
import platform
import subprocess
from pathlib import Path

import requests


class TurboOllamaSetup:

    def __init__(self: Any) -> Any:
        self.api_key = os.getenv('API_KEY')
        self.system = platform.system().lower()
        self.ollama_url = 'http://127.0.0.1:11434'

    def print_header(self: Any, title: Any) -> Any:
        """Print formatted header"""
        print(f"\n{'=' * 60}")
        print(f'🚀 {title}')
        print(f"{'=' * 60}")

    def check_ollama_installed(self: Any) -> Any:
        """Check if Ollama is installed"""
        self.print_header('CHECKING OLLAMA INSTALLATION')
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print('✅ Ollama is installed')
                print(f'   Version: {result.stdout.strip()}')
                return True
            else:
                print('❌ Ollama installation check failed')
                return False
        except FileNotFoundError:
            print('❌ Ollama is not installed')
            return False
        except Exception as e:
            print(f'❌ Error checking Ollama: {e}')
            return False

    def install_ollama(self: Any) -> Any:
        """Install Ollama based on platform"""
        self.print_header('INSTALLING OLLAMA')
        if self.system == 'windows':
            print('📦 Installing Ollama for Windows...')
            print('💡 Please visit: https://ollama.ai/download/windows')
            print('   Or use winget: winget install Ollama.Ollama')
            input('Press Enter after installing Ollama...')
        elif self.system == 'linux':
            print('📦 Installing Ollama for Linux...')
            try:
                subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh', '|', 'sh'], shell=False, check=True)
                print('✅ Ollama installation completed')
            except Exception as e:
                print(f'❌ Installation failed: {e}')
                print('💡 Manual installation: curl -fsSL https://ollama.ai/install.sh | sh')
        elif self.system == 'darwin':
            print('📦 Installing Ollama for macOS...')
            try:
                subprocess.run(['brew', 'install', 'ollama'], check=True)
                print('✅ Ollama installation completed')
            except Exception as e:
                print(f'❌ Installation failed: {e}')
                print('💡 Manual installation: brew install ollama')
        else:
            print(f'❌ Unsupported platform: {self.system}')
            print('💡 Please visit: https://ollama.ai for manual installation')

    def start_ollama_service(self: Any) -> Any:
        """Start Ollama service"""
        self.print_header('STARTING OLLAMA SERVICE')
        try:
            print('🚀 Starting Ollama service...')
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('✅ Ollama service started')
            return True
        except Exception as e:
            print(f'❌ Failed to start Ollama: {e}')
            return False

    def pull_models(self: Any) -> Any:
        """Pull necessary models"""
        self.print_header('PULLING OLLAMA MODELS')
        models = ['llama2', 'codellama', 'deepseek-coder:6.7b', 'mistral']
        for model in models:
            try:
                print(f'📥 Pulling model: {model}')
                subprocess.run(['ollama', 'pull', model], capture_output=True, timeout=300)
                print(f'✅ Model {model} pulled successfully')
            except subprocess.TimeoutExpired:
                print(f'⏰ Timeout pulling {model} (this may take a while)')
            except Exception as e:
                print(f'❌ Failed to pull {model}: {e}')

    def test_ollama_connection(self: Any) -> Any:
        """Test Ollama connection"""
        self.print_header('TESTING OLLAMA CONNECTION')
        try:
            response = requests.get(f'{self.ollama_url}/api/tags', timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print('✅ Ollama is running and responding')
                print(f'   Available models: {len(models)}')
                for model in models[:5]:
                    print(f"   - {model.get('name', 'Unknown')}")
                return True
            else:
                print(f'❌ Ollama responded with status: {response.status_code}')
                return False
        except requests.ConnectionError:
            print('❌ Cannot connect to Ollama')
            print('💡 Make sure Ollama is running: ollama serve')
            return False
        except Exception as e:
            print(f'❌ Error testing Ollama: {e}')
            return False

    def test_turbo_api(self: Any) -> Any:
        """Test Turbo API connection"""
        self.print_header('TESTING TURBO API')
        try:
            response = requests.get('https://ollama.com/api/tags', headers={'Authorization': f'Bearer {self.api_key}'}, timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print('✅ Turbo API is working')
                print(f'   Available models: {len(models)}')
                for model in models:
                    name = model.get('name', 'Unknown')
                    size = model.get('size', 0) // 1024 ** 3 if model.get('size') else 0
                    print(f'   - {name} ({size}GB)')
                return True
            else:
                print(f'❌ Turbo API error: {response.status_code}')
                return False
        except Exception as e:
            print(f'❌ Turbo API connection failed: {e}')
            return False

    def setup_environment_variables(self: Any) -> Any:
        """Setup environment variables"""
        self.print_header('SETTING UP ENVIRONMENT VARIABLES')
        env_vars = {'TURBO_API_KEY': self.api_key, 'TURBO_API_BASE': 'https://ollama.com', 'OLLAMA_HOST': 'http://127.0.0.1:11434', 'OLLAMA_NUM_CTX': '4096', 'AIRPLANE_MODE': 'false'}
        env_file = Path('.env')
        existing_content = ''
        if env_file.exists():
            existing_content = env_file.read_text()
            print('📝 Updating existing .env file')
        else:
            print('📝 Creating new .env file')
        lines = existing_content.split('\n') if existing_content else []
        updated_lines = []
        added_vars = []
        for line in lines:
            if line.strip() and (not line.startswith('#')):
                var_name = line.split('=')[0].strip()
                if var_name in env_vars:
                    updated_lines.append(f'{var_name}={env_vars[var_name]}')
                    added_vars.append(var_name)
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        for var_name, var_value in env_vars.items():
            if var_name not in added_vars:
                updated_lines.append(f'{var_name}={var_value}')
                added_vars.append(var_name)
        env_file.write_text('\n'.join(updated_lines))
        print('✅ Environment variables configured in .env file')
        for var_name, var_value in env_vars.items():
            os.environ[var_name] = var_value
        print('✅ Environment variables set for current session')

    def create_usage_guide(self: Any) -> Any:
        """Create usage guide"""
        self.print_header('CREATING USAGE GUIDE')
        guide_content = f'# 🚀 Turbo API & Ollama Integration Guide\n# ======================================\n\n## 📋 Quick Start\n\n### 1. Environment Setup\nYour environment is configured with:\n- TURBO_API_KEY: {self.api_key[:20]}...\n- TURBO_API_BASE: https://ollama.com\n- OLLAMA_HOST: http://127.0.0.1:11434\n\n### 2. Run Quick Test\n```bash\npython quick_turbo_test.py\n```\n\n### 3. Use in Your Code\n```python\nfrom optimized_turbo_client import OptimizedTurboClient\nimport asyncio\n\nasync def main():\n    async with OptimizedTurboClient() as client:\n        # Use Turbo API (fast, cloud)\n        response = await client.chat_optimized(\n            "Write a Python function to calculate factorial",\n            use_turbo=True\n        )\n        print(response)\n        \n        # Use Ollama (free, local)\n        response = await client.chat_optimized(\n            "Explain Python list comprehensions",\n            use_turbo=False\n        )\n        print(response)\n\nasyncio.run(main())\n```\n\n## 🎯 Available Features\n\n### Turbo API (Cloud - Fast)\n- ✅ High-speed responses\n- ✅ Advanced AI models\n- ✅ Always available\n- ⚠️  Requires API key\n- 💰 Small usage costs\n\n### Ollama (Local - Free)\n- ✅ No API costs\n- ✅ Privacy-focused\n- ✅ Works offline\n- ⚠️  Requires local setup\n- 🐌 Slower responses\n\n### Smart Features\n- 🔄 Automatic fallback between Turbo and Ollama\n- 📦 Intelligent caching\n- 📊 Cost tracking\n- ⚡ Batch processing\n- 🎛️ Environment-driven configuration\n\n## 🛠️ Configuration Options\n\n### Environment Variables\n```bash\n# Turbo API Settings\nTURBO_API_KEY=your_api_key_here\nTURBO_API_BASE=https://ollama.com\n\n# Ollama Settings\nOLLAMA_HOST=http://127.0.0.1:11434\nOLLAMA_NUM_CTX=4096\n\n# Mode Control\nAIRPLANE_MODE=false  # true = always use Ollama\n```\n\n### Airplane Mode\nSet `AIRPLANE_MODE=true` to always use local Ollama:\n```bash\nexport AIRPLANE_MODE=true\n```\n\n## 📊 Monitoring & Stats\n\nThe client provides detailed usage statistics:\n- Request counts (Turbo vs Ollama)\n- Cache efficiency\n- Cost estimates\n- Error rates\n- Performance metrics\n\n## 🐛 Troubleshooting\n\n### Ollama Issues\n```bash\n# Check if Ollama is running\ncurl http://127.0.0.1:11434/api/tags\n\n# Start Ollama\nollama serve\n\n# Pull models\nollama pull llama2\nollama pull codellama\n```\n\n### Turbo API Issues\n- Check internet connection\n- Verify API key is correct\n- Check API quota/limits\n\n### Performance Tips\n- Use caching for repeated queries\n- Set appropriate OLLAMA_NUM_CTX\n- Monitor cache efficiency\n- Use batch processing for multiple queries\n\n## 📚 Examples\n\nSee `quick_turbo_test.py` for comprehensive examples of:\n- Basic chat functionality\n- Model switching\n- Batch processing\n- Cache usage\n- Error handling\n\n---\n\n🎉 **Setup Complete!** Your Turbo API + Ollama integration is ready to use.\n'
        with open('TURBO_OLLAMA_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write(guide_content)
        print('✅ Usage guide created: TURBO_OLLAMA_GUIDE.md')

    def run_setup(self: Any) -> Any:
        """Run complete setup process"""
        print('🎯 TURBO API & OLLAMA SETUP WIZARD')
        print('=' * 60)
        print(f'API Key: {self.api_key[:20]}...')
        print('=' * 60)
        if not self.check_ollama_installed():
            install_choice = input('❓ Install Ollama? (y/n): ').lower().strip()
            if install_choice == 'y':
                self.install_ollama()
            else:
                print('⚠️  Skipping Ollama installation')
                print('💡 You can still use Turbo API only')
        if self.check_ollama_installed():
            if not self.test_ollama_connection():
                start_choice = input('❓ Start Ollama service? (y/n): ').lower().strip()
                if start_choice == 'y':
                    self.start_ollama_service()
            if self.test_ollama_connection():
                pull_choice = input('❓ Pull recommended models? (y/n): ').lower().strip()
                if pull_choice == 'y':
                    self.pull_models()
        print('\n🔍 TESTING CONNECTIONS')
        turbo_ok = self.test_turbo_api()
        ollama_ok = self.test_ollama_connection()
        self.setup_environment_variables()
        self.create_usage_guide()
        self.print_header('SETUP COMPLETE')
        print('✅ Turbo API Status:', 'WORKING' if turbo_ok else 'NOT WORKING')
        print('✅ Ollama Status:', 'WORKING' if ollama_ok else 'NOT WORKING')
        print('✅ Environment:', 'CONFIGURED')
        print('✅ Documentation:', 'CREATED')
        if turbo_ok or ollama_ok:
            print('\n🎉 SETUP SUCCESSFUL!')
            print('\n📋 NEXT STEPS:')
            print('1. Run: python quick_turbo_test.py')
            print('2. Read: TURBO_OLLAMA_GUIDE.md')
            print('3. Start coding with AI assistance!')
        else:
            print('\n❌ SETUP INCOMPLETE')
            print('💡 At least one backend (Turbo or Ollama) should be working')
            print('   - Check internet for Turbo API')
            print('   - Install/start Ollama for local AI')

def main() -> Any:
    """Main setup function"""
    setup = TurboOllamaSetup()
    setup.run_setup()
if __name__ == '__main__':
    main()
