from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time, os, platform, psutil


app = FastAPI(title="SentimentIA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()

ENV_TYPE = os.getenv("ENV_TYPE", "docker")
ENV_NAME = os.getenv("ENV_NAME", "Docker Container")


class TextInput(BaseModel):
    text: str


def get_system_metrics():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    return {
        "cpu_percent": cpu,
        "ram_total_mb": round(ram.total / 1024 / 1024, 1),
        "ram_used_mb": round(ram.used / 1024 / 1024, 1),
        "ram_percent": ram.percent,
        "ram_available_mb": round(ram.available / 1024 / 1024, 1),
    }


@app.get("/")
def root():
    return {
        "status": "ok",
        "env": ENV_TYPE,
        "env_name": ENV_NAME,
        "hostname": platform.node(),
    }


@app.get("/health")
def health():
    return {"status": "healthy", "env": ENV_TYPE}


@app.get("/metrics")
def metrics():
    return {"env": ENV_TYPE, "env_name": ENV_NAME, **get_system_metrics()}


@app.post("/analyze")
def analyze(input: TextInput):
    start = time.time()
    scores = analyzer.polarity_scores(input.text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment, emoji = "POSITIF", "😊"
    elif compound <= -0.05:
        sentiment, emoji = "NÉGATIF", "😞"
    else:
        sentiment, emoji = "NEUTRE", "😐"

    elapsed_ms = round((time.time() - start) * 1000, 2)

    return {
        "sentiment": sentiment,
        "emoji": emoji,
        "score": round(compound, 4),
        "details": {
            "positif": round(scores["pos"], 4),
            "négatif": round(scores["neg"], 4),
            "neutre": round(scores["neu"], 4),
        },
        "latency_ms": elapsed_ms,
        "env": ENV_TYPE,
        "env_name": ENV_NAME,
        "hostname": platform.node(),
        "words": len(input.text.split()),
        "system": get_system_metrics(),
    }