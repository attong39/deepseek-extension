# Setup hoàn chỉnh DeepSeek + VS Code Extension

Write-Host "🚀 SETUP DEEPSEEK + VSCODE EXTENSION" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# 1. Install prerequisites  
Write-Host "`n1️⃣ Cài đặt prerequisites..." -ForegroundColor Yellow
& .\scripts\install-ollama.ps1 -Models @("gpt-oss:20b", "deepseek-r1:latest") -StartService
& .\scripts\install-node.ps1 -InstallYarn

# 2. Build extension
Write-Host "`n2️⃣ Build VS Code Extension..." -ForegroundColor Yellow
Push-Location "deepseek-extension"
npm install
npm run compile
Pop-Location

# 3. Test Ollama API
Write-Host "`n3️⃣ Test Ollama API..." -ForegroundColor Yellow  
& .\scripts\test-ollama-api.ps1 -Model "gpt-oss:20b"

# 4. Launch VS Code
Write-Host "`n4️⃣ Launch VS Code..." -ForegroundColor Yellow
code deepseek-extension

Write-Host "`n✅ SETUP HOÀN THÀNH!" -ForegroundColor Green
Write-Host "Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. Trong VS Code: nhấn F5 để mở Extension Development Host" -ForegroundColor White
Write-Host "2. Chạy command: DeepSeek: Health Check" -ForegroundColor White  
Write-Host "3. Test: DeepSeek: Review Current File" -ForegroundColor White
