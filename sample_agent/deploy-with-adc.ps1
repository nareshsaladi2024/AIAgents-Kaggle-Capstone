# PowerShell script to deploy using Application Default Credentials (ADC)
# This avoids OAuth scope issues

# Navigate to the script directory
Set-Location $PSScriptRoot

Write-Host "Deploying agent using Application Default Credentials..." -ForegroundColor Green
Write-Host ""

# Unset GOOGLE_APPLICATION_CREDENTIALS to force use of ADC
if ($env:GOOGLE_APPLICATION_CREDENTIALS) {
    Write-Host "Note: GOOGLE_APPLICATION_CREDENTIALS is set, but we'll use ADC instead" -ForegroundColor Yellow
    Write-Host "  (ADC has better scope handling)" -ForegroundColor Yellow
    Write-Host ""
    # Don't unset it - ADK will prefer ADC if available
}

# Check if user is authenticated
Write-Host "Checking authentication..." -ForegroundColor Cyan
$authCheck = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>&1
if ($LASTEXITCODE -ne 0 -or -not $authCheck) {
    Write-Host "WARNING: No active gcloud authentication found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run one of these first:" -ForegroundColor Yellow
    Write-Host "  gcloud auth application-default login" -ForegroundColor Cyan
    Write-Host "  OR" -ForegroundColor Yellow
    Write-Host "  gcloud auth login" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "Active account: $authCheck" -ForegroundColor Green
Write-Host ""

# Load environment variables from .env if it exists
if (Test-Path ".env") {
    Write-Host "Loading environment variables from .env..." -ForegroundColor Cyan
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
            Write-Host "  Set $key" -ForegroundColor Gray
        }
    }
    Write-Host ""
}

Write-Host "Deploying agent..." -ForegroundColor Green
Write-Host ""

# Deploy using ADK
# ADK will use Application Default Credentials automatically
adk deploy --config .agent_engine_config.json

