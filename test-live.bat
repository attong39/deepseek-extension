@echo off
echo.
echo ========================================
echo 🚀 AI AGENT LIVE TEST SCRIPT
echo ========================================
echo.

REM Check if VS Code is running
tasklist /FI "IMAGENAME eq Code.exe" 2>NUL | find /I /N "Code.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ VS Code is running
) else (
    echo ❌ VS Code not detected - starting...
    start code .
    timeout /t 3 >NUL
)

echo.
echo 📋 TEST CHECKLIST:
echo.
echo [1] Press F5 in VS Code (Extension Development Host)
echo [2] Press Ctrl+Shift+P in new window  
echo [3] Type "AI Agent" - should see 5 commands
echo [4] Try "AI Agent: Check Status" first
echo [5] Open src/test-sample.ts
echo [6] Try "AI Agent: Optimize Code"
echo [7] Watch Output channel "DeepSeek Agent"
echo.

echo 🔧 Quick Ollama check...
curl -s http://127.0.0.1:11434/api/tags >NUL 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Ollama server responding
) else (
    echo ❌ Ollama not responding - check service
)

echo.
echo 🎯 READY FOR LIVE TESTING!
echo.
echo Monitor these windows:
echo - VS Code Extension Development Host
echo - Output channel "DeepSeek Agent"  
echo - This terminal for status
echo.
pause
