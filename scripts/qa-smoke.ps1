$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"

Write-Host "[qa] backend tests"
Push-Location $Backend
python -m pytest tests
Pop-Location

Write-Host "[qa] frontend build"
Push-Location $Frontend
npm run build
Pop-Location

Write-Host "[qa] backend health"
$health = Invoke-WebRequest -UseBasicParsing "http://localhost:8000/api/health" -TimeoutSec 10
if ($health.StatusCode -ne 200) {
  throw "Backend health check failed"
}

Write-Host "[qa] dashboard summary"
$dashboard = Invoke-WebRequest -UseBasicParsing "http://localhost:8000/api/dashboard/summary" -TimeoutSec 10
if ($dashboard.StatusCode -ne 200) {
  throw "Dashboard summary check failed"
}

Write-Host "[qa] risk kill switches"
$risk = Invoke-WebRequest -UseBasicParsing "http://localhost:8000/api/risk/kill-switches" -TimeoutSec 10
if ($risk.StatusCode -ne 200) {
  throw "Risk kill switch check failed"
}

Write-Host "[qa] passed"
