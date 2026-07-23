$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.10 or newer is required."
}

$Version = & python -c "import sys; print('%d.%d' % sys.version_info[:2])"
$Parts = $Version.Split(".")
if ([int]$Parts[0] -lt 3 -or ([int]$Parts[0] -eq 3 -and [int]$Parts[1] -lt 10)) {
    throw "Python 3.10 or newer is required; found $Version."
}

$EnvTarget = Join-Path $ProjectRoot ".env"
$EnvExample = Join-Path $ProjectRoot ".env.example"
if (-not (Test-Path -LiteralPath $EnvTarget)) {
    Copy-Item -LiteralPath $EnvExample -Destination $EnvTarget
}

& python (Join-Path $PSScriptRoot "build_catalog.py")
& python (Join-Path $PSScriptRoot "validate_repo.py")
& python (Join-Path $PSScriptRoot "doctor.py")
Write-Host "Setup complete. Run .\scripts\start.ps1"
