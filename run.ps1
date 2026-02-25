# ============================================================
# Iconora Studio - Quick Start PowerShell Script
# Windows Easy Setup and Launch
# ============================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🎨 Iconora Studio - Setup & Launch                   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.12 from: https://www.python.org" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow

# Check if dependencies are installed
try {
    python -c "import customtkinter" 2>$null
    Write-Host "✅ Dependencies already installed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Dependencies not found. Installing..." -ForegroundColor Yellow
    Write-Host ""
    pip install -r requirements.txt

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "🚀 Starting Iconora Studio..." -ForegroundColor Cyan
Write-Host ""

python main.py

Read-Host "Press Enter to exit"
