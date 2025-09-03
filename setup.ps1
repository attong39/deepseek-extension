# DeepSeek R1 Agent Setup Script for Windows
# Chạy bằng PowerShell với quyền Administrator

Write-Host "🚀 DeepSeek R1 Agent Setup for Windows" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "📦 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install ollama aiofiles

# Check Ollama
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "✅ Ollama found: $ollamaVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Ollama not found." -ForegroundColor Red
    Write-Host "Please download from: https://ollama.ai/download" -ForegroundColor Yellow
    Write-Host "After installing, run: ollama pull deepseek-r1:latest" -ForegroundColor Yellow
    exit 1
}

# Check Ollama server
Write-Host "🔍 Checking Ollama server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5
    Write-Host "✅ Ollama server is running" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Ollama server not running. Starting..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -NoNewWindow
    Start-Sleep -Seconds 3
}

# Check and pull model
Write-Host "📥 Checking DeepSeek R1 model..." -ForegroundColor Yellow
$models = ollama list 2>&1
if ($models -notmatch "deepseek-r1:latest") {
    Write-Host "📥 Pulling DeepSeek R1 model..." -ForegroundColor Yellow
    ollama pull deepseek-r1:latest
}
else {
    Write-Host "✅ DeepSeek R1 model already available" -ForegroundColor Green
}

# Check Node.js and npm
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green

    $npmVersion = npm --version 2>&1
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green

    Write-Host "📦 Installing TypeScript dependencies..." -ForegroundColor Yellow
    npm install --save-dev typescript @types/node eslint concurrently
}
catch {
    Write-Host "⚠️  Node.js/npm not found. TypeScript compilation will be skipped." -ForegroundColor Yellow
    Write-Host "Install Node.js from: https://nodejs.org" -ForegroundColor Yellow
}

# Create config directory
if (!(Test-Path ".deepseek")) {
    New-Item -ItemType Directory -Path ".deepseek" -Force
}

# Create config file
$config = @"
{
  "ollamaBaseUrl": "http://127.0.0.1:11434",
  "model": "deepseek-r1:latest",
  "maxTokens": 4096,
  "temperature": 0.7,
  "timeout": 300
}
"@

$config | Out-File -FilePath ".deepseek\config.json" -Encoding UTF8
Write-Host "✅ Config file created: .deepseek\config.json" -ForegroundColor Green

Write-Host "" -ForegroundColor White
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "Usage examples:" -ForegroundColor Cyan
Write-Host "  python run_deepseek_agent.py chat 'Hello, how are you?'" -ForegroundColor White
Write-Host "  python run_deepseek_agent.py review src\extension.ts" -ForegroundColor White
Write-Host "  python run_deepseek_agent.py optimize src\aiAgent.ts" -ForegroundColor White
Write-Host "  python run_deepseek_agent.py test --file src\extension.ts" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "For VS Code development:" -ForegroundColor Cyan
Write-Host "  .\start-dev.bat" -ForegroundColor White
Write-Host "  python scripts\deepseek_start_assistant.py" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "Happy coding! 🤖" -ForegroundColor Magenta
