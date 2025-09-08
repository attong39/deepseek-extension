# Zeta Virtual Environment Helper Module

function Activate-ZetaVenv {
    $activateScript = "E:\zeta-monorepo\.venv\Scripts\Activate.ps1"
    if (Test-Path $activateScript) {
        . $activateScript
        Write-Host "🚀 Zeta virtual environment activated!" -ForegroundColor Green
    } else {
        Write-Host "❌ Activation script not found: $activateScript" -ForegroundColor Red
    }
}

function Deactivate-ZetaVenv {
    if ($env:VIRTUAL_ENV) {
        deactivate
        Write-Host "✅ Virtual environment deactivated" -ForegroundColor Green
    } else {
        Write-Host "⚠️ No virtual environment active" -ForegroundColor Yellow
    }
}

function Check-ZetaVenv {
    Write-Host "🔍 Virtual Environment Status:" -ForegroundColor Cyan
    if ($env:VIRTUAL_ENV) {
        Write-Host "✅ Active: $env:VIRTUAL_ENV" -ForegroundColor Green
        Write-Host "🐍 Python: $(python --version 2>&1)" -ForegroundColor White
        Write-Host "📦 Pip: $(pip --version 2>&1)" -ForegroundColor White
    } else {
        Write-Host "❌ No virtual environment active" -ForegroundColor Red
        Write-Host "💡 Run: Activate-ZetaVenv" -ForegroundColor Cyan
    }
}

# Aliases for convenience
Set-Alias -Name "venv" -Value "Activate-ZetaVenv"
Set-Alias -Name "devenv" -Value "Check-ZetaVenv"

Export-ModuleMember -Function Activate-ZetaVenv, Deactivate-ZetaVenv, Check-ZetaVenv -Alias venv, devenv
