param(
      [switch]$NoWatchdog,
      [switch]$OneShot
)

$ErrorActionPreference = 'Stop'

# Activate venv if present
if (Test-Path (Join-Path $PSScriptRoot '..\\.venv')) {
      $venvPath = Resolve-Path (Join-Path $PSScriptRoot '..\\.venv')
      $activate = Join-Path $venvPath 'Scripts\\Activate.ps1'
      if (Test-Path $activate) { . $activate }
}

if (-not $NoWatchdog) {
      try {
            Write-Host 'Ensuring dependencies (watchdog, libcst)...' -ForegroundColor Yellow
            pip install watchdog libcst | Out-Null
      }
      catch {
            Write-Warning 'Python not found or pip install failed. Please install dependencies manually.'
      }
}

$monitor = Join-Path $PSScriptRoot '..\\tools\\ai-project-intelligence\\continuous-monitor.py'
if ($OneShot) {
      python $monitor --one-shot
}
else {
      python $monitor
}
