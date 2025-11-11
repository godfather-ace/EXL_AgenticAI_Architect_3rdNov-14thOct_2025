from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

# Configure the client with GEMINI API
client = genai.Client(api_key = os.environ["GEMINI_API_KEY"])

# Define structured output schemas
class Response(BaseModel): 
    handoff: str = Field(default = "", description = "The name/role of the agent to hand off to. Available agents: 'Restaurant Agent', 'Hotel Agent'")
    message: str = Field(description = "The response message to the user or context for the next agent")
    
# Agent function
def run_agent(agent_name: str, system_prompt: str, prompt: str) -> Response:
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt, 
        config = {"system_instruction": f"You are {agent_name}. {system_prompt}", 
                "response_mime_type": "application/json",
                "response_schema": Response
        } 
    )
    return response.parsed

# Define the system prompts for the agents
hotel_system_prompt = """You are a Hotel Booking Agent. 
                    You ONLY handle hotel bookings. 
                    if the user ask about restaurants, flights, or anything else, respond 
                    with a short handoff message containing the original message 
                    and set the 'handoff' field to 'Restaurant Agent'. 
                    Otherwise, handle the hotel request and leave 'handoff' empty.
                    """
restaurant_system_prompt = """You are a Restaurant Booking Agent. 
                        You handle restaurant recommendations and booking 
                        based on the user's request provided in the prompt.
                        """

# Initial prompt (about a restaurant)
initial_prompt = "Can you book me a table at an italian restaurant for 3 people tonight."
print(f"Initial user request: {initial_prompt}")

output = run_agent("Hotel Agent", hotel_system_prompt, initial_prompt)

# Simulate a user interaction to change the prompt and handoff
if output.handoff == "Restaurant Agent":
    print("Handoff Triggered: Hotel to Restaurant")
    output = run_agent("Restaurant Agent", restaurant_system_prompt, initial_prompt)
elif output.handoff == "Hotel Agent":
    print("Handoff Triggered: Restaurant to Hotel")
    output = run_agent("Hotel Agent", hotel_system_prompt, initial_prompt)

print(output.message)

