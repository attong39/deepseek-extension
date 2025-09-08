#!/usr/bin/env pwsh
# ZETA AI Monorepo Setup Script

Write-Host " Setting up ZETA AI Monorepo..." -ForegroundColor Green

# Check prerequisites
Write-Host " Checking prerequisites..." -ForegroundColor Blue

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "   Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "   Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "   Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Poetry
try {
    $poetryVersion = poetry --version
    Write-Host "   Poetry: $poetryVersion" -ForegroundColor Green
} catch {
    Write-Host "   Poetry not found. Installing..." -ForegroundColor Yellow
    pip install poetry
}

# Install dependencies
Write-Host " Installing dependencies..." -ForegroundColor Blue

# Install root dependencies
Write-Host "   Installing root dependencies..." -ForegroundColor Cyan
npm install

# Install apps/backend dependencies  
Write-Host "   Installing apps/backend dependencies..." -ForegroundColor Cyan
cd apps/backend
poetry install --with dev,ai
cd ..

# Install extension dependencies
Write-Host "   Installing extension dependencies..." -ForegroundColor Cyan
cd extension
npm install
cd ..

# Install apps/desktop dependencies
Write-Host "    Installing apps/desktop dependencies..." -ForegroundColor Cyan
cd apps/desktop  
npm install
cd ..

# Setup pre-commit hooks
Write-Host " Setting up pre-commit hooks..." -ForegroundColor Blue
cd apps/backend
poetry run pre-commit install
cd ..

Write-Host " Setup completed successfully!" -ForegroundColor Green
Write-Host " Next steps:" -ForegroundColor Yellow
Write-Host "  1. npm run dev          # Start all services" -ForegroundColor White
Write-Host "  2. npm run test         # Run all tests" -ForegroundColor White
Write-Host "  3. npm run build        # Build all projects" -ForegroundColor White
