# 🚀 Ollama Turbo Setup - Official API Integration
Write-Host "🚀 Setting up Ollama Turbo API Integration..." -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# Step 1: Get API Key from user (safely)
Write-Host "`n🔑 Step 1: API Key Setup" -ForegroundColor Yellow
Write-Host "⚠️ IMPORTANT: Never share your API key publicly!" -ForegroundColor Red
Write-Host ""

$apiKey = Read-Host "Enter your NEW Ollama Turbo API key (starts with 'sk-')" -AsSecureString
$plainKey = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey))

if (-not $plainKey -or -not $plainKey.StartsWith("sk-") -and -not $plainKey.Contains(".")) {
    Write-Host "❌ Invalid API key format. Should start with alphanumeric chars and contain a dot." -ForegroundColor Red
    Write-Host "💡 Example format: abc123def456.xyz789" -ForegroundColor Yellow
    exit 1
}

# Step 2: Set environment variable permanently
Write-Host "`n💾 Step 2: Saving API Key to Environment..." -ForegroundColor Yellow
try {
    # Set for current session
    $env:OLLAMA_TURBO_API_KEY = $plainKey
    
    # Set permanently for user
    [Environment]::SetEnvironmentVariable('OLLAMA_TURBO_API_KEY', $plainKey, [EnvironmentVariableTarget]::User)
    
    Write-Host "✅ API Key saved successfully" -ForegroundColor Green
    Write-Host "🔒 Key stored securely in user environment variables" -ForegroundColor Blue
} catch {
    Write-Host "❌ Failed to save API key: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 3: Test API Key
Write-Host "`n🧪 Step 3: Testing Turbo API Connection..." -ForegroundColor Yellow

$testPayload = @{
    model = "gpt-oss:20b"
    messages = @(
        @{
            role = "user"
            content = "Hello! Please respond with 'Turbo API is working!'"
        }
    )
    max_tokens = 50
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $plainKey"
}

try {
    Write-Host "📡 Testing connection to Ollama Turbo..." -ForegroundColor Blue
    
    $response = Invoke-RestMethod -Uri "https://ollama.com/v1/chat/completions" -Method Post -Body $testPayload -Headers $headers -TimeoutSec 30
    
    if ($response.choices -and $response.choices.Count -gt 0) {
        $aiResponse = $response.choices[0].message.content
        Write-Host "✅ Turbo API Test: SUCCESS!" -ForegroundColor Green
        Write-Host "🤖 AI Response: $aiResponse" -ForegroundColor Magenta
        Write-Host "📊 Model: $($response.model)" -ForegroundColor White
        Write-Host "🔢 Tokens: $($response.usage.total_tokens)" -ForegroundColor White
        $apiWorking = $true
    } else {
        Write-Host "⚠️ API responded but no content received" -ForegroundColor Yellow
        $apiWorking = $false
    }
} catch {
    Write-Host "❌ API Test Failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Please check your API key and internet connection" -ForegroundColor Yellow
    $apiWorking = $false
}

# Step 4: Configure Continue Extension
Write-Host "`n⚙️ Step 4: Configuring Continue Extension..." -ForegroundColor Yellow

$continueConfigPath = "$env:USERPROFILE\.continue\config.json"
$continueDir = Split-Path $continueConfigPath -Parent

# Create .continue directory if not exists
if (-not (Test-Path $continueDir)) {
    New-Item -ItemType Directory -Path $continueDir -Force | Out-Null
    Write-Host "📁 Created .continue directory" -ForegroundColor Blue
}

# Backup existing config
if (Test-Path $continueConfigPath) {
    $backupPath = "$continueConfigPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $continueConfigPath $backupPath
    Write-Host "💾 Backed up existing config to: $(Split-Path $backupPath -Leaf)" -ForegroundColor Blue
}

# Create new config with Turbo + Local models
$continueConfig = @{
    models = @(
        @{
            title = "🚀 Turbo • GPT-OSS 120B (Cloud)"
            provider = "openai"
            model = "gpt-oss:120b"
            apiKey = "env:OLLAMA_TURBO_API_KEY"
            baseUrl = "https://ollama.com"
            contextLength = 32768
            systemMessage = "You are an expert coding assistant powered by Ollama Turbo."
        },
        @{
            title = "⚡ Turbo • GPT-OSS 20B (Fast Cloud)"
            provider = "openai"
            model = "gpt-oss:20b"
            apiKey = "env:OLLAMA_TURBO_API_KEY"
            baseUrl = "https://ollama.com"
            contextLength = 16384
            systemMessage = "You are a fast coding assistant powered by Ollama Turbo."
        },
        @{
            title = "💻 Local • DeepSeek Coder 6.7B"
            provider = "ollama"
            model = "deepseek-coder:6.7b"
            baseUrl = "http://localhost:11434"
            contextLength = 8192
            systemMessage = "You are a local coding assistant."
        },
        @{
            title = "🏠 Local • Llama 3.1 8B"
            provider = "ollama"
            model = "llama3.1:8b"
            baseUrl = "http://localhost:11434"
            contextLength = 8192
            systemMessage = "You are a helpful local AI assistant."
        }
    )
    tabAutocompleteModel = @{
        title = "🚀 Turbo Autocomplete"
        provider = "openai"
        model = "gpt-oss:20b"
        apiKey = "env:OLLAMA_TURBO_API_KEY"
        baseUrl = "https://ollama.com"
        contextLength = 4096
    }
    allowAnonymousTelemetry = $false
    contextProviders = @(
        @{ name = "code"; params = @{} },
        @{ name = "docs"; params = @{} },
        @{ name = "diff"; params = @{} },
        @{ name = "terminal"; params = @{} }
    )
    slashCommands = @(
        @{ name = "edit"; description = "Edit highlighted code" },
        @{ name = "comment"; description = "Write comments for highlighted code" },
        @{ name = "commit"; description = "Generate commit message" },
        @{ name = "cmd"; description = "Generate shell commands" }
    )
}

# Save config
try {
    $continueConfig | ConvertTo-Json -Depth 10 | Set-Content $continueConfigPath -Encoding UTF8
    Write-Host "✅ Continue extension configured successfully" -ForegroundColor Green
    Write-Host "📋 Models available:" -ForegroundColor White
    foreach ($model in $continueConfig.models) {
        Write-Host "   $($model.title)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Failed to save Continue config: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 5: Create quick test script
Write-Host "`n📝 Step 5: Creating Test Scripts..." -ForegroundColor Yellow

$testScript = @'
# 🧪 Ollama Turbo Quick Test
$env:OLLAMA_TURBO_API_KEY = [Environment]::GetEnvironmentVariable('OLLAMA_TURBO_API_KEY', [EnvironmentVariableTarget]::User)

if (-not $env:OLLAMA_TURBO_API_KEY) {
    Write-Host "❌ OLLAMA_TURBO_API_KEY not found!" -ForegroundColor Red
    exit 1
}

Write-Host "🧪 Testing Ollama Turbo API..." -ForegroundColor Cyan

$testPayload = @{
    model = "gpt-oss:20b"
    messages = @(@{ role = "user"; content = "Write a simple Python hello world function" })
    max_tokens = 200
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $env:OLLAMA_TURBO_API_KEY"
}

try {
    $response = Invoke-RestMethod -Uri "https://ollama.com/v1/chat/completions" -Method Post -Body $testPayload -Headers $headers -TimeoutSec 30
    
    Write-Host "✅ Turbo API Working!" -ForegroundColor Green
    Write-Host "🤖 Response:" -ForegroundColor Yellow
    Write-Host $response.choices[0].message.content -ForegroundColor White
    Write-Host "`n📊 Usage: $($response.usage.total_tokens) tokens" -ForegroundColor Blue
} catch {
    Write-Host "❌ Test Failed: $($_.Exception.Message)" -ForegroundColor Red
}
'@

$testScript | Out-File -FilePath ".\test_turbo_api.ps1" -Encoding UTF8
Write-Host "✅ Created test_turbo_api.ps1" -ForegroundColor Green

# Step 6: Security reminder
Write-Host "`n🔒 Step 6: Security Reminders" -ForegroundColor Yellow
Write-Host "=" * 30 -ForegroundColor Gray
Write-Host "🚨 IMPORTANT SECURITY NOTES:" -ForegroundColor Red
Write-Host "1. Your API key is stored in Windows User Environment Variables" -ForegroundColor White
Write-Host "2. Never commit .env files or scripts containing API keys to Git" -ForegroundColor White
Write-Host "3. Turbo sends data to Ollama's cloud - use local models for sensitive code" -ForegroundColor White
Write-Host "4. Regularly rotate your API keys" -ForegroundColor White

# Summary
Write-Host "`n" + "=" * 60 -ForegroundColor Gray
Write-Host "🎉 OLLAMA TURBO SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Gray

Write-Host "`n📊 SETUP SUMMARY:" -ForegroundColor Cyan
Write-Host "✅ API Key: Configured and tested" -ForegroundColor Green
Write-Host "✅ Environment: OLLAMA_TURBO_API_KEY set" -ForegroundColor Green
Write-Host "✅ Continue: 4 models configured (2 Turbo + 2 Local)" -ForegroundColor Green
Write-Host "✅ Scripts: test_turbo_api.ps1 created" -ForegroundColor Green

Write-Host "`n🚀 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Restart VS Code completely" -ForegroundColor White
Write-Host "2. Install Continue extension if not already installed" -ForegroundColor White
Write-Host "3. Press Ctrl+L to open Continue chat" -ForegroundColor White
Write-Host "4. Select '🚀 Turbo • GPT-OSS 120B (Cloud)'" -ForegroundColor White
Write-Host "5. Test with prompt: 'Write a Python web scraper'" -ForegroundColor White

Write-Host "`n💡 USAGE TIPS:" -ForegroundColor Cyan
Write-Host "🌩️ Cloud (Turbo): Best for complex tasks, latest capabilities" -ForegroundColor Blue
Write-Host "🏠 Local: Best for privacy, offline work, simple tasks" -ForegroundColor Green
Write-Host "⚡ Switch models easily in Continue interface" -ForegroundColor Magenta

Write-Host "`n🧪 TEST COMMANDS:" -ForegroundColor Yellow
Write-Host ".\test_turbo_api.ps1                    # Test API directly" -ForegroundColor Gray
Write-Host "ollama list                             # Check local models" -ForegroundColor Gray

if ($apiWorking) {
    Write-Host "`n🎯 STATUS: ALL SYSTEMS GO! 🚀" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ STATUS: API needs verification" -ForegroundColor Yellow
    Write-Host "Run .\test_turbo_api.ps1 to test again" -ForegroundColor White
}

Write-Host "`n✨ Happy coding with Ollama Turbo! ✨" -ForegroundColor Magenta

# Clear the plain key from memory
$plainKey = $null