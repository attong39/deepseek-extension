<#
Bootstrap developer environment on Windows (PowerShell).

What it does:
- Create `.venv` if missing
- Install `requirements-dev.txt` if present
- Enable git hooks via `scripts/setup_hooks.ps1`
- Run duplicate checks once via `scripts/run_duplicate_checks.ps1`

Usage (PowerShell):
  .\scripts\bootstrap.ps1
#>

Set-StrictMode -Version Latest

$repoRoot = Resolve-Path (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")
Push-Location $repoRoot
try {
    if (-Not (Test-Path ".venv\Scripts\python.exe")) {
        Write-Host "Creating virtualenv .venv..."
        python -m venv .venv
    }
    else {
        Write-Host "Using existing .venv"
    }

    $pip = Join-Path $repoRoot ".venv\Scripts\pip.exe"
    if (Test-Path "requirements-dev.txt") {
        Write-Host "Installing requirements-dev.txt..."
        & $pip install -r requirements-dev.txt
    }
    else {
        Write-Host "No requirements-dev.txt found, skipping pip install"
    }

    Write-Host "Enabling git hooks..."
    .\scripts\setup_hooks.ps1

    Write-Host "Running duplicate checks once..."
    .\scripts\run_duplicate_checks.ps1
}
finally {
    Pop-Location
}

exit 0
