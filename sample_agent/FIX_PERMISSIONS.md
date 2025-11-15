# Fix Permission Error: aiplatform.sessions.create

## Current Error

```
Permission 'aiplatform.sessions.create' denied on resource
```

## Quick Fix (5 minutes)

### Step 1: Go to IAM & Admin

**Direct Link**: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject

### Step 2: Find Your Service Account

Look for: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`

### Step 3: Edit Permissions

1. Click the **Edit** button (pencil icon) next to the service account
2. Click **ADD ANOTHER ROLE**
3. Select: **Vertex AI User** (`roles/aiplatform.user`)
4. Click **SAVE**

### Step 4: Wait for Propagation

Wait **1-2 minutes** for IAM changes to propagate.

### Step 5: Test Again

**IMPORTANT**: You must set `GOOGLE_APPLICATION_CREDENTIALS` before running the script!

**Option 1: Use the helper script (Recommended)**
```powershell
cd "C:\AI Agents\Day5\sample_agent"
.\run-retrieveAgent.ps1
```

**Option 2: Set environment variable manually**
```powershell
cd "C:\AI Agents\Day5\sample_agent"
$env:GOOGLE_APPLICATION_CREDENTIALS = "aiagent-capstoneproject-10beb4eeaf31.json"
python retrieveAgent.py
```

**⚠️ Without setting `GOOGLE_APPLICATION_CREDENTIALS`, the script will use your user credentials from a different project, which won't have the required permissions!**

## What This Role Includes

The `roles/aiplatform.user` role provides:
- ✅ `aiplatform.sessions.create` - Create sessions
- ✅ `aiplatform.sessions.get` - Get session info
- ✅ `aiplatform.sessions.list` - List sessions
- ✅ `aiplatform.reasoningEngines.query` - Query reasoning engines
- ✅ Other necessary Vertex AI permissions

## Alternative: Grant Specific Permission

If you prefer to grant only the specific permission (not recommended):

1. Go to: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject
2. Click **Edit** on your service account
3. Click **ADD ANOTHER ROLE**
4. Type: `aiplatform.sessions.create`
5. Select the custom role or use the predefined role

**Note**: Using `roles/aiplatform.user` is recommended as it includes all necessary permissions.

## Verify Permissions

After granting, you can verify at:
https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject

The service account should show:
- **Vertex AI User** (`roles/aiplatform.user`)

## Still Having Issues?

1. **Double-check the service account name**: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`
2. **Wait longer**: IAM changes can take up to 5 minutes
3. **Check project**: Make sure you're in the correct project (`aiagent-capstoneproject`)
4. **Verify credentials**: Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to the correct service account key

