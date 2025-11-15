# PowerShell script to query deployed agent using ADK API Server

# Navigate to the script directory
Set-Location $PSScriptRoot

# Set the service account credentials
$env:GOOGLE_APPLICATION_CREDENTIALS = "aiagent-capstoneproject-10beb4eeaf31.json"

# Your deployed reasoning engine resource name or ID
# Can use full name or just the ID
$REASONING_ENGINE = "projects/1276251306/locations/us-central1/reasoningEngines/1245962178549252096"
# Or just the ID: $REASONING_ENGINE = "1245962178549252096"

Write-Host "🚀 Starting ADK API Server..." -ForegroundColor Green
Write-Host "   Reasoning Engine: $REASONING_ENGINE" -ForegroundColor Cyan
Write-Host "   Agent Directory: ." -ForegroundColor Cyan
Write-Host ""
Write-Host "The API server will start on http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "Once started, you can query the agent from another terminal:" -ForegroundColor Yellow
Write-Host '  .\test-agent-query.ps1 "What is the weather in Tokyo?"' -ForegroundColor Cyan
Write-Host ""
Write-Host "Or manually:" -ForegroundColor Yellow
Write-Host '  Invoke-WebRequest -Uri "http://localhost:8000/agents/weather_assistant/run" \' -ForegroundColor Cyan
Write-Host '    -Method POST -ContentType "application/json" \' -ForegroundColor Cyan
Write-Host '    -Body ''{"message": "What is the weather in Tokyo?"}''' -ForegroundColor Cyan
Write-Host ""

# Start the ADK API server
# Format: agentengine://<agent_engine>
# The agent_engine can be full resource name or just the ID
# ADK expects AGENTS_DIR where each subdirectory is an agent
# We use 'agents' directory which contains 'weather_assistant' subdirectory
adk api_server --session_service_uri="agentengine://$REASONING_ENGINE" --port=8000 agents

