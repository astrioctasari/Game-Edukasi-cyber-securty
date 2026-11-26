$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
  python -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --name "DetektifSiber-Python" `
    --distpath ".\dist" `
    --workpath ".\build" `
    --add-data "data;data" `
    --add-data "..\reference-web\img;img" `
    native_app.py
  if ($LASTEXITCODE -ne 0) { throw "Build aplikasi native gagal." }

  $iscc = Get-Command ISCC.exe -ErrorAction SilentlyContinue
  $isccPath = if ($iscc) { $iscc.Source } else { "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" }
  if (-not (Test-Path -LiteralPath $isccPath)) {
    throw "Inno Setup compiler tidak ditemukan. Pasang dengan: winget install --id JRSoftware.InnoSetup -e"
  }

  $installerOutput = Join-Path (Split-Path -Parent $PSScriptRoot) "dist\Full Python Native"
  New-Item -ItemType Directory -Force -Path $installerOutput | Out-Null
  & $isccPath .\installer_native.iss
  if ($LASTEXITCODE -ne 0) { throw "Build installer Inno Setup gagal." }

  Write-Host "Native Python app: native-python\dist\DetektifSiber-Python\DetektifSiber-Python.exe"
  Write-Host "Native Python installer: dist\Full Python Native\DetektifSiber-Full-Python-Native-Setup.exe"
}
finally {
  Pop-Location
}
