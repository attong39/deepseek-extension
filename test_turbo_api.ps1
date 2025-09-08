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
    $response = Invoke-RestMethod -Uri "https://api.ollama.com/v1/chat/completions" -Method Post -Body $testPayload -Headers $headers -TimeoutSec 30
    
    Write-Host "✅ Turbo API Working!" -ForegroundColor Green
    Write-Host "🤖 Response:" -ForegroundColor Yellow
    Write-Host $response.choices[0].message.content -ForegroundColor White
    Write-Host "`n📊 Usage: $($response.usage.total_tokens) tokens" -ForegroundColor Blue
} catch {
    Write-Host "❌ Test Failed: $($_.Exception.Message)" -ForegroundColor Red
}
