from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import pandas as pd
from typing import Dict, Any
from io import StringIO
import os

APP_NAME = "eda_on_csv"
USER_ID = "st004"
SESSION_ID = "0017"

load_dotenv()

def analyze_csv_eda(csv_content: str) -> Dict[str, Any]:
    """
    Analyzes the content of a CSV file provided as a string and performs basic EDA.
    Args:
        csv_content: A string containing the content of the CSV file.
    Returns:
        A dictionary containing the EDA results, including:
            - 'head': The first 5 rows of the DataFrame.
            - 'describe': Descriptive statistics of the numerical columns.
            - 'value_counts': Value counts for each categorical column (top 5).
            - 'null_counts': Number of null values per column.
    """
    try:
        df = pd.read_csv(StringIO(csv_content))
    except Exception as e:
        return {"error": f"Failed to read CSV content: {e}"}

    results = {}
    results['head'] = df.head().to_string()
    results['describe'] = df.describe(include='all').to_string()
    results['null_counts'] = df.isnull().sum().to_string()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    value_counts = {}
    for col in categorical_cols:
        value_counts[col] = df[col].value_counts().head().to_string()
    results['value_counts'] = value_counts
    return results

root_agent = Agent(
    model = LiteLlm(model='openai/gpt-4o'),
    name='eda_agent',
    instruction= 'As an agent, you will apply EDA on the csv file content provided to you using the available tools.',
    description="""This agent will apply EDA on the csv file content provided to you. Give proper points with explainations based on the EDA results. 
    Also provide the list and types of statistical charts that can be created using the columns, 
    Give the column names along with chart recommendation. Suggest Python based code for printing one chart. """,
    tools=[analyze_csv_eda]
)

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

def call_agent_with_csv(csv_content):
    """Calls the EDA agent with the content of a CSV file."""
    query = f"Perform EDA on this CSV data:\n\n{csv_content}"
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

if __name__ == "__main__":
    file_path = '/Users/sachintripathi/Documents/Py_files/EXL_AgenticAI_Engineering/Agentic Frameworks/Google_ADK/csv_eda/sample.csv'  
    if not os.path.exists(file_path):
        sample_data = """col1,col2,col3
a,1,10.5
b,2,20.3
a,1,15.0
c,3,22.1
b,2,18.7
a,,11.2
"""
        with open(file_path, 'w') as f:
            f.write(sample_data)
        print(f"Created a sample CSV file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            csv_content = f.read()
        print("Sending CSV content to the agent for EDA...")
        call_agent_with_csv(csv_content)
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{file_path}'. Please create or specify the correct path.")
    except Exception as e:
        print(f"An error occurred: {e}")
