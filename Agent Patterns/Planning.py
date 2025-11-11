from google import genai
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

# Configure the client with GEMINI API
client = genai.Client(api_key = os.environ["GEMINI_API_KEY"])

# Define the plan schema
class Task(BaseModel): 
    task_id: int
    description: str
    assigned_to: str = Field(description = "Which worker type should handle this? E.g., Researcher, Writer, Coder")

class Plan(BaseModel):
    goal: str
    steps: List[Task]

# Step 1: Generate the plan (Planner LLM)
user_goal = "Write a short blog post about Agentic AI"
prompt_planner = f"""Create a step-by-step plan to achieve the following goal. 
                Assign each step to a hypothetical worker type (Researcher, Writer).
                Goal: {user_goal}
                """ 
print(f"Goal: {user_goal}")
print("Generating plan........")

# Use a model capable of planning and structured output
response_plan = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = prompt_planner, 
    config = {
        "response_mime_type": "application/json",
        "response_schema": Plan
    }
)

# Step 2: Execute the plan
for step in response_plan.parsed.steps:
    print(f"Step {step.task_id}: {step.description} (Assignee: {step.assigned_to})")