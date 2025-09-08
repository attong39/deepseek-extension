@echo off
rem -------------------------------------------------
rem  setup_ollama.bat – khởi động Ollama & tải model
rem -------------------------------------------------

rem 1. Kiểm tra xem Ollama đã được cài chưa
where ollama >nul 2>&1
if errorlevel 1 (
    echo [ERR] Ollama không được tìm thấy trong PATH.
    echo      Vui lòng cài Ollama hoặc thêm vào PATH.
    echo      Download: https://ollama.com/download/Ollama-Windows-x64.exe
    exit /b 1
)

rem 2. Khởi động daemon (nếu chưa chạy)
echo [INFO] Khởi động Ollama daemon...
start "" /b ollama serve
timeout /t 3 >nul

rem 3. Kiểm tra server đang lắng nghe trên 11434
curl -s http://127.0.0.1:11434/api/version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERR] Không thể kết nối tới http://127.0.0.1:11434
    echo      Đợi vài giây rồi thử lại.
    exit /b 1
)

rem 4. Tải model mặc định (có thể thay đổi)
set MODEL=%1
if "%MODEL%"=="" set MODEL=gemma:2b
echo [INFO] Đang tải model %MODEL% …
ollama pull %MODEL%

rem 5. Kết thúc
echo [OK] Ollama đã sẵn sàng trên http://127.0.0.1:11434
exit /b 0
