<#
.SYNOPSIS
    Chạy chuỗi kiểm tra duplicate code (jscpd, aggregator, quick analyzer) không tương tác.

Mô tả:
    Script này gọi `scripts/check_duplicates.py` bằng Python của venv nếu có,
    truyền tham số mặc định (min-lines/min-tokens) và tuỳ chọn threshold để
    bỏ fail nếu duplication vượt ngưỡng. Kết quả (logs, summary) sẽ nằm trong
    `reports/duplicates/`.

    Dùng trên Windows PowerShell (developer machines).

Usage:
    PS> .\scripts\run_duplicate_checks.ps1

#>

param(
    [int] $MinLines = 12,
    [int] $MinTokens = 50,
    [double] $FailIfDupAbove = 1.0
)

Set-StrictMode -Version Latest

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

# Prefer venv python if exists
$venvPy = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-Not (Test-Path $venvPy)) {
    Write-Host "⚠️ venv python not found at $venvPy — fallback to 'python' from PATH"
    $venvPy = "python"
}

$checkScript = Join-Path $scriptDir "check_duplicates.py"
$reportDir = Join-Path $repoRoot "reports\duplicates"

Write-Host "🚀 Running duplicate checks (jscpd -> aggregator -> quick analyzer)"
Write-Host "  report dir: $reportDir"
Write-Host "  min-lines: $MinLines, min-tokens: $MinTokens, fail-if-dup-above: $FailIfDupAbove"

# Ensure report dir exists
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null


$scriptArgs = @(
    $checkScript,
    "--report-dir", $reportDir,
    "--min-lines", $MinLines,
    "--min-tokens", $MinTokens,
    "--fail-if-dup-above", $FailIfDupAbove
)

Write-Host "Running: $venvPy $($scriptArgs -join ' ')"
& $venvPy @scriptArgs
$rc = $LASTEXITCODE

if ($rc -ne 0) {
    Write-Host "❌ Duplicate checks failed (exit code $rc). See reports in: $reportDir" -ForegroundColor Red
    exit $rc
}

Write-Host "✅ Duplicate checks completed successfully. Reports (if any) are under: $reportDir" -ForegroundColor Green
exit 0
