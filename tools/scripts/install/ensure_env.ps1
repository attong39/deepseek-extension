#!/usr/bin/env pwsh
param([switch]$WithNode = $false)

Write-Host "==> Ensuring Python tools via uv..." -ForegroundColor Cyan
try {
    uv pip install `
        "ruff>=0.4,<1" `
        "mypy>=1.10,<2" `
        "bandit>=1.7,<2" `
        "pytest>=8,<9" `
        "coverage>=7.5,<8" `
        "requests>=2.31,<3" `
        "httpx>=0.27,<0.28" `
        "pydantic>=2.6,<3" `
        "watchdog>=3,<5" `
        "autoflake>=2.2,<3" `
        "pycln>=2.4,<3" `
        "psutil>=5.9,<6" `
        "uvicorn>=0.30,<1" --quiet
    Write-Host "✔ Python toolchain OK" -ForegroundColor Green
}
catch {
    Write-Error "Failed to install Python tools: $_"
    exit 1
}

if ($WithNode) {
    Write-Host "==> Ensuring Node tools (dev deps)..." -ForegroundColor Cyan
    
    # Check if Node.js is available
    npm -v >$null 2>&1
    if ($LASTEXITCODE -ne 0) { 
        Write-Error "Node.js chưa có. Cài Node rồi chạy lại -WithNode"
        exit 1 
    }
    
    # Install local dev dependencies with specific versions
    try {
        npm install --no-audit --no-fund -D `
            "typescript@^5.4" `
            "eslint@^9" `
            "prettier@^3" `
            "vitest@^1" `
            "ts-node@^10" `
            "ts-prune@^0.10" `
            "jscpd@^3.5" `
            "openapi-typescript@^6.7" >$null
        Write-Host "✔ Node dev deps OK" -ForegroundColor Green
    }
    catch {
        Write-Warning "Node tools installation failed: $_"
    }
}
else {
    Write-Host "⚠ Bỏ qua Node dev deps (các bước TS sẽ skip). Dùng -WithNode để cài." -ForegroundColor Yellow
}

Write-Host "✔ Environment setup complete!" -ForegroundColor Green
