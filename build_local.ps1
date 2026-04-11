# Iconora Studio - Local Build Script
# This PowerShell script rebuilds the application including UI and core packages.

$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# ensure Python available
Write-Host "Checking for Python..."
try {
    python --version | Out-Null
} catch {
    Write-Host "Python is not installed or not on PATH." -ForegroundColor Red
    exit 1
}

# ensure PyInstaller installed
try {
    python -c "import PyInstaller" 2>$null
} catch {
    Write-Host "Installing PyInstaller..."
    pip install pyinstaller
}

# cleanup old outputs
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue

# run PyInstaller build
python -m PyInstaller `
    --onefile `
    --windowed `
    --name="Iconora Studio" `
    --icon=assets/icons/app.ico `
    --add-data="assets;assets" `
    --add-data="ui;ui" `
    --add-data="core;core" `
    --collect-all=customtkinter `
    --collect-all=PIL `
    --hidden-import=customtkinter `
    --hidden-import=PIL `
    --hidden-import=tkinterdnd2 `
    --hidden-import=cairosvg `
    --hidden-import=rembg `
    --exclude-module=onnxruntime `
    --clean `
    --noconfirm `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful! Executable at dist\Iconora Studio.exe" -ForegroundColor Green
} else {
    Write-Host "Build failed." -ForegroundColor Red
}

Read-Host "Press Enter to exit"
