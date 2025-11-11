from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import enum

load_dotenv()

# Configure the client with GEMINI API
client = genai.Client(api_key = os.environ["GEMINI_API_KEY"])

# Define the routing schema
class Category(enum.Enum):
    WEATHER = "weather"
    SCIENCE = "science"
    UNKNOWN = "unknown"
    
class RoutingDecision(BaseModel): 
    category: Category
    reasoning: str
    
# Step 1: Route the query
#user_query = "What is the weather in Bengaluru, India?"
#user_query = "What is the idea behind Quantum Physics?"
user_query = "Who is the lead cast in The Witcher series on Netflix?"

prompt_router = f"""
Analyze the user query below and determine its category.
Categories: 
- weather: For questions about weather conditions. 
- science: For questions about science.
- unknown: If the category is unclear. 

Query: {user_query}
"""

# Use client.models.generate_content with config for structured output
response_router = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = prompt_router, 
    config = {
        "response_mime_type": "application/json",
        "response_schema": RoutingDecision
    }
)

# Step 2: Handoff based-on routing decision
final_response = ""
if response_router.parsed.category == Category.WEATHER:
    weather_prompt = f"Provide a brief weather forecast for the mentioned location in: '{user_query}'"
    weather_response = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = weather_prompt, 
    )
    final_response = weather_response.text
elif response_router.parsed.category == Category.SCIENCE:
    science_response = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = user_query, 
    )
    final_response = science_response.text
else: 
    unknown_response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = f"The user query is: {prompt_router}, but could not be answered. Here is the reasoning: {response_router.parsed.reasoning}."
    )
    final_response = unknown_response.text

print(f"\nFinal Response: {final_response}")