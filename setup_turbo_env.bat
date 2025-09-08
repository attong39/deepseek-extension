@echo off
echo Setting up Turbo API environment...

rem Set Turbo API configuration
set TURBO_API_KEY=5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP
set TURBO_API_ENDPOINT=https://api.turbo.ai/v1
set TURBO_MODEL=turbo

rem Set Ollama configuration  
set OLLAMA_ENDPOINT=http://127.0.0.1:11434
set OLLAMA_MODEL=deepseek-coder

echo ✅ Environment variables set!
echo.
echo Testing API configuration...

python -c "import os; print('Turbo API Key:', os.environ.get('TURBO_API_KEY', 'Not found')[:10] + '...' if os.environ.get('TURBO_API_KEY') else 'Not found')"

echo.
echo 🚀 Now you can run Python scripts that use the Turbo API
echo.
pause
