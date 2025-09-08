@echo off
echo 🚀 STARTING OLLAMA WITH TURBO API INTEGRATION
echo =============================================

echo 🔧 Setting up environment...
set OLLAMA_HOST=0.0.0.0:11434
set OLLAMA_ORIGINS=*
set OLLAMA_API_BASE_URL=http://localhost:11434
set TURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP

echo 🚀 Starting Ollama server...
start "Ollama Server" /min ollama serve

echo ⏳ Waiting for server to start...
timeout /t 10 >nul

echo 📥 Pulling essential models...
ollama pull deepseek-coder:6.7b
ollama pull deepseek-coder:1.3b

echo 🧪 Testing installation...
ollama list

echo ✅ Ollama is ready for VS Code integration!
echo 💡 Tips:
echo   • Use Ctrl+I in VS Code for inline AI help
echo   • Use Ctrl+L for AI chat
echo   • Your Turbo API key is configured
echo   • DeepSeek Coder models are ready

echo 🎯 VS Code Extensions to install:
echo   • Continue (AI Assistant)
echo   • Python 
echo   • Deepseek Extension (if available)

pause
