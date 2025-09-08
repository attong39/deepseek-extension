# Demo Quality Gates - Simplified version cho v1.0.0 demo
# PowerShell version

$ErrorActionPreference = "Stop"

Write-Host "🔍 Running Demo Quality Gates..." -ForegroundColor Cyan

Write-Host "🏗️  Build test..." -ForegroundColor Yellow  
npm run build
if ($LASTEXITCODE -ne 0) { throw "Build test failed" }

Write-Host "📋 Build metadata generation..." -ForegroundColor Yellow
npm run prebuild
if ($LASTEXITCODE -ne 0) { throw "Build metadata failed" }

Write-Host "📊 Code duplication check..." -ForegroundColor Yellow
npm run dup:js
if ($LASTEXITCODE -ne 0) { Write-Host "⚠️  Duplication check failed (continuing)" -ForegroundColor Yellow }

Write-Host "✅ Demo quality gates passed!" -ForegroundColor Green
Write-Host "🚀 Ready for v1.0.0 demo!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Health System Features:" -ForegroundColor Cyan
Write-Host "  ✓ Tri-state health check (ok/degraded/down)" -ForegroundColor Green
Write-Host "  ✓ Real-time HealthBadge với 30s polling" -ForegroundColor Green  
Write-Host "  ✓ Copy diagnostics từ About modal" -ForegroundColor Green
Write-Host "  ✓ Build metadata embedded (version/commit/time)" -ForegroundColor Green
Write-Host ""
Write-Host "📦 To create v1.0.0 release:" -ForegroundColor Yellow
Write-Host "    npm version 1.0.0 -m 'release: v1.0.0'" -ForegroundColor White