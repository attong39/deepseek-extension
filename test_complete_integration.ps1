# 🧪 Complete Ollama & VS Code Integration Test
Write-Host "🧪 Testing Ollama & VS Code Integration..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Test 1: Environment Variables
Write-Host "`n1️⃣ Testing Environment Variables..." -ForegroundColor Yellow
$ollamaHome = $env:OLLAMA_HOME
if ($ollamaHome) {
    Write-Host "✅ OLLAMA_HOME: $ollamaHome" -ForegroundColor Green
    
    if (Test-Path $ollamaHome) {
        Write-Host "✅ Directory exists" -ForegroundColor Green
        
        $modelsPath = Join-Path $ollamaHome "models"
        if (Test-Path $modelsPath) {
            Write-Host "✅ Models directory exists" -ForegroundColor Green
            $modelFiles = Get-ChildItem $modelsPath -Recurse | Measure-Object | Select-Object -ExpandProperty Count
            Write-Host "📦 Model files: $modelFiles" -ForegroundColor White
        } else {
            Write-Host "❌ Models directory not found" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ OLLAMA_HOME directory not found" -ForegroundColor Red
    }
} else {
    Write-Host "❌ OLLAMA_HOME not set" -ForegroundColor Red
}

# Test 2: Ollama CLI
Write-Host "`n2️⃣ Testing Ollama CLI..." -ForegroundColor Yellow
try {
    $models = ollama list 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Ollama CLI working" -ForegroundColor Green
        Write-Host "📋 Available models:" -ForegroundColor White
        ollama list | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
    } else {
        Write-Host "❌ Ollama CLI error" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Ollama CLI not found or not working" -ForegroundColor Red
}

# Test 3: Ollama API
Write-Host "`n3️⃣ Testing Ollama API..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get -TimeoutSec 5
    Write-Host "✅ Ollama API responding" -ForegroundColor Green
    $modelCount = $response.models.Count
    Write-Host "📦 API reports $modelCount models available" -ForegroundColor White
} catch {
    Write-Host "❌ Ollama API not responding" -ForegroundColor Red
    Write-Host "💡 Try: ollama serve" -ForegroundColor Yellow
}

# Test 4: VS Code Settings
Write-Host "`n4️⃣ Testing VS Code Settings..." -ForegroundColor Yellow
$settingsPath = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $settingsPath) {
    Write-Host "✅ VS Code settings found" -ForegroundColor Green
    
    try {
        $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
        
        $ollamaSettings = @()
        $settings.PSObject.Properties | Where-Object { $_.Name -like "*ollama*" } | ForEach-Object {
            $ollamaSettings += "$($_.Name): $($_.Value)"
        }
        
        if ($ollamaSettings.Count -gt 0) {
            Write-Host "✅ Ollama settings configured:" -ForegroundColor Green
            $ollamaSettings | ForEach-Object { Write-Host "   $_" -ForegroundColor White }
        } else {
            Write-Host "⚠️ No Ollama settings found in VS Code" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "⚠️ Could not parse VS Code settings" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ VS Code settings not found" -ForegroundColor Red
}

# Test 5: Continue Extension Config
Write-Host "`n5️⃣ Testing Continue Extension Config..." -ForegroundColor Yellow
$continueConfig = "$env:USERPROFILE\.continue\config.json"
if (Test-Path $continueConfig) {
    Write-Host "✅ Continue config found" -ForegroundColor Green
    
    try {
        $config = Get-Content $continueConfig -Raw | ConvertFrom-Json
        $modelCount = $config.models.Count
        Write-Host "📋 Continue has $modelCount models configured:" -ForegroundColor White
        
        $config.models | ForEach-Object {
            $provider = $_.provider
            $model = $_.model
            $title = $_.title
            Write-Host "   - $title ($provider): $model" -ForegroundColor Gray
        }
    } catch {
        Write-Host "⚠️ Could not parse Continue config" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Continue config not found" -ForegroundColor Red
}

# Test 6: Quick Generation Test
Write-Host "`n6️⃣ Testing Model Generation..." -ForegroundColor Yellow
try {
    $body = @{
        model = "deepseek-coder:6.7b"
        prompt = "Hello! Respond with just 'Model working!'"
        stream = $false
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/generate" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 15
    
    Write-Host "✅ Model generation successful!" -ForegroundColor Green
    Write-Host "🤖 Response: $($response.response)" -ForegroundColor Magenta
} catch {
    Write-Host "❌ Model generation failed" -ForegroundColor Red
    Write-Host "💡 Model might be loading, try again in a moment" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "📊 INTEGRATION STATUS SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

$checks = @(
    @{ Name = "Environment Variables"; Status = if ($env:OLLAMA_HOME) { "✅ PASS" } else { "❌ FAIL" } },
    @{ Name = "Ollama CLI"; Status = if ((ollama list 2>$null) -and ($LASTEXITCODE -eq 0)) { "✅ PASS" } else { "❌ FAIL" } },
    @{ Name = "Ollama API"; Status = try { Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3 | Out-Null; "✅ PASS" } catch { "❌ FAIL" } },
    @{ Name = "VS Code Settings"; Status = if (Test-Path "$env:APPDATA\Code\User\settings.json") { "✅ PASS" } else { "❌ FAIL" } },
    @{ Name = "Continue Config"; Status = if (Test-Path "$env:USERPROFILE\.continue\config.json") { "✅ PASS" } else { "❌ FAIL" } }
)

$checks | ForEach-Object {
    Write-Host "$($_.Status) $($_.Name)" -ForegroundColor White
}

Write-Host "`n🚀 NEXT STEPS:" -ForegroundColor Green
Write-Host "1. Restart VS Code completely" -ForegroundColor White
Write-Host "2. Press Ctrl+L to open Continue" -ForegroundColor White
Write-Host "3. Select your preferred model" -ForegroundColor White
Write-Host "4. Start coding with AI assistance!" -ForegroundColor White

Write-Host "`n💡 RECOMMENDED MODELS:" -ForegroundColor Yellow
Write-Host "🎯 General coding: DeepSeek Coder v2 Tool Calling 16B" -ForegroundColor White
Write-Host "⚡ Fast responses: DeepSeek Coder 6.7B" -ForegroundColor White
Write-Host "🔧 Quick completion: DeepSeek Coder 1.3B" -ForegroundColor White