<#
.SYNOPSIS
    Tạo branch git mới (local) và commit các file được chỉ định.

.DESCRIPTION
    Script này giúp tự động hóa bước tạo branch và commit local sau khi đã chạy format/fix.
    - Không push remote.
    - Kiểm tra git có sẵn.
    - Hiển thị trạng thái trước khi commit.

.EXAMPLE
    .\scripts\git_create_branch_and_commit.ps1

.EXAMPLE
    .\scripts\git_create_branch_and_commit.ps1 -BranchName "fix/foo" -Files @("scripts/check_duplicates.py","docs/JSC_PD_NEXT_STEPS.md")
#>

param(
    [string] $BranchName = "fix/dup-check-jscpd-diagnostics",
    [string[]] $Files = @("scripts/check_duplicates.py", "docs/JSC_PD_NEXT_STEPS.md"),
    [string] $Message = "chore: improve jscpd diagnostics + docs (auto ruff fixes applied)"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-GitAvailable {
    try {
        git --version | Out-Null
        return $true
    }
    catch {
        Write-Error "git not found in PATH. Install git or run from an environment where git is available."
        return $false
    }
}

if (-not (Test-GitAvailable)) { exit 2 }

Write-Host "Repository root: $(Resolve-Path .)"

Write-Host "Git status (porcelain):"
git status --porcelain

try {
    # Create or switch to branch
    $exists = $false
    try { git rev-parse --verify $BranchName > $null 2>&1; $exists = $true } catch { $exists = $false }
    if ($exists) {
        Write-Host "Switching to existing branch: $BranchName"
        git switch $BranchName
    }
    else {
        Write-Host "Creating and switching to branch: $BranchName"
        git switch -c $BranchName
    }

    # Stage files (only those that exist)
    $toAdd = @()
    foreach ($f in $Files) {
        if (Test-Path $f) {
            $toAdd += $f
        }
        else {
            Write-Warning "File not found, skipping: $f"
        }
    }

    if ($toAdd.Count -eq 0) {
        Write-Error "No files to add. Exiting."
        exit 3
    }

    Write-Host "Staging files: $($toAdd -join ", ")"
    git add -- $toAdd

    # Commit
    Write-Host "Committing: $Message"
    git commit -m $Message

    Write-Host "Commit created on branch $BranchName"
    git --no-pager log -1 --name-only
}
catch {
    Write-Error "Failed to create branch or commit: $_"
    exit 1
}

Write-Host "Done. To push branch run: git push --set-upstream origin $BranchName"
