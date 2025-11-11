from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import enum

load_dotenv()

# Configure the client with GEMINI API
client = genai.Client(api_key = os.environ["GEMINI_API_KEY"])

class EvaluationStatus(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class Evaluation(BaseModel):
    evaluation: EvaluationStatus
    feedback: str
    reasoning: str

#=======================================Initial Generation Function=======================================
def generate_articlepost(topic: str, feedback: str = None) -> str:
    prompt = f"Write a short post on {topic}"
    if feedback: 
        prompt += f"\nIncorporate this feedback: {feedback}"
    
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )
    articlepost = response.text.strip()
    print(f"Generated Article Post: \n{articlepost}")
    return articlepost

#=======================================Evaluation Function=======================================
def evaluate(articlepost: str) -> Evaluation: 
    print("\nEvaluation Article Post")
    prompt_critique = f"""Critique the following article post. Is it technical? 
    Respond with PASS or FAIL and provide feedback.

    ArticlePost: 
    {articlepost}
    """
    response_critique = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt_critique,
        config = {
            "response_mime_type": "application/json",
            "response_schema": Evaluation
        }
    )
    critique = response_critique.parsed
    print(f"Evaluation Status: {critique.evaluation}")
    print(f"Evaluation Feedback: {critique.feedback}")
    return critique

#=======================================Reflection Loop=======================================
max_iterations = 3 
current_iteration = 0
topic = "What is Market Analysis?"

current_articlepost = "Market analysis is the process of studying customers, competitors, and trends to understand demand, preferences, and opportunities. It helps businesses make better decisions, identify growth areas, and plan strategies to meet customer needs and stay ahead in the market."
while current_iteration < max_iterations:
    current_iteration +=1 
    print(f"\n===========Iteration {current_iteration}===========")
    evaluation_result = evaluate(current_articlepost)
    if evaluation_result.evaluation == EvaluationStatus.PASS: 
        print("\nFinal Article Post:")
        print(current_articlepost)
    else: 
        current_articlepost = generate_articlepost(topic, feedback = evaluation_result.feedback)
        if current_iteration == max_iterations:
            print("\nMax iterations reached, last attempt: ")
            print(current_articlepost)

