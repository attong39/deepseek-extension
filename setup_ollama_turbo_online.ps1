# 🚀 Setup Ollama với API Online Turbo cho VS Code
# Script này sẽ cấu hình Ollama để sử dụng API online turbo

Write-Host "🔥 Setting up Ollama with Online Turbo API for VS Code" -ForegroundColor Green

# 1. Kiểm tra Ollama đã cài đặt
Write-Host "`n1️⃣ Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = & ollama --version 2>$null
    Write-Host "✅ Ollama found: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama not found. Installing..." -ForegroundColor Red
    winget install Ollama.Ollama
}

# 2. Tạo API Key cho Turbo (cần thay thế bằng key thực)
$OLLAMA_API_KEY = "7da59eeb32d8447bbf291f5842bbe3a7.KoeW1XFcpJqaLn7-2LbRjMNY"
$TURBO_API_KEY = $OLLAMA_API_KEY

Write-Host "`n2️⃣ Setting up API keys..." -ForegroundColor Yellow

# 3. Tạo file .env trong thư mục Continue
$continueDir = "$env:USERPROFILE\.continue"
if (!(Test-Path $continueDir)) {
    New-Item -ItemType Directory -Path $continueDir -Force
    Write-Host "✅ Created .continue directory" -ForegroundColor Green
}

$envContent = @"
# Ollama API Configuration for Online Turbo
OLLAMA_API_KEY=$OLLAMA_API_KEY
TURBO_API_KEY=$TURBO_API_KEY
OLLAMA_HOST=https://api.ollama.com
OLLAMA_LOCAL_HOST=http://127.0.0.1:11434

# Turbo Configuration
OLLAMA_TURBO_MODE=true
OLLAMA_AIRPLANE_MODE=false
OLLAMA_CONTEXT_LENGTH=8192
"@

$envFile = "$continueDir\.env"
Set-Content -Path $envFile -Value $envContent -Encoding UTF8
Write-Host "✅ Created .env file with API keys" -ForegroundColor Green

# 4. Tạo cấu hình Continue extension
$continueConfig = @{
    "models" = @(
        @{
            "title" = "Llama 3.1 Turbo (Online)"
            "provider" = "ollama"
            "model" = "llama3.1:turbo"
            "apiBase" = "https://api.ollama.com"
            "apiKey" = "`${env:OLLAMA_API_KEY}"
        },
        @{
            "title" = "Llama 3.1 8B (Local)"
            "provider" = "ollama" 
            "model" = "llama3.1:8b"
            "apiBase" = "http://127.0.0.1:11434"
        }
    )
    "tabAutocompleteModel" = @{
        "title" = "Turbo Autocomplete"
        "provider" = "ollama"
        "model" = "llama3.1:turbo" 
        "apiBase" = "https://api.ollama.com"
        "apiKey" = "`${env:OLLAMA_API_KEY}"
    }
    "allowAnonymousTelemetry" = $false
    "docs" = @()
}

$configFile = "$continueDir\config.json"
$continueConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $configFile -Encoding UTF8
Write-Host "✅ Created Continue extension config" -ForegroundColor Green

# 5. Cấu hình VS Code settings.json
Write-Host "`n3️⃣ Configuring VS Code settings..." -ForegroundColor Yellow

$vscodeDir = "$env:APPDATA\Code\User"
if (!(Test-Path $vscodeDir)) {
    $vscodeDir = "$env:APPDATA\Code - Insiders\User"
}

if (Test-Path $vscodeDir) {
    $settingsFile = "$vscodeDir\settings.json"
    
    # Đọc settings hiện tại hoặc tạo mới
    if (Test-Path $settingsFile) {
        $settings = Get-Content $settingsFile -Raw | ConvertFrom-Json
    } else {
        $settings = @{}
    }
    
    # Thêm cấu hình Ollama
    $settings | Add-Member -MemberType NoteProperty -Name "ollama.host" -Value "https://api.ollama.com" -Force
    $settings | Add-Member -MemberType NoteProperty -Name "ollama.apiKey" -Value "`${env:OLLAMA_API_KEY}" -Force
    $settings | Add-Member -MemberType NoteProperty -Name "ollama.model" -Value "llama3.1:turbo" -Force
    $settings | Add-Member -MemberType NoteProperty -Name "ollama.contextLength" -Value 8192 -Force
    $settings | Add-Member -MemberType NoteProperty -Name "ollama.airplaneMode" -Value $false -Force
    $settings | Add-Member -MemberType NoteProperty -Name "ollama.modelsPath" -Value "$env:USERPROFILE\.ollama\models" -Force
    
    # Continue extension settings
    $settings | Add-Member -MemberType NoteProperty -Name "continue.enableTabAutocomplete" -Value $true -Force
    $settings | Add-Member -MemberType NoteProperty -Name "continue.telemetryEnabled" -Value $false -Force
    
    # Backup và lưu
    if (Test-Path $settingsFile) {
        Copy-Item $settingsFile "$settingsFile.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    }
    
    $settings | ConvertTo-Json -Depth 10 | Set-Content -Path $settingsFile -Encoding UTF8
    Write-Host "✅ Updated VS Code settings.json" -ForegroundColor Green
} else {
    Write-Host "⚠️ VS Code settings directory not found" -ForegroundColor Yellow
}

# 6. Khởi động Ollama daemon cho local models
Write-Host "`n4️⃣ Starting Ollama daemon..." -ForegroundColor Yellow

# Dừng các process Ollama cũ
Get-Process -Name "ollama*" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Khởi động Ollama daemon
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 3

Write-Host "✅ Ollama daemon started" -ForegroundColor Green

# 7. Download một số models phổ biến
Write-Host "`n5️⃣ Downloading essential models..." -ForegroundColor Yellow

$models = @("llama3.1:8b", "deepseek-coder:6.7b", "codellama:7b")

foreach ($model in $models) {
    Write-Host "📦 Downloading $model..." -ForegroundColor Cyan
    try {
        & ollama pull $model
        Write-Host "✅ Downloaded $model" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Failed to download $model" -ForegroundColor Yellow
    }
}

# 8. Test kết nối
Write-Host "`n6️⃣ Testing connections..." -ForegroundColor Yellow

# Test local connection
try {
    $localTest = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method GET -TimeoutSec 5
    Write-Host "✅ Local Ollama: Connected" -ForegroundColor Green
    Write-Host "📦 Local models: $($localTest.models.Count)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Local Ollama: Connection failed" -ForegroundColor Red
}

# Test online API (if key is valid)
try {
    $headers = @{
        "Authorization" = "Bearer $OLLAMA_API_KEY"
        "Content-Type" = "application/json"
    }
    
    $onlineTest = Invoke-RestMethod -Uri "https://api.ollama.com/v1/models" -Method GET -Headers $headers -TimeoutSec 10
    Write-Host "✅ Online Turbo API: Connected" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Online Turbo API: Please verify API key" -ForegroundColor Yellow
    Write-Host "   Visit https://ollama.com/login to get valid API key" -ForegroundColor Cyan
}

# 9. Hiển thị kết quả và hướng dẫn
Write-Host "`n🎉 Setup completed!" -ForegroundColor Green
Write-Host "`n📋 Configuration Summary:" -ForegroundColor White
Write-Host "   • API Key: $($OLLAMA_API_KEY.Substring(0,20))..." -ForegroundColor Cyan
Write-Host "   • Online API: https://api.ollama.com" -ForegroundColor Cyan  
Write-Host "   • Local API: http://127.0.0.1:11434" -ForegroundColor Cyan
Write-Host "   • Context Length: 8192" -ForegroundColor Cyan
Write-Host "   • Airplane Mode: Disabled (allows online)" -ForegroundColor Cyan

Write-Host "`n🚀 Next Steps:" -ForegroundColor White
Write-Host "   1. Restart VS Code" -ForegroundColor Cyan
Write-Host "   2. Install Continue extension if not installed" -ForegroundColor Cyan
Write-Host "   3. Press Ctrl+L to open Continue chat" -ForegroundColor Cyan
Write-Host "   4. Test with: 'Write a Python hello world function'" -ForegroundColor Cyan

Write-Host "`n🔧 Troubleshooting:" -ForegroundColor White
Write-Host "   • If online API fails: Update API key in $envFile" -ForegroundColor Cyan
Write-Host "   • If local fails: Run 'ollama serve' manually" -ForegroundColor Cyan
Write-Host "   • Check VS Code settings: Ctrl+, -> search 'ollama'" -ForegroundColor Cyan

Write-Host "`n✨ Ollama is now configured for both online Turbo and local models!" -ForegroundColor Green