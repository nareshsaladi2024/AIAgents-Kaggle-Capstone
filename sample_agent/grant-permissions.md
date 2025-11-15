# Grant aiplatform.reasoningEngines.create Permission

## Method 1: Using Google Cloud Console (Recommended)

### Step 1: Navigate to IAM
1. Go to: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject
2. Or: Google Cloud Console → IAM & Admin → IAM

### Step 2: Find Your Service Account
1. Search for: `adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com`
2. Click the **Edit** (pencil icon) next to the service account

### Step 3: Grant Permission
**Option A: Grant a Role (Easiest)**
- Click **ADD ANOTHER ROLE**
- Select one of these roles (they include the permission):
  - **Vertex AI User** (`roles/aiplatform.user`)
  - **Vertex AI Service Agent** (`roles/aiplatform.serviceAgent`)
  - **Vertex AI Admin** (`roles/aiplatform.admin`) - Full access
- Click **SAVE**

### Step 4: Wait for Propagation
- IAM changes can take 1-2 minutes to propagate
- Try the deployment again after a minute

---

## Method 2: Using gcloud CLI (Command Line)

If you have gcloud CLI installed, run:

```bash
# Grant Vertex AI User role (includes reasoningEngines.create)
gcloud projects add-iam-policy-binding aiagent-capstoneproject \
    --member="serviceAccount:adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Or grant Vertex AI Service Agent role
gcloud projects add-iam-policy-binding aiagent-capstoneproject \
    --member="serviceAccount:adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com" \
    --role="roles/aiplatform.serviceAgent"
```

---

## Method 3: Create Custom Role (Advanced)

If you want ONLY the specific permission:

1. Go to: https://console.cloud.google.com/iam-admin/roles?project=aiagent-capstoneproject
2. Click **CREATE ROLE**
3. Set:
   - **Role name**: `reasoningEnginesCreator`
   - **Role ID**: `reasoningEnginesCreator`
   - **Description**: Custom role for creating reasoning engines
4. Click **ADD PERMISSIONS**
5. Search for: `aiplatform.reasoningEngines.create`
6. Check the box and click **ADD**
7. Click **CREATE**
8. Then assign this custom role to your service account in IAM

---

## Verify Permissions

After granting, verify with:

```bash
gcloud projects get-iam-policy aiagent-capstoneproject \
    --flatten="bindings[].members" \
    --filter="bindings.members:adk-agent-service@aiagent-capstoneproject.iam.gserviceaccount.com"
```

