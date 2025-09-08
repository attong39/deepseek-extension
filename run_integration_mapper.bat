@echo off
REM =====================================
REM DeepSeek Extension - Integration Mapper Runner
REM =====================================

echo 🎯 DEEPSEEK EXTENSION - INTEGRATION MAPPER
echo ==========================================

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

REM Điều hướng đến thư mục chứa script
cd /d "%~dp0"

echo 🔍 Analyzing project integration...
echo.

REM Chạy integration mapper
python integration_mapper.py --preview

echo.
echo 📊 Opening integration reports...

REM Mở file markdown trong VS Code hoặc browser
if exist "INTEGRATION_MAP.md" (
    echo ✅ Opening INTEGRATION_MAP.md...
    start "" "INTEGRATION_MAP.md"
)

if exist "integration_map.json" (
    echo ✅ JSON report generated: integration_map.json
)

echo.
echo 🎉 Integration analysis completed!
echo.
echo Generated files:
echo   - INTEGRATION_MAP.md  (Human-readable report)
echo   - integration_map.json (Machine-readable data)
echo.

pause
