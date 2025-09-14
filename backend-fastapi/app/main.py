
from fastapi import FastAPI
from app.api.v1 import routes_resume
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import requests
import time


app = FastAPI(title="CareerLM Backend")

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3"

def is_ollama_running():
    try:
        r = requests.get(OLLAMA_HOST, timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def start_ollama():
    # Start ollama serve in a subprocess
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Wait for Ollama to be up
        for _ in range(30):
            if is_ollama_running():
                break
            time.sleep(1)
    except Exception as e:
        print(f"Could not start Ollama: {e}")

@app.on_event("startup")
def ensure_ollama_running():
    if not is_ollama_running():
        print("Ollama not running. Starting Ollama server...")
        start_ollama()
    else:
        print("Ollama server is already running.")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Resume Optimizer routes
app.include_router(routes_resume.router, prefix="/api/v1/resume", tags=["Resume"])
