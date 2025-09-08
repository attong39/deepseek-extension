Param(
      [string]$Root = ".",
      [string]$OutDir = "reports/quick_audit",
      [switch]$NoNear,
      [string]$ExcludeDirs = $null
)

# Prefer repo venv python if available with a valid pyvenv.cfg, else fallback to PATH python
$venvPy = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
$venvCfg = Join-Path $PSScriptRoot "..\.venv\pyvenv.cfg"
if ((Test-Path $venvPy) -and (Test-Path $venvCfg)) {
      $py = $venvPy
}
else {
      $py = "python"
}

$flags = "--root", $Root, "--report-dir", $OutDir
if ($NoNear) { $flags += "--no-near" }
if ($ExcludeDirs) { $flags += "--exclude-dirs"; $flags += $ExcludeDirs }

Write-Host "Running quick audit with:" $py scripts\consolidation_audit.py $flags
& $py scripts\consolidation_audit.py @flags
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }