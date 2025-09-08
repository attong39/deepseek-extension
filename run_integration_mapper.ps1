# =====================================
# DeepSeek Extension - Integration Mapper
# PowerShell Advanced Runner
# =====================================

param(
    [string]$ProjectRoot = ".",
    [switch]$JsonOnly,
    [switch]$Preview,
    [switch]$OpenReports,
    [string]$OutputMd = "INTEGRATION_MAP.md",
    [string]$OutputJson = "integration_map.json"
)

Write-Host "🎯 DEEPSEEK EXTENSION - INTEGRATION MAPPER" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Python
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and add it to PATH" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Tạo command arguments
$args = @(
    "integration_mapper.py",
    "--project-root", $ProjectRoot,
    "--output-md", $OutputMd,
    "--output-json", $OutputJson
)

if ($JsonOnly) {
    $args += "--json-only"
}

if ($Preview) {
    $args += "--preview"
}

Write-Host "🔍 Analyzing project integration..." -ForegroundColor Yellow
Write-Host ""

# Chạy integration mapper
try {
    & python @args
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Integration analysis completed successfully!" -ForegroundColor Green
        
        # Mở báo cáo nếu được yêu cầu
        if ($OpenReports -or (-not $JsonOnly)) {
            Write-Host ""
            Write-Host "📊 Opening integration reports..." -ForegroundColor Cyan
            
            if (Test-Path $OutputMd) {
                Write-Host "📄 Opening $OutputMd..." -ForegroundColor Blue
                Start-Process $OutputMd
            }
            
            if (Test-Path $OutputJson) {
                Write-Host "📋 JSON report available: $OutputJson" -ForegroundColor Blue
            }
        }
        
        # Hiển thị summary
        Write-Host ""
        Write-Host "📁 Generated files:" -ForegroundColor Green
        if (Test-Path $OutputMd) {
            $mdSize = (Get-Item $OutputMd).Length
            Write-Host "   ✅ $OutputMd ($([math]::Round($mdSize/1KB, 1)) KB)" -ForegroundColor White
        }
        if (Test-Path $OutputJson) {
            $jsonSize = (Get-Item $OutputJson).Length
            Write-Host "   ✅ $OutputJson ($([math]::Round($jsonSize/1KB, 1)) KB)" -ForegroundColor White
        }
        
        Write-Host ""
        Write-Host "🎯 Integration Points Identified:" -ForegroundColor Cyan
        Write-Host "   • VS Code Commands & Configuration" -ForegroundColor White
        Write-Host "   • Ollama API Integration" -ForegroundColor White
        Write-Host "   • TypeScript Build Flow" -ForegroundColor White
        Write-Host "   • Python AI Assistant Connection" -ForegroundColor White
        Write-Host "   • Dependencies & File Relationships" -ForegroundColor White
        
    } else {
        Write-Host "❌ Integration analysis failed!" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "❌ Error running integration mapper: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🚀 Ready for development! Use the reports to understand:" -ForegroundColor Green
Write-Host "   • File dependencies and relationships" -ForegroundColor White
Write-Host "   • Build and runtime flows" -ForegroundColor White
Write-Host "   • Integration points and critical paths" -ForegroundColor White
Write-Host "   • Issues and optimization opportunities" -ForegroundColor White

if (-not $OpenReports) {
    Write-Host ""
    Write-Host "💡 Tip: Use -OpenReports to automatically open the generated files" -ForegroundColor Yellow
}
