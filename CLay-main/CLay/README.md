CLay — quick run & dashboard instructions

This README explains how to run CLay (proxy) and the dashboard so the dashboard reads the same attacker log entries the proxy produces.

Prerequisites
- Python 3.8+ (you used Python 3.13 in this environment)
- Install dependencies (prefer a virtual environment)

Install (recommended, PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the proxy
- The repository contains a nested package layout. Use the helper that sets PYTHONPATH so the package imports resolve.

From the project root (one level above the inner `CLay-main` folder):

```powershell
$env:PYTHONPATH = '.\\CLay-main'
python -m CLay.main -c config.json
```

Or run interactively from the inner `CLay` folder and then start the module with PYTHONPATH as shown above.

Trigger attacks (another terminal)

```powershell
Invoke-WebRequest -Uri http://localhost:5000 -Headers @{ 'User-Agent'='sqlmap/1.6'; 'X-Forwarded-For'='45.155.205.233' }
```

Run the dashboard

```powershell
cd .\\CLay-main\\CLay\\dashboard
python app.py
# open http://localhost:8080 in your browser
```

Notes
- The dashboard reads `logs/attackers.log`. The dashboard has been updated to search common locations under the project so it should find the file regardless of where you started the proxy.
- If you prefer, use the included PowerShell helpers to start each service.
