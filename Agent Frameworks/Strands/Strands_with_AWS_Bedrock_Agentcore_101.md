# 🤖 Strands with AWS Bedrock and AgentCore - 101

This guide demonstrates how to build an **AI Agent** using **Strands**, **AWS Bedrock**, and **AgentCore**.  
You’ll learn to configure, test, and deploy your first intelligent agent powered by Bedrock’s runtime — using the **AgentCore Starter Toolkit**.

---

## 🧰 Prerequisites

Before you begin, ensure you have:

- ✅ An **AWS account** with valid credentials.
- 🐍 **Python 3.10+** installed.
- 🔧 **boto3** installed (`pip install boto3`).
- 🧾 **Amazon Bedrock access** to at least one model (e.g., *Claude Sonnet 4.0*).
- ⚙️ AWS CLI configured locally (`aws configure`).

---

## 🪄 Step 1 — Set Up the Project

1. Create and activate a new virtual environment:

   ```bash
   mkdir strands-bedrock-agentcore
   cd strands-bedrock-agentcore
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   > On Windows: `.venv\Scripts\activate`

2. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

3. Install the required dependencies:
   ```bash
   pip install bedrock-agentcore strands-agents bedrock-agentcore-starter-toolkit
   ```

4. Verify your installation:
   ```bash
   agentcore --help
   ```

---

## 🤖 Step 2 — Create Your First Agent

Create a file named **`my_agent.py`** and paste the following code:

```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
agent = Agent()

@app.entrypoint
def invoke(payload):
    '''Your AI agent entrypoint'''
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
```

Then, create a **`requirements.txt`** file with:
```
bedrock-agentcore
strands-agents
```

---

## 🧪 Step 3 — Test Locally

Run your agent locally:

```bash
python my_agent.py
```

In a new terminal window, test it with `curl`:

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'
```

✅ Expected output:
```json
{"result": "Hello! I'm here to help..."}
```

> Ensure port **8080** is available before running the local server.

---

## ⚙️ Step 4 — Configure Your Agent for Deployment

Use the CLI to configure your agent:

```bash
agentcore configure -e my_agent.py
```

This will:
- Create a configuration file `.bedrock_agentcore.yaml`
- Prompt you to enable **short-term** or **long-term memory**
- Set up IAM roles, policies, and resources automatically

### Optional Flags

| Option | Description |
|--------|--------------|
| `--disable-memory` | Skip memory setup |
| `-r <region>` | Deploy to a specific AWS region (default: `us-west-2`) |

Example:
```bash
agentcore configure -e my_agent.py -r us-east-1 --disable-memory
```

---

## 📊 Step 5 — Enable Observability

To monitor, trace, and debug your deployed agent:
- Enable **CloudWatch** transaction search.
- View runtime logs and metrics under `/aws/bedrock-agentcore/runtimes/{agent-id}` in CloudWatch.

---

## ☁️ Step 6 — Deploy to AgentCore Runtime

Launch your agent to the AWS AgentCore environment:

```bash
agentcore launch
```

This command will:
- Package your code (or build a container)
- Create AWS resources (S3, ECR, IAM roles)
- Deploy the agent to **AgentCore Runtime**
- Configure observability and memory (if enabled)

Once complete, note:
- The **ARN** of your deployed agent
- The **CloudWatch log group name**

Check deployment status anytime with:
```bash
agentcore status
```

---

## 💬 Step 7 — Test Your Deployed Agent

Invoke the agent you just deployed:

```bash
agentcore invoke '{"prompt": "Tell me a joke"}'
```

✅ If successful, you’ll receive a joke in the output!

If not, check your logs and configuration:
```bash
agentcore status
```

---

## 🧩 Step 8 — Programmatic Invocation

You can also invoke your deployed agent directly using Python.

Create a file named **`invoke_agent.py`**:

```python
import json
import uuid
import boto3

agent_arn = "<your-agent-arn>"
prompt = "Tell me a joke"

client = boto3.client("bedrock-agentcore")

payload = json.dumps({"prompt": prompt}).encode()

response = client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    runtimeSessionId=str(uuid.uuid4()),
    payload=payload,
    qualifier="DEFAULT"
)

content = []
for chunk in response.get("response", []):
    content.append(chunk.decode("utf-8"))

print(json.loads("".join(content)))
```

Run:
```bash
python invoke_agent.py
```

> Ensure your IAM user/role has the `bedrock-agentcore:InvokeAgentRuntime` permission.

---

## 🧹 Step 9 — Clean Up Resources

When done experimenting, destroy all deployed resources to avoid extra costs:

```bash
agentcore destroy
```

Alternatively, you can manually delete resources from the **AgentCore Console** or AWS services such as **S3**, **IAM**, and **ECR**.

---

## 🗂️ Resource Reference

| Resource | Location |
|-----------|-----------|
| **Agent Logs** | CloudWatch → Log groups → `/aws/bedrock-agentcore/runtimes/{agent-id}-DEFAULT` |
| **Memory** | AgentCore Console → Memory section |
| **Container Images** | ECR → Repository: `bedrock-agentcore-{agent-name}` |
| **Deployment Zips** | S3 → Bucket → `{agent-name}/deployment.zip` |
| **IAM Roles** | IAM Console → Roles → Search `BedrockAgentCore` |

---

## ⚠️ Common Issues & Fixes

| Problem | Cause | Fix |
|----------|--------|-----|
| **Access Denied (Permissions)** | Missing IAM policies | Run `aws sts get-caller-identity` to confirm and attach necessary roles |
| **Docker warning** | Using code deployment | Ignore; Docker is optional unless containerizing |
| **Model access denied** | Model not enabled in your region | Enable model (e.g., Claude 4.0) in AWS Bedrock console |
| **Port 8080 already in use** | Another process bound to port | Stop conflicting process or use a different port |

---

## 🌟 What’s Next?

Once your first agent is live:
- Explore **Memory**, **Gateway**, **Identity**, and **Observability** modules.
- Add custom **tools** or **external APIs**.
- Integrate your Bedrock agent with **LangGraph**, **CrewAI**, or **Autogen** workflows.
- Deploy a **multi-agent architecture** using AgentCore Runtime as the backend.

---
