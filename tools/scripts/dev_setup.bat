@echo off
REM Script kích hoạt môi trường và chạy quality check cho Zeta AI Server

echo 🎯 ZETA AI SERVER - DEVELOPMENT ENVIRONMENT
echo ================================================

REM Kiểm tra virtual environment
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

echo ✅ Virtual environment found

REM Kích hoạt môi trường
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Kiểm tra Python và packages
echo 🔄 Checking Python version...
python --version

echo 🔄 Checking installed packages...
python -c "import ruff, pytest, pre_commit; print('✅ All required packages installed')"
if errorlevel 1 (
    echo ❌ Missing required packages!
    echo Installing dependencies...
    python -m pip install -r requirements.txt
)

REM Chạy quality check
echo.
echo 🔄 Running quality checks...
python scripts\check_quality.py

if errorlevel 1 (
    echo.
    echo ❌ Quality checks failed!
    pause
    exit /b 1
) else (
    echo.
    echo 🎉 All quality checks passed!
    echo Environment is ready for development
)

pause
