# PowerShell script để đóng tất cả background processes
# Sử dụng: .\stop_all_background.ps1

Write-Host "🛑 ĐÓNG TẤT CẢ BACKGROUND PROCESSES" -ForegroundColor White -BackgroundColor Red
Write-Host "====================================" -ForegroundColor White -BackgroundColor Red

Write-Host "`n🔍 Kiểm tra processes đang chạy..." -ForegroundColor Cyan
$processes = Get-Process | Where-Object {
    $_.ProcessName -like "*ollama*" -or 
    $_.ProcessName -like "*python*" -or 
    $_.ProcessName -like "*node*" -or
    $_.ProcessName -match "(uvicorn|fastapi|flask|django|streamlit|jupyter|gradio)"
}

if ($processes) {
    Write-Host "📋 Processes được tìm thấy:" -ForegroundColor Yellow
    $processes | Select-Object ProcessName, Id, CPU | Format-Table
} else {
    Write-Host "✅ Không tìm thấy background processes nào" -ForegroundColor Green
    exit
}

Write-Host "`n🛑 Đang đóng các processes..." -ForegroundColor Red

# Đóng Ollama
Write-Host "  • Đóng Ollama processes..." -ForegroundColor Yellow
Get-Process -Name "ollama*" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "    ✓ Done" -ForegroundColor Green

# Đóng Python (trừ VS Code extensions)
Write-Host "  • Đóng Python processes..." -ForegroundColor Yellow
Get-Process -Name "python*" | Where-Object {$_.CPU -gt 0.5} | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "    ✓ Done" -ForegroundColor Green

# Đóng Node.js
Write-Host "  • Đóng Node.js processes..." -ForegroundColor Yellow
Get-Process -Name "node*" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "    ✓ Done" -ForegroundColor Green

# Đóng web frameworks
Write-Host "  • Đóng web framework processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -match "(uvicorn|fastapi|flask|django|streamlit|jupyter|gradio)"} | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "    ✓ Done" -ForegroundColor Green

Write-Host "`n🧹 Kiểm tra network ports..." -ForegroundColor Magenta

$ports = @(11434, 9100, 3000, 8000, 5000, 8080)
foreach ($port in $ports) {
    $connections = netstat -ano | Select-String ":$port"
    if ($connections) {
        Write-Host "  ⚠️  Port $port still in use:" -ForegroundColor Yellow
        $connections | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    } else {
        Write-Host "  ✓ Port $port is free" -ForegroundColor Green
    }
}

Write-Host "`n📊 Kiểm tra cuối cùng..." -ForegroundColor Cyan
$remainingProcesses = Get-Process | Where-Object {
    $_.ProcessName -like "*ollama*" -or 
    $_.ProcessName -like "*python*" -or 
    $_.ProcessName -like "*node*"
} | Where-Object {$_.CPU -gt 0.1}

if ($remainingProcesses) {
    Write-Host "⚠️  Một số processes vẫn đang chạy:" -ForegroundColor Yellow
    $remainingProcesses | Select-Object ProcessName, Id, CPU | Format-Table
} else {
    Write-Host "✅ Tất cả background processes đã được đóng thành công!" -ForegroundColor Green -BackgroundColor Black
}

Write-Host "`n🎉 HOÀN THÀNH!" -ForegroundColor White -BackgroundColor Green
