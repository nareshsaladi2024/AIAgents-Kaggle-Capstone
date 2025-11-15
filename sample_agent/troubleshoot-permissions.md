# Troubleshooting Permission Issues

## Current Error
```
403 PERMISSION_DENIED: Permission 'aiplatform.reasoningEngines.create' denied
```

## Possible Causes & Solutions

### 1. IAM Changes Haven't Propagated Yet
**Wait Time**: IAM changes can take 1-5 minutes to propagate
- **Solution**: Wait 5 minutes and try again

### 2. Wrong Role Assigned
**Check**: Verify the role includes `aiplatform.reasoningEngines.create`

**Roles that include this permission:**
- ✅ `roles/aiplatform.user` - **RECOMMENDED**
- ✅ `roles/aiplatform.serviceAgent`
- ✅ `roles/aiplatform.admin` - Full access

**Roles that DON'T include it:**
- ❌ `roles/aiplatform.viewer` - Read-only
- ❌ Custom roles without the permission

### 3. Verify Role Assignment in Console

1. Go to: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject
2. Find: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`
3. Check the **Roles** column - you should see:
   - `Vertex AI User` (roles/aiplatform.user)
   - OR `Vertex AI Service Agent` (roles/aiplatform.serviceAgent)
   - OR `Vertex AI Admin` (roles/aiplatform.admin)

### 4. Check if Custom Role Was Created Correctly

If you created a custom role:
1. Go to: https://console.cloud.google.com/iam-admin/roles?project=aiagent-capstoneproject
2. Find your custom role
3. Click on it
4. Verify it includes: `aiplatform.reasoningEngines.create`
5. If missing, edit the role and add the permission

### 5. Service Account Impersonation

The deployment might be using your user credentials instead of the service account.

**Check your .env file:**
```env
GOOGLE_APPLICATION_CREDENTIALS=aiagent-capstoneproject-10beb4eeaf31.json
```

**Verify the service account key is being used:**
- The key file should be in the same directory as `.env`
- Or use absolute path: `C:\AI Agents\Day5\sample_agent\aiagent-capstoneproject-10beb4eeaf31.json`

### 6. Organization Policies

If this is an organization project, there might be organization policies blocking the permission.

**Check**: Go to IAM & Admin → Organization Policies
- Look for policies that restrict Vertex AI permissions

### 7. Try Granting Multiple Roles

Sometimes you need multiple roles. Try granting:
1. `roles/aiplatform.user`
2. `roles/aiplatform.serviceAgent`
3. `roles/serviceusage.serviceUsageConsumer` (if needed)

## Step-by-Step Verification

1. **Verify Role Assignment:**
   - Console → IAM → Find service account
   - Confirm role is listed

2. **Wait 5 minutes** for propagation

3. **Verify Service Account Key:**
   - Check `.env` file has correct path
   - Verify key file exists

4. **Try deployment again**

5. **If still failing, try:**
   - Grant `roles/aiplatform.admin` (temporary, for testing)
   - If that works, then narrow down to specific permissions

## Quick Test Command

After granting permissions, test with:
```powershell
cd "C:\AI Agents\Day5"
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\AI Agents\Day5\sample_agent\aiagent-capstoneproject-10beb4eeaf31.json"
$env:PROJECT_ID = "aiagent-capstoneproject"
$env:DEPLOYED_REGION = "us-central1"
.\.venv\Scripts\adk.exe deploy agent_engine --project=$env:PROJECT_ID --region=$env:DEPLOYED_REGION sample_agent --agent_engine_config_file=sample_agent\.agent_engine_config.json
```

