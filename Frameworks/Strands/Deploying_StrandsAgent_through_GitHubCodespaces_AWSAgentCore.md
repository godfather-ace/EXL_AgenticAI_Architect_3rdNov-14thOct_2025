# 🤖 Strands with AWS Bedrock and AgentCore — Complete Setup Guide

This guide helps you **set up, build, and deploy** your first AI Agent using **Strands**, **AWS Bedrock**, and **AgentCore**.  
It combines local setup steps, Codespaces configuration, and full deployment to the **Bedrock AgentCore Runtime**.

---

## 🧰 Prerequisites

Before starting, ensure you have:

- ✅ An **AWS account** with valid credentials.
- 🐍 **Python 3.10+** installed.
- 🔧 **boto3** installed (`pip install boto3`).
- 🧾 **Amazon Bedrock access** with permission for at least one model (e.g., *Claude Sonnet 4.0*).
- ⚙️ **AWS CLI** configured locally (`aws configure`).
- 💻 A **GitHub Codespaces** or local environment ready.

---

# 🧱 Part 1 — Setup GitHub Repository and AWS IAM Access

## Step 1 — Create a New Repository on GitHub

<p align="center">
  <img src="ss/1.png" alt="New Repo" />
  <br/>
</p>

1. Go to your GitHub profile → **New Repository**.  
2. Name it `agentcore`.  
3. Set visibility to **Private** and check **Add README**.  
4. Click **Create Repository**.

---

## Step 2 — Open Repository in Codespaces

<p align="center">
  <img src="ss/2.png" alt="Codespaces" />
  <br/>
</p>

1. Click **Code → Codespaces → Create codespace on main**.

---

## Step 3 — Initialize Your Codespace

<p align="center">
  <img src="ss/3.png" alt="Initialize Codespace" />
  <br/>
</p>

```bash
touch .gitignore .env
```

Both files will appear in your workspace.

---

## Step 4 — Update `.gitignore` File

<p align="center">
  <img src="ss/2.png" alt=".gitignore file" />
  <br/>
</p>
```
.env
.bedrock_agentcore.yaml
```

---

## Step 5 — Configure AWS Credentials

![Edit .env file](5.png)

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
```

---

## Step 6 — Create an IAM User

![Create IAM user](6.png)

Navigate to **IAM → Users → Create User**.

---

## Step 7 — Assign IAM Permissions

![Attach IAM policies](6-1.png)

Choose **Attach policies directly → AdministratorAccess**.

---

## Step 8 — Review and Create IAM User

![Review IAM user](7.png)

Confirm and click **Create User**.

---

## Step 9 — Generate Access Keys

![Access key wizard](7-1.png)

Select **Command Line Interface (CLI)** → click **Next**.

---

## Step 10 — Retrieve Access Keys

![Retrieve access keys](8.png)

Copy or download credentials and update `.env`.

---

# ⚙️ Part 2 — Build and Deploy Your First AgentCore AI Agent

## Step 11 — Create Agent Folder and Script

![Create docker folder and agent file](9.png)

```bash
mkdir docker
cd docker
touch agentcore.py
```

---

## Step 12 — Add Requirements

![Create requirements.txt file](10.png)

```bash
touch requirements.txt
```

Contents:

```
strands-agents
bedrock-agentcore
```

---

## Step 13 — Write the AgentCore Python Script

![Add agentcore.py code](11.png)

```python
from dotenv import load_dotenv
from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

load_dotenv()

agent = Agent("us.anthropic.claude-3-7-sonnet-20250219-v1:0")
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke_agent(payload, context):
    prompt = payload.get("prompt")
    return {"result": agent(prompt).message}

app.run()
```

---

## Step 14 — Install Dependencies

![Install dependencies](12.png)

```bash
pip install -r requirements.txt
```

---

## Step 15 — Run the Agent Locally

![Run the agent locally](13.png)

```bash
python agentcore.py
```

---

## Step 16 — Verify Port Forwarding

![Verify forwarded port](13-1.png)

Ensure **port 8080** is active and auto-forwarded.

---

## Step 17 — Configure Bedrock AgentCore

![Configure agentcore](14.png)

```bash
agentcore configure --entrypoint agentcore.py --name demoagent
```

Follow prompts to auto-create IAM role, ECR repo, and short-term memory.

---

## Step 18 — Confirm Configuration Summary

![Configuration summary](15.png)

You’ll see:

```
Agent Name: demoagent
Deployment: container
Region: us-east-1
Execution Role: Auto-create
ECR Repository: Auto-create
Memory: Short-term (30-day retention)
```

---

## Step 19 — Launch Your Agent

![Launch agentcore](16.png)

```bash
agentcore launch
```

---

## Step 20 — Deployment Success

![Deployment success](17.png)

**Key Outputs:**  
- Agent ARN  
- ECR URI  
- CloudWatch Log Group  
- GenAI Observability Dashboard URL

Use:
```bash
agentcore status
agentcore invoke '{"prompt": "Hello"}'
```

---

## Step 21 — Test the Agent in AWS Agent Sandbox

![AWS Agent Sandbox test](8.png)

Example input:
```json
{ "prompt": "Who is LLM?" }
```

**Output:**
> “LLM stands for Large Language Model. It’s a type of artificial intelligence system trained on vast amounts of text data to understand and generate human language...”

---

# 🧩 Summary

You have successfully:

✅ Created and configured a **Strands-powered Agent**  
✅ Deployed it to **AWS Bedrock AgentCore** Runtime  
✅ Verified runtime behavior using **Agent Sandbox**  
✅ Integrated short-term memory, IAM, and observability

---

# 🌟 Next Steps

- Integrate multi-agent orchestration using **LangGraph** or **CrewAI**.  
- Add **custom tool plugins** or API connectors.  
- Build a frontend interface using **FastAPI** or **Streamlit**.  
- Enable **CloudWatch Metrics** and Observability Dashboard for runtime monitoring.

---
