# How to Query Your Deployed Agent

## Current Issue: Missing Permission

You need the `aiplatform.sessions.create` permission to create sessions.

**Service Account**: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`

**Grant Permission:**
1. Go to: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject
2. Find the service account
3. Click **Edit** (pencil icon)
4. Add role: **Vertex AI User** (`roles/aiplatform.user`)
5. Click **SAVE**

This role includes:
- ✅ `aiplatform.sessions.create`
- ✅ `aiplatform.sessions.get`
- ✅ `aiplatform.sessions.list`
- ✅ `aiplatform.reasoningEngines.query` (if available)

## The Issue with Query Method

The deployed reasoning engine **does not have a `query` method**. Available methods are:
- `create_session`
- `get_session`
- `list_sessions`
- `delete_session`
- Session memory methods

## Solution: Use ADK's API Server or Web UI

The recommended way to interact with deployed agents is through ADK's API server:

### Option 1: Use ADK API Server

```powershell
# Start the ADK API server (it will connect to your deployed agent)
cd "C:\AI Agents\Day5\sample_agent"
adk api_server --reasoning-engine=projects/1276251306/locations/us-central1/reasoningEngines/1245962178549252096
```

Then query via HTTP:
```powershell
# In another terminal
Invoke-WebRequest -Uri "http://localhost:8000/agents/weather_assistant/run" -Method POST -ContentType "application/json" -Body '{"message": "What is the weather in Tokyo?"}'
```

### Option 2: Use ADK Web UI

```powershell
cd "C:\AI Agents\Day5\sample_agent"
adk web --reasoning-engine=projects/1276251306/locations/us-central1/reasoningEngines/1245962178549252096
```

This opens a web interface where you can interact with your deployed agent.

### Option 3: Use Agent Locally (Not Deployed)

If you want to test the agent locally before deployment:

```python
from sample_agent.agent import root_agent

# Run the agent locally
response = root_agent.run("What is the weather in Tokyo?")
print(response)
```

### Option 4: Check ADK Documentation

The ADK might have specific methods for connecting to deployed reasoning engines. Check:
- ADK documentation
- `adk --help`
- `adk run --help`

## Permission Required

To query deployed agents, your service account needs:
- `aiplatform.sessions.create` - To create sessions
- `aiplatform.reasoningEngines.query` - To query reasoning engines

**Grant these permissions:**
1. Go to: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject
2. Find: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`
3. Click **Edit** (pencil icon)
4. Add role: **Vertex AI User** (`roles/aiplatform.user`)
5. Click **Save**
6. Wait 1-2 minutes for propagation

## Your Deployed Agent Details

- **Resource Name**: `projects/1276251306/locations/us-central1/reasoningEngines/1245962178549252096`
- **Project**: `aiagent-capstoneproject`
- **Region**: `us-central1`
- **Service Account**: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`

