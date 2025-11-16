"""Verify that your credentials have the right OAuth scopes"""
import os
from google.auth import default
from google.auth.transport.requests import Request

def check_credentials():
    print("Checking credentials and OAuth scopes...")
    print("=" * 60)
    
    # Check if using service account key
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path:
        print(f"Using service account key: {creds_path}")
        if os.path.exists(creds_path):
            print("  Key file exists")
        else:
            print("  WARNING: Key file not found!")
    else:
        print("Using Application Default Credentials (ADC)")
        print("  (No GOOGLE_APPLICATION_CREDENTIALS set)")
    
    print()
    
    try:
        # Get credentials
        credentials, project = default()
        
        # Refresh to get access token with scopes
        if credentials.requires_scopes:
            print("Credentials require scopes, requesting cloud-platform scope...")
            credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
        
        if not credentials.valid:
            print("Refreshing credentials...")
            credentials.refresh(Request())
        
        # Get token info
        token = credentials.token
        print(f"Access token obtained: {token[:20]}...")
        print()
        
        # Check scopes (if available in token info)
        if hasattr(credentials, 'scopes') and credentials.scopes:
            print("OAuth Scopes:")
            for scope in credentials.scopes:
                print(f"  - {scope}")
        else:
            print("Note: Scope information not available in credentials object")
            print("  (This is normal for service account keys)")
        
        print()
        print("Project:", project or "Not set")
        print()
        print("Credentials appear to be valid!")
        print("If you still get scope errors, try Option 1 from FIX_OAUTH_SCOPES.md")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Troubleshooting:")
        print("1. Make sure GOOGLE_APPLICATION_CREDENTIALS points to a valid key file")
        print("2. Or run: gcloud auth application-default login")
        print("3. Check FIX_OAUTH_SCOPES.md for more solutions")

if __name__ == "__main__":
    check_credentials()

