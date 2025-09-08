#!/usr/bin/env pwsh
# Auto-fix: deps & virtualenv (Windows PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "▶ Auto-fix: deps & virtualenv (Windows)" -ForegroundColor Cyan

# 1) Sửa _virtualenv.pth + tạo venv bằng uv
Write-Host "→ Repairing environment..." -ForegroundColor Yellow
uv run python scripts/fix/repair_env.py --apply

# 2) Đồng bộ apps/backend (nếu có)
Write-Host "→ Syncing apps/backend dependencies..." -ForegroundColor Yellow
if (Test-Path "zeta_vn_restructured") { 
    Push-Location zeta_vn_restructured
    uv sync
    Pop-Location
}
elseif (Test-Path "zeta_vn") { 
    Push-Location zeta_vn
    uv sync
    Pop-Location
}

# 3) Cài tối thiểu cho Deepseek Agent (an toàn, idempotent)
Write-Host "→ Installing essential packages..." -ForegroundColor Yellow
try {
    uv add typer==0.12.5 rich requests --dev
}
catch {
    Write-Host "Warning: Failed to add some packages, continuing..." -ForegroundColor Yellow
}

# 4) Desktop deps (nếu có)
if (Test-Path "apps/desktop") {
    Write-Host "→ Installing apps/desktop dependencies..." -ForegroundColor Yellow
    Push-Location apps/desktop
    try {
        npm ci 2>$null
        if ($LASTEXITCODE -ne 0) { 
            npm i --include=dev 
        }
    }
    catch {
        Write-Host "Warning: npm install failed, continuing..." -ForegroundColor Yellow
    }
    Pop-Location
}

# 5) Kiểm tra nhanh
Write-Host "→ Verifying stack..." -ForegroundColor Yellow
uv run python scripts/fix/verify_stack.py

Write-Host "✔ Done! Gợi ý: uv run python -m deepseek agent --apply" -ForegroundColor Green
