# Install Node.js và dependencies

param(
  [string]$NodeVersion = "lts",
  [switch]$InstallYarn
)

Write-Host "🚀 Cài đặt Node.js..." -ForegroundColor Cyan

# Cài Node.js
if ($NodeVersion -eq "lts") {
  choco install nodejs-lts -y
} else {
  choco install nodejs --version $NodeVersion -y  
}

# Kiểm tra
$nodeVer = & node -v 2>$null
$npmVer = & npm -v 2>$null

if ($nodeVer -and $npmVer) {
  Write-Host "✅ Node.js: $nodeVer, npm: $npmVer" -ForegroundColor Green
} else {
  Write-Host "❌ Node.js không cài được" -ForegroundColor Red
  exit 1
}

# Cài Yarn (tùy chọn)
if ($InstallYarn) {
  npm install -g yarn
  $yarnVer = & yarn -v 2>$null
  Write-Host "✅ Yarn: $yarnVer" -ForegroundColor Green
}

# Cài TypeScript global
npm install -g typescript @types/node

Write-Host "🎉 Hoàn thành cài đặt Node.js!" -ForegroundColor Green
