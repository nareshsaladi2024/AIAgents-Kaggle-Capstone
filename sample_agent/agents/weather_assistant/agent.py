from google.adk.agents import Agent
import vertexai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Try multiple paths to find .env file
env_paths = [
    os.path.join(os.path.dirname(__file__), '..', '..', '.env'),  # sample_agent/.env
    os.path.join(os.path.dirname(__file__), '..', '.env'),       # agents/.env
    os.path.join(os.path.dirname(__file__), '.env'),             # weather_assistant/.env
]

for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        break
else:
    # If no .env file found, try loading from current directory
    load_dotenv()

# Get project and location from environment variables with defaults
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aiagent-capstoneproject")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

# Ensure environment variables are set (ADK may need these)
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", PROJECT_ID)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", LOCATION)
# Critical: Tell ADK to use Vertex AI instead of Google AI Studio
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")

# Initialize Vertex AI with credentials from environment variables
# Google Cloud SDK will automatically use Application Default Credentials (ADC)
# which can be set via:
# 1. GOOGLE_APPLICATION_CREDENTIALS pointing to a service account JSON file
# 2. gcloud auth application-default login
# 3. Or running on GCP with default service account

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)

def get_weather(city: str) -> dict:
    """
    Returns weather information for a given city.

    This is a TOOL that the agent can call when users ask about weather.
    In production, this would call a real weather API (e.g., OpenWeatherMap).
    For this demo, we use mock data.

    Args:
        city: Name of the city (e.g., "Tokyo", "New York")

    Returns:
        dict: Dictionary with status and weather report or error message
    """
    # Mock weather database with structured responses
    weather_data = {
        "san francisco": {"status": "success", "report": "The weather in San Francisco is sunny with a temperature of 72°F (22°C)."},
        "new york": {"status": "success", "report": "The weather in New York is cloudy with a temperature of 65°F (18°C)."},
        "london": {"status": "success", "report": "The weather in London is rainy with a temperature of 58°F (14°C)."},
        "tokyo": {"status": "success", "report": "The weather in Tokyo is clear with a temperature of 70°F (21°C)."},
        "paris": {"status": "success", "report": "The weather in Paris is partly cloudy with a temperature of 68°F (20°C)."}
    }

    city_lower = city.lower()
    if city_lower in weather_data:
        return weather_data[city_lower]
    else:
        available_cities = ", ".join([c.title() for c in weather_data.keys()])
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available. Try: {available_cities}"
        }

root_agent = Agent(
    name="weather_assistant",
    model="gemini-2.5-flash-lite",  # Fast, cost-effective Gemini model
    description="A helpful weather assistant that provides weather information for cities.",
    instruction="""
    You are a friendly weather assistant. When users ask about the weather:

    1. Identify the city name from their question
    2. Use the get_weather tool to fetch current weather information
    3. Respond in a friendly, conversational tone
    4. If the city isn't available, suggest one of the available cities

    Be helpful and concise in your responses.
    """,
    tools=[get_weather]
)