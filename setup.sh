#!/bin/bash
# DeepSeek R1 Agent Setup Script
# Cross-platform setup cho Windows, Linux, macOS

echo "🚀 DeepSeek R1 Agent Setup"
echo "=========================="

# Detect OS
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
    PYTHON_CMD="python"
    PIP_CMD="pip"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "✅ Detected OS: $OS"

# Check Python
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+ first."
    if [[ "$OS" == "windows" ]]; then
        echo "Download from: https://python.org"
    elif [[ "$OS" == "linux" ]]; then
        echo "Run: sudo apt install python3 python3-pip"
    elif [[ "$OS" == "macos" ]]; then
        echo "Run: brew install python3"
    fi
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python found: $PYTHON_VERSION"

# Check pip
if ! command -v $PIP_CMD &> /dev/null; then
    echo "❌ pip not found. Installing pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | $PYTHON_CMD
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
$PIP_CMD install --upgrade pip
$PIP_CMD install ollama aiofiles

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found."
    if [[ "$OS" == "windows" ]]; then
        echo "Download from: https://ollama.ai/download"
    elif [[ "$OS" == "linux" ]]; then
        echo "Run: curl -fsSL https://ollama.ai/install.sh | sh"
    elif [[ "$OS" == "macos" ]]; then
        echo "Run: brew install ollama"
    fi
    echo "After installing Ollama, run: ollama pull deepseek-r1:latest"
    exit 1
fi

echo "✅ Ollama found"

# Check if Ollama server is running
if ! curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama server not running. Starting..."
    if [[ "$OS" == "windows" ]]; then
        start "Ollama Server" ollama serve
    else
        nohup ollama serve > /dev/null 2>&1 &
    fi
    sleep 3
fi

# Check and pull model
if ! ollama list | grep -q "deepseek-r1:latest"; then
    echo "📥 Pulling DeepSeek R1 model..."
    ollama pull deepseek-r1:latest
else
    echo "✅ DeepSeek R1 model already available"
fi

# Check Node.js and npm (for TypeScript compilation)
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    echo "✅ Node.js and npm found"
    echo "📦 Installing TypeScript dependencies..."
    npm install --save-dev typescript @types/node eslint concurrently
else
    echo "⚠️  Node.js/npm not found. TypeScript compilation will be skipped."
    echo "Install Node.js from: https://nodejs.org"
fi

# Create config file
cat > .deepseek/config.json << EOF
{
  "ollamaBaseUrl": "http://127.0.0.1:11434",
  "model": "deepseek-r1:latest",
  "maxTokens": 4096,
  "temperature": 0.7,
  "timeout": 300
}
EOF

echo "✅ Config file created: .deepseek/config.json"

# Make scripts executable
if [[ "$OS" != "windows" ]]; then
    chmod +x run_deepseek_agent.py
    chmod +x setup.sh
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Usage examples:"
echo "  python run_deepseek_agent.py chat \"Hello, how are you?\""
echo "  python run_deepseek_agent.py review src/extension.ts"
echo "  python run_deepseek_agent.py optimize src/aiAgent.ts"
echo "  python run_deepseek_agent.py test --file src/extension.ts"
echo ""
echo "For VS Code development:"
echo "  ./start-dev.bat  (Windows)"
echo "  python scripts/deepseek_start_assistant.py  (Cross-platform)"
echo ""
echo "Happy coding! 🤖"
