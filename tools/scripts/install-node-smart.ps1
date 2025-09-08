# Node.js installer thông minh - không cần Chocolatey

param(
    [string]$NodeVersion = "lts",
    [switch]$InstallYarn,
    [switch]$Force
)

Write-Host "🚀 Smart Node.js Installer..." -ForegroundColor Cyan

# Kiểm tra Node.js đã có chưa
$nodeVer = & node -v 2>$null
$npmVer = & npm -v 2>$null

if ($nodeVer -and $npmVer -and -not $Force) {
    Write-Host "✅ Node.js đã có: $nodeVer, npm: $npmVer" -ForegroundColor Green
} else {
    Write-Host "📦 Cài đặt Node.js..." -ForegroundColor Yellow
    
    # Method 1: winget (Windows 10+)
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "🔧 Sử dụng winget..." -ForegroundColor Cyan
        if ($NodeVersion -eq "lts") {
            winget install OpenJS.NodeJS --silent
        } else {
            winget install OpenJS.NodeJS --version $NodeVersion --silent
        }
    }
    # Method 2: nvs (Node Version Switcher)
    elseif (Get-Command nvs -ErrorAction SilentlyContinue) {
        Write-Host "🔧 Sử dụng nvs..." -ForegroundColor Cyan
        nvs install $NodeVersion
        nvs use $NodeVersion
    }
    # Method 3: Manual download
    else {
        Write-Host "📥 Download manual..." -ForegroundColor Yellow
        Write-Host "Chạy: winget install OpenJS.NodeJS" -ForegroundColor White
        Write-Host "Hoặc tải từ: https://nodejs.org/download" -ForegroundColor White
        exit 1
    }
}

# Verify installation
Start-Sleep -Seconds 2
$nodeCheck = & node -v 2>$null
$npmCheck = & npm -v 2>$null

if ($nodeCheck -and $npmCheck) {
    Write-Host "✅ Node.js ready: $nodeCheck, npm: $npmCheck" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js install failed" -ForegroundColor Red
    exit 1
}

# Cài Yarn nếu yêu cầu
if ($InstallYarn) {
    $yarnCheck = & yarn -v 2>$null
    if ($yarnCheck) {
        Write-Host "✅ Yarn đã có: $yarnCheck" -ForegroundColor Green
    } else {
        Write-Host "📦 Cài Yarn..." -ForegroundColor Yellow
        npm install -g yarn --silent
        $yarnVer = & yarn -v 2>$null
        if ($yarnVer) {
            Write-Host "✅ Yarn installed: $yarnVer" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Yarn install có vấn đề" -ForegroundColor Yellow
        }
    }
}

# Cài TypeScript global nếu chưa có
$tscCheck = & tsc -v 2>$null
if (-not $tscCheck) {
    Write-Host "📦 Cài TypeScript..." -ForegroundColor Yellow
    npm install -g typescript @types/node --silent
    Write-Host "✅ TypeScript installed" -ForegroundColor Green
} else {
    Write-Host "✅ TypeScript đã có: $tscCheck" -ForegroundColor Green
}

Write-Host "🎉 Node.js setup hoàn thành!" -ForegroundColor Green
