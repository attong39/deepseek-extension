param(
      [string[]]$Paths = @('.'),
      [string]$Output = "reports/duplicates/duplicate_files.json",
      [string]$MdOutput = "reports/duplicates/duplicate_files.md",
      [switch]$IncludeHidden,
      [switch]$FollowSymlinks,
      [int]$MinSize = 1,
      [int]$HeadBytes = 65536,
      [int]$Workers = 0,
      [int]$PrintTop = 10,
      [switch]$CIFailOnDuplicates
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptPath = Join-Path $repoRoot "tools/find_duplicate_files.py"

# Build argument list
$argsList = @("--paths") + $Paths
$argsList += @("--output", $Output)
$argsList += @("--md-output", $MdOutput)
$argsList += @("--min-size", $MinSize)
$argsList += @("--head-bytes", $HeadBytes)
if ($Workers -gt 0) { $argsList += @("--workers", $Workers) }
if ($IncludeHidden) { $argsList += "--include-hidden" }
if ($FollowSymlinks) { $argsList += "--follow-symlinks" }
if ($PrintTop -ge 0) { $argsList += @("--print-top", $PrintTop) }
if ($CIFailOnDuplicates) { $argsList += "--ci-fail-on-duplicates" }

# Reasonable default excludes
$defaultExcludes = @(".git", "node_modules", ".venv")
foreach ($ex in $defaultExcludes) { $argsList += @("--exclude", $ex) }

Write-Host "Running duplicate scan..." -ForegroundColor Cyan
python $scriptPath @argsList
if ($LASTEXITCODE -eq 2) {
      Write-Warning "Duplicates found (exit code 2)."
      exit 2
}
exit $LASTEXITCODE
