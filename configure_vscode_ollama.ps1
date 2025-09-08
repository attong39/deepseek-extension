# 🔧 Configure VS Code for Ollama
param(
    [string]$OllamaHome = "C:\Users\USDT239\.ollama"
)

Write-Host "🔧 Configuring VS Code for Ollama..." -ForegroundColor Cyan
Write-Host "OLLAMA_HOME: $OllamaHome" -ForegroundColor Yellow

# VS Code settings path
$settingsPath = "$env:APPDATA\Code\User\settings.json"

# Create settings if not exists
if (-not (Test-Path $settingsPath)) {
    Write-Host "📁 Creating VS Code settings.json..." -ForegroundColor Green
    New-Item -Path $settingsPath -ItemType File -Force | Out-Null
    Set-Content -Path $settingsPath -Value "{}" -Encoding UTF8
}

# Read current settings
try {
    $settingsContent = Get-Content $settingsPath -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($settingsContent)) {
        $settingsContent = "{}"
    }
    $settings = $settingsContent | ConvertFrom-Json
} catch {
    Write-Host "⚠️ Error reading settings, creating new..." -ForegroundColor Yellow
    $settings = @{}
}

# Add Ollama configuration
Write-Host "⚙️ Adding Ollama settings..." -ForegroundColor Green

# Convert to hashtable if needed
if ($settings -is [PSCustomObject]) {
    $settingsHash = @{}
    $settings.PSObject.Properties | ForEach-Object {
        $settingsHash[$_.Name] = $_.Value
    }
    $settings = $settingsHash
}

# Ollama settings
$settings["ollama.home"] = $OllamaHome
$settings["ollama.homePath"] = $OllamaHome
$settings["ollama.modelsPath"] = "$OllamaHome\models"
$settings["ollama.host"] = "127.0.0.1:11434"
$settings["ollama.apiKey"] = ""

# Continue extension settings
$settings["continue.enableTabAutocomplete"] = $true
$settings["continue.manuallyTriggerCompletion"] = $false

# Convert back to JSON and save
$jsonSettings = $settings | ConvertTo-Json -Depth 10
Set-Content -Path $settingsPath -Value $jsonSettings -Encoding UTF8

Write-Host "✅ VS Code settings updated!" -ForegroundColor Green
Write-Host "📂 Settings saved to: $settingsPath" -ForegroundColor White

# Show relevant settings
Write-Host "`n📋 Ollama Settings Added:" -ForegroundColor Cyan
Write-Host "  ollama.home: $OllamaHome" -ForegroundColor White
Write-Host "  ollama.modelsPath: $OllamaHome\models" -ForegroundColor White
Write-Host "  ollama.host: 127.0.0.1:11434" -ForegroundColor White

Write-Host "`n🔄 Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart VS Code (Ctrl+Shift+P → Developer: Reload Window)" -ForegroundColor White
Write-Host "2. Open Continue extension (Ctrl+L)" -ForegroundColor White
Write-Host "3. Test with your models!" -ForegroundColor White