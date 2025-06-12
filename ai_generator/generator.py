import requests
import yaml
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "codellama"
SCENARIO_DIR = "scenarios"

PROMPT = """
Generate a Kubernetes Deployment YAML with a subtle bug or misconfiguration.
Make the YAML syntactically valid but functionally broken.
Examples of bugs include: invalid image, missing environment variable, bad selector, invalid port, etc.
Do NOT explain anything. Only return the YAML.
"""

def generate_yaml():
    print("[*] Generating broken Kubernetes YAML using Ollama...")

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False
    })

    content = response.json()["response"]

    # Save to file
    filename = f"{SCENARIO_DIR}/generated_{datetime.now().isoformat(timespec='seconds')}.yaml"
    os.makedirs(SCENARIO_DIR, exist_ok=True)

    try:
        # Ensure it parses correctly (syntactically valid)
        parsed = list(yaml.safe_load_all(content))
        with open(filename, "w") as f:
            yaml.dump_all(parsed, f)
        print(f"[+] Saved generated YAML to {filename}")
        return filename
    except Exception as e:
        print("[!] Failed to parse generated YAML:", e)
        print("Raw Output:\n", content)
        return None
