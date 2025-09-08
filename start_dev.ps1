# 🚀 Zeta AI Agent - Development Launcher
# Quick start script for local development

param(
    [string]$Mode = "full",
    [switch]$Setup,
    [switch]$Help
)

# Color functions for better output
function Write-Header {
    param([string]$Text)
    Write-Host "`n$('='*60)" -ForegroundColor Cyan
    Write-Host "🎯 $Text" -ForegroundColor Yellow
    Write-Host "$('='*60)" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠️ $Text" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Text)
    Write-Host "❌ $Text" -ForegroundColor Red
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ️ $Text" -ForegroundColor Blue
}

function Show-Help {
    Write-Header "Zeta AI Agent - Development Launcher Help"
    
    Write-Host @"
USAGE:
    .\start_dev.ps1 [MODE] [OPTIONS]

MODES:
    full        Start full development environment (default)
    server      Start only the FastAPI development server
    extension   Start only VS Code extension development
    apps/desktop     Start only Electron apps/desktop app development
    test        Run all tests

OPTIONS:
    -Setup      Run initial development setup first
    -Help       Show this help message

EXAMPLES:
    .\start_dev.ps1                    # Start full development environment
    .\start_dev.ps1 server             # Start only the server
    .\start_dev.ps1 -Setup             # Run setup then start full environment
    .\start_dev.ps1 test               # Run all tests
    .\start_dev.ps1 -Help              # Show this help

DEVELOPMENT ENDPOINTS:
    🏠 Server:     http://127.0.0.1:9100
    💚 Health:     http://127.0.0.1:9100/health
    📊 Dev Info:   http://127.0.0.1:9100/dev
    📈 Metrics:    http://127.0.0.1:9100/metrics

VS CODE INTEGRATION:
    • Press F5 to start debugging
    • Use Ctrl+Shift+P → "Tasks: Run Task"
    • Select "🚀 Full Stack Development"
"@
}

function Test-Prerequisites {
    Write-Header "Checking Prerequisites"
    
    $missing = @()
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python: $pythonVersion"
        }
        else {
            $missing += "Python 3.11+"
        }
    }
    catch {
        $missing += "Python 3.11+"
    }
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Node.js: $nodeVersion"
        }
        else {
            $missing += "Node.js 18+"
        }
    }
    catch {
        $missing += "Node.js 18+"
    }
    
    # Check npm
    try {
        $npmVersion = npm --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "npm: v$npmVersion"
        }
        else {
            $missing += "npm"
        }
    }
    catch {
        $missing += "npm"
    }
    
    if ($missing.Count -gt 0) {
        Write-Error "Missing prerequisites: $($missing -join ', ')"
        Write-Info "Please install the missing prerequisites and try again."
        return $false
    }
    
    return $true
}

function Test-Environment {
    Write-Header "Checking Development Environment"
    
    # Check virtual environment
    if (Test-Path ".venv") {
        Write-Success "Python virtual environment exists"
    }
    else {
        Write-Warning "Python virtual environment not found"
        return $false
    }
    
    # Check VS Code configuration
    if (Test-Path ".vscode") {
        Write-Success "VS Code configuration exists"
    }
    else {
        Write-Warning "VS Code configuration not found"
    }
    
    # Check development server
    if (Test-Path "apps/zeta-ai-agent\dev_server.py") {
        Write-Success "Development server exists"
    }
    else {
        Write-Warning "Development server not found"
        return $false
    }
    
    # Check dependencies
    if (Test-Path "apps/zeta-ai-agent\requirements-dev.txt") {
        Write-Success "Development requirements found"
    }
    else {
        Write-Warning "Development requirements not found"
    }
    
    return $true
}

function Start-Server {
    Write-Header "Starting FastAPI Development Server"
    
    # Activate virtual environment and start server
    Write-Info "Activating Python virtual environment..."
    
    $env:VIRTUAL_ENV = "$PWD\.venv"
    $env:PATH = "$PWD\.venv\Scripts;$env:PATH"
    
    Write-Info "Starting development server at http://127.0.0.1:9100"
    Write-Info "Press Ctrl+C to stop the server"
    
    & ".venv\Scripts\python.exe" "apps/zeta-ai-agent\dev_server.py"
}

function Start-FullEnvironment {
    Write-Header "Starting Full Development Environment"
    
    # Check if VS Code is available
    try {
        code --version 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "VS Code detected, opening workspace..."
            
            # Open VS Code with the workspace
            code .
            
            Write-Info @"
🚀 VS Code opened! Next steps:

1. Press F5 to start debugging
2. Or use Ctrl+Shift+P → 'Tasks: Run Task' → '🚀 Full Stack Development'
3. Set breakpoints and debug your code!

Development endpoints:
• Server: http://127.0.0.1:9100
• Health: http://127.0.0.1:9100/health
• Dev Info: http://127.0.0.1:9100/dev
"@
        }
        else {
            Write-Warning "VS Code not found, starting server only..."
            Start-Server
        }
    }
    catch {
        Write-Warning "VS Code not found, starting server only..."
        Start-Server
    }
}

function Start-ExtensionDev {
    Write-Header "Starting VS Code Extension Development"
    
    Write-Info "Building extension..."
    Set-Location "extension"
    npm run compile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Extension built successfully"
        Write-Info "Starting extension development..."
        
        # Open VS Code for extension development
        code . --extensionDevelopmentPath="$PWD"
        
        Write-Info @"
🔌 Extension development started!

• Extension Development Host window should open
• Set breakpoints in TypeScript files
• Press F5 in the Extension Development Host to reload
"@
    }
    else {
        Write-Error "Failed to build extension"
    }
    
    Set-Location ".."
}

function Start-DesktopDev {
    Write-Header "Starting Desktop App Development"
    
    Write-Info "Building apps/desktop app..."
    Set-Location "apps/desktop"
    npm run build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Desktop app built successfully"
        Write-Info "Starting apps/desktop development..."
        npm run dev
    }
    else {
        Write-Error "Failed to build apps/desktop app"
    }
    
    Set-Location ".."
}

function Start-Tests {
    Write-Header "Running All Tests"
    
    # Python tests
    Write-Info "Running Python tests..."
    & ".venv\Scripts\python.exe" -m pytest
    
    # Extension tests
    if (Test-Path "extension") {
        Write-Info "Running extension tests..."
        Set-Location "extension"
        npm test
        Set-Location ".."
    }
    
    # Desktop tests
    if (Test-Path "apps/desktop") {
        Write-Info "Running apps/desktop app tests..."
        Set-Location "apps/desktop"
        npm test
        Set-Location ".."
    }
    
    Write-Success "All tests completed"
}

function Main {
    # Show help if requested
    if ($Help) {
        Show-Help
        return
    }
    
    Write-Header "Zeta AI Agent - Development Environment"
    Write-Info "Mode: $Mode"
    
    # Check prerequisites
    if (-not (Test-Prerequisites)) {
        return
    }
    
    # Run setup if requested
    if ($Setup) {
        Write-Info "Running development setup..."
        python setup_dev.py
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Setup failed. Please check the output above."
            return
        }
    }
    
    # Check environment
    if (-not (Test-Environment)) {
        Write-Warning "Environment not ready. Run with -Setup flag to initialize."
        Write-Info "Example: .\start_dev.ps1 -Setup"
        return
    }
    
    # Start based on mode
    switch ($Mode.ToLower()) {
        "full" { Start-FullEnvironment }
        "server" { Start-Server }
        "extension" { Start-ExtensionDev }
        "apps/desktop" { Start-DesktopDev }
        "test" { Start-Tests }
        default {
            Write-Error "Unknown mode: $Mode"
            Write-Info "Valid modes: full, server, extension, apps/desktop, test"
            Write-Info "Use -Help for more information"
        }
    }
}

# Run main function
Main
