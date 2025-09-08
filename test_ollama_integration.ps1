# 🧪 Zeta AI - Ollama Integration Test
# Test script to verify Ollama model integration with development server and VS Code extension

param(
    [string]$ModelName = "gemma:2b",
    [string]$ServerUrl = "http://localhost:8000",
    [string]$OllamaUrl = "http://localhost:11434",
    [switch]$Verbose
)

# Configuration
$TestPrompts = @(
    "Xin chào! Bạn có thể giúp tôi với Python không?",
    "Viết một hàm Python đơn giản để tính tổng của một danh sách số",
    "Giải thích khái niệm 'machine learning' một cách đơn giản"
)

function Write-Header {
    param([string]$Text)
    Write-Host "`n$('='*60)" -ForegroundColor Cyan
    Write-Host "🧪 $Text" -ForegroundColor Yellow
    Write-Host "$('='*60)" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor Green
}

function Write-Error {
    param([string]$Text)
    Write-Host "❌ $Text" -ForegroundColor Red
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ️ $Text" -ForegroundColor Blue
}

function Test-OllamaDirect {
    Write-Header "Testing Ollama Direct API"

    Write-Info "Testing direct Ollama API connection..."

    foreach ($prompt in $TestPrompts) {
        Write-Info "Testing prompt: $prompt"

        try {
            $body = @{
                model  = $ModelName
                prompt = $prompt
                stream = $false
            } | ConvertTo-Json

            $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 30

            if ($response.response) {
                Write-Success "Direct Ollama test successful!"
                if ($Verbose) {
                    Write-Host "Response: $($response.response)" -ForegroundColor Gray
                }
            }
            else {
                Write-Warning "No response received from Ollama"
            }
        }
        catch {
            Write-Error "Direct Ollama test failed: $_"
            return $false
        }
    }

    return $true
}

function Test-DevelopmentServer {
    Write-Header "Testing Development Server Integration"

    Write-Info "Testing development server health endpoint..."

    try {
        $healthResponse = Invoke-RestMethod -Uri "$ServerUrl/health" -Method Get -TimeoutSec 10
        Write-Success "Development server is running"
        if ($Verbose) {
            Write-Host "Health response: $($healthResponse | ConvertTo-Json)" -ForegroundColor Gray
        }
    }
    catch {
        Write-Error "Development server health check failed: $_"
        Write-Info "Make sure the development server is running on $ServerUrl"
        return $false
    }

    Write-Info "Testing AI chat endpoint..."

    foreach ($prompt in $TestPrompts) {
        Write-Info "Testing prompt: $prompt"

        try {
            $body = @{
                message = $prompt
                model   = $ModelName
            } | ConvertTo-Json

            $response = Invoke-RestMethod -Uri "$ServerUrl/chat" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 30

            if ($response.response) {
                Write-Success "Development server AI chat test successful!"
                if ($Verbose) {
                    Write-Host "Response: $($response.response)" -ForegroundColor Gray
                }
            }
            else {
                Write-Warning "No response received from development server"
            }
        }
        catch {
            Write-Error "Development server AI chat test failed: $_"
            return $false
        }
    }

    return $true
}

function Test-Environment {
    Write-Header "Testing Environment Configuration"

    Write-Info "Checking environment variables..."

    $envVars = @(
        "OLLAMA_MODEL",
        "OLLAMA_API_KEY",
        "OLLAMA_BASE_URL"
    )

    foreach ($var in $envVars) {
        $value = [Environment]::GetEnvironmentVariable($var)
        if ($value) {
            Write-Success "Environment variable $var is set"
            if ($Verbose) {
                Write-Host "Value: $value" -ForegroundColor Gray
            }
        }
        else {
            Write-Warning "Environment variable $var is not set"
        }
    }

    Write-Info "Checking Ollama service..."

    try {
        $ollamaVersion = ollama --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Ollama service is running: $ollamaVersion"
        }
        else {
            Write-Error "Ollama service is not responding"
            return $false
        }
    }
    catch {
        Write-Error "Ollama command not found: $_"
        return $false
    }

    Write-Info "Checking model availability..."

    try {
        $models = ollama list 2>&1
        if ($LASTEXITCODE -eq 0 -and $models -match $ModelName) {
            Write-Success "Model $ModelName is available"
        }
        else {
            Write-Error "Model $ModelName is not available"
            Write-Info "Available models:"
            Write-Host $models -ForegroundColor Gray
            return $false
        }
    }
    catch {
        Write-Error "Failed to check model availability: $_"
        return $false
    }

    return $true
}

function Main {
    Write-Header "Zeta AI - Ollama Integration Test"

    Write-Info "Model: $ModelName"
    Write-Info "Server: $ServerUrl"
    Write-Info "Verbose: $Verbose"

    $allTestsPassed = $true

    # Test environment first
    if (-not (Test-Environment)) {
        $allTestsPassed = $false
        Write-Error "Environment test failed. Please check your setup."
    }

    # Test direct Ollama API
    if (-not (Test-OllamaDirect)) {
        $allTestsPassed = $false
        Write-Error "Direct Ollama test failed."
    }

    # Test development server integration
    if (-not (Test-DevelopmentServer)) {
        $allTestsPassed = $false
        Write-Error "Development server test failed."
    }

    # Summary
    Write-Header "Test Summary"

    if ($allTestsPassed) {
        Write-Success "All tests passed! 🎉"
        Write-Info "Your Zeta AI setup is working correctly."
        Write-Info "You can now use the AI features in your development environment."
    }
    else {
        Write-Error "Some tests failed. Please check the errors above and fix any issues."
        Write-Info "Common fixes:"
        Write-Info "1. Make sure Ollama is running: ollama serve"
        Write-Info "2. Make sure the model is created: .\setup_ollama.ps1 -Setup"
        Write-Info "3. Make sure the development server is running"
        Write-Info "4. Check your .env file configuration"
    }
}

# Run main function
Main
