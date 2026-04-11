# Helper to build Inno Setup installer for Iconora Studio
# Requires Inno Setup Compiler (ISCC.exe) installed. Default path used below.
$defaultISCC = 'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'
# check environment variable only if set and valid
if ($env:ISCC -and (Test-Path $env:ISCC)) {
    $iscc = $env:ISCC
} elseif (Test-Path $defaultISCC) {
    $iscc = $defaultISCC
} else {
    # try to locate via PATH using Get-Command or where.exe
    $cmd = Get-Command iscc -ErrorAction SilentlyContinue
    if ($cmd) {
        $iscc = $cmd.Source
    } else {
        $where = & where.exe iscc 2>$null | Select-Object -First 1
        if ($where) { $iscc = $where }
        else { $iscc = $null }
    }
}

if (-not $iscc) {
  Write-Error "ISCC.exe not found. Install Inno Setup and ensure ISCC is on PATH or set ISCC env var."
  exit 1
}

# 1. Rebuild the application first
Write-Output "Building the application executable (.exe)..."
$python = "python"
# Try to find python in PATH
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
    $python = "py"
    if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
        Write-Error "Python not found. Please ensure Python is installed and on PATH."
        exit 1
    }
}

$buildScript = Join-Path $PSScriptRoot '..\build_exe.py'
& $python "$buildScript"
if ($LASTEXITCODE -ne 0) {
  Write-Error "Application build failed."
  exit $LASTEXITCODE
}

$script = Join-Path $PSScriptRoot 'Iconora-Studio.iss'
if (-not (Test-Path $script)) { Write-Error "Installer script not found: $script"; exit 1 }

# Ensure dist exists
$distFile = Join-Path $PSScriptRoot '..\dist\Iconora Studio\Iconora Studio.exe' | Resolve-Path -ErrorAction SilentlyContinue
if (-not $distFile) { Write-Error "dist\Iconora Studio\Iconora Studio.exe not found. Build the app first."; exit 1 }

# Run ISCC
Write-Output "Using ISCC: $iscc"
Write-Output "Building installer from: $script"
& "$iscc" "$script"

if ($LASTEXITCODE -ne 0) { Write-Error "ISCC exited with code $LASTEXITCODE"; exit $LASTEXITCODE }
Write-Output "Installer build finished. Check output .exe in the current directory (OutputBaseFilename)."
