# Installer Ollama thông minh - không cần Chocolatey

param(
    [string[]]$Models = @("gpt-oss:20b", "deepseek-r1:latest"),
    [switch]$StartService,
    [switch]$TestAPI,
    [switch]$Force
)

Write-Host "🚀 Smart Ollama Installer..." -ForegroundColor Cyan

# Kiểm tra Ollama đã cài chưa
$ollamaInstalled = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaInstalled -and -not $Force) {
    Write-Host "✅ Ollama đã có: $(ollama --version)" -ForegroundColor Green
} else {
    Write-Host "📦 Cài đặt Ollama..." -ForegroundColor Yellow
    
    # Method 1: winget (Windows 10+)
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "🔧 Sử dụng winget..." -ForegroundColor Cyan
        winget install ollama --silent
    }
    # Method 2: Direct download
    else {
        Write-Host "📥 Download trực tiếp..." -ForegroundColor Cyan
        $downloadUrl = "https://ollama.com/download/ollama-windows.zip"
        $tempPath = "$env:TEMP\ollama.zip"
        $installPath = "$env:LOCALAPPDATA\Programs\Ollama"
        
        Invoke-WebRequest -Uri $downloadUrl -OutFile $tempPath
        Expand-Archive $tempPath -DestinationPath $installPath -Force
        
        # Add to PATH
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$installPath*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$installPath", "User")
            $env:PATH = "$env:PATH;$installPath"
        }
        
        Remove-Item $tempPath -Force
        Write-Host "✅ Ollama đã cài vào: $installPath" -ForegroundColor Green
    }
}

# Kiểm tra cài đặt thành công
Start-Sleep -Seconds 2
$ollamaCheck = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaCheck) {
    Write-Host "❌ Ollama install failed. Thử manual:" -ForegroundColor Red
    Write-Host "1. Tải từ: https://ollama.com/download" -ForegroundColor Yellow
    Write-Host "2. Hoặc: winget install ollama" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Ollama sẵn sàng: $(ollama --version)" -ForegroundColor Green

# Start service nếu cần
if ($StartService) {
    Write-Host "🔧 Khởi động Ollama service..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 5
    
    try {
        Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5 | Out-Null
        Write-Host "✅ Service đang chạy" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Service chưa ready, có thể cần chờ thêm" -ForegroundColor Yellow
    }
}

# Pull models
if ($Models.Count -gt 0) {
    Write-Host "📥 Pulling models..." -ForegroundColor Yellow
    foreach ($model in $Models) {
        Write-Host "🔄 Pulling: $model" -ForegroundColor Cyan
        & ollama pull $model
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $model ready" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $model pull có vấn đề" -ForegroundColor Yellow
        }
    }
}

# Test API nếu yêu cầu
if ($TestAPI) {
    Write-Host "🧪 Testing API..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 10
        $models = ($response.Content | ConvertFrom-Json).models.name
        Write-Host "✅ API OK. Models: $($models -join ', ')" -ForegroundColor Green
    } catch {
        Write-Host "❌ API test failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "🎉 Ollama setup hoàn thành!" -ForegroundColor Green
