# Script PowerShell khắc phục lỗi môi trường ảo VS Code
# Tác giả: ZETA AI Team
# Mục đích: Khắc phục các vấn đề phổ biến với môi trường ảo trong VS Code

param(
    [switch]$Force,
    [switch]$Verbose
)

Write-Host "🔍 ZETA: Kiểm tra môi trường ảo VS Code..." -ForegroundColor Cyan

# Biến môi trường
$WorkspaceRoot = Get-Location
$VenvPath = Join-Path $WorkspaceRoot ".venv"
$PythonExe = Join-Path $VenvPath "Scripts\python.exe"
$VsCodeSettings = Join-Path $WorkspaceRoot ".vscode\settings.json"

Write-Host "📁 Workspace: $WorkspaceRoot" -ForegroundColor White
Write-Host "🐍 Virtual env: $VenvPath" -ForegroundColor White

# 1. Kiểm tra môi trường ảo
if (-not (Test-Path $VenvPath)) {
    Write-Host "❌ Môi trường ảo không tồn tại!" -ForegroundColor Red
    Write-Host "📋 Chạy: uv venv để tạo môi trường ảo" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $PythonExe)) {
    Write-Host "❌ Python executable không tồn tại: $PythonExe" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python executable: $PythonExe" -ForegroundColor Green

# 2. Test import packages
Write-Host "`n🧪 Test import packages..." -ForegroundColor Cyan
try {
    $TestResult = & $PythonExe -c "import fastapi, uvicorn, pydantic; print('✅ Core packages OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host $TestResult -ForegroundColor Green
    }
    else {
        Write-Host "❌ Import error: $TestResult" -ForegroundColor Red
        Write-Host "📋 Chạy: uv sync để cài đặt dependencies" -ForegroundColor Yellow
        exit 1
    }
}
catch {
    Write-Host "❌ Lỗi test import: $_" -ForegroundColor Red
    exit 1
}

# 3. Kiểm tra VS Code đang chạy
$VsCodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue
if ($VsCodeProcess) {
    Write-Host "`n⚠️  VS Code đang chạy. Khuyến nghị restart VS Code sau khi hoàn thành." -ForegroundColor Yellow
}

# 4. Kiểm tra Python interpreter hiện tại
Write-Host "`n🔍 Kiểm tra Python interpreter hiện tại..." -ForegroundColor Cyan
$CurrentPython = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($CurrentPython) {
    Write-Host "📍 Python hiện tại: $CurrentPython" -ForegroundColor White
    if ($CurrentPython -eq $PythonExe) {
        Write-Host "✅ Đang sử dụng môi trường ảo đúng!" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Không sử dụng môi trường ảo!" -ForegroundColor Yellow
    }
}

# 5. Kích hoạt môi trường ảo cho session hiện tại
Write-Host "`n🔄 Kích hoạt môi trường ảo..." -ForegroundColor Cyan
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    Write-Host "📋 Chạy: & '$ActivateScript'" -ForegroundColor White
    & $ActivateScript
    Write-Host "✅ Môi trường ảo đã được kích hoạt!" -ForegroundColor Green
}
else {
    Write-Host "❌ Script kích hoạt không tồn tại: $ActivateScript" -ForegroundColor Red
}

# 6. Kiểm tra PYTHONPATH
Write-Host "`n🛤️  Kiểm tra PYTHONPATH..." -ForegroundColor Cyan
try {
    $PythonPathResult = & $PythonExe -c "import sys; [print(f'  {p}') for p in sys.path if 'zeta' in p.lower()]" 2>&1
    if ($LASTEXITCODE -eq 0 -and $PythonPathResult) {
        Write-Host "✅ PYTHONPATH có chứa zeta modules:" -ForegroundColor Green
        $PythonPathResult | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    }
    else {
        Write-Host "⚠️  PYTHONPATH có thể chưa được cấu hình đúng" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Lỗi kiểm tra PYTHONPATH: $_" -ForegroundColor Red
}

# 7. Hướng dẫn khắc phục VS Code
Write-Host "`n📋 Các bước khắc phục VS Code:" -ForegroundColor Cyan
Write-Host "1. 🔄 Restart VS Code" -ForegroundColor White
Write-Host "2. ⌨️  Ctrl+Shift+P → 'Python: Select Interpreter'" -ForegroundColor White
Write-Host "3. 📁 Chọn: $PythonExe" -ForegroundColor White
Write-Host "4. 💻 Mở terminal mới trong VS Code (Ctrl+Shift+`)" -ForegroundColor White
Write-Host "5. ✅ Kiểm tra lại với: python --version" -ForegroundColor White

# 8. Test nhanh server
Write-Host "`n🚀 Test nhanh server (optional)..." -ForegroundColor Cyan
$TestServer = Read-Host "Có muốn test server? (y/N)"
if ($TestServer -eq 'y' -or $TestServer -eq 'Y') {
    Write-Host "🌐 Khởi động server test..." -ForegroundColor White
    try {
        Start-Process -FilePath $PythonExe -ArgumentList "-m", "uvicorn", "zeta_vn.app.main_production:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -NoNewWindow
        Write-Host "✅ Server test đã khởi động tại http://localhost:8000" -ForegroundColor Green
        Write-Host "📋 Kiểm tra: http://localhost:8000/docs" -ForegroundColor White
    }
    catch {
        Write-Host "❌ Lỗi khởi động server: $_" -ForegroundColor Red
    }
}

Write-Host "`n✅ Hoàn thành khắc phục môi trường ảo!" -ForegroundColor Green
Write-Host "🎯 Môi trường Python đã sẵn sàng cho development!" -ForegroundColor Cyan
