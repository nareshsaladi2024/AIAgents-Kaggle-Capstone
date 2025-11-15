# PowerShell script to run retrieveAgent.py with correct credentials

# Navigate to the script directory
Set-Location $PSScriptRoot

# Set the service account credentials
$env:GOOGLE_APPLICATION_CREDENTIALS = "aiagent-capstoneproject-10beb4eeaf31.json"

# Verify the file exists
if (-not (Test-Path $env:GOOGLE_APPLICATION_CREDENTIALS)) {
    Write-Host "❌ Error: Service account key file not found: $env:GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor Red
    Write-Host "   Make sure the file exists in the current directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Using service account: $env:GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor Green
Write-Host ""

# Run the script
python retrieveAgent.py

