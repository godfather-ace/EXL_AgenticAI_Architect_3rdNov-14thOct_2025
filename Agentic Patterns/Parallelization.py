from google import genai
from dotenv import load_dotenv
import os
import time
import asyncio

load_dotenv()

# Configure the client with GEMINI API
client = genai.Client(api_key = os.environ["GEMINI_API_KEY"])

async def generate_content(prompt: str) -> str: 
    response = await client.aio.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )
    return response.text.strip()

async def parallel_tasks():
    topic = "Large Language Models"
    prompts = [
        f"Write a short description about the {topic}.",
        f"Write the importance of the {topic}.",
        f"Write the applications of the {topic}."
    ]
    start_time = time.time()
    tasks = [generate_content(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Time Taken: {end_time - start_time} seconds")
    
    print("\n=======================================Individual Results=======================================")
    for i, result in enumerate(results):
        print(f"Result {i+1}: {result}\n")
        
    # Aggregate the results and generate the complete story
    story_ideas = '\n'.join([f"Idea {i+1}: {result}" for i, result in enumerate(results)])
    aggregation_prompt = f"Combine the following three story ideas into a single, cohesive paragraph: {story_ideas}"
    aggregation_response = await client.aio.models.generate_content(
        model = "gemini-2.5-flash",
        contents = aggregation_prompt
    )
    return aggregation_response.text

result = asyncio.run(parallel_tasks())
print("\n==============================================================================================")
print(f"\n======================================Aggregated Summary====================================== \n{result}")
    
    