@echo off
REM ============================================================
REM Iconora Studio - Quick Start Batch Script
REM Windows Easy Setup and Launch
REM ============================================================

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🎨 Iconora Studio - Setup & Launch                   ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Change to project directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.12 from: https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found!
python --version
echo.

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import customtkinter" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Dependencies not found. Installing...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed!
) else (
    echo ✅ Dependencies already installed!
)

echo.
echo 🚀 Starting Iconora Studio...
echo.

python main.py

pause
