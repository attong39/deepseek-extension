@echo off
echo Starting Python Assistant...

REM Ensure we're in the script directory
cd /d "%~dp0"

REM Create venv if missing
if not exist "venv" (
  echo Creating virtual environment...
  python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
  echo Installing requirements...
  pip install -r requirements.txt
)

echo Launching Python Assistant...
python assistant.py

pause
