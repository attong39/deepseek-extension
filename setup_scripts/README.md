# 🚀 Ollama API Turbo Setup Scripts

This directory contains supporting scripts for the comprehensive Ollama API Turbo setup guide.

## 📁 Files

### Core Setup Scripts
- `quick_setup.py` - One-command setup script for experienced users
- `test_api.py` - Standalone API testing script
- `backup_config.py` - Configuration backup utility
- `diagnose.py` - Troubleshooting and diagnostic tool

### Platform-Specific Scripts
- `setup_windows.ps1` - Windows PowerShell setup script
- `setup_macos.sh` - macOS/Unix shell setup script
- `setup_linux.sh` - Linux shell setup script

### Configuration Templates
- `settings_template.json` - VS Code settings template
- `continue_config_template.json` - Continue extension config template
- `.env.template` - Environment variables template

## 🎯 Quick Start

For a one-command setup experience:

```bash
python setup_scripts/quick_setup.py --api-key YOUR_API_KEY
```

For detailed step-by-step setup, use the main Jupyter notebook:
```bash
jupyter notebook ollama_api_turbo_setup_guide.ipynb
```

## 🔒 Security

All scripts follow security best practices:
- API keys stored in environment variables
- Sensitive files added to .gitignore automatically
- Backup and restore functionality included
- Clear outputs function for safe sharing

## 📖 Documentation

Refer to the main notebook `ollama_api_turbo_setup_guide.ipynb` for comprehensive documentation and explanations.