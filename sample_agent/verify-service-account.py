"""
Script to verify which service account is being used and check its permissions.
"""
import os
import json
from google.auth import default
from google.auth.transport.requests import Request

def get_service_account_email():
    """Get the service account email from credentials."""
    try:
        # Check if GOOGLE_APPLICATION_CREDENTIALS is set
        creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if creds_path:
            print(f"📁 Using credentials from: {creds_path}")
            if os.path.exists(creds_path):
                with open(creds_path, 'r') as f:
                    creds_data = json.load(f)
                    email = creds_data.get('client_email', 'Not found')
                    print(f"✅ Service Account Email: {email}")
                    return email
            else:
                print(f"❌ File not found: {creds_path}")
        else:
            print("⚠️  GOOGLE_APPLICATION_CREDENTIALS not set")
        
        # Try to get from default credentials
        print("\n🔍 Trying to get credentials from default...")
        credentials, project = default()
        if hasattr(credentials, 'service_account_email'):
            email = credentials.service_account_email
            print(f"✅ Service Account Email: {email}")
            return email
        else:
            print("ℹ️  Using user credentials (not service account)")
            print(f"   Project: {project}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("Service Account Verification")
    print("=" * 60)
    print()
    
    email = get_service_account_email()
    
    if email:
        print()
        print("=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print(f"1. Go to: https://console.cloud.google.com/iam-admin/iam?project=aiagent-capstoneproject")
        print(f"2. Find this service account: {email}")
        print(f"3. Click Edit (pencil icon)")
        print(f"4. Add role: Vertex AI User (roles/aiplatform.user)")
        print(f"5. Click Save")
        print(f"6. Wait 1-2 minutes for propagation")
        print()
    else:
        print()
        print("=" * 60)
        print("Authentication Setup:")
        print("=" * 60)
        print("Set GOOGLE_APPLICATION_CREDENTIALS to your service account key:")
        print('  $env:GOOGLE_APPLICATION_CREDENTIALS = "path\\to\\your-key.json"')
        print()

if __name__ == "__main__":
    main()

