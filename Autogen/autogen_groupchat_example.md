# 🧠 Collaborative Multi-Agent Group Chat with AutoGen (Using Groq + LLaMA 3.1)

This script demonstrates how to build a **collaborative AI agent conversation** using AutoGen’s `GroupChat` and `GroupChatManager` features.  
It sets up a **multi-agent system** where three AI agents — a **Coder**, a **Critic**, and an **Admin** — collaboratively design, review, and execute Python code.

---

## 🔧 Prerequisites

Before running this script, make sure you have installed all dependencies:

```bash
pip install pyautogen autogen python-dotenv
```

Also, set up your **Groq API key** in a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## 🧑🏻‍💻 Full Python Code

```python
# ========================================================================================
#  AutoGen Multi-Agent Group Chat Example
#  Description: Collaborative Coder–Critic–Admin workflow using Groq API
# ============================================

import autogen
import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION SETUP ---
try:
    # Load configuration from .env file
    load_dotenv()

    llm_config = {
        "config_list": [
            {
                "model": "llama-3.1-8b-instant",     # Groq-hosted LLaMA 3.1 model
                "api_key": os.getenv("GROQ_API_KEY"),# API key loaded securely
                "api_type": "groq"                   # API provider type
            }
        ]
    }
except Exception as e:
    print(f"Error loading config: {e}")
    print("Please ensure your AutoGen config is set up correctly")
    exit()

# --- 2. AGENT DEFINITIONS ---
# 2.1. User Proxy / Admin
# This agent initiates the task, handles code execution, and determines when the conversation is finished.
user_proxy = autogen.UserProxyAgent(
    name = "Admin",
    system_message = "A human admin. Send comments and terminate the chat by saying 'TERMINATE' when the task is fully complete.",
    # Configuration for running code. Code will be executed in a 'group_chat_work' directory.
    code_execution_config = {
        "work_dir": "group_chat_work",
        "use_docker": False # Set to True if Docker is available and preferred
    },
    is_termination_msg = lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode = "NEVER", # Set to "ALWAYS" for interactive mode
)

# 2.2. Coder Agent
coder = autogen.AssistantAgent(
    name = "Coder",
    llm_config = llm_config,
    system_message = "You are a professional Python programmer. You write and suggest high-quality, self-contained Python code to solve tasks. You must wait for the Critic's approval before executing or confirming the final code.",
)

# 2.3. Critic/Reviewer Agent
critic = autogen.AssistantAgent(
    name = "Critic",
    llm_config = llm_config,
    system_message = "You are a rigorous software quality assurance reviewer. Your job is to check the Coder's plan and code for correctness, efficiency, and strict adherence to ALL user requirements. You provide constructive criticism and must explicitly give final approval ('Looks good!') only when the code is perfect and ready for execution. DO NOT write code yourself.",
)

# --- 3. GROUP CHAT SETUP ---
# 3.1. GroupChat
# Defines the agents, the conversation history, and the maximum number of turns.
group_chat = autogen.GroupChat(
    agents = [user_proxy, coder, critic], # All participating agents
    messages = [],
    max_round = 5, # Max rounds before the chat stops automatically
    # Defines which agent should speak next based on the last message.
    allow_repeat_speaker = False,
)

# 3.2. GroupChatManager
# This agent acts as the moderator, deciding who speaks next based on the group chat policy.
manager = autogen.GroupChatManager(
    groupchat = group_chat,
    llm_config = llm_config,
    # The system message guides the manager's moderation behavior.
    system_message = "You are the Group Chat Manager. You moderate the conversation between the Coder and the Critic, ensuring the Coder provides code and the Critic reviews it before the Admin approves the final solution."
)

# --- 4. START THE CONVERSATION ---
print("--- Starting Group Chat Execution ---")
print("Task: Write a Python script to calculate the first 10 Fibonacci numbers and save them to 'fibonacci.txt'.")
print("The Coder must get explicit approval from the Critic before finalizing the code.")

user_proxy.initiate_chat(
    manager,
    message = "Write a Python script to calculate the first 10 Fibonacci numbers. The script must then save these 10 numbers to a file named 'fibonacci.txt'. The Coder must get approval from the Critic before executing or proposing the final solution.",
)

print("\n--- Script Finished ---")
print(f"Check the '{os.path.join(os.getcwd(), 'group_chat_work')}' directory for the output file 'fibonacci.txt'.")

# ========================================================================================
```

---

## 💡 How It Works

1. **Admin (User Proxy)**  
   - Initiates the conversation.  
   - Manages code execution.  
   - Terminates the chat when satisfied (message ends with `"TERMINATE"`).

2. **Coder Agent**  
   - Writes Python code solutions (e.g., to compute Fibonacci numbers).  
   - Waits for **Critic approval** before finalizing or running code.

3. **Critic Agent**  
   - Reviews the Coder’s code for logic, efficiency, and adherence to the task.  
   - Provides constructive feedback and only approves perfect code.

4. **GroupChat & Manager**  
   - `GroupChat` defines participants and dialogue policies.  
   - `GroupChatManager` moderates who speaks next and ensures orderly collaboration.

---

## 🗺️ Example Output Flow

**System Message:**
```
--- Starting Group Chat Execution ---
Task: Write a Python script to calculate the first 10 Fibonacci numbers...
```

**Conversation Example:**
```
Coder: I propose a Python script that generates Fibonacci numbers using iteration.
Critic: The logic looks correct, but ensure results are saved to 'fibonacci.txt'.
Coder: Updated code now includes file output.
Critic: Looks good!
Admin: Great work. TERMINATE
```

**Result:**  
A file named `fibonacci.txt` is created in the `group_chat_work` directory containing:
```
0
1
1
2
3
5
8
13
21
34
```

---

## 📝 Notes

- To enable **interactive approval**, set:
  ```python
  human_input_mode="ALWAYS"
  ```
- To use Docker for safe code execution, change:
  ```python
  "use_docker": True
  ```
- You can easily extend this setup to include:
  - A **Data Validator Agent**
  - A **Documentation Agent**
  - A **Performance Optimizer**

---
