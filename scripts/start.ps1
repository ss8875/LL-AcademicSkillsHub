$ErrorActionPreference = "Stop"
& python (Join-Path $PSScriptRoot "serve.py") @args
