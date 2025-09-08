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
    $response = Invoke-RestMethod -Uri "http://localhost:11434/v1/chat/completions" -Method Post -Body $testPayload -Headers $headers -TimeoutSec 60
    
    Write-Host "✅ Local Ollama Working!" -ForegroundColor Green
    Write-Host "🤖 Response:" -ForegroundColor Yellow
    Write-Host $response.choices[0].message.content -ForegroundColor White
    Write-Host "`n📊 Usage: $($response.usage.total_tokens) tokens" -ForegroundColor Blue
} catch {
    Write-Host "❌ Test Failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Check if Ollama daemon is running: Get-Process ollama" -ForegroundColor Blue
}
