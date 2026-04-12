$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

$pythonExe = "python"
$venv313Python = Join-Path $scriptDir ".venv313\Scripts\python.exe"
$venvPython = Join-Path $scriptDir ".venv\Scripts\python.exe"
if (Test-Path $venv313Python) {
    $pythonExe = $venv313Python
} elseif (Test-Path $venvPython) {
    $pythonExe = $venvPython
}

Write-Host "Building frontend bundle..."
Push-Location frontend
npm run build
$frontendExit = $LASTEXITCODE
Pop-Location
if ($frontendExit -ne 0) {
    Write-Host "Frontend build failed." -ForegroundColor Red
    exit 1
}

$frontendDist = Join-Path $scriptDir "frontend\\dist"
$backendStatic = Join-Path $scriptDir "backend\\static"
if (Test-Path $backendStatic) {
    Remove-Item -Recurse -Force $backendStatic
}
Copy-Item -Recurse -Force $frontendDist $backendStatic

Write-Host "Building desktop shell..."
& $pythonExe scripts/build_desktop.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Desktop build failed." -ForegroundColor Red
    exit 1
}

Write-Host "Build successful." -ForegroundColor Green
