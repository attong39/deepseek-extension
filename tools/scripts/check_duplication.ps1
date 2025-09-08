# Kiểm tra trùng lặp code toàn repo (PowerShell)
# Tương đương check_duplication.sh

$ErrorActionPreference = 'Stop'
$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Đảm bảo desktop_ai_zeta đã cài deps nếu có package.json
$desktopPath = Join-Path $rootDir 'desktop_ai_zeta'
$packageJson = Join-Path $desktopPath 'package.json'
if (Test-Path $packageJson) {
    Write-Host 'Đang chạy npm ci cho desktop_ai_zeta...'
    Push-Location $desktopPath
    npm ci
    Pop-Location
}

# Chạy jscpd với các ignore tương đương
$npxArgs = @(
    'jscpd',
    '--min-lines', '20',
    '--threshold', '0',
    '--reporters', 'console',
    '--ignore', '**/node_modules/**',
    '--ignore', '**/.venv/**',
    '--ignore', '**/.pytest_cache/**',
    '--ignore', '**/__pycache__/**',
    '--ignore', '**/build/**',
    '--ignore', '**/dist/**',
    '--ignore', '**/desktop_ai_zeta/src/api/generated/**',
    $rootDir
)
Write-Host 'Đang chạy kiểm tra trùng lặp toàn repo...'
npx @npxArgs
