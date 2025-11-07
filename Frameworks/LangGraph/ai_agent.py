from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

def get_response_from_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider == 'Groq':
        llm = ChatGroq(model=llm_id)

    tools = [TavilySearchResults(max_results = 2)] if allow_search else []

    agent = create_react_agent(
        model = llm,
        tools = tools,
        prompt = system_prompt
    )
    
    state = {"messages":query}
    response = agent.invoke(state)
    messages  = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]
    return ai_messages[-1]