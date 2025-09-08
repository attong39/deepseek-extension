@echo off
echo 🔄 REINSTALLING OLLAMA IN VS CODE
echo ================================

echo 1. Stopping existing processes...
taskkill /f /im ollama.exe >nul 2>&1
taskkill /f /im python.exe /fi "WINDOWTITLE eq *ollama*" >nul 2>&1

echo 2. Cleaning up old installations...
rmdir /s /q "%USERPROFILE%\.ollama" >nul 2>&1
rmdir /s /q "%LOCALAPPDATA%\Programs\Ollama" >nul 2>&1

echo 3. Downloading latest Ollama...
curl -L https://ollama.com/download/windows -o "%TEMP%\OllamaSetup.exe"

echo 4. Installing Ollama...
"%TEMP%\OllamaSetup.exe" /S

echo 5. Setting up API configuration...
set OLLAMA_HOST=0.0.0.0:11434
set OLLAMA_ORIGINS=*
set OLLAMA_API_BASE_URL=http://localhost:11434

echo 6. Starting Ollama service...
start "" "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve

echo 7. Waiting for service to start...
timeout /t 5 >nul

echo 8. Installing recommended models...
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" pull deepseek-coder:6.7b
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" pull deepseek-coder:1.3b

echo ✅ Ollama installation complete!
echo 🚀 Ready for VS Code integration
pause
