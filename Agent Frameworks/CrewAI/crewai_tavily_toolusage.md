# ⚙️ Single-Agent CrewAI Prototype with Tavily Search and Groq LLaMA 3.1

This example demonstrates how to create a **baseline single-agent CrewAI setup** integrated with a **web search tool (Tavily)** and powered by **Groq’s LLaMA 3.1 model**.  
The agent performs **factual data retrieval**, leveraging both an LLM and an external search tool to produce accurate, real-world information.

---

## 🔧 Prerequisites

Install the required dependencies:

```bash
pip install crewai tavily-python 'crewai[tools]' litellm python-dotenv
```

Set up your environment variables in a `.env` file:

```
TAVILY_API_KEY=your_tavily_key_here
GROQ_API_KEY=your_groq_key_here
```

---

## 🧑🏻‍💻 Full Python Code

```python
# =============================================================================================
#  CrewAI Single-Agent Example
#  Description: A single-agent setup with Tavily Search and Groq LLM
# ============================================

import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv

# ============================================
#  Load Environment Variables
# ============================================
load_dotenv()

# --- 1. CONFIGURATION CHECK & LLM SETUP ---
if not os.getenv("TAVILY_API_KEY") or not os.getenv("GROQ_API_KEY"):
    print("FATAL ERROR: Please set both TAVILY_API_KEY and GROQ_API_KEY environment variables.")
    exit()

# Instantiate Groq LLM (LLaMA 3.1)
llm = LLM(model = "groq/llama-3.1-8b-instant", max_completion_tokens = 256)

# --- 2. TOOL DEFINITION ---
# Initialize Tavily search tool using your TAVILY_API_KEY automatically
tavily_tool = TavilySearchTool()

# --- 3. AGENT DEFINITION ---
researcher_agent = Agent(
    role = 'Simple Fact Checker',
    goal = 'Quickly and accurately retrieve a single, recent factual data point using web search.',
    backstory=(
        "A reliable data retrieval bot known for its efficiency and speed in answering specific, single-point queries. "
        "It uses the Tavily Search tool to find definitive answers to factual questions."
    ),
    tools = [tavily_tool],
    llm = llm,
    verbose = True,
    allow_delegation = False
)

# --- 4. TASK DEFINITION ---
research_task = Task(
    description = (
        "Use the search tool to find the current official world record time for the men's 100-meter sprint.\n"
        "Your final answer MUST be only the time and the name of the athlete who holds the record, as a single sentence."
    ),
    expected_output = "A single sentence containing the record time and athlete's name (e.g., The record is 9.58 seconds, held by Usain Bolt).",
    agent = researcher_agent
)

# --- 5. CREW SETUP AND EXECUTION ---
single_agent_crew = Crew(
    agents = [researcher_agent],
    tasks = [research_task],
    verbose = True
)

print("--- Starting Single-Agent Crew Execution (Powered by Groq) ---")
print("The Researcher will now use the Tavily Search tool to gather information...")

result = single_agent_crew.kickoff()

print("\n\n################################")
print("## CREW EXECUTION FINISHED ##")
print("################################\n")
print(f"Final Research Summary:\n\n{result}")
# =============================================================================================

```

---

## 💡 How It Works

1. **LLM Initialization**  
   The `LLM` class connects to Groq’s hosted **LLaMA 3.1** model.

2. **Tool Setup – Tavily Search**  
   The agent uses the `TavilySearchTool` for real-time information retrieval via web search.

3. **Agent Definition**  
   - Role: `Simple Fact Checker`  
   - Function: Retrieves **one factual data point** with precision and speed.  
   - Tools: Integrated with the Tavily search API.  
   - No delegation or multi-agent orchestration required.

4. **Task Definition**  
   - Describes what the agent must achieve.  
   - Sets clear expectations for the output format.

5. **Crew Execution**  
   - Even single agents use a `Crew` container for consistency.  
   - `kickoff()` runs the process and returns the final result.

---

## 🗺️ Example Run

**Console Output Example:**

```
--- Starting Single-Agent Crew Execution (Powered by Groq) ---
The Researcher will now use the Tavily Search tool to gather information...

## CREW EXECUTION FINISHED ##

Final Research Summary:
The record is 9.58 seconds, held by Usain Bolt.
```

---

## 📝 Notes

- You can change the **search query** in the `research_task` to fetch any real-time factual data.
- CrewAI supports adding:
  - **Additional tools** (e.g., code interpreters, data analysis plugins)
  - **Multiple agents** for reasoning and verification
- To debug the agent’s thought process, set `verbose=True`.

---

## 🌈 Optional Extensions

Want to make it multi-agent? Add:
- A **Verification Agent** that checks multiple sources for consistency.
- A **Summarizer Agent** that formats the output for publication.

---