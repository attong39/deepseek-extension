<#
Enable repository git hooks by setting core.hooksPath to .githooks

Usage (PowerShell):
  .\scripts\setup_hooks.ps1

This will run:
  git config core.hooksPath .githooks

You can skip running hooks locally by setting environment variable:
  $env:SKIP_DUP_CHECK = '1'
#>

Set-StrictMode -Version Latest

Write-Host "Setting repository git hooks path to '.githooks'..."

$repoRoot = Resolve-Path (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")
Push-Location $repoRoot
try {
    git --version > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "git is not available in PATH." -ForegroundColor Yellow
        exit 1
    }

    git config core.hooksPath .githooks
    Write-Host "✅ Hooks enabled: git config core.hooksPath .githooks"
}
catch {
    Write-Host "Failed to set hooks path: $_" -ForegroundColor Red
    exit 1
}
finally {
    Pop-Location
}

exit 0
