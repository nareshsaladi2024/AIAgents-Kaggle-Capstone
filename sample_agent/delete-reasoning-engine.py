"""
Script to delete a reasoning engine and all its sessions.
Usage: python delete-reasoning-engine.py
"""
import os
import requests
from dotenv import load_dotenv
from google.auth import default
from google.auth.transport.requests import Request

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aiagent-capstoneproject")
PROJECT_NUMBER = "1276251306"
DEPLOYED_REGION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
REASONING_ENGINE_ID = "1245962178549252096"
REASONING_ENGINE_NAME = f"projects/{PROJECT_NUMBER}/locations/{DEPLOYED_REGION}/reasoningEngines/{REASONING_ENGINE_ID}"

def get_access_token():
    """Get access token for API calls"""
    credentials, project = default()
    if credentials.requires_scopes:
        credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    if not credentials.valid:
        credentials.refresh(Request())
    return credentials.token

def list_sessions(reasoning_engine_name, access_token):
    """List all sessions for a reasoning engine"""
    api_endpoint = f"https://{DEPLOYED_REGION}-aiplatform.googleapis.com/v1beta1/{reasoning_engine_name}/sessions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        return response.json().get("sessions", [])
    elif response.status_code == 404:
        return []  # No sessions found
    else:
        print(f"⚠️  Warning: Could not list sessions: {response.status_code} - {response.text[:200]}")
        return []

def delete_session(session_name, access_token):
    """Delete a session"""
    api_endpoint = f"https://{DEPLOYED_REGION}-aiplatform.googleapis.com/v1beta1/{session_name}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(api_endpoint, headers=headers)
    return response.status_code == 200

def delete_reasoning_engine(reasoning_engine_name, access_token, force=True):
    """Delete a reasoning engine (with force option to delete child resources)"""
    force_param = "?force=true" if force else ""
    api_endpoint = f"https://{DEPLOYED_REGION}-aiplatform.googleapis.com/v1beta1/{reasoning_engine_name}{force_param}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(api_endpoint, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

def main():
    print(f"🗑️  Deleting Reasoning Engine: {REASONING_ENGINE_NAME}")
    print()
    
    access_token = get_access_token()
    
    # Step 1: List and delete all sessions
    print("=" * 60)
    print("Step 1: Listing and deleting all sessions...")
    print("=" * 60)
    
    sessions = list_sessions(REASONING_ENGINE_NAME, access_token)
    
    if sessions:
        print(f"Found {len(sessions)} session(s). Deleting...")
        for session in sessions:
            session_name = session.get("name")
            if session_name:
                print(f"  Deleting session: {session_name}")
                if delete_session(session_name, access_token):
                    print("    ✅ Deleted")
                else:
                    print("    ⚠️  Failed to delete")
    else:
        print("No sessions found.")
    
    print()
    
    # Step 2: Delete the reasoning engine (with force=true)
    print("=" * 60)
    print("Step 2: Deleting reasoning engine (with force=true)...")
    print("=" * 60)
    
    if delete_reasoning_engine(REASONING_ENGINE_NAME, access_token, force=True):
        print("✅ Reasoning engine deleted successfully!")
    else:
        print("❌ Failed to delete reasoning engine.")
        print()
        print("Alternative: Use gcloud CLI:")
        print(f"  gcloud ai reasoning-engines delete {REASONING_ENGINE_ID} --region={DEPLOYED_REGION} --project={PROJECT_ID} --force")

if __name__ == "__main__":
    main()


