@echo off
REM Turbo API Quick Start Script for Windows
REM API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP

echo 🚀 TURBO API QUICK START
echo ========================

REM Set environment variables
set TURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
set TURBO_API_BASE=https://api.turbo.ai/v1
set OLLAMA_HOST=http://127.0.0.1:11434

echo ✅ Environment variables set
echo 🔑 API Key: %TURBO_API_KEY:~0,20%...
echo 🌐 Endpoint: %TURBO_API_BASE%

REM Install dependencies if needed
echo.
echo 📦 Checking dependencies...
pip install -q aiohttp requests python-dotenv

REM Test basic functionality
echo.
echo 🧪 Testing implementation...
python turbo_api_implementation.py

echo.
echo ✅ Quick start complete!
echo 📚 Next: Use Continue extension in VS Code (Ctrl+L)
pause