from google.adk.agents import Agent
from google.cloud import aiplatform
import vertexai
import os
import json
import urllib.parse
from dotenv import load_dotenv
from google.auth import default
from google.auth.transport.requests import Request
import requests

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aiagent-capstoneproject")
DEPLOYED_REGION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

# Your deployed reasoning engine resource name
# Format: projects/{PROJECT_NUMBER}/locations/{REGION}/reasoningEngines/{ENGINE_ID}
REASONING_ENGINE_NAME = "projects/1276251306/locations/us-central1/reasoningEngines/1245962178549252096"

# Project number (different from PROJECT_ID which is the project name)
PROJECT_NUMBER = "1276251306"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=DEPLOYED_REGION)

# Initialize AI Platform
aiplatform.init(project=PROJECT_ID, location=DEPLOYED_REGION)

def get_access_token():
    """Get access token for API calls"""
    credentials, project = default()
    if credentials.requires_scopes:
        credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    if not credentials.valid:
        credentials.refresh(Request())
    return credentials.token

def create_session(resource_name, user_id="user_42"):
    """Create a session for the reasoning engine"""
    access_token = get_access_token()
    api_endpoint = f"https://{DEPLOYED_REGION}-aiplatform.googleapis.com/v1beta1/{resource_name}/sessions"
    
    payload = {
        "user_id": user_id
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print(f"📝 Creating session for user: {user_id}")
    response = requests.post(api_endpoint, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        # Check if it's an operation (async) or direct session response
        operation_name = result.get("name", "")
        
        # Extract session name from operation name
        # Format: projects/.../reasoningEngines/.../sessions/{session_id}/operations/{operation_id}
        if "/operations/" in operation_name:
            # Extract the session part (everything before /operations/)
            session_name = operation_name.split("/operations/")[0]
            print(f"📝 Extracted session name from operation")
        elif "/sessions/" in operation_name:
            # Already a session name, but might have operations suffix
            if "/operations/" in operation_name:
                session_name = operation_name.split("/operations/")[0]
            else:
                session_name = operation_name
        else:
            # Direct session response
            session_name = result.get("name", "")
        
        session_id = session_name.split("/")[-1] if session_name else ""
        print(f"✅ Session created: {session_id}")
        print(f"   Full session name: {session_name}")
        return {"name": session_name, "raw_response": result}
    else:
        raise Exception(f"Failed to create session: {response.status_code} - {response.text}")

def query_reasoning_engine_using_adk(reasoning_engine_name, session_name, message):
    """Query deployed agent - try multiple approaches"""
    # The reasoning engine doesn't have a 'query' method
    # Available methods are session management only
    # We need to use ADK's API server or a different approach
    
    print(f"📤 Querying deployed agent...")
    print(f"   Reasoning Engine: {reasoning_engine_name}")
    print(f"   Session: {session_name}")
    print("-" * 60)
    print("⚠️  Note: Reasoning engines don't have a direct 'query' method.")
    print("   Available methods: session management only")
    print("   Trying alternative approaches...")
    print()
    
    # Try REST API with 'run' method first
    try:
        return query_reasoning_engine_via_run(reasoning_engine_name, session_name, message)
    except Exception as e:
        print(f"⚠️  REST API approach failed: {e}")
        print()
    
    # Alternative: Use ADK's API server endpoint if available
    # The deployed agent might be accessible via ADK's API server
    print("💡 Suggestion: Use ADK's API server or web UI to interact with deployed agents:")
    print("   1. Start ADK API server: adk api_server")
    print("   2. Or use ADK web UI: adk web")
    print("   3. Or use the Agent's run method locally (not deployed)")
    print()
    
    raise Exception(
        "Cannot query deployed reasoning engine directly via REST API.\n"
        "Reasoning engines only expose session management methods, not query methods.\n\n"
        "Options:\n"
        "1. Use ADK's API server: 'adk api_server' then query via HTTP\n"
        "2. Use ADK's web UI: 'adk web' for interactive interface\n"
        "3. Query the agent locally before deployment using Agent.run()\n"
        "4. Check ADK documentation for deployed agent invocation methods"
    )

def query_reasoning_engine_via_run(reasoning_engine_name, session_name, message):
    """Query using the 'run' method endpoint (if available)"""
    access_token = get_access_token()
    session_id = session_name.split("/")[-1] if "/" in session_name else session_name
    
    # Try the 'run' method endpoint instead of 'query'
    api_endpoint = f"https://{DEPLOYED_REGION}-aiplatform.googleapis.com/v1beta1/{reasoning_engine_name}:run"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print(f"📤 Querying via 'run' method...")
    print(f"🔗 Endpoint: {api_endpoint}")
    print("-" * 60)
    
    # Try different payload formats for 'run' method
    payloads = [
        {"input": message, "session_id": session_id},
        {"input": {"message": message}, "session_id": session_id},
        {"message": message, "session_id": session_id},
        {"input": message},
        {"message": message}
    ]
    
    for i, payload in enumerate(payloads, 1):
        print(f"🔗 Trying payload format {i}...")
        response = requests.post(api_endpoint, json=payload, headers=headers)
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            return result
        elif response.status_code != 404:  # 404 means endpoint doesn't exist
            print(f"⚠️  Error: {response.text[:200]}")
    
    # If 'run' doesn't work, the agent might need to be invoked differently
    raise Exception(f"Could not find working endpoint. The reasoning engine doesn't have a 'query' or 'run' method.\nAvailable methods: session management only.\n\nYou may need to use ADK's Agent class or a different invocation method.")

def delete_session(session_name):
    """Delete a session"""
    access_token = get_access_token()
    api_endpoint = f"https://{DEPLOYED_REGION}-aiplatform.googleapis.com/v1beta1/{session_name}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(api_endpoint, headers=headers)
    return response.status_code == 200

def list_reasoning_engines():
    """List all reasoning engines in the project"""
    access_token = get_access_token()
    parent = f"projects/{PROJECT_NUMBER}/locations/{DEPLOYED_REGION}"
    api_endpoint = f"https://{DEPLOYED_REGION}-aiplatform.googleapis.com/v1beta1/{parent}/reasoningEngines"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(api_endpoint, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def main():
    """Connect to deployed agent and query it"""
    try:
        print(f"🔍 Connecting to deployed agent...")
        print(f"   Project: {PROJECT_ID}")
        print(f"   Region: {DEPLOYED_REGION}")
        print(f"   Resource: {REASONING_ENGINE_NAME}")
        print()
        
        # Step 1: Create a session
        print("=" * 60)
        print("Step 1: Creating session...")
        print("=" * 60)
        
        session = create_session(REASONING_ENGINE_NAME, user_id="user_42")
        session_name = session.get("name")
        
        if not session_name:
            raise Exception("Failed to get session name from response")
        
        # Verify session name doesn't contain /operations/
        if "/operations/" in session_name:
            print(f"⚠️  Warning: Session name contains /operations/, cleaning it up...")
            session_name = session_name.split("/operations/")[0]
            print(f"✅ Cleaned session name: {session_name}")
        
        # Step 2: Query using the session
        print("\n" + "=" * 60)
        print("Step 2: Querying deployed agent...")
        print("=" * 60)
        
        response = query_reasoning_engine_using_adk(
            REASONING_ENGINE_NAME,
            session_name,
            "What is the weather in Tokyo?"
        )
        
        print("\n📥 Response from agent:")
        print(json.dumps(response, indent=2))
        
        # Step 3: Clean up - delete session (optional)
        print("\n" + "=" * 60)
        print("Step 3: Cleaning up session...")
        print("=" * 60)
        try:
            delete_session(session_name)
            print("✅ Session deleted")
        except Exception as e:
            print(f"⚠️  Could not delete session: {e}")
        
        # Option 2: List all reasoning engines (optional)
        print("\n" + "=" * 60)
        print("Listing all reasoning engines...")
        print("=" * 60)
        try:
            engines = list_reasoning_engines()
            if "reasoningEngines" in engines:
                print(f"Found {len(engines['reasoningEngines'])} reasoning engine(s):")
                for engine in engines["reasoningEngines"]:
                    print(f"  - {engine.get('name', 'Unknown')}")
                    print(f"    Display Name: {engine.get('displayName', 'N/A')}")
            else:
                print("No reasoning engines found in response")
        except Exception as e:
            print(f"Could not list engines: {e}")
            
    except Exception as e:
        print(f"❌ Error connecting to deployed agent: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Make sure the agent is deployed")
        print("2. Check PROJECT_ID and DEPLOYED_REGION are correct")
        print("3. Verify GOOGLE_APPLICATION_CREDENTIALS is set")
        print("4. Grant required permissions to service account:")
        print("   - aiplatform.sessions.create (to create sessions)")
        print("   - aiplatform.reasoningEngines.query (to query agents)")
        print("   These are included in 'Vertex AI User' role (roles/aiplatform.user)")
        print("5. Verify the resource name is correct")

if __name__ == "__main__":
    main()
