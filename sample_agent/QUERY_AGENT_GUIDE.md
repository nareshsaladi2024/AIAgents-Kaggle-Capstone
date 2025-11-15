# How to Query Your Deployed Agent

## ✅ Success: Session Creation Works!

Your session was successfully created, which means:
- ✅ Permissions are correctly configured
- ✅ Service account authentication is working
- ✅ Connection to deployed reasoning engine is successful

## The Challenge: Direct REST API Query

The deployed reasoning engine **does not expose a direct REST API query endpoint**. This is by design - reasoning engines use session management, not direct query methods.

## Solution: Use ADK's API Server or Web UI

### Option 1: ADK API Server (Recommended for Programmatic Access)

**Step 1: Start the API Server**

```powershell
cd "C:\AI Agents\Day5\sample_agent"
.\query-via-adk-api.ps1
```

This will:
- Set up authentication automatically
- Start the API server on `http://localhost:8000`
- Connect to your deployed reasoning engine

**Step 2: Query the Agent (in another terminal)**

```powershell
cd "C:\AI Agents\Day5\sample_agent"
.\test-agent-query.ps1 "What is the weather in Tokyo?"
```

Or manually:
```powershell
$body = @{ message = "What is the weather in Tokyo?" } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/agents/weather_assistant/run" `
  -Method POST -ContentType "application/json" -Body $body
```

### Option 2: ADK Web UI (Easiest - Interactive)

```powershell
cd "C:\AI Agents\Day5\sample_agent"
.\query-via-adk-web.ps1
```

This will:
- Open a web interface in your browser
- Allow you to interact with your agent visually
- Handle all authentication automatically

### Option 3: Use Agent Locally (For Testing)

If you want to test the agent logic without the deployed version:

```python
from sample_agent.agent import root_agent

response = root_agent.run("What is the weather in Tokyo?")
print(response)
```

## Understanding the Architecture

```
Your Code → ADK API Server → Deployed Reasoning Engine → Agent Response
```

The ADK API server acts as a bridge between your code and the deployed reasoning engine, handling:
- Session management
- Authentication
- Request/response formatting
- Error handling

## Troubleshooting

### If API Server Fails to Start

1. **Check authentication:**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "aiagent-capstoneproject-10beb4eeaf31.json"
   ```

2. **Verify agent structure:**
   - Ensure `agent.py` exists
- Ensure `__init__.py` exists

3. **Check ADK version:**
   ```powershell
   adk --version
   ```

### If Query Returns 404

- Make sure the API server is running
- Check the agent name matches: `weather_assistant`
- Verify the endpoint: `http://localhost:8000/agents/weather_assistant/run`

### If Query Returns 403

- Verify service account has `Vertex AI User` role
- Check `GOOGLE_APPLICATION_CREDENTIALS` is set correctly
- Wait 2-5 minutes after granting permissions

## Next Steps

1. **Start with Web UI** (easiest): `.\query-via-adk-web.ps1`
2. **Use API Server** for programmatic access: `.\query-via-adk-api.ps1`
3. **Integrate into your application** using the API server endpoints

## Your Deployed Agent Details

- **Resource Name**: `projects/1276251306/locations/us-central1/reasoningEngines/1245962178549252096`
- **Agent Name**: `weather_assistant`
- **Project**: `aiagent-capstoneproject`
- **Region**: `us-central1`

