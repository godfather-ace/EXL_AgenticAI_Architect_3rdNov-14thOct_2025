from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import yfinance as yf

APP_NAME = "get_stock_price"
USER_ID = "st04"
SESSION_ID = "007"

load_dotenv()

def get_stock_price(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        historical_data = stock.history(period="1d")
        if not historical_data.empty:
            current_price = historical_data['Close'].iloc[-1]
            return current_price
        else:
            return None
    except Exception as e:
        print(f"Error retrieving stock price for {symbol}: {e}")
        return None

root_agent = Agent(
    model=LiteLlm("openai/gpt-4o"),
    name='stock_agent',
    instruction= 'As an agent, you will retrieve stock prices for a given ticker symbol or company name.',
    description='This agent will retrieve stock prices for a given ticker symbol or company name.',
    tools=[get_stock_price]
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
