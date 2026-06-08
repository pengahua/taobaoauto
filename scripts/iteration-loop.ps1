$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"

function Ensure-Backend {
  try {
    Invoke-WebRequest -UseBasicParsing "http://localhost:8000/api/health" -TimeoutSec 3 | Out-Null
    return
  } catch {
    Write-Host "[loop] starting backend"
  }

  $python = (Get-Command python).Source
  Start-Process -WindowStyle Hidden -FilePath $python -ArgumentList @(
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
  ) -WorkingDirectory $Backend
  Start-Sleep -Seconds 5
}

function Ensure-Frontend {
  try {
    Invoke-WebRequest -UseBasicParsing "http://localhost:5173" -TimeoutSec 3 | Out-Null
    return
  } catch {
    Write-Host "[loop] starting frontend"
  }

  Start-Process -WindowStyle Hidden -FilePath "C:\Program Files\nodejs\npm.cmd" -ArgumentList @(
    "run",
    "dev",
    "--",
    "--port",
    "5173"
  ) -WorkingDirectory $Frontend
  Start-Sleep -Seconds 5
}

Ensure-Backend
Ensure-Frontend

& (Join-Path $PSScriptRoot "qa-smoke.ps1")

Write-Host "[loop] git status"
Push-Location $Root
git status --short
Pop-Location

