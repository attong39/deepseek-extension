# Setup thông minh - tự động detect và chỉ cài những gì cần thiết

Write-Host "🚀 SMART SETUP - DEEPSEEK + VSCODE EXTENSION" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Kiểm tra prerequisites
Write-Host "`n🔍 Kiểm tra prerequisites..." -ForegroundColor Yellow

# Check Ollama
$ollamaInstalled = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaInstalled) {
    Write-Host "✅ Ollama đã có: $(ollama --version)" -ForegroundColor Green
}
else {
    Write-Host "❌ Cần cài Ollama" -ForegroundColor Red
    Write-Host "Chạy: winget install ollama" -ForegroundColor Yellow
    Write-Host "Hoặc tải từ: https://ollama.com/download" -ForegroundColor Yellow
    exit 1
}

# Check Node.js
$nodeVer = & node -v 2>$null
$npmVer = & npm -v 2>$null
if ($nodeVer -and $npmVer) {
    Write-Host "✅ Node.js: $nodeVer, npm: $npmVer" -ForegroundColor Green
}
else {
    Write-Host "❌ Cần cài Node.js" -ForegroundColor Red
    Write-Host "Chạy: winget install OpenJS.NodeJS" -ForegroundColor Yellow
    exit 1
}

# Check Ollama service
Write-Host "`n🔧 Kiểm tra Ollama service..." -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Ollama service đang chạy" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ Ollama service chưa chạy, đang khởi động..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 5
    
    try {
        $health = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5
        Write-Host "✅ Ollama service đã khởi động" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Không thể khởi động Ollama service" -ForegroundColor Red
        exit 1
    }
}

# Check models
Write-Host "`n📦 Kiểm tra models..." -ForegroundColor Yellow
$models = (Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" | ConvertFrom-Json).models.name

$requiredModels = @("gpt-oss:20b", "deepseek-r1:latest")
foreach ($model in $requiredModels) {
    if ($models -contains $model) {
        Write-Host "✅ Model có sẵn: $model" -ForegroundColor Green
    }
    else {
        Write-Host "📥 Pulling model: $model" -ForegroundColor Yellow
        & ollama pull $model
    }
}

# Build extension
Write-Host "`n🔨 Build VS Code Extension..." -ForegroundColor Yellow
Push-Location "deepseek-extension"

if (-not (Test-Path "package.json")) {
    Write-Host "❌ Không tìm thấy package.json trong deepseek-extension/" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Install dependencies
Write-Host "📦 Installing npm dependencies..." -ForegroundColor Cyan
npm install --silent

# Compile TypeScript
Write-Host "🔧 Compiling TypeScript..." -ForegroundColor Cyan
npm run compile

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ TypeScript compilation failed" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host "✅ Extension build thành công" -ForegroundColor Green
Pop-Location

# Test Ollama API
Write-Host "`n🧪 Test Ollama API..." -ForegroundColor Yellow

# Test with gpt-oss:20b
$testPayload = @{
    model    = "gpt-oss:20b"
    messages = @(
        @{ role = "user"; content = "Hello! Just say 'Hi' back." }
    )
    stream   = $false
} | ConvertTo-Json -Depth 3

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/chat" `
        -Method POST -ContentType "application/json" -Body $testPayload -TimeoutSec 30
    $result = ($response.Content | ConvertFrom-Json).message.content
    Write-Host "✅ API test thành công: $($result.Substring(0, [Math]::Min(50, $result.Length)))" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ API test thất bại: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Create .vscode/settings.json with proper config
Write-Host "`n⚙️ Cấu hình VS Code settings..." -ForegroundColor Yellow
$settingsPath = "deepseek-extension\.vscode"
$settingsFile = "$settingsPath\settings.json"

if (-not (Test-Path $settingsPath)) {
    New-Item -ItemType Directory -Path $settingsPath -Force | Out-Null
}

$vsCodeSettings = @{
    "deepseek.agent.model"                                 = "gpt-oss:20b"
    "deepseek.agent.baseUrl"                               = "http://127.0.0.1:11434"
    "deepseek.agent.timeout"                               = 120000
    "typescript.preferences.includePackageJsonAutoImports" = "on"
    "editor.formatOnSave"                                  = $true
} | ConvertTo-Json -Depth 2

$vsCodeSettings | Out-File -FilePath $settingsFile -Encoding UTF8
Write-Host "✅ Đã tạo .vscode/settings.json" -ForegroundColor Green

# Launch VS Code
Write-Host "`n🚀 Khởi động VS Code..." -ForegroundColor Yellow
code deepseek-extension

Write-Host "`n🎉 SETUP HOÀN THÀNH!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📋 Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. 🔥 Trong VS Code: nhấn F5 để mở Extension Development Host" -ForegroundColor White
Write-Host "2. 🏥 Chạy command: DeepSeek: Health Check" -ForegroundColor White  
Write-Host "3. 📝 Test: DeepSeek: Review Current File" -ForegroundColor White
Write-Host "4. 🎮 Hoặc thử: DeepSeek: Run Task" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n💡 Quick commands:" -ForegroundColor Yellow
Write-Host "• CLI test: .\cli\deepseek-agent.ps1 review run_deepseek_agent.py" -ForegroundColor White
Write-Host "• Health check: .\scripts\test-ollama-api.ps1" -ForegroundColor White
Write-Host "• Extension logs: View → Output → 'DeepSeek Agent'" -ForegroundColor White
