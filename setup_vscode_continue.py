from typing import Any
import Exception
import all
import bool
import check
import e
import f
import int
import name
import open
import path
import print
import status
import str

"""
🔧 VS Code Continue Configuration Setup
=======================================

Automatically configures VS Code Continue extension with Turbo API
API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
"""
import json
import os
import shutil
from pathlib import Path


def backup_existing_config() -> Any:
    """Backup existing Continue config if it exists"""
    continue_dir = Path.home() / '.continue'
    config_file = continue_dir / 'config.json'
    if config_file.exists():
        backup_file = continue_dir / f'config.backup.{int(time.time())}.json'
        shutil.copy2(config_file, backup_file)
        print(f'📦 Backed up existing config to: {backup_file}')
        return True
    return False

def create_continue_config() -> Any:
    """Create optimized Continue configuration"""
    continue_dir = Path.home() / '.continue'
    continue_dir.mkdir(exist_ok=True)
    config = {'models': [{'title': '🚀 Turbo API (Primary)', 'provider': 'openai', 'model': 'turbo', 'apiKey': '5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP', 'apiBase': 'https://api.turbo.ai/v1', 'contextLength': 8192, 'completionOptions': {'temperature': 0.7, 'maxTokens': 1000, 'topP': 0.9}}, {'title': '🤖 DeepSeek Coder 6.7B (Local)', 'provider': 'ollama', 'model': 'deepseek-coder:6.7b', 'apiBase': 'http://localhost:11434', 'contextLength': 8192, 'completionOptions': {'temperature': 0.2, 'topP': 0.9}}, {'title': '⚡ DeepSeek Coder 1.3B (Fast)', 'provider': 'ollama', 'model': 'deepseek-coder:1.3b', 'apiBase': 'http://localhost:11434', 'contextLength': 4096, 'completionOptions': {'temperature': 0.1, 'topP': 0.8}}, {'title': '💬 CodeLlama (Chat)', 'provider': 'ollama', 'model': 'codellama:7b', 'apiBase': 'http://localhost:11434', 'contextLength': 4096}], 'tabAutocompleteModel': {'title': '🏃 Fast Autocomplete', 'provider': 'ollama', 'model': 'deepseek-coder:1.3b', 'apiBase': 'http://localhost:11434', 'contextLength': 2048, 'completionOptions': {'temperature': 0.1, 'maxTokens': 50}}, 'systemMessage': 'You are an expert AI coding assistant. You help with programming tasks, code review, debugging, and technical explanations. Respond in Vietnamese when the user writes in Vietnamese, otherwise use English. Be concise but thorough.', 'customCommands': [{'name': 'review', 'prompt': 'Please review this code for potential issues, improvements, and best practices:\n\n{{{ input }}}'}, {'name': 'explain', 'prompt': 'Please explain this code in detail, including what it does and how it works:\n\n{{{ input }}}'}, {'name': 'optimize', 'prompt': 'Please suggest optimizations for this code to improve performance, readability, or maintainability:\n\n{{{ input }}}'}, {'name': 'debug', 'prompt': 'Help me debug this code. Identify potential issues and suggest fixes:\n\n{{{ input }}}'}, {'name': 'test', 'prompt': 'Generate comprehensive test cases for this code:\n\n{{{ input }}}'}], 'contextProviders': [{'name': 'code', 'params': {'maxSubmenuLength': 10}}, {'name': 'docs', 'params': {}}, {'name': 'diff', 'params': {}}, {'name': 'terminal', 'params': {}}, {'name': 'problems', 'params': {}}, {'name': 'folder', 'params': {}}, {'name': 'codebase', 'params': {}}], 'slashCommands': [{'name': 'edit', 'description': 'Edit code in the current file'}, {'name': 'comment', 'description': 'Add comments to code'}, {'name': 'share', 'description': 'Share code snippet'}, {'name': 'cmd', 'description': 'Generate terminal command'}, {'name': 'commit', 'description': 'Generate git commit message'}], 'allowAnonymousTelemetry': False, 'disableIndexing': False, 'disableSessionTitles': False, 'userToken': '', 'embeddingsProvider': {'provider': 'ollama', 'model': 'nomic-embed-text', 'apiBase': 'http://localhost:11434'}, 'reranker': {'name': 'llm', 'params': {'modelTitle': '🤖 DeepSeek Coder 6.7B (Local)'}}}
    config_file = continue_dir / 'config.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f'✅ Continue config created: {config_file}')
    return config_file

def create_vscode_settings() -> Any:
    """Create VS Code settings for optimal integration"""
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    settings = {'continue.telemetryEnabled': False, 'continue.enableTabAutocomplete': True, 'continue.enableDebugLogs': False, 'python.defaultInterpreterPath': 'python', 'python.terminal.activateEnvironment': True, 'editor.inlineSuggest.enabled': True, 'editor.suggest.preview': True, 'editor.quickSuggestions': {'other': True, 'comments': True, 'strings': True}, 'github.copilot.enable': {'*': True, 'plaintext': False, 'markdown': True, 'scminput': False}, 'terminal.integrated.env.windows': {'TURBO_API_KEY': '5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP', 'OLLAMA_HOST': 'http://localhost:11434'}}
    settings_file = vscode_dir / 'settings.json'
    if settings_file.exists():
        with open(settings_file, encoding='utf-8') as f:
            try:
                existing_settings = json.load(f)
                existing_settings.update(settings)
                settings = existing_settings
            except json.JSONDecodeError:
                print('⚠️ Warning: Existing settings.json is invalid, creating new one')
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    print(f'✅ VS Code settings updated: {settings_file}')
    return settings_file

def create_launch_config() -> Any:
    """Create VS Code launch configuration for debugging"""
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    launch_config = {'version': '0.2.0', 'configurations': [{'name': '🚀 Run Turbo API Implementation', 'type': 'python', 'request': 'launch', 'program': '${workspaceFolder}/turbo_api_implementation.py', 'console': 'integratedTerminal', 'env': {'TURBO_API_KEY': '5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP', 'OLLAMA_HOST': 'http://localhost:11434', 'PYTHONPATH': '${workspaceFolder}'}, 'justMyCode': True}, {'name': '🧪 Debug Current Python File', 'type': 'python', 'request': 'launch', 'program': '${file}', 'console': 'integratedTerminal', 'env': {'TURBO_API_KEY': '5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP'}}, {'name': '🤖 Test Ollama Integration', 'type': 'python', 'request': 'launch', 'program': '${workspaceFolder}/quick_turbo_test.py', 'console': 'integratedTerminal'}]}
    launch_file = vscode_dir / 'launch.json'
    with open(launch_file, 'w', encoding='utf-8') as f:
        json.dump(launch_config, f, indent=2, ensure_ascii=False)
    print(f'✅ Launch config created: {launch_file}')
    return launch_file

def setup_environment_file() -> Any:
    """Setup .env file with all necessary variables"""
    env_content = '# Turbo API Configuration\nTURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP\nTURBO_API_BASE=https://api.turbo.ai/v1\n\n# Ollama Configuration\nOLLAMA_HOST=http://127.0.0.1:11434\nOLLAMA_NUM_CTX=8192\nOLLAMA_NUM_PARALLEL=8\nOLLAMA_GPU_LAYERS=35\nOLLAMA_MAX_LOADED_MODELS=3\n\n# Mode Settings\nAIRPLANE_MODE=false\nTURBO_MODE=hybrid\n\n# Performance Optimization\nOLLAMA_CONTEXT_LENGTH=8192\nOLLAMA_NUM_BATCH=512\n\n# Logging and Monitoring\nTURBO_LOG_LEVEL=INFO\nTURBO_CACHE_ENABLED=true\nTURBO_RATE_LIMIT_RPM=60\n\n# VS Code Integration\nCONTINUE_CONFIG_PATH=%USERPROFILE%\\.continue\\config.json\nVSCODE_SETTINGS_PATH=.vscode\\settings.json\n'
    env_file = Path('.env')
    if env_file.exists():
        backup_file = Path(f'.env.backup.{int(time.time())}')
        shutil.copy2(env_file, backup_file)
        print(f'📦 Backed up existing .env to: {backup_file}')
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print(f'✅ Environment file created: {env_file}')
    return env_file

def verify_setup() -> Any:
    """Verify that all configurations are in place"""
    print('\n🔍 Verifying setup...')
    checks = []
    continue_config = Path.home() / '.continue' / 'config.json'
    checks.append(('Continue config', continue_config.exists(), str(continue_config)))
    vscode_settings = Path('.vscode') / 'settings.json'
    checks.append(('VS Code settings', vscode_settings.exists(), str(vscode_settings)))
    launch_config = Path('.vscode') / 'launch.json'
    checks.append(('Launch config', launch_config.exists(), str(launch_config)))
    env_file = Path('.env')
    checks.append(('Environment file', env_file.exists(), str(env_file)))
    api_key = os.getenv('TURBO_API_KEY')
    checks.append(('API key loaded', bool(api_key), f'Key: {api_key[:10]}...' if api_key else 'Not found'))
    print('\n📋 Setup verification:')
    for name, status, path in checks:
        status_icon = '✅' if status else '❌'
        print(f'  {status_icon} {name}: {path}')
    return all(check[1] for check in checks)

def main() -> Any:
    """Main setup function"""
    print('🔧 VS CODE CONTINUE CONFIGURATION SETUP')
    print('=' * 50)
    print('API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP')
    print('=' * 50)
    try:
        print('\n1. 📦 Backing up existing configs...')
        backup_existing_config()
        print('\n2. 🔧 Creating Continue configuration...')
        create_continue_config()
        print('\n3. ⚙️ Setting up VS Code settings...')
        create_vscode_settings()
        print('\n4. 🚀 Creating launch configuration...')
        create_launch_config()
        print('\n5. 🌍 Setting up environment file...')
        setup_environment_file()
        print('\n6. 🔍 Verifying setup...')
        success = verify_setup()
        if success:
            print('\n🎉 SETUP COMPLETE!')
            print('\n📋 Next steps:')
            print('  1. Restart VS Code to load new configurations')
            print('  2. Install Continue extension if not already installed')
            print('  3. Open Command Palette (Ctrl+Shift+P)')
            print("  4. Type 'Continue: Chat' to start using AI assistance")
            print('  5. Use Ctrl+I for inline AI suggestions')
            print('  6. Use Ctrl+L for AI chat')
            print('\n🎯 Features enabled:')
            print('  • 🚀 Turbo API for fast responses')
            print('  • 🤖 Local Ollama for cost-effective coding')
            print('  • ⚡ Fast tab autocomplete')
            print('  • 💬 Custom slash commands')
            print('  • 🔧 Advanced context providers')
            print('  • 📊 Usage tracking and optimization')
        else:
            print('\n⚠️ Setup incomplete - please check the errors above')
    except Exception as e:
        print(f'\n❌ Setup failed: {e}')
        print('Please check permissions and try again')
if __name__ == '__main__':
    import time
    main()
