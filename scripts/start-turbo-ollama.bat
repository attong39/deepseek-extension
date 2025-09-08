@echo off
setlocal ENABLEDELAYEDEXPANSION

echo Starting Turbo Ollama Mode...

rem Performance-related environment variables
set OLLAMA_NUM_PARALLEL=4
set OLLAMA_NUM_GPU=%OLLAMA_NUM_GPU:~0,1%
if "%OLLAMA_NUM_GPU%"=="" set OLLAMA_NUM_GPU=1
set OLLAMA_MAX_LOADED_MODELS=2

rem Optional GPU layers for partial acceleration
if "%OLLAMA_GPU_LAYERS%"=="" set OLLAMA_GPU_LAYERS=20

rem Start the Ollama server in background
start "ollama-serve" /B ollama serve
rem Allow a moment for the server to start
ping -n 3 127.0.0.1 >NUL 2>&1

rem Preload commonly used models
if not "%1"=="--no-preload" (
  echo Preloading models...
  start "ollama-load1" /B cmd /c "ollama run deepseek-coder:6.7b >NUL 2>&1"
  start "ollama-load2" /B cmd /c "ollama run codellama:7b >NUL 2>&1"
)

set TURBO_API_KEY=YOUR_KEY_HERE
set TURBO_API_ENDPOINT=https://api.turbo.ai/v1

echo Turbo Ollama is ready! Use Ctrl+Alt+T in VS Code.
exit /B 0
