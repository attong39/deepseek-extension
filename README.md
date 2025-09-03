
<h1>DeepSeek AI Assistant - Enhanced Python Edition</h1>

<h3>Your Local AI Programming Assistant for VS Code with Advanced Python Workflow Integration</h3>


[![Version](https://img.shields.io/visual-studio-marketplace/v/aryansrao.deekseek-extension?logo=visualstudiocode&logoColor=white&label=Version)](https://marketplace.visualstudio.com/items?itemName=aryansrao.deekseek-extension) [![Downloads](https://img.shields.io/visual-studio-marketplace/d/aryansrao.deekseek-extension)](https://marketplace.visualstudio.com/items?itemName=aryansrao.deekseek-extension) [![Rating](https://img.shields.io/visual-studio-marketplace/r/aryansrao.deekseek-extension)](https://marketplace.visualstudio.com/items?itemName=aryansrao.deekseek-extension) [![Issues](https://img.shields.io/github/issues/aryansrao/deepseek-extension)](https://github.com/aryansrao/deepseek-extension/issues) [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Last Commit](https://img.shields.io/github/last-commit/aryansrao/deepseek-extension)](https://github.com/aryansrao/deepseek-extension/commits) [![Code Size](https://img.shields.io/github/languages/code-size/aryansrao/deepseek-extension)](https://github.com/aryansrao/deepseek-extension) ![Release Date](https://img.shields.io/github/release-date/aryansrao/deepseek-extension) [![Discussions](https://img.shields.io/github/discussions/aryansrao/deepseek-extension)](https://github.com/aryansrao/deepseek-extension/discussions) [![Vercel](https://img.shields.io/website?url=https%3A%2F%2Fdeepseek-extension.vercel.app&logo=vercel&label=Vercel)](https://deepseek-extension.vercel.app)

  

## Screenshots
<div align="center">
    <img src="media/demo.gif" alt="DeepSeek Chat Interface - Full" width="75%" />
    <p><em>DeepSeek Chat Interface - Full</em></p>
</div>
  

<div  align="center">

<table>

<tr>



<td  width="50%">

<img  src="media/screenshot1.png"  alt="DeepSeek Chat Interface - Dark"  width="100%" />

<p  align="center"><em>DeepSeek Chat Interface - Dark</em></p>

</td>

<td  width="50%">

<img  src="media/screenshot2.png"  alt="DeepSeek Chat Interface - Light"  width="100%" />

<p  align="center"><em>DeepSeek Chat Interface - Light</em></p>

</td>

</tr>

</table>

</div>

  

> 💡 **Pro tip**: Use `Cmd/Ctrl + Shift + P` and type "start" to begin

  

## Quick Setup

  

# 1. Install Ollama

  

visit https://ollama.com

  

# 2. Pull DeepSeek Model

  

```

ollama run deepseek-r1

```

Visit https://ollama.com/library/deepseek-r1 for more info.

  

# 3. Install Extension

  

```

code --install-extension aryansrao.deekseek-extension

```

### OR

  

visit https://marketplace.visualstudio.com/items?itemName=aryansrao.deekseek-extension

  

## What It Does

DeepSeek brings powerful AI assistance directly into VS Code, running completely locally through Ollama:

### 🚀 New AI Agent Features (GitHub Copilot-like)

The extension now includes an advanced AI Agent that can understand entire projects and make intelligent code modifications:

- **🤖 Project Understanding** - Analyzes your entire codebase contextually
- **🔧 JSON-based Actions** - Precise code modifications (upsert, replace, insert, optimize)
- **📁 Workspace Integration** - Direct file editing through VS Code WorkspaceEdit
- **✅ Confirmation Dialogs** - Preview and approve changes before applying
- **🎯 Context-aware** - Detects frameworks (React, Vue, Python) and dependencies
- **🔒 Security-focused** - Path sanitization and safe operations only

### Core AI Features
- **Code Generation** - Get intelligent code suggestions
- **Real-time Help** - Ask questions about your code
- **Documentation** - Generate comments and documentation
- **Debugging** - Get help fixing bugs
- **Best Practices** - Learn coding patterns and improvements

### 🐍 Python Development Workflow Integration

#### Smart Auto-Detection
- **Automatic Project Detection**: Detects Python projects by scanning for `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock`
- **File Type Recognition**: Supports `.py`, `.pyi`, `.pyx`, `.pxd` files
- **Auto-Start Chat**: Offers Python-specific assistance when opening Python files

#### Specialized Python Commands
- **Start Python Assistant** - Context-aware Python development chat
- **Review Python Code** - Comprehensive code review with security & performance analysis
- **Debug Python Code** - Intelligent bug detection and debugging strategies
- **Optimize Python Code** - Performance optimization recommendations
- **Generate Documentation** - Automatic docstring and documentation generation
- **Generate Tests** - Unit test generation with best practices

#### Custom Code Review Prompts
- **Security Review**: SQL injection, command injection, path traversal detection
- **Performance Review**: Algorithm complexity, memory usage, I/O optimization
- **Best Practices Review**: PEP 8 compliance, type hints, error handling
- **Testing Review**: Unit test coverage, integration tests, mock strategies

### 🛠️ AI Agent Commands

#### Available Commands (Ctrl+Shift+P)
- **DeepSeek: Run AI Agent Task** - Choose from predefined tasks like code review, debugging, optimization
- **DeepSeek: Review Current File** - Comprehensive analysis of the active file
- **DeepSeek: Continuous Optimize (Light)** - Multi-iteration improvements (1-10 rounds)

#### Configuration

Create a `.env` file in your project root:
```env
OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=deepseek-r1:latest
OLLAMA_TIMEOUT_MS=15000
```

Or configure via VS Code settings:
- `deepseek.ollamaUrl` - Ollama service URL
- `deepseek.ollamaModel` - Model to use  
- `deepseek.autoApply` - Auto-apply changes without confirmation
- `deepseek.maxContextBytes` - Context size limit (default: 40KB)

#### Action Types Supported
- **upsert_file** - Create or overwrite files
- **append** - Add content to end of file
- **replace** - Regex-based replacements
- **insert** - Insert content above/below anchor
- **optimize_imports** - Sort and clean imports

  

## Requirements

  

- VS Code 1.96+

  

- MacOS/Linux/Windows

  

- [Ollama](https://ollama.com) installed

  

## Troubleshooting

  

**Extension Not Working?**

  

1. Verify Ollama is running:

  

2. Check model is downloaded: `ollama list`

  

3. Restart VS Code

  
  

## Resources

  

- [Link to the extension](https://marketplace.visualstudio.com/items?itemName=aryansrao.deekseek-extension)

  

- [Issue Tracker](https://github.com/aryansrao/deepseek-extension/issues)

  

- [Website](https://deepseek-extension.vercel.app)

  

## Contributing

  

Contributions are welcome!
