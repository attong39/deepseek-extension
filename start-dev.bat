@echo off
echo 🚀 Starting AI Agent Extension Development...
echo.

echo ✅ Checking prerequisites...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama not found in PATH
    echo Please install Ollama first: https://ollama.ai
    pause
    exit /b 1
)

echo ✅ Ollama found
echo.

echo 📡 Testing Ollama connection...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama server not running
    echo Starting Ollama server...
    start "Ollama Server" ollama serve
    timeout /t 3 >nul
)

echo ✅ Ollama server ready
echo.

echo 🔨 Compiling TypeScript...
call npm run compile
if %errorlevel% neq 0 (
    echo ❌ Compilation failed
    pause
    exit /b 1
)

echo ✅ Compilation successful
echo.

echo 🎯 Ready to test! Next steps:
echo   1. VS Code will open
echo   2. Press F5 to launch Extension Development Host
echo   3. Test commands: Ctrl+Shift+P → "AI Agent"
echo   4. Open src/test-sample.ts and try optimize
echo.

echo 📝 Opening VS Code...
code .

echo.
echo 🎉 Development environment ready!
echo Check the USAGE_GUIDE.md for detailed instructions.
pause
