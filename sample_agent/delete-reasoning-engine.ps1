# Script to delete a reasoning engine and its sessions
# Usage: .\delete-reasoning-engine.ps1

# Load environment variables
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\AI Agents\Day5\sample_agent\adk-agent-service-key.json"

# Configuration
$PROJECT_ID = "aiagent-capstoneproject"
$PROJECT_NUMBER = "1276251306"
$DEPLOYED_REGION = "us-central1"
$REASONING_ENGINE_ID = "1245962178549252096"
$REASONING_ENGINE_NAME = "projects/$PROJECT_NUMBER/locations/$DEPLOYED_REGION/reasoningEngines/$REASONING_ENGINE_ID"

Write-Host "🗑️  Deleting Reasoning Engine: $REASONING_ENGINE_NAME" -ForegroundColor Yellow
Write-Host ""

# Step 1: List and delete all sessions
Write-Host "Step 1: Listing all sessions..." -ForegroundColor Cyan
$accessToken = python -c "from google.auth import default; from google.auth.transport.requests import Request; creds, _ = default(); creds.refresh(Request()); print(creds.token)"

$listSessionsUrl = "https://$DEPLOYED_REGION-aiplatform.googleapis.com/v1beta1/$REASONING_ENGINE_NAME/sessions"
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

try {
    $sessionsResponse = Invoke-RestMethod -Uri $listSessionsUrl -Method Get -Headers $headers
    $sessions = $sessionsResponse.sessions
    
    if ($sessions -and $sessions.Count -gt 0) {
        Write-Host "Found $($sessions.Count) session(s). Deleting..." -ForegroundColor Yellow
        
        foreach ($session in $sessions) {
            $sessionName = $session.name
            Write-Host "  Deleting session: $sessionName" -ForegroundColor Gray
            
            $deleteSessionUrl = "https://$DEPLOYED_REGION-aiplatform.googleapis.com/v1beta1/$sessionName"
            try {
                Invoke-RestMethod -Uri $deleteSessionUrl -Method Delete -Headers $headers | Out-Null
                Write-Host "    ✅ Deleted" -ForegroundColor Green
            } catch {
                Write-Host "    ⚠️  Error: $_" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "No sessions found." -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Could not list sessions: $_" -ForegroundColor Yellow
    Write-Host "   Continuing with force delete..." -ForegroundColor Yellow
}

Write-Host ""

# Step 2: Delete the reasoning engine (with force=true to delete any remaining sessions)
Write-Host "Step 2: Deleting reasoning engine (with force=true)..." -ForegroundColor Cyan

$deleteEngineUrl = "https://$DEPLOYED_REGION-aiplatform.googleapis.com/v1beta1/$REASONING_ENGINE_NAME?force=true"
try {
    Invoke-RestMethod -Uri $deleteEngineUrl -Method Delete -Headers $headers | Out-Null
    Write-Host "✅ Reasoning engine deleted successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error deleting reasoning engine: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Use gcloud CLI:" -ForegroundColor Yellow
    Write-Host "  gcloud ai reasoning-engines delete $REASONING_ENGINE_ID --region=$DEPLOYED_REGION --project=$PROJECT_ID --force" -ForegroundColor Gray
}


