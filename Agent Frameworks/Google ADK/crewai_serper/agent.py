from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.crewai_tool import CrewaiTool
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

APP_NAME = "news_app"
USER_ID = "st04"
SESSION_ID = "01234"

load_dotenv()

serper_tool_instance = SerperDevTool(
    n_results=5,
    save_file=False,
    search_type="news",
)

adk_serper_tool = CrewaiTool(
    name="NewsSearch",
    description="Searches the internet for news articles using Serper.",
    tool=serper_tool_instance
)

root_agent = Agent(
    name="news_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="QA based on Google Search using Serper",
    instruction="I can search the internet for news articles and answer your questions.",
    tools=[adk_serper_tool]
)

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)
