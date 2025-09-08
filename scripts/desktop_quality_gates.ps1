# Quality Gates Script - Kiểm tra chất lượng trước khi release
# PowerShell version

$ErrorActionPreference = "Stop"

Write-Host "🔍 Running Quality Gates for Release..." -ForegroundColor Cyan

Write-Host "📝 TypeScript type check..." -ForegroundColor Yellow
npm run ts:check
if ($LASTEXITCODE -ne 0) { throw "TypeScript check failed" }

Write-Host "🏗️  Build test..." -ForegroundColor Yellow  
npm run build
if ($LASTEXITCODE -ne 0) { throw "Build test failed" }

Write-Host "🧪 Running unit tests..." -ForegroundColor Yellow
npm run test:unit
if ($LASTEXITCODE -ne 0) { throw "Unit tests failed" }

Write-Host "💨 Running smoke tests..." -ForegroundColor Yellow
npm run test:smoke
if ($LASTEXITCODE -ne 0) { throw "Smoke tests failed" }

Write-Host "📋 Contract validation..." -ForegroundColor Yellow
npm run contract:guard
if ($LASTEXITCODE -ne 0) { throw "Contract validation failed" }

Write-Host "📊 Code duplication check..." -ForegroundColor Yellow
npm run dup:js
if ($LASTEXITCODE -ne 0) { throw "Duplication check failed" }

Write-Host "🔗 API schema sync check..." -ForegroundColor Yellow
npm run api:gen
if ($LASTEXITCODE -ne 0) { throw "API generation failed" }

# Check if git has changes in generated files
$gitStatus = git status --porcelain src/api/generated/ 2>$null
if ($gitStatus) {
    Write-Host "❌ API schema is out of sync. Run 'npm run api:gen' and commit changes." -ForegroundColor Red
    exit 1
}

Write-Host "✅ All quality gates passed!" -ForegroundColor Green
Write-Host "🚀 Ready for release!" -ForegroundColor Green