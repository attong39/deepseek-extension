@echo off
echo 🛑 ĐÓNG TẤT CẢ BACKGROUND PROCESSES
echo ====================================

echo.
echo 🔍 Đang kiểm tra các processes đang chạy...
powershell -Command "Get-Process | Where-Object {$_.ProcessName -like '*ollama*' -or $_.ProcessName -like '*python*' -or $_.ProcessName -like '*node*'} | Select-Object ProcessName, Id, CPU"

echo.
echo 🛑 Đóng Ollama processes...
powershell -Command "Get-Process -Name 'ollama*' -ErrorAction SilentlyContinue | Stop-Process -Force"

echo.
echo 🛑 Đóng Python processes...
powershell -Command "Get-Process -Name 'python*' | Where-Object {$_.CPU -gt 0.5} | Stop-Process -Force -ErrorAction SilentlyContinue"

echo.
echo 🛑 Đóng Node.js processes...
powershell -Command "Get-Process -Name 'node*' -ErrorAction SilentlyContinue | Stop-Process -Force"

echo.
echo 🛑 Đóng web framework processes...
powershell -Command "Get-Process | Where-Object {$_.ProcessName -match '(uvicorn|fastapi|flask|django|streamlit|jupyter|gradio)'} | Stop-Process -Force -ErrorAction SilentlyContinue"

echo.
echo 🧹 Kiểm tra ports đang mở...
echo Port 11434 (Ollama):
netstat -ano | findstr ":11434"
echo Port 9100 (Metrics):
netstat -ano | findstr ":9100"
echo Port 3000 (React):
netstat -ano | findstr ":3000"

echo.
echo ✅ HOÀN THÀNH! Tất cả background processes đã được đóng.
echo.
pause
