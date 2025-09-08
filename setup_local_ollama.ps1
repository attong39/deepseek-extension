# 🚀 Setup Local Ollama with OpenAI-Compatible API

Write-Host "`n🚀 Setting up Local Ollama Integration..." -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Green

# Step 1: Start Ollama daemon
Write-Host "`n🔧 Step 1: Starting Ollama daemon..." -ForegroundColor Yellow
try {
    $ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue
    if ($ollamaProcess) {
        Write-Host "✅ Ollama daemon already running (PID: $($ollamaProcess.Id))" -ForegroundColor Green
    } else {
        Write-Host "🚀 Starting Ollama daemon..." -ForegroundColor Cyan
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep 3
        Write-Host "✅ Ollama daemon started" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Failed to start Ollama daemon: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 2: Test local API
Write-Host "`n🧪 Step 2: Testing Local API..." -ForegroundColor Yellow
$testPayload = @{
    model = "deepseek-coder:6.7b"
    messages = @(@{ role = "user"; content = "Write a simple Python hello function" })
    max_tokens = 100
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
}

try {
    Write-Host "📡 Testing connection to local Ollama..." -ForegroundColor Cyan
    $response = Invoke-RestMethod -Uri "http://localhost:11434/v1/chat/completions" -Method Post -Body $testPayload -Headers $headers -TimeoutSec 30
    
    Write-Host "✅ Local API Working!" -ForegroundColor Green
    Write-Host "🤖 Response:" -ForegroundColor Yellow
    Write-Host $response.choices[0].message.content -ForegroundColor White
} catch {
    Write-Host "❌ Local API Test Failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure models are downloaded: ollama pull deepseek-coder:6.7b" -ForegroundColor Blue
}

# Step 3: Configure Continue Extension for LOCAL use
Write-Host "`n⚙️ Step 3: Configuring Continue Extension..." -ForegroundColor Yellow

$continueConfigPath = "$env:APPDATA\Continue\config.json"
$continueConfigDir = Split-Path $continueConfigPath -Parent

# Create Continue config directory
if (-not (Test-Path $continueConfigDir)) {
    New-Item -ItemType Directory -Path $continueConfigDir -Force | Out-Null
    Write-Host "📁 Created Continue config directory" -ForegroundColor Green
}

# Backup existing config
if (Test-Path $continueConfigPath) {
    $backupPath = "$continueConfigPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $continueConfigPath $backupPath
    Write-Host "💾 Backed up existing config to: $(Split-Path $backupPath -Leaf)" -ForegroundColor Blue
}

# Create optimized local config
$continueConfig = @{
    models = @(
        @{
            title = "💻 Local • DeepSeek Coder 6.7B"
            provider = "ollama"
            model = "deepseek-coder:6.7b"
            apiBase = "http://localhost:11434"
        },
        @{
            title = "🏠 Local • Llama 3.1 8B"
            provider = "ollama"
            model = "llama3.1:8b"
            apiBase = "http://localhost:11434"
        },
        @{
            title = "⚡ Local • Qwen 2.5 Coder 7B"
            provider = "ollama"
            model = "qwen2.5-coder:7b"
            apiBase = "http://localhost:11434"
        }
    )
    tabAutocompleteModel = @{
        title = "🚀 DeepSeek Coder (Autocomplete)"
        provider = "ollama"
        model = "deepseek-coder:6.7b"
        apiBase = "http://localhost:11434"
    }
    embeddingsProvider = @{
        provider = "ollama"
        model = "nomic-embed-text:latest"
        apiBase = "http://localhost:11434"
    }
    allowAnonymousTelemetry = $false
    systemMessage = "You are an expert AI coding assistant. Provide clear, concise, and accurate responses."
}

$continueConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $continueConfigPath -Encoding UTF8
Write-Host "✅ Continue extension configured successfully" -ForegroundColor Green

Write-Host "`n📋 Models available:" -ForegroundColor Cyan
Write-Host "   💻 Local • DeepSeek Coder 6.7B" -ForegroundColor Green
Write-Host "   🏠 Local • Llama 3.1 8B" -ForegroundColor Green
Write-Host "   ⚡ Local • Qwen 2.5 Coder 7B" -ForegroundColor Green

# Step 4: Create test script
Write-Host "`n📝 Step 4: Creating Test Scripts..." -ForegroundColor Yellow

$testScript = @'
# 🧪 Local Ollama Quick Test
Write-Host "🧪 Testing Local Ollama API..." -ForegroundColor Cyan

$testPayload = @{
    model = "deepseek-coder:6.7b"
    messages = @(@{ role = "user"; content = "Write a simple Python function to calculate fibonacci" })
    max_tokens = 200
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/v1/chat/completions" -Method Post -Body $testPayload -Headers $headers -TimeoutSec 30
    
    Write-Host "✅ Local Ollama Working!" -ForegroundColor Green
    Write-Host "🤖 Response:" -ForegroundColor Yellow
    Write-Host $response.choices[0].message.content -ForegroundColor White
    Write-Host "`n📊 Usage: $($response.usage.total_tokens) tokens" -ForegroundColor Blue
} catch {
    Write-Host "❌ Test Failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Check if Ollama daemon is running: Get-Process ollama" -ForegroundColor Blue
}
'@

$testScript | Out-File -FilePath "test_local_ollama.ps1" -Encoding UTF8
Write-Host "✅ Created test_local_ollama.ps1" -ForegroundColor Green

# Final summary
Write-Host "`n" -NoNewline
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "🎉 LOCAL OLLAMA SETUP COMPLETE!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green

Write-Host "`n📊 SETUP SUMMARY:" -ForegroundColor Cyan
Write-Host "✅ Daemon: Ollama running locally" -ForegroundColor Green
Write-Host "✅ API: OpenAI-compatible on localhost:11434" -ForegroundColor Green
Write-Host "✅ Continue: 3 local models configured" -ForegroundColor Green
Write-Host "✅ Scripts: test_local_ollama.ps1 created" -ForegroundColor Green

Write-Host "`n🚀 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Restart VS Code completely" -ForegroundColor White
Write-Host "2. Install Continue extension if not already installed" -ForegroundColor White
Write-Host "3. Press Ctrl+L to open Continue chat" -ForegroundColor White
Write-Host "4. Select '💻 Local • DeepSeek Coder 6.7B'" -ForegroundColor White
Write-Host "5. Test with prompt: 'Write a Python web scraper'" -ForegroundColor White

Write-Host "`n💡 USAGE TIPS:" -ForegroundColor Blue
Write-Host "🏠 All models run locally - perfect for privacy" -ForegroundColor Green
Write-Host "⚡ DeepSeek Coder - best for programming tasks" -ForegroundColor Green
Write-Host "🤖 Llama 3.1 - best for general conversations" -ForegroundColor Green
Write-Host "🚀 Qwen 2.5 - fast and efficient coding" -ForegroundColor Green

Write-Host "`n🧪 TEST COMMANDS:" -ForegroundColor Cyan
Write-Host ".\test_local_ollama.ps1               # Test API directly" -ForegroundColor White
Write-Host "ollama list                           # Check local models" -ForegroundColor White
Write-Host "ollama serve                          # Start daemon manually" -ForegroundColor White

Write-Host "`n✨ Happy coding with Local Ollama! ✨" -ForegroundColor Magenta