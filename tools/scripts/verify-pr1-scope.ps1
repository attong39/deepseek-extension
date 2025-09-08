param(
    [string]$DefaultBranch = "main"
)

$ErrorActionPreference = "Stop"

# Danh sách file thuộc PR1
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

# Chọn base: origin/<branch> nếu có, nếu không dùng local <branch>
$baseRef = "origin/$DefaultBranch"
try {
    # Try to resolve remote ref; PowerShell captures non-zero exit via exception when -ErrorAction Stop
    $proc = Start-Process git -ArgumentList @('rev-parse', '--verify', $baseRef) -NoNewWindow -RedirectStandardOutput 'NUL' -RedirectStandardError 'NUL' -Wait -PassThru
    if ($proc.ExitCode -eq 0) { $base = $baseRef } else { $base = $DefaultBranch }
}
catch {
    # Could be no origin or ambiguous; fallback to local branch
    $base = $DefaultBranch
}

# Lấy danh sách file thay đổi từ base..HEAD (không bật rename detection để nhanh, tránh kẹt)
$changed = @(git diff --name-only --no-renames "$base..HEAD")

# 1) Có file ngoài phạm vi PR1 không?
$extra = @()
foreach ($f in $changed) {
    if (-not $PR1.Contains($f)) { $extra += $f }
}

# 2) Có file PR1 nào chưa vào commit hiện tại không?
$missing = @()
foreach ($p in $PR1) {
    if (-not $changed.Contains($p)) { $missing += $p }
}

Write-Host "Base: $base"
Write-Host "Files changed: $($changed.Count)"

if ($extra.Count -gt 0) {
    Write-Host "`n❌ Có file ngoài phạm vi PR1:" -ForegroundColor Red
    $extra | ForEach-Object { Write-Host "  - $_" }
    exit 1
}

if ($missing.Count -gt 0) {
    Write-Host "`n❌ Thiếu file thuộc PR1 (chưa nằm trong diff HEAD):" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  - $_" }
    exit 1
}

Write-Host "`n✅ Phạm vi PR1 chính xác: chỉ 10 file mong đợi." -ForegroundColor Green
exit 0
