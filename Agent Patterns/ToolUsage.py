from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

# Configure the client with GEMINI API
client = genai.Client(api_key = os.environ["GEMINI_API_KEY"])

# Define the function for the model
weather_function = {
    "name": "get_current_temperature",
    "description": "Determine the current temperature in my location",
    "parameters": {
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": "The city and state e.g. Bengaluru, Karnataka"
            },
        },
    "required": ["location"]
    }
}

# Placeholder function to simulate API call
def get_current_temperature(location: str) -> dict: 
    return {"temperature": "15", "unit": "Celsius"}

# Create the config object
tools = types.Tool(function_declarations = [weather_function])
contents = ["What is the temperature in Mumbai right now"]
response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = contents,
    config = types.GenerateContentConfig(tools = [tools]) 
)

# Process the response
response_part = response.candidates[0].content.parts[0]
if response_part.function_call: 
    function_call = response_part.function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {dict(function_call.args)}")
    if function_call.name == "get_current_temperature":
        api_result = get_current_temperature(*function_call.args)
        # Append function call and result of the function execution to contents
        follow_up_contents = [
            types.Part(function_call = function_call),
            types.Part.from_function_response(
                name = "get_current_temperature",
                response = api_result
            )
        ]
        # Generate the final response
        response_final = client.models.generate_content(
            model = "gemini-2.5-flash", 
            contents = contents + follow_up_contents,
            config = types.GenerateContentConfig(tools = [tools])
        )
        print(response_final.text)
    else: 
        print(f"Error: Unknown function call requested: {function_call.name}")
else: 
    print("No function call foudn in the resonse.")
    print(response.text)