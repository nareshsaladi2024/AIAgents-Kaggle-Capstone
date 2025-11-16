"""Test if the agent can be imported correctly"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from agents.weather_assistant import root_agent
    print("✅ Agent imported successfully")
    print(f"   Agent name: {root_agent.name}")
    print(f"   Agent description: {root_agent.description}")
    print(f"   Agent model: {root_agent.model}")
except Exception as e:
    print(f"❌ Error importing agent: {e}")
    import traceback
    traceback.print_exc()

