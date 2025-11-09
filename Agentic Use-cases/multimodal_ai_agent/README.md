## 🧬 Multimodal AI Agent

A Streamlit application that combines video analysis and web search capabilities using Google's Gemini 2.0 model. This agent can analyze uploaded videos and answer questions by combining visual understanding with web-search.

### Features

- Video analysis using Gemini 2.0 Flash
- Web research integration via DuckDuckGo
- Support for multiple video formats (MP4, MOV, AVI)
- Real-time video processing
- Combined visual and textual analysis

### How to get Started?

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```
2. Get your Google Gemini API Key

- Sign up for an [Google AI Studio account](https://aistudio.google.com/apikey) and obtain your API key.

3. Set up your Gemini API Key as the environment variable

```bash
GOOGLE_API_KEY=your_api_key_here
```

4. Run the Streamlit App
```bash
streamlit run multimodal_agent.py
```
