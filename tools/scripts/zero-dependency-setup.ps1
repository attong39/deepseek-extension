# ZERO-DEPENDENCY SETUP - Chỉ dùng winget và npm
# Không cần Chocolatey, tự động detect và cài những gì cần thiết

Write-Host "🚀 ZERO-DEPENDENCY SETUP" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host "Auto-detect và chỉ cài những gì thực sự cần" -ForegroundColor Gray

# Function để hiển thị progress
function Show-Progress {
    param([string]$Status, [string]$Activity)
    Write-Host "🔄 $Activity" -ForegroundColor Yellow
}

function Show-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Show-Skip {
    param([string]$Message)
    Write-Host "⏭️ $Message" -ForegroundColor Cyan
}

function Show-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# 1. Kiểm tra Ollama
Write-Host "`n1️⃣ KIỂM TRA OLLAMA" -ForegroundColor Yellow
$ollamaExists = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaExists) {
    Show-Success "Ollama đã có: $(ollama --version)"
}
else {
    Show-Progress "Cài đặt Ollama..." "Downloading Ollama"
    
    # Try winget first
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install ollama --silent
        if ($LASTEXITCODE -eq 0) {
            Show-Success "Ollama đã cài qua winget"
        }
        else {
            Show-Error "winget failed, cần cài manual từ https://ollama.com"
            exit 1
        }
    }
    else {
        Show-Error "Cần cài winget hoặc download manual từ https://ollama.com"
        exit 1
    }
}

# 2. Kiểm tra Node.js
Write-Host "`n2️⃣ KIỂM TRA NODE.JS" -ForegroundColor Yellow
$nodeVer = & node -v 2>$null
if ($nodeVer) {
    Show-Success "Node.js đã có: $nodeVer"
}
else {
    Show-Progress "Cài đặt Node.js..." "Downloading Node.js LTS"
    
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install OpenJS.NodeJS --silent
        if ($LASTEXITCODE -eq 0) {
            Show-Success "Node.js đã cài qua winget"
            # Refresh environment
            $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        }
        else {
            Show-Error "winget failed, cần cài manual từ https://nodejs.org"
            exit 1
        }
    }
    else {
        Show-Error "Cần cài winget hoặc download manual từ https://nodejs.org"
        exit 1
    }
}

# 3. Kiểm tra Ollama service
Write-Host "`n3️⃣ KIỂM TRA OLLAMA SERVICE" -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3 | Out-Null
    Show-Success "Ollama service đang chạy"
}
catch {
    Show-Progress "Khởi động Ollama service..." "Starting ollama serve"
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 8
    
    try {
        Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5 | Out-Null
        Show-Success "Ollama service đã khởi động"
    }
    catch {
        Show-Error "Không thể khởi động Ollama service"
        Write-Host "Thử chạy manual: ollama serve" -ForegroundColor Yellow
        exit 1
    }
}

# 4. Kiểm tra models
Write-Host "`n4️⃣ KIỂM TRA MODELS" -ForegroundColor Yellow
try {
    $existingModels = (Invoke-WebRequest "http://127.0.0.1:11434/api/tags" | ConvertFrom-Json).models.name
    $requiredModels = @("gpt-oss:20b", "deepseek-r1:latest")
    
    foreach ($model in $requiredModels) {
        if ($existingModels -contains $model) {
            Show-Success "Model có sẵn: $model"
        }
        else {
            Show-Progress "Pulling model: $model" "Downloading $model (có thể mất vài phút)"
            & ollama pull $model
            if ($LASTEXITCODE -eq 0) {
                Show-Success "Model $model đã pull xong"
            }
            else {
                Show-Error "Lỗi pulling model $model"
            }
        }
    }
}
catch {
    Show-Error "Không thể kiểm tra models: $($_.Exception.Message)"
}

# 5. Build Extension
Write-Host "`n5️⃣ BUILD EXTENSION" -ForegroundColor Yellow
if (Test-Path "deepseek-extension\package.json") {
    Push-Location "deepseek-extension"
    
    Show-Progress "Installing dependencies..." "npm install"
    npm install --silent --no-audit
    
    Show-Progress "Compiling TypeScript..." "tsc"
    npm run compile
    
    if ($LASTEXITCODE -eq 0) {
        Show-Success "Extension build thành công"
    }
    else {
        Show-Error "Extension build failed"
        Pop-Location
        exit 1
    }
    
    Pop-Location
}
else {
    Show-Error "Không tìm thấy deepseek-extension/package.json"
    exit 1
}

# 6. Quick API Test
Write-Host "`n6️⃣ QUICK API TEST" -ForegroundColor Yellow
$testPayload = @{
    model  = "gpt-oss:20b"
    prompt = "Hi"
    stream = $false
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/generate" `
        -Method POST -ContentType "application/json" -Body $testPayload -TimeoutSec 20
    $result = ($response.Content | ConvertFrom-Json).response
    Show-Success "API test OK: $(($result -replace '\n', ' ').Substring(0, [Math]::Min(30, $result.Length)))..."
}
catch {
    Show-Error "API test failed: $($_.Exception.Message)"
}

# 7. Setup VS Code config
Write-Host "`n7️⃣ VSCODE CONFIG" -ForegroundColor Yellow
$vscodePath = "deepseek-extension\.vscode"
if (-not (Test-Path $vscodePath)) {
    New-Item -ItemType Directory -Path $vscodePath -Force | Out-Null
}

$settings = @{
    "deepseek.agent.model"   = "gpt-oss:20b"
    "deepseek.agent.baseUrl" = "http://127.0.0.1:11434"
    "deepseek.agent.timeout" = 120000
} | ConvertTo-Json -Depth 2

$settings | Out-File "$vscodePath\settings.json" -Encoding UTF8
Show-Success "VS Code settings created"

# 8. Launch
Write-Host "`n8️⃣ LAUNCH VSCODE" -ForegroundColor Yellow
if (Get-Command code -ErrorAction SilentlyContinue) {
    code deepseek-extension
    Show-Success "VS Code launched"
}
else {
    Show-Error "VS Code không tìm thấy, cài VS Code trước"
}

Write-Host "`n🎉 ZERO-DEPENDENCY SETUP HOÀN THÀNH!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📝 Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. Trong VS Code: F5 → Extension Development Host" -ForegroundColor White
Write-Host "2. Ctrl+Shift+P → 'DeepSeek: Health Check'" -ForegroundColor White
Write-Host "3. Ctrl+Shift+P → 'DeepSeek: Review Current File'" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n🚀 Quick tests:" -ForegroundColor Yellow
Write-Host "• CLI: .\cli\deepseek-agent.ps1 review run_deepseek_agent.py" -ForegroundColor Gray
Write-Host "• Health: .\scripts\test-ollama-api.ps1" -ForegroundColor Gray
Write-Host "• Models: ollama list" -ForegroundColor Gray
