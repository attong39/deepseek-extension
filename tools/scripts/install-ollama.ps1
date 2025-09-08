# Requires -Version 5.1
# Install Ollama trên Windows

param(
    [string[]]$Models = @("deepseek-r1:latest", "gpt-oss:20b"),
    [switch]$StartService,
    [switch]$TestAPI
)

Write-Host "🚀 Cài đặt Ollama..." -ForegroundColor Cyan

# Kiểm tra Chocolatey
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Cần cài Chocolatey trước. Chạy:" -ForegroundColor Red
    Write-Host "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    exit 1
}

# Cài Ollama
Write-Host "📦 Cài đặt Ollama..." -ForegroundColor Yellow
choco install ollama -y

# Kiểm tra cài đặt
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Ollama không cài được" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Ollama đã cài: $(ollama --version)" -ForegroundColor Green

# Start service
if ($StartService) {
    Write-Host "🔧 Khởi động Ollama service..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 5
}

# Pull models
foreach ($model in $Models) {
    Write-Host "📥 Pulling model: $model" -ForegroundColor Yellow
    & ollama pull $model
}

# Test API
if ($TestAPI) {
    Write-Host "🧪 Test Ollama API..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 10
        Write-Host "✅ API hoạt động: HTTP $($response.StatusCode)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ API không hoạt động: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "🎉 Hoàn thành cài đặt Ollama!" -ForegroundColor Green
