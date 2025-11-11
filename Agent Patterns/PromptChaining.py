#pip install google-genai

from gettext import translation
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

# Configure the client with GEMINI API
client = genai.Client(api_key = os.environ["GEMINI_API_KEY"])

# Step 1 - Summarize the text
original_text = "LLMs, or Large Language Models, are a type of artificial intelligence system trained to understand and generate human-like text. They’re built using deep learning—specifically a neural network architecture called a Transformer—and trained on massive amounts of text data from books, websites, and other sources."
prompt1 = f"Summarize the following text in one sentence: {original_text}"

# Use client.models.generate_content
response1 = client.models.generate_content(
    model = "gemini-2.0-flash", 
    contents = prompt1
)
summary = response1.text.strip()
print(f"Summary: {summary}")

# Step 2 - Translation of the summary
prompt2 = f"Translate the following summary into French, only return the translation, no other text: {summary}"

# Use client.models.generate_content
response2 = client.models.generate_content(
    model = "gemini-2.0-flash", 
    contents = prompt2
)
translation = response2.text.strip()
print(f"Translation: {translation}")

