from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from datetime import datetime
from ai_generator.generator import generate_yaml
from failure_injector.injector import apply_manifest
from health_checker.checker import detect_crashloop
from utils.logger import log_scenario
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HISTORY_FILE = "logs/history.json"

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/scenarios")
def get_scenarios():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE) as f:
        return json.load(f)

@app.post("/generate")
def generate_and_apply():
    path = generate_yaml()
    if not path:
        return {"status": "error", "message": "Failed to generate YAML"}
    
    apply_manifest(path)
    issues = detect_crashloop()
    log_scenario(path, issues)
    return {
        "status": "generated",
        "file": path,
        "issues": issues
    }
