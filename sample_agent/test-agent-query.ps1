# PowerShell script to test querying the agent via ADK API Server
# Make sure the API server is running first (run query-via-adk-api.ps1)

$message = "What is the weather in Tokyo?"

if ($args.Count -gt 0) {
    $message = $args[0]
}

Write-Host "Querying deployed agent..." -ForegroundColor Green
Write-Host "   Message: $message" -ForegroundColor Cyan
Write-Host ""

$body = @{
    message = $message
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/agents/weather_assistant/run" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Response received:" -ForegroundColor Green
    Write-Host ""
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error querying agent:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure the ADK API server is running:" -ForegroundColor Yellow
    Write-Host "   .\query-via-adk-api.ps1" -ForegroundColor Cyan
}

