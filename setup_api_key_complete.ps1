# 🔑 SETUP API KEY HOÀN CHỈNH
Write-Host "🔑 THIẾT LẬP API KEY HOÀN CHỈNH" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# Lấy API key từ environment variable hoặc prompt user
$apiKey = $env:OLLAMA_TURBO_API_KEY
if (-not $apiKey) {
    $apiKey = Read-Host "Nhập API key của bạn (hoặc để trống để sử dụng environment variable)"
    if ($apiKey) {
        $env:OLLAMA_TURBO_API_KEY = $apiKey
    }
}
$continueDir = "$env:USERPROFILE\.continue"

Write-Host "`n1️⃣ CẬP NHẬT ENVIRONMENT VARIABLE:" -ForegroundColor Yellow
# Set cho session hiện tại
$env:OLLAMA_TURBO_API_KEY = $apiKey
Write-Host "✅ Set cho PowerShell session hiện tại" -ForegroundColor Green

# Set vĩnh viễn cho user
try {
    [Environment]::SetEnvironmentVariable("OLLAMA_TURBO_API_KEY", $apiKey, "User")
    Write-Host "✅ Set vĩnh viễn cho user environment" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Không thể set vĩnh viễn: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n2️⃣ TẠO FILE .ENV CHO CONTINUE:" -ForegroundColor Yellow
$envContent = "OLLAMA_TURBO_API_KEY=$apiKey"
$envPath = "$continueDir\.env"
$envContent | Set-Content -Path $envPath -Encoding UTF8
Write-Host "✅ Tạo file .env: $envPath" -ForegroundColor Green

Write-Host "`n3️⃣ CẬP NHẬT CONFIG.JSON VỚI API KEY TRỰC TIẾP:" -ForegroundColor Yellow
$configPath = "$continueDir\config.json"
if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        
        # Cập nhật tất cả Turbo models với API key trực tiếp
        foreach ($model in $config.models) {
            if ($model.provider -eq "openai" -and $model.model -eq "gpt-oss:120b") {
                $model.apiKey = $apiKey  # Không dùng env:, dùng trực tiếp
                Write-Host "✅ Cập nhật model: $($model.title)" -ForegroundColor Green
            }
        }
        
        # Cập nhật autocomplete model
        if ($config.tabAutocompleteModel -and $config.tabAutocompleteModel.provider -eq "openai") {
            $config.tabAutocompleteModel.apiKey = $apiKey
            Write-Host "✅ Cập nhật autocomplete model" -ForegroundColor Green
        }
        
        # Lưu config
        $config | ConvertTo-Json -Depth 10 | Set-Content -Path $configPath -Encoding UTF8
        Write-Host "✅ Lưu config.json với API key trực tiếp" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Lỗi cập nhật config: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Không tìm thấy config.json" -ForegroundColor Red
}

Write-Host "`n4️⃣ TEST API KEY:" -ForegroundColor Yellow
try {
    $headers = @{ "Authorization" = "Bearer $apiKey"; "Content-Type" = "application/json" }
    $body = '{"model": "gpt-oss:120b", "prompt": "Hello", "stream": false}'
    $response = Invoke-RestMethod -Uri "https://ollama.com/api/generate" -Method POST -Headers $headers -Body $body
    Write-Host "✅ API Test: SUCCESS" -ForegroundColor Green
    Write-Host "Response: $($response.response)" -ForegroundColor White
} catch {
    Write-Host "❌ API Test: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 BƯỚC CUỐI CÙNG:" -ForegroundColor Magenta
Write-Host "1. 🔄 ĐÓNG VS CODE HOÀN TOÀN" -ForegroundColor White
Write-Host "2. 🚀 MỞ LẠI VS CODE" -ForegroundColor White
Write-Host "3. ⏱️  Đợi Continue load (10-15 giây)" -ForegroundColor White
Write-Host "4. 🧪 Test với Ctrl+L → Chọn 'Turbo • gpt-oss:120b'" -ForegroundColor White

Write-Host "`n✅ API KEY ĐÃ ĐƯỢC CẬP NHẬT TOÀN BỘ!" -ForegroundColor Green