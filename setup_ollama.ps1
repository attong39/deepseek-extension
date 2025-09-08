# 🚀 Zeta AI - Ollama Model Setup Script
# Automated setup for creating and pushing attong39/zeta model

param(
    [switch]$Install,
    [switch]$Setup,
    [switch]$Test,
    [switch]$Push,
    [switch]$Help
)

# Configuration
$ModelName = "attong39/zeta"
$BaseModel = "llama3.2"
$ModelfilePath = "Modelfile"

function Write-Header {
    param([string]$Text)
    Write-Host "`n$('='*60)" -ForegroundColor Cyan
    Write-Host "🎯 $Text" -ForegroundColor Yellow
    Write-Host "$('='*60)" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠️ $Text" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Text)
    Write-Host "❌ $Text" -ForegroundColor Red
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ️ $Text" -ForegroundColor Blue
}

function Test-Ollama {
    Write-Info "Checking Ollama installation..."
    try {
        $version = ollama --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Ollama is installed: $version"
            return $true
        }
        else {
            Write-Warning "Ollama not found or not working"
            return $false
        }
    }
    catch {
        Write-Warning "Ollama command not found"
        return $false
    }
}

function Install-Ollama {
    Write-Header "Installing Ollama"

    Write-Info "Downloading Ollama installer..."
    try {
        Invoke-WebRequest -Uri "https://ollama.ai/download/OllamaSetup.exe" -OutFile "OllamaSetup.exe"
        Write-Success "Downloaded OllamaSetup.exe"
    }
    catch {
        Write-Error "Failed to download Ollama installer: $_"
        Write-Info "Please download manually from: https://ollama.ai/download"
        return $false
    }

    Write-Info "Running installer (you may need to run as Administrator)..."
    Write-Warning "Please complete the Ollama installation and restart your terminal"
    Write-Info "After installation, run this script again with -Setup flag"

    return $true
}

function New-Model {
    Write-Header "Setting up Zeta AI Model"

    # Check if Modelfile exists
    if (-not (Test-Path $ModelfilePath)) {
        Write-Error "Modelfile not found at: $ModelfilePath"
        Write-Info "Please ensure Modelfile exists in the current directory"
        return $false
    }

    Write-Info "Pulling base model: $BaseModel"
    try {
        ollama pull $BaseModel
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Successfully pulled $BaseModel"
        }
        else {
            Write-Error "Failed to pull $BaseModel"
            return $false
        }
    }
    catch {
        Write-Error "Error pulling base model: $_"
        return $false
    }

    Write-Info "Creating custom model: $ModelName"
    try {
        ollama create -f $ModelfilePath $ModelName
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Successfully created $ModelName"
        }
        else {
            Write-Error "Failed to create $ModelName"
            return $false
        }
    }
    catch {
        Write-Error "Error creating model: $_"
        return $false
    }

    return $true
}

function Test-Model {
    Write-Header "Testing Zeta AI Model"

    Write-Info "Testing model: $ModelName"
    try {
        $testPrompt = "Xin chào! Bạn có thể giúp tôi với Python không?"
        Write-Info "Test prompt: $testPrompt"

        # Test with API
        $body = @{
            model  = $ModelName
            prompt = $testPrompt
            stream = $false
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json"

        if ($response.response) {
            Write-Success "Model test successful!"
            Write-Info "Response: $($response.response)"
        }
        else {
            Write-Warning "Model test completed but no response received"
        }

        return $true
    }
    catch {
        Write-Error "Model test failed: $_"
        Write-Info "Make sure Ollama is running and model is available"
        return $false
    }
}

function Push-Model {
    Write-Header "Pushing Model to Registry"

    Write-Info "Pushing $ModelName to Ollama registry..."
    try {
        ollama push $ModelName
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Successfully pushed $ModelName to registry"
            Write-Info "Your model is now available at: https://ollama.ai/$ModelName"
        }
        else {
            Write-Error "Failed to push $ModelName"
            return $false
        }
    }
    catch {
        Write-Error "Error pushing model: $_"
        return $false
    }

    return $true
}

function Show-Help {
    Write-Header "Zeta AI - Ollama Model Setup Help"

    Write-Host @"
USAGE:
    .\setup_ollama.ps1 [OPTIONS]

OPTIONS:
    -Install    Install Ollama (download and run installer)
    -Setup      Setup the model (pull base model, create custom model)
    -Test       Test the created model
    -Push       Push model to Ollama registry
    -Help       Show this help message

EXAMPLES:
    .\setup_ollama.ps1 -Install          # Install Ollama
    .\setup_ollama.ps1 -Setup            # Setup the model
    .\setup_ollama.ps1 -Test             # Test the model
    .\setup_ollama.ps1 -Push             # Push to registry

WORKFLOW:
    1. .\setup_ollama.ps1 -Install       # Install Ollama
    2. Restart terminal/command prompt
    3. .\setup_ollama.ps1 -Setup         # Create model
    4. .\setup_ollama.ps1 -Test          # Test model
    5. .\setup_ollama.ps1 -Push          # Push to registry

MODEL INFO:
    • Base Model: $BaseModel
    • Custom Model: $ModelName
    • Modelfile: $ModelfilePath

TROUBLESHOOTING:
    • If 'ollama' command not found, restart terminal after installation
    • If model creation fails, check Modelfile exists and is valid
    • If push fails, ensure you have internet connection
"@
}

function Main {
    if ($Help) {
        Show-Help
        return
    }

    Write-Header "Zeta AI - Ollama Model Setup"

    if ($Install) {
        if (Install-Ollama) {
            Write-Info "Installation initiated. Please complete the setup and restart your terminal."
        }
        return
    }

    # Check Ollama installation for other operations
    if (-not (Test-Ollama)) {
        Write-Error "Ollama is not installed or not working properly."
        Write-Info "Run: .\setup_ollama.ps1 -Install"
        Write-Info "Then restart your terminal and run setup again."
        return
    }

    if ($Setup) {
        if (New-Model) {
            Write-Success "Model setup completed successfully!"
            Write-Info "You can now test the model with: .\setup_ollama.ps1 -Test"
        }
    }

    if ($Test) {
        if (Test-Model) {
            Write-Success "Model test completed successfully!"
            Write-Info "You can now push the model with: .\setup_ollama.ps1 -Push"
        }
    }

    if ($Push) {
        if (Push-Model) {
            Write-Success "Model push completed successfully!"
            Write-Info "Your model is now available at: https://ollama.ai/$ModelName"
        }
    }

    # If no specific flag, show help
    if (-not ($Setup -or $Test -or $Push)) {
        Write-Info "No operation specified. Use -Help for usage information."
        Write-Info "Quick start: .\setup_ollama.ps1 -Setup -Test -Push"
    }
}

# Run main function
Main
