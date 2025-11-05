# 🧠 Autogen Conversational Agent Example (Using Groq + LLaMA 3.1)

This guide demonstrates how to build a simple **Conversational AI Agent** using the `autogen` library.  
The example uses the **Groq API** (with the LLaMA 3.1 model) to create a **travel planner assistant** that interacts conversationally with the user.

---

## 🔧 Prerequisites

Make sure to install the required packages before running the code.

```bash
pip install pyautogen autogen groq python-dotenv
```

You’ll also need to create a `.env` file containing your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

---

## 🧑🏻‍💻 Full Python Code

```python
# =============================================================================================
#  Autogen Travel Planner Assistant
#  Description: Conversational AI using Groq API and LLaMA 3.1
# ============================================

# Import required libraries
import os
from dotenv import load_dotenv                 # For securely loading API keys from .env file
from autogen import ConversableAgent, UserProxyAgent  # Core classes from the Autogen library

# ============================================
#  Load environment variables
# ============================================
load_dotenv()  # Loads all variables defined in the .env file into the environment

# ============================================
#  Define the LLM Configuration
# ============================================
llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-8b-instant",     # Model name (Groq-hosted LLaMA 3.1)
            "api_key": os.getenv("GROQ_API_KEY"),# Securely fetched API key
            "api_type": "groq"                   # Specifies Groq API provider
        }
    ]
}

# ============================================
#  Create the User Proxy Agent
# ============================================
# Acts as the user's interface in the conversation
user_proxy_agent = UserProxyAgent(
    name = "User Agent",
    system_message = "User proxy agent"
)

# ============================================
#  Create the Assistant Agent
# ============================================
# This agent performs the actual reasoning and generates travel recommendations
assistant_agent = ConversableAgent(
    name = "Assistant",
    system_message = (
        "You are a travel planner who provides detailed plans for travel destinations, "
        "dining, and the best places to visit. Offer insightful recommendations "
        "based on the user's query."
    ),
    llm_config = llm_config
)

# ============================================
#  Main Program Loop
# ============================================
def main():
    '''Runs an interactive chat loop between the user and the assistant.'''
    while True:
        # Take user input
        user_input = input("User: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Assistant: Goodbye!")
            break

        # Initiate chat between the user proxy and assistant agent
        user_proxy_agent.initiate_chat(assistant_agent, message=user_input)

# ============================================
#  Entry Point
# ============================================
if __name__ == "__main__":
    main()

# =============================================================================================
```

---

## 💡 How It Works

1. **Environment Setup**  
   - Loads your Groq API key from `.env`.  
   - Ensures all sensitive data is kept secure.

2. **Agent Configuration**  
   - `UserProxyAgent` → Represents the user.  
   - `ConversableAgent` → Represents the AI travel assistant powered by Groq’s LLaMA model.

3. **Chat Loop**  
   - Takes input continuously from the user.  
   - Ends when the user types `exit`, `quit`, or `bye`.  
   - Each input triggers the assistant’s response through `initiate_chat()`.

---

## 🗺️ Example Interaction

```
User: Plan a 3-day trip to Kyoto with good food options.
Assistant: Here’s a detailed 3-day itinerary for Kyoto...
```

---

## 📝 Notes

- You can replace the assistant’s `system_message` with any custom persona, such as:
  - A **career coach**
  - A **data analyst**
  - A **personal finance advisor**
- The framework supports **multi-agent orchestration**, so you can extend this into agentic AI systems that coordinate tasks.

