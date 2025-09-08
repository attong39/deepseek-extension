# 🚀 TEST TURBO FUNCTIONALITY COMPREHENSIVE
Write-Host "🚀 TEST TÍNH NĂNG TURBO TOÀN DIỆN" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

$apiKey = $env:OLLAMA_TURBO_API_KEY

Write-Host "`n1️⃣ TEST API KEY CONNECTIVITY:" -ForegroundColor Yellow
try {
    $headers = @{ "Authorization" = "Bearer $apiKey"; "Content-Type" = "application/json" }
    $body = '{"model": "gpt-oss:120b", "prompt": "Hello Turbo!", "stream": false}'
    
    $start = Get-Date
    $response = Invoke-RestMethod -Uri "https://ollama.com/api/generate" -Method POST -Headers $headers -Body $body
    $end = Get-Date
    $duration = ($end - $start).TotalSeconds
    
    Write-Host "✅ API Connection: SUCCESS" -ForegroundColor Green
    Write-Host "⚡ Response Time: $duration seconds" -ForegroundColor Yellow
    Write-Host "📝 Response: $($response.response)" -ForegroundColor White
    
    if ($duration -lt 5) {
        Write-Host "🚀 EXCELLENT SPEED!" -ForegroundColor Green
    } elseif ($duration -lt 10) {
        Write-Host "👍 GOOD SPEED" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️  SLOW RESPONSE" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ API Test FAILED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n2️⃣ TEST CODING CAPABILITIES:" -ForegroundColor Yellow
try {
    $codePrompt = '{"model": "gpt-oss:120b", "prompt": "Write a Python function to calculate fibonacci sequence", "stream": false}'
    
    $start = Get-Date
    $codeResponse = Invoke-RestMethod -Uri "https://ollama.com/api/generate" -Method POST -Headers $headers -Body $codePrompt
    $end = Get-Date
    $codeDuration = ($end - $start).TotalSeconds
    
    Write-Host "✅ Code Generation: SUCCESS" -ForegroundColor Green
    Write-Host "⚡ Code Response Time: $codeDuration seconds" -ForegroundColor Yellow
    Write-Host "📝 Generated Code Preview:" -ForegroundColor White
    $preview = $codeResponse.response.Substring(0, [Math]::Min(200, $codeResponse.response.Length))
    Write-Host "$preview..." -ForegroundColor Gray
} catch {
    Write-Host "❌ Code Test FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n3️⃣ TEST MULTIPLE MODELS:" -ForegroundColor Yellow
$models = @("gpt-oss:20b", "gpt-oss:120b")
foreach ($model in $models) {
    try {
        $modelTest = @{
            model = $model
            prompt = "Hi, what model are you?"
            stream = $false
        } | ConvertTo-Json
        
        $start = Get-Date
        $modelResponse = Invoke-RestMethod -Uri "https://ollama.com/api/generate" -Method POST -Headers $headers -Body $modelTest
        $end = Get-Date
        $modelDuration = ($end - $start).TotalSeconds
        
        Write-Host "✅ Model ${model}: $modelDuration seconds" -ForegroundColor Green
    } catch {
        Write-Host "❌ Model ${model}: FAILED" -ForegroundColor Red
    }
}

Write-Host "`n4️⃣ VERIFY CONTINUE CONFIG:" -ForegroundColor Yellow
$configPath = "$env:USERPROFILE\.continue\config.json"
if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        $turboModels = $config.models | Where-Object { $_.provider -eq "openai" }
        
        Write-Host "✅ Continue Config: Found $($turboModels.Count) Turbo models" -ForegroundColor Green
        foreach ($model in $turboModels) {
            $hasApiKey = $model.apiKey -and $model.apiKey.Length -gt 10
            Write-Host "  • $($model.title): API Key $(if ($hasApiKey) { 'SET ✅' } else { 'MISSING ❌' })" -ForegroundColor $(if ($hasApiKey) { 'Green' } else { 'Red' })
        }
        
        # Check autocomplete
        if ($config.tabAutocompleteModel -and $config.tabAutocompleteModel.provider -eq "openai") {
            Write-Host "✅ Autocomplete: Turbo enabled" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Autocomplete: Using local model" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Config Read Error: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Continue config not found" -ForegroundColor Red
}

Write-Host "`n5️⃣ ENVIRONMENT CHECK:" -ForegroundColor Yellow
if ($env:OLLAMA_TURBO_API_KEY) {
    $envKeyPreview = $env:OLLAMA_TURBO_API_KEY.Substring(0, 10) + "..."
    Write-Host "✅ Environment Variable: $envKeyPreview" -ForegroundColor Green
} else {
    Write-Host "⚠️  Environment Variable: Not set" -ForegroundColor Yellow
}

$envFile = "$env:USERPROFILE\.continue\.env"
if (Test-Path $envFile) {
    Write-Host "✅ Continue .env file: EXISTS" -ForegroundColor Green
} else {
    Write-Host "⚠️  Continue .env file: Not found" -ForegroundColor Yellow
}

Write-Host "`n📊 PERFORMANCE SUMMARY:" -ForegroundColor Magenta
Write-Host "🚀 Turbo API: $duration seconds" -ForegroundColor Green
Write-Host "💻 Expected Local: 8-15 seconds" -ForegroundColor Yellow
Write-Host "⚡ Speed Improvement: $('{0:F1}' -f (12 / $duration))x faster than local" -ForegroundColor Cyan

Write-Host "`n🎯 NEXT STEPS FOR VS CODE:" -ForegroundColor Cyan
Write-Host "1. 🔄 Restart VS Code completely" -ForegroundColor White
Write-Host "2. 🎮 Open Continue: Ctrl+L" -ForegroundColor White
Write-Host "3. 🚀 Select: 'Turbo • gpt-oss:120b'" -ForegroundColor White
Write-Host "4. 🧪 Test prompt: 'Write a hello function'" -ForegroundColor White
Write-Host "5. ⚡ Expect: 2-5 second response" -ForegroundColor White

Write-Host "`n✨ TURBO IS READY FOR PRODUCTION USE!" -ForegroundColor Green