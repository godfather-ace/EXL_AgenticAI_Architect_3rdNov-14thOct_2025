FROM python:3.11.12-slim-bullseye

ENV HOST=0.0.0.0

ENV LISTEN_PORT=8080

EXPOSE 8080

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pydantic-ai openai-agents nest-asyncio streamlit

CMD ["streamlit", "run", "app.py", "--server.port", "8080"]