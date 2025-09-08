# Test Ollama API endpoints

param(
  [string]$BaseUrl = "http://127.0.0.1:11434",
  [string]$Model = "gpt-oss:20b"
)

Write-Host "🧪 Testing Ollama API..." -ForegroundColor Cyan

# Test 1: Health check
Write-Host "1️⃣ Health check..." -ForegroundColor Yellow
try {
  $health = Invoke-WebRequest -Uri "$BaseUrl/api/tags" -TimeoutSec 5
  Write-Host "✅ Health: HTTP $($health.StatusCode)" -ForegroundColor Green
} catch {
  Write-Host "❌ Health failed: $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}

# Test 2: List models
Write-Host "2️⃣ List models..." -ForegroundColor Yellow
try {
  $models = Invoke-WebRequest -Uri "$BaseUrl/api/tags" | ConvertFrom-Json
  $modelNames = $models.models | ForEach-Object { $_.name }
  Write-Host "✅ Models: $($modelNames -join ', ')" -ForegroundColor Green
} catch {
  Write-Host "❌ Cannot list models" -ForegroundColor Red
}

# Test 3: Simple generate
Write-Host "3️⃣ Test generate..." -ForegroundColor Yellow
$generatePayload = @{
  model = $Model
  prompt = "Hello, respond with just 'Hi'"
  stream = $false
} | ConvertTo-Json

try {
  $generate = Invoke-WebRequest -Uri "$BaseUrl/api/generate" `
    -Method POST -ContentType "application/json" -Body $generatePayload -TimeoutSec 30
  $result = $generate.Content | ConvertFrom-Json
  Write-Host "✅ Generate: $($result.response)" -ForegroundColor Green
} catch {
  Write-Host "❌ Generate failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Chat API
Write-Host "4️⃣ Test chat..." -ForegroundColor Yellow
$chatPayload = @{
  model = $Model
  messages = @(
    @{ role = "user"; content = "Say hi" }
  )
  stream = $false
} | ConvertTo-Json -Depth 3

try {
  $chat = Invoke-WebRequest -Uri "$BaseUrl/api/chat" `
    -Method POST -ContentType "application/json" -Body $chatPayload -TimeoutSec 30
  $chatResult = $chat.Content | ConvertFrom-Json
  Write-Host "✅ Chat: $($chatResult.message.content)" -ForegroundColor Green
} catch {
  Write-Host "❌ Chat failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "🎉 API testing hoàn thành!" -ForegroundColor Green
