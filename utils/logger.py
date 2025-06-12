import json
import os
from datetime import datetime

LOG_FILE = "logs/history.json"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_scenario(manifest_path, issues):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "scenario": manifest_path,
        "issues": issues
    }

    # Load existing logs
    try:
        with open(LOG_FILE, "r") as f:
            history = json.load(f)
    except Exception:
        history = []

    history.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)
