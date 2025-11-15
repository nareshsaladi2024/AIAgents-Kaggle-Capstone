# PowerShell script to query deployed agent using ADK Web UI

# Navigate to the script directory
Set-Location $PSScriptRoot

# Set the service account credentials
$env:GOOGLE_APPLICATION_CREDENTIALS = "aiagent-capstoneproject-10beb4eeaf31.json"

# Your deployed reasoning engine resource name or ID
# Can use full name or just the ID
$REASONING_ENGINE = "projects/1276251306/locations/us-central1/reasoningEngines/1245962178549252096"
# Or just the ID: $REASONING_ENGINE = "1245962178549252096"

Write-Host "🌐 Starting ADK Web UI..." -ForegroundColor Green
Write-Host "   Reasoning Engine: $REASONING_ENGINE" -ForegroundColor Cyan
Write-Host "   Agent Directory: ." -ForegroundColor Cyan
Write-Host ""
Write-Host "The web UI will open in your browser at http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the ADK web UI
# Format: agentengine://<agent_engine>
# The agent_engine can be full resource name or just the ID
# ADK expects AGENTS_DIR where each subdirectory is an agent
# We use 'agents' directory which contains 'weather_assistant' subdirectory
adk web --session_service_uri="agentengine://$REASONING_ENGINE" --port=8000 agents

