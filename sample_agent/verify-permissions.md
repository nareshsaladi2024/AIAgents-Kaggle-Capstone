# Verify Permissions - Step by Step

## Issue: Still getting 403 after adding custom role

The `roles/aiplatform.user` role **DOES include** `aiplatform.reasoningEngines.create`.

## Verification Steps

### 1. Check What Role Was Actually Assigned

Go to: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject

1. Find: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`
2. Look at the **Roles** column
3. **What role do you see?**
   - If you see a **custom role name** (not "Vertex AI User"), that's the problem
   - Custom roles need to explicitly include the permission

### 2. If You Created a Custom Role

**Problem**: Custom roles only have the permissions you explicitly added.

**Solution**: 
1. Go to: https://console.cloud.google.com/iam-admin/roles?project=aiagent-capstoneproject
2. Find your custom role
3. Click **EDIT**
4. Click **ADD PERMISSIONS**
5. Search for: `aiplatform.reasoningEngines.create`
6. Check the box and click **ADD**
7. Click **SAVE**

### 3. Use the Standard Role Instead (Recommended)

**Remove the custom role** and use the standard role:

1. Go to IAM: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject
2. Find your service account
3. Click **Edit** (pencil icon)
4. **Remove** the custom role (click X)
5. Click **ADD ANOTHER ROLE**
6. Select: **Vertex AI User** (`roles/aiplatform.user`)
7. Click **SAVE**

### 4. Wait for Propagation

- IAM changes can take **5-10 minutes** to fully propagate
- Wait 10 minutes after making changes
- Try the deployment again

### 5. Verify Service Account Key is Being Used

The deployment should use the service account key, not your user credentials.

**Check your .env file has:**
```
GOOGLE_APPLICATION_CREDENTIALS=C:\AI Agents\Day5\sample_agent\aiagent-capstoneproject-10beb4eeaf31.json
```

**Or set it explicitly before deployment:**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\AI Agents\Day5\sample_agent\aiagent-capstoneproject-10beb4eeaf31.json"
```

### 6. Try Granting Multiple Roles

Sometimes you need multiple roles. Try granting both:
- `roles/aiplatform.user`
- `roles/aiplatform.serviceAgent`

## Quick Fix: Use Standard Role

**Best solution**: Remove any custom roles and use the standard `roles/aiplatform.user` role.

This role includes:
- ✅ `aiplatform.reasoningEngines.create`
- ✅ `aiplatform.reasoningEngines.get`
- ✅ `aiplatform.reasoningEngines.list`
- ✅ `aiplatform.reasoningEngines.update`
- ✅ `aiplatform.reasoningEngines.delete`
- ✅ All other Vertex AI permissions needed

## After Making Changes

1. Wait **10 minutes** for IAM propagation
2. Set the environment variable:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\AI Agents\Day5\sample_agent\aiagent-capstoneproject-10beb4eeaf31.json"
   ```
3. Try deployment again

