<#
start-dev.ps1

Opens two PowerShell windows and starts the proxy and the dashboard for development.
Usage: Right-click -> Run with PowerShell or execute from an elevated/non-elevated PowerShell.
#>

# Resolve project root (script lives in project root)
$projectRoot = Split-Path -Path $MyInvocation.MyCommand.Path -Parent

Write-Host "Opening Proxy window..."
$proxyCmd = "Set-Location -LiteralPath '$projectRoot'; .\ .venv\Scripts\Activate.ps1; `$env:PYTHONPATH = '$projectRoot'; .\ .venv\Scripts\python.exe -m CLay.main -c `"$projectRoot\config.json`""
Start-Process -FilePath powershell -ArgumentList '-NoExit', '-Command', $proxyCmd

Start-Sleep -Milliseconds 300
Write-Host "Opening Dashboard window..."
$dashCmd = "Set-Location -LiteralPath '$projectRoot\dashboard'; .\ .venv\Scripts\Activate.ps1; python app.py"
Start-Process -FilePath powershell -ArgumentList '-NoExit', '-Command', $dashCmd

Write-Host "Started proxy and dashboard in two new windows. Close them with Ctrl+C when finished." -ForegroundColor Green
