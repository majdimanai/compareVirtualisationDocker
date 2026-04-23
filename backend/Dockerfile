
FROM python:3.11-slim


LABEL maintainer="SentimentIA"
LABEL description="Backend analyse de sentiment - Docker"


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY app.py .


ENV ENV_TYPE=docker
ENV ENV_NAME="Docker Container"


EXPOSE 8000


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
