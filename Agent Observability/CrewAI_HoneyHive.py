from honeyhive import HoneyHiveTracer, trace
from crewai import Agent, Task, Crew, LLM, Process
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Place the code below at the beginning of your application to initialize the tracer
HoneyHiveTracer.init(
    api_key='******',
    project='demo',
    source='dev', #Optional
    session_name='Test Session', #Optional
    
)

llm = LLM(model = "groq/llama-3.1-8b-instant", 
        temperature = 0.2,
        max_completion_tokens = 256,
        top_p = 0.9
    )

planner = Agent(
    role = "Content Planner", 
    goal = "Plan engaging and factually accurate content on {topic}", 
    backstory = "You're working on planning a blog article about the: {topic}"
                "You collect information that helps the audience learn something"
                "and make informed decisions."
                "Your work is the basis for the content writer to write an article on this topic.", 
    llm = llm, 
    allow_delegation = False, 
    verbose = True
)

writer = Agent(
    role = "Content Writer",
    goal = "Write a factually accurate opinion piece about the topic: {topic}",
    backstory = "You are working on writing a new opinion piece about the topic: {topic}."
                "You base your writing on the work of the content planner, who provides an outline"
                "You also provide objective and insights and back them up with the information"
                "provided by the content planner",
    llm = llm, 
    allow_delegation = False, 
    verbose = True
)

editor = Agent(
    role = "Editor", 
    goal = "Edit the given blog post with a proper writing style.",
    backstory = "You an editor who receives a blog post from the content writer."
                "Your goal is to ensure that it follows journalistic best practices.",
    llm = llm, 
    allow_delegation = False, 
    verbose = True
)   

plan = Task(
    description = (
        "1. Prioritize the latest trends and news on the {topic}.\n"
        "2. Identify the target audience based on their interests.\n"
        "3. Develop a detailed content outline including an introduction, and key points.\n"
        "4. Include SEO keywords and relevant data sources.\n"
    ),
    expected_output = "A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.\n",
    agent = planner
)

write = Task(
    description = (
        "1. Use the content plan to craft a blog post on the {topic}.\n"
        "2. Incoporate SEO keywords naturally.\n"
        "3. Ensure the post is properly structured with an introduction, insightful body, and a summarising conclusion.\n"
        "4. Proofread for grammatical errors.\n"
    ),
    expected_output = "A well-written blog post in markdown format, ready for publication.", 
    agent = writer
)

edit = Task(
    description = (
        "Proofread the given blog post for grammatical errors and alignment with the core-opinion."
    ),
    expected_output = "A well-written blog post in markdown format, ready for publication.",
    agent = editor
)

crew = Crew(
    agents = [planner, writer, editor],
    tasks = [plan, write, edit],
    verbose = True
)   

try: 
    result = crew.kickoff(inputs = {"topic": "Autonomous Enterprises"})
    print("Result:", result)
except Exception as e: 
    print(f"An error occured: {e}")