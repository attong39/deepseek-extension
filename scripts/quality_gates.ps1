Param(
      [switch]$Fix
)

# Choose python from valid repo venv if present, else PATH
$venvPy = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
$venvCfg = Join-Path $PSScriptRoot "..\.venv\pyvenv.cfg"
if ((Test-Path $venvPy) -and (Test-Path $venvCfg)) {
      $py = $venvPy
}
else {
      $py = "python"
}

# 1) Ruff (lint + import order)
if ($Fix) {
      Write-Host "[Ruff] Fixing..."
      & $py -m ruff check . --fix
}
else {
      Write-Host "[Ruff] Checking..."
      & $py -m ruff check .
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 2) mypy (type-check)
Write-Host "[mypy] Type checking..."
& $py -m mypy .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 3) pytest + coverage
Write-Host "[pytest] Running tests with coverage..."
& $py -m pytest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "All quality gates passed."
