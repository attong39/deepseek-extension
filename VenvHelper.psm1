# Virtual Environment Helper for PowerShell
function Activate-ZetaEnv {
    $venvPath = "E:\zeta-monorepo\.venv\Scripts\Activate.ps1"
    if (Test-Path $venvPath) {
        & $venvPath
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } else {
        Write-Host "❌ Virtual environment not found" -ForegroundColor Red
        Write-Host "💡 Create with: python -m venv .venv" -ForegroundColor Cyan
    }
}

# Export function
Export-ModuleMember -Function Activate-ZetaEnv
