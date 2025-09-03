@echo off
echo ========================================
echo 🚀 DeepSeek Extension Test Launcher
echo ========================================
echo.

echo 📦 Checking extension files...
if not exist "out\src\extension.js" (
    echo ❌ Extension not compiled! Run: npm run compile
    pause
    exit /b 1
)

if not exist "out\src\aiAgent.js" (
    echo ❌ AI Agent not compiled! Run: npm run compile
    pause
    exit /b 1
)

echo ✅ Extension files found
echo.

echo 🔍 Checking Ollama connection...
curl -s http://localhost:11434/api/tags > ollama_check.json
if errorlevel 1 (
    echo ❌ Ollama server not running!
    echo Please start Ollama first: ollama serve
    pause
    exit /b 1
)

findstr "deepseek-r1" ollama_check.json > nul
if errorlevel 1 (
    echo ❌ DeepSeek R1 model not found!
    echo Please pull model: ollama pull deepseek-r1
    pause
    exit /b 1
)

echo ✅ Ollama and DeepSeek R1 ready
echo.

echo 🎯 Launching Extension Development Host...
echo Press F5 in VS Code to start testing
echo.

echo 📋 Test Commands Available:
echo   • AI Agent: Check Status
echo   • AI Agent: Review Code
echo   • AI Agent: Debug Code
echo   • AI Agent: Optimize Code
echo   • AI Agent: Interactive Mode
echo.

echo 💡 Tips:
echo   1. Open test-sample.ts file
echo   2. Press Ctrl+Shift+P
echo   3. Type "AI Agent: Check Status"
echo   4. Check Output panel for logs
echo.

pause
