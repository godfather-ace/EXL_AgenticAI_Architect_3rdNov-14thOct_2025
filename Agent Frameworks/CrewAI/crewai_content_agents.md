# 🤖 Multi-Agent Content Generation using CrewAI + Groq LLaMA 3.1

This example demonstrates how to use **CrewAI**, a lightweight framework for orchestrating multiple AI agents, together with **Groq’s LLaMA 3.1 model** for collaborative content generation.  
In this setup, two agents — a **Content Planner** and a **Content Writer** — work together to plan and write a LinkedIn post.

---

## 🔧 Prerequisites

Make sure to install the required dependencies:

```bash
pip install crewai litellm python-dotenv
```

You’ll also need a `.env` file containing your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

---

## 🧩 Full Python Code

```python
# =============================================================================================
#  CrewAI Content Generation Example
#  Description: Multi-agent collaboration using CrewAI and Groq API
# ============================================

# Install dependencies (uncomment if not installed)
# pip install crewai litellm python-dotenv

# ============================================
#  Import required libraries
# ============================================
from crewai import Agent, Task, Crew, LLM, Process
from dotenv import load_dotenv
import os

# ============================================
#  Load environment variables
# ============================================
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ============================================
#  Configure the LLM (Groq-hosted LLaMA model)
# ============================================
llm = LLM(
    model = "groq/llama-3.1-8b-instant",   # Groq LLaMA model
    max_completion_tokens = 256            # Token limit per response
)

# ============================================
#  Define the Planner Agent
# ============================================
planner = Agent(
    role = "Content Planner",
    goal = "Agent is able to plan an engaging and factually correct content on {topic}",
    backstory = (
        "You have to plan a LinkedIn post on the topic: {topic}. "
        "Your job is to collect clear and simple information for the audience. "
        "Your plan will guide the Content Writer Agent."
    ),
    llm = llm,
    verbose = True
)

# ============================================
#  Define the Writer Agent
# ============================================
writer = Agent(
    role = "Content Writer",
    goal = "Agent is able to write a post about the topic: {topic}",
    backstory = (
        "You have to write a LinkedIn post on the topic: {topic}. "
        "Your writing is based on the work of the Content Planner Agent, "
        "who provides you with the outline."
    ),
    llm = llm,
    verbose = True
)

# ============================================
#  Define Tasks for Each Agent
# ============================================
plan = Task(
    description = (
        "1. Get the information on the topic: {topic}. "
        "2. Plan a proper content outline around the topic."
    ),
    expected_output = "A detailed and engaging content plan based on reliable information.",
    agent = planner
)

write = Task(
    description = (
        "1. Use the content plan to craft a polished LinkedIn post on the topic: {topic}."
    ),
    expected_output = "A well-written and engaging LinkedIn post.",
    agent = writer
)

# ============================================
#  Assemble the Crew
# ============================================
crew = Crew(
    agents = [planner, writer],
    tasks = [plan, write],
    verbose = True
)

# ============================================
#  Run the Multi-Agent Process
# ============================================
result = crew.kickoff(inputs = {"topic": "Large Language Models"})

# Print the generated post
print(result)

# =============================================================================================
```

---

## 🧠 How It Works

1. **Planner Agent**  
   - Collects and structures information about the given topic.  
   - Produces a coherent content plan.

2. **Writer Agent**  
   - Uses the planner’s outline to draft a LinkedIn post.  
   - Focuses on clarity, engagement, and tone consistency.

3. **CrewAI Orchestration**  
   - The `Crew` class coordinates both agents.  
   - Tasks are executed sequentially or in parallel (depending on process type).

---

## 🗂️ Example Workflow

**Input:**  
`topic = "Large Language Models"`

**Execution Flow:**
1. Planner Agent → Creates an outline and key talking points.  
2. Writer Agent → Expands that outline into a LinkedIn-style post.  
3. Crew → Combines and outputs the final result.

**Sample Output (Simplified):**
```
Large Language Models (LLMs) are transforming the way we interact with information...
```

---

## 🧩 Notes

- You can easily extend this setup to more agents, such as:
  - **Fact Checker Agent**
  - **SEO Optimizer Agent**
  - **Social Media Strategist**
- CrewAI supports custom workflows and inter-agent communication.

---

## 🌈 Optional: Adding Parallelism

CrewAI can run agents **in parallel** using:

```python
crew = Crew(
    agents=[planner, writer],
    tasks=[plan, write],
    process=Process.parallel,   # Enables concurrent task execution
    verbose=True
)
```
