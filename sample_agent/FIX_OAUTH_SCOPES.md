# Fix: Insufficient OAuth Scopes Error

## Error Message
```
403 PERMISSION_DENIED. Request had insufficient authentication scopes.
ACCESS_TOKEN_SCOPE_INSUFFICIENT
```

## Problem
Your service account key doesn't have the required OAuth scopes for Vertex AI operations.

## Solution Options

### Option 1: Use Application Default Credentials (Recommended)

Instead of using a service account key file, use `gcloud` authentication:

```powershell
# Authenticate with your Google account
gcloud auth application-default login

# This will open a browser for you to sign in
# Make sure you're signed in with an account that has the right permissions
```

Then deploy without setting `GOOGLE_APPLICATION_CREDENTIALS`:

```powershell
cd "C:\AI Agents\Day5\sample_agent"

# Don't set GOOGLE_APPLICATION_CREDENTIALS - use ADC instead
# $env:GOOGLE_APPLICATION_CREDENTIALS = "..."  # Don't set this

# Deploy
adk deploy --config .agent_engine_config.json
```

### Option 2: Re-download Service Account Key with Proper Scopes

1. Go to Google Cloud Console: https://console.cloud.google.com/iam-admin/serviceaccounts?project=aiagent-capstoneproject

2. Find your service account: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`

3. Click on the service account

4. Go to **Keys** tab

5. Click **Add Key** → **Create new key**

6. Select **JSON** format

7. Download the key

8. Replace your existing key file with the new one

9. Make sure the key has these scopes (they should be included by default):
   - `https://www.googleapis.com/auth/cloud-platform`

### Option 3: Use gcloud with Service Account Impersonation

If you have the right permissions, you can impersonate the service account:

```powershell
# Authenticate as yourself first
gcloud auth login

# Then impersonate the service account for ADC
gcloud auth application-default login --impersonate-service-account=adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com
```

## Verify Your Credentials

Run this to check your current credentials:

```powershell
python verify-credentials-scopes.py
```

## Why This Happens

Service account keys created through the console should have the right scopes by default. However:
- Keys created programmatically might not include all scopes
- Keys created for specific purposes might have limited scopes
- User credentials (from `gcloud auth login`) have different scopes than service accounts

## Recommended Approach

**Use Application Default Credentials (Option 1)** - it's the most reliable and handles scopes automatically.

