# run_proxy.ps1
# Start CLay proxy setting PYTHONPATH to the parent folder of this script so the
# `CLay` package is importable regardless of the current working directory.

# This script lives at: <...>\CLay\run_proxy.ps1
# It will set PYTHONPATH to the parent folder (the folder that contains `CLay`).

param(
	[string]$ConfigPath = "config.json"
)

$scriptFolder = Split-Path -Parent $MyInvocation.MyCommand.Definition
$parentOfScript = Split-Path -Parent $scriptFolder
Write-Host "Setting PYTHONPATH to: $parentOfScript"
$env:PYTHONPATH = $parentOfScript

# Run from the script folder so relative config paths (like ./config.json) resolve
Push-Location $scriptFolder
try {
	if ($ConfigPath -ne "config.json") {
		# If absolute path passed, use it; otherwise use relative to script folder
		if (-not (Test-Path $ConfigPath)) {
			$candidate = Join-Path $scriptFolder $ConfigPath
			if (Test-Path $candidate) { $ConfigPath = $candidate }
		}
	} else {
		# ensure config.json in script folder if exists
		$candidate = Join-Path $scriptFolder 'config.json'
		if (Test-Path $candidate) { $ConfigPath = 'config.json' }
	}

	Write-Host "Using config: $ConfigPath"
	python -m CLay.main -c $ConfigPath
}
finally {
	Pop-Location
}
