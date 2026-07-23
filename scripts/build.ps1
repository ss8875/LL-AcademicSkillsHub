$ErrorActionPreference = "Stop"
& python (Join-Path $PSScriptRoot "build_catalog.py")
& python (Join-Path $PSScriptRoot "validate_repo.py")
& python -m unittest discover -s (Join-Path (Split-Path -Parent $PSScriptRoot) "tests") -v
& python (Join-Path $PSScriptRoot "package_release.py")
