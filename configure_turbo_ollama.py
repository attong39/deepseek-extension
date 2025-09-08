from typing import Any
import Exception
import FileNotFoundError
import ImportError
import KeyboardInterrupt
import e
import f
import input
import key
import len
import line
import model
import open
import package
import print
import value

"""
🔧 Turbo Ollama Configuration Script
===================================

Script to configure and optimize Turbo Ollama settings
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def check_ollama_installation() -> Any:
    """Check if Ollama is installed and running"""
    print('🔍 Checking Ollama installation...')
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'✅ Ollama installed: {result.stdout.strip()}')
        else:
            print('❌ Ollama not found')
            return False
    except FileNotFoundError:
        print('❌ Ollama not installed')
        print('📥 Download from: https://ollama.com/download')
        return False
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print('✅ Ollama is running')
            return True
        else:
            print('⚠️  Ollama not running. Start with: ollama serve')
            return False
    except Exception as e:
        print(f'❌ Error checking Ollama status: {e}')
        return False

def list_available_models() -> Any:
    """List available Ollama models"""
    print('\n📋 Available models:')
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print('❌ Could not list models')
    except Exception as e:
        print(f'❌ Error listing models: {e}')

def pull_recommended_models() -> Any:
    """Pull recommended models for Turbo Ollama"""
    recommended_models = ['deepseek-coder:6.7b', 'deepseek-coder:1.3b', 'codellama:7b', 'llama3.2:3b']
    print('\n📥 Pulling recommended models...')
    for model in recommended_models:
        print(f'  📦 Pulling {model}...')
        try:
            result = subprocess.run(['ollama', 'pull', model], capture_output=True, text=True)
            if result.returncode == 0:
                print(f'  ✅ {model} pulled successfully')
            else:
                print(f'  ❌ Failed to pull {model}: {result.stderr}')
        except Exception as e:
            print(f'  ❌ Error pulling {model}: {e}')

def create_optimized_config() -> Any:
    """Create optimized configuration file"""
    config_dir = Path.home() / '.turbo_ollama'
    config_dir.mkdir(exist_ok=True)
    config = {'ollama': {'endpoint': 'http://127.0.0.1:11434', 'models': {'default': 'deepseek-coder:6.7b', 'fast': 'deepseek-coder:1.3b', 'code': 'deepseek-coder:6.7b', 'chat': 'llama3.2:3b'}, 'performance': {'gpu_layers': 35, 'num_parallel': 8, 'max_loaded_models': 3, 'context_length': 8192, 'batch_size': 512}}, 'turbo': {'endpoint': 'https://api.turbo.ai/v1', 'model': 'turbo', 'api_key': None}, 'cache': {'enabled': True, 'ttl_seconds': 300, 'max_entries': 1000}, 'vietnamese': {'enabled': True, 'system_prompt': 'Bạn là AI assistant thông minh, hỗ trợ tiếng Việt tự nhiên.'}}
    config_file = config_dir / 'config.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f'\n📝 Configuration saved to: {config_file}')
    return config_file

def setup_environment_variables() -> Any:
    """Setup environment variables"""
    print('\n🔧 Setting up environment variables...')
    env_vars = {'OLLAMA_ENDPOINT': 'http://127.0.0.1:11434', 'OLLAMA_MODEL': 'deepseek-coder:6.7b', 'OLLAMA_GPU_LAYERS': '35', 'OLLAMA_NUM_PARALLEL': '8', 'OLLAMA_MAX_LOADED_MODELS': '3', 'OLLAMA_CONTEXT_LENGTH': '8192', 'OLLAMA_NUM_BATCH': '512'}
    if os.name == 'nt':
        bat_file = Path.cwd() / 'setup_turbo_env.bat'
        with open(bat_file, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Setting up Turbo Ollama environment...\n')
            for key, value in env_vars.items():
                f.write(f'set {key}={value}\n')
            f.write('echo Environment variables set!\n')
            f.write("echo Run 'setup_turbo_env.bat' before using Turbo Ollama\n")
        print(f'✅ Windows batch file created: {bat_file}')
        print('   Run this file before using Turbo Ollama')
    else:
        sh_file = Path.cwd() / 'setup_turbo_env.sh'
        with open(sh_file, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write("echo 'Setting up Turbo Ollama environment...'\n")
            for key, value in env_vars.items():
                f.write(f'export {key}={value}\n')
            f.write("echo 'Environment variables set!'\n")
            f.write("echo 'Run: source setup_turbo_env.sh'\n")
        os.chmod(sh_file, 493)
        print(f'✅ Shell script created: {sh_file}')
        print('   Run: source setup_turbo_env.sh')

def create_turbo_start_script() -> Any:
    """Create optimized start script"""
    if os.name == 'nt':
        script_content = '@echo off\necho Starting Optimized Turbo Ollama...\n\nrem Performance optimizations\nset OLLAMA_NUM_PARALLEL=8\nset OLLAMA_GPU_LAYERS=35\nset OLLAMA_MAX_LOADED_MODELS=3\nset OLLAMA_NUM_BATCH=512\nset OLLAMA_CONTEXT_LENGTH=8192\nset OLLAMA_USE_MMAP=true\n\nrem Start Ollama server\necho Starting Ollama server...\nstart "Ollama Server" /B ollama serve\n\nrem Wait for server to start\nping -n 3 127.0.0.1 >NUL 2>&1\n\nrem Preload models\necho Preloading models...\nstart "Model Load 1" /B cmd /c "ollama run deepseek-coder:6.7b exit >NUL 2>&1"\nstart "Model Load 2" /B cmd /c "ollama run deepseek-coder:1.3b exit >NUL 2>&1"\n\necho Turbo Ollama is ready!\necho Available at: http://127.0.0.1:11434\npause\n'
        script_file = Path.cwd() / 'start_turbo_ollama.bat'
    else:
        script_content = '#!/bin/bash\necho "Starting Optimized Turbo Ollama..."\n\n# Performance optimizations\nexport OLLAMA_NUM_PARALLEL=8\nexport OLLAMA_GPU_LAYERS=35\nexport OLLAMA_MAX_LOADED_MODELS=3\nexport OLLAMA_NUM_BATCH=512\nexport OLLAMA_CONTEXT_LENGTH=8192\nexport OLLAMA_USE_MMAP=true\n\n# Start Ollama server\necho "Starting Ollama server..."\nollama serve &\n\n# Wait for server to start\nsleep 3\n\n# Preload models\necho "Preloading models..."\nollama run deepseek-coder:6.7b "" &\nollama run deepseek-coder:1.3b "" &\n\necho "Turbo Ollama is ready!"\necho "Available at: http://127.0.0.1:11434"\n'
        script_file = Path.cwd() / 'start_turbo_ollama.sh'
    with open(script_file, 'w') as f:
        f.write(script_content)
    if os.name != 'nt':
        os.chmod(script_file, 493)
    print(f'\n🚀 Start script created: {script_file}')

def run_system_check() -> Any:
    """Run comprehensive system check"""
    print('🔍 Running system check...')
    print('=' * 50)
    python_version = sys.version_info
    print(f'🐍 Python: {python_version.major}.{python_version.minor}.{python_version.micro}')
    required_packages = ['aiohttp', 'asyncio']
    for package in required_packages:
        try:
            __import__(package)
            print(f'✅ {package}: installed')
        except ImportError:
            print(f'❌ {package}: not installed')
            print(f'   Install with: pip install {package}')
    try:
        import subprocess
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print('✅ NVIDIA GPU detected')
            lines = result.stdout.split('\n')
            for line in lines:
                if 'GeForce' in line or 'RTX' in line or 'GTX' in line:
                    print(f"   GPU: {line.split('|')[1].strip()}")
                    break
        else:
            print('⚠️  No NVIDIA GPU detected')
    except FileNotFoundError:
        print('⚠️  nvidia-smi not found (no NVIDIA GPU)')
    import psutil
    memory = psutil.virtual_memory()
    print(f'💾 RAM: {memory.total // 1024 ** 3} GB ({memory.percent}% used)')
    disk = psutil.disk_usage('/')
    print(f'💽 Disk: {disk.free // 1024 ** 3} GB free')

def main() -> Any:
    """Main configuration function"""
    print('🚀 Turbo Ollama Configuration')
    print('=' * 50)
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = 'all'
    if command in ['check', 'status']:
        run_system_check()
        check_ollama_installation()
        list_available_models()
    elif command in ['models', 'pull']:
        pull_recommended_models()
    elif command in ['config', 'setup']:
        create_optimized_config()
        setup_environment_variables()
        create_turbo_start_script()
    elif command in ['all', 'full']:
        run_system_check()
        if check_ollama_installation():
            list_available_models()
            choice = input('\n📥 Pull recommended models? (y/N): ').lower()
            if choice in ['y', 'yes']:
                pull_recommended_models()
        create_optimized_config()
        setup_environment_variables()
        create_turbo_start_script()
        print('\n✅ Configuration complete!')
        print('\n🚀 Next steps:')
        print('1. Start Ollama: ./start_turbo_ollama.bat (Windows) or ./start_turbo_ollama.sh (Unix)')
        print('2. Test API: python quick_start_turbo.py')
    else:
        print('❌ Unknown command. Available commands:')
        print('  check  - Check system and Ollama status')
        print('  models - Pull recommended models')
        print('  config - Create configuration files')
        print('  all    - Full setup (default)')
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n👋 Configuration cancelled')
    except Exception as e:
        print(f'❌ Error: {e}')
