# Requires -Version 5.1
param(
    [string]$Model = "deepseek-r1:latest",
    [string]$ExtDir = "E:\zeta\deepseek-extension",
    [switch]$DevHost,      # nếu muốn mở VS Code Dev Host thay vì cài .vsix
    [switch]$QuickReview   # gọi review file đang mở ngay
)

function Test-Port11434 {
    try { (Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 2).StatusCode -eq 200 } 
    catch { $false }
}

Write-Host "=== 1) Start Ollama service" -ForegroundColor Cyan
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden | Out-Null
Start-Sleep -Seconds 3

Write-Host "=== 2) Pull model ($Model)" -ForegroundColor Cyan
& ollama pull $Model

Write-Host "=== 3) Sanity‑check REST (generate ping)" -ForegroundColor Cyan
$payload = @{ model = $Model; prompt = "ping"; stream = $false } | ConvertTo-Json
Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/generate" -Method POST -ContentType "application/json" -Body $payload | Out-Null

Write-Host "=== 4) Build VS Code extension" -ForegroundColor Cyan
Push-Location $ExtDir
if (-not (Test-Path package.json)) { Write-Error "Không thấy package.json"; exit 1 }

npm install
# khắc phục thiếu scripts nhanh
npm pkg set scripts.compile="tsc -p ."
npm pkg set scripts.watch="tsc -p . -w"
npm pkg set scripts.lint="eslint . --ext .ts"
npm run compile

Write-Host "=== 5) Launch extension" -ForegroundColor Cyan
if ($DevHost) {
    code .
    Write-Host "=> Nhấn F5 (Debug Extension)" -ForegroundColor Yellow
}
else {
    # auto‑install .vsix nếu có
    $vsix = Get-ChildItem -Path $ExtDir -Filter *.vsix -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($vsix) { code --install-extension $vsix.FullName }
    code .
}

Write-Host "=== 6) Run AI Agent (optional)" -ForegroundColor Cyan
if ($QuickReview) {
    code --reuse-window --command deepseek.agent.reviewActiveFile
    Write-Host "=> Đã gọi: deepseek.agent.reviewActiveFile" -ForegroundColor Green
}

Pop-Location
Write-Host "✅ DONE." -ForegroundColor Green
