# 🔐 Turbo Ollama Login Manager
param(
    [Parameter(Position=0)]
    [ValidateSet("login", "logout", "status", "switch", "help")]
    [string]$Action = "help",
    
    [Parameter()]
    [ValidateSet("local", "online")]
    [string]$Mode
)

function Show-Help {
    Write-Host "🔐 TURBO OLLAMA LOGIN MANAGER" -ForegroundColor Cyan
    Write-Host "=" * 40 -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\login.ps1 login          # Interactive login" -ForegroundColor White
    Write-Host "  .\login.ps1 status         # Show current status" -ForegroundColor White
    Write-Host "  .\login.ps1 logout         # Logout and clear auth" -ForegroundColor White
    Write-Host "  .\login.ps1 switch local   # Switch to local mode" -ForegroundColor White
    Write-Host "  .\login.ps1 switch online  # Switch to online mode" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  # First time setup" -ForegroundColor Gray
    Write-Host "  .\login.ps1 login" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Check if logged in" -ForegroundColor Gray
    Write-Host "  .\login.ps1 status" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Use local models only" -ForegroundColor Gray
    Write-Host "  .\login.ps1 switch local" -ForegroundColor White
}

function Test-PythonAvailable {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

function Invoke-TurboLogin {
    param([string]$LoginAction, [string]$SwitchMode)
    
    if (-not (Test-PythonAvailable)) {
        Write-Host "❌ Python not found" -ForegroundColor Red
        Write-Host "💡 Please install Python first" -ForegroundColor Yellow
        return
    }
    
    $loginScript = "turbo_ollama_login.py"
    
    if (-not (Test-Path $loginScript)) {
        Write-Host "❌ Login script not found: $loginScript" -ForegroundColor Red
        return
    }
    
    if ($LoginAction -eq "switch" -and $SwitchMode) {
        python $loginScript $LoginAction --mode $SwitchMode
    } else {
        python $loginScript $LoginAction
    }
}

# Main execution
switch ($Action) {
    "help" {
        Show-Help
    }
    
    "login" {
        Write-Host "🔐 Starting Turbo Ollama Login..." -ForegroundColor Cyan
        Invoke-TurboLogin "login"
    }
    
    "logout" {
        Write-Host "👋 Logging out..." -ForegroundColor Yellow
        Invoke-TurboLogin "logout"
    }
    
    "status" {
        Write-Host "📊 Checking status..." -ForegroundColor Cyan
        Invoke-TurboLogin "status"
    }
    
    "switch" {
        if (-not $Mode) {
            Write-Host "❌ Please specify mode: -Mode local or -Mode online" -ForegroundColor Red
            Write-Host "Example: .\login.ps1 switch -Mode local" -ForegroundColor Yellow
            return
        }
        
        Write-Host "🔄 Switching to $Mode mode..." -ForegroundColor Cyan
        Invoke-TurboLogin "switch" $Mode
    }
    
    default {
        Write-Host "❌ Unknown action: $Action" -ForegroundColor Red
        Show-Help
    }
}