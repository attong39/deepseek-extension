param(
    [string]$DefaultBranch = "main",
    [string]$TestPattern = "memory",
    [switch]$SkipSecurity = $true,
    [string[]]$Files
)

$ErrorActionPreference = "Stop"

function Run($cmd) {
    Write-Host ">> $cmd" -ForegroundColor Cyan
    iex $cmd
    if ($LASTEXITCODE -ne 0) { throw "Command failed: $cmd" }
}

# Tập PR1 mặc định nếu không truyền -Files
$PR1 = @(
    "zeta_vn/core/ports/memory.py",
    "zeta_vn/data/services/memory_adapter.py",
    "zeta_vn/data/services/memory_legacy.py",
    "zeta_vn/core/use_cases/memory/query_memory.py",
    "zeta_vn/core/use_cases/memory/upsert_memory.py",
    "zeta_vn/core/use_cases/memory/delete_memory_simple.py",
    "zeta_vn/core/use_cases/memory/rebuild_embeddings.py",
    "zeta_vn/app/dependencies/memory.py",
    "zeta_vn/app/api/v1/memory.py",
    "tests/test_memory_adapter_and_usecases.py"
)

function Existing($paths) {
    $out = @()
    foreach ($p in $paths) { if (Test-Path $p) { $out += $p } }
    return $out
}

$TARGET = if ($Files -and $Files.Count -gt 0) { Existing $Files } else { Existing $PR1 }
if ($TARGET.Count -eq 0) { throw "No target files found for CI." }
$Q = $TARGET | ForEach-Object { '"{0}"' -f $_ }
$JOINED = ($Q -join ' ')

# Kiểm tra uv có sẵn
uv --version *> $null
if ($LASTEXITCODE -ne 0) {
    throw "uv chưa được cài. Cài: https://github.com/astral-sh/uv"
}

# Lint & type-check (giới hạn phạm vi PR1)
Run "uv run ruff check --fix $JOINED"
Run "uv run mypy --config-file mypy.ini $JOINED"

# Security & deps (tuỳ chọn, skip mặc định)
if (-not $SkipSecurity) {
    $SEC_TARGET = @(
        "zeta_vn/core/use_cases/memory",
        "zeta_vn/app/dependencies/memory.py",
        "zeta_vn/app/api/v1/memory.py",
        "zeta_vn/data/services/memory_adapter.py",
        "zeta_vn/data/services/memory_legacy.py",
        "zeta_vn/core/ports/memory.py"
    ) | Where-Object { Test-Path $_ }
    if ($SEC_TARGET.Count -gt 0) {
        $SECQ = $SEC_TARGET | ForEach-Object { '"{0}"' -f $_ }
        $SECJ = ($SECQ -join ' ')
        Run "uv run bandit -q -r $SECJ -x tests"
    }
    Run "uv run pip-audit -ry"
    if (Test-Path "zeta_vn/core/use_cases/memory") {
        Run "uv run vulture zeta_vn/core/use_cases/memory --min-confidence 80"
    }
}

# Unit tests theo pattern
Run "uv run pytest -q -k $TestPattern --maxfail=1 -c pytest.ini tests --ignore wt_feat_memory_protocol_wiring_clean"

Write-Host "`n✅ CI local passed for PR1 pattern: $TestPattern" -ForegroundColor Green
