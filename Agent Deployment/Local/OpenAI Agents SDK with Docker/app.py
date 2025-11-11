import nest_asyncio
nest_asyncio.apply()

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import streamlit as st
import asyncio
import time
import os

st.title("Locally Deployed AI Agent")
st.write("This is a locally deployed AI agent then can assist in research")

add_selectbox = st.sidebar.selectbox(
    "Select the LLM provider", 
    (["OpenAI"])
)

openai_key = st.sidebar.text_input("Enter your OpenAI Key", type = "password")
os.environ["OPENAI_API_KEY"] = openai_key

class ResearchOutput(BaseModel): 
    is_research: bool
    reasoning: str

guardrail_agent = Agent(
    name = "Guardrail Check",
    instructions = "Check if the user is asking about research.", 
    output_type = ResearchOutput
)

physics_research_agent = Agent(
    name = "Physics Researcher", 
    handoff_description = "Specialist agent for Physics Research",
    instructions = """You provide assistance with Physics Research. Explain your reasoning at each step
                    and include examples."""
)

financial_research_agent = Agent(
    name = "Financial Researcher", 
    handoff_description = "Specialist agent for Financial Research",
    instructions = """You provide assistance with Financial Research. Explain important events and
                    context clearly"""
)

async def research_guardrail(ctx, agent, input_data): 
    result = await Runner.run(guardrail_agent, input_data, context = ctx.context)
    final_output = result.final_output_as(ResearchOutput)
    return GuardrailFunctionOutput(
        output_info = final_output,
        tripwire_triggered = not final_output.is_research
    )

triage_agent = Agent(
    name = "Triage Agent", 
    instructions = "You determine which agent to use based on user's research query.",
    handoffs = [physics_research_agent, financial_research_agent],
    input_guardrails = [
        InputGuardrail(guardrail_function = research_guardrail)
    ]
)

from agents.tracing.setup import GLOBAL_TRACE_PROVIDER
from agents import set_tracing_export_api_key
set_tracing_export_api_key(os.getenv("OPENAI_API_KEY"))
GLOBAL_TRACE_PROVIDER._multi_processor.force_flush()

async def main():
    user_input = st.text_input("Enter your research query:")
    if st.button("Submit"):
        with st.spinner("Processing..."):
            time.sleep(10)
        result = await Runner.run(triage_agent, user_input)
        st.write(result.final_output)
        
if __name__ == "__main__":
    asyncio.run(main())
