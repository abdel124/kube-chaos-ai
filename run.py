import subprocess
import time
from health_checker.checker import detect_crashloop
from ai_generator.generator import generate_yaml
from utils.logger import log_scenario
from observer.prometheus_metrics import (
    scenarios_generated, issues_detected, issue_type_counter, start_metrics_server
)

def apply_manifest(yaml_path):
    print(f"Applying manifest: {yaml_path}")
    subprocess.run(["kubectl", "apply", "-f", yaml_path], check=True)

if __name__ == "__main__":
    start_metrics_server()
    path = generate_yaml()
    scenarios_generated.inc()
    if not path:
        print("❌ Skipping deployment due to invalid YAML.")
        exit(1)

    apply_manifest(path)

    print("\nChecking for issues...")
    issues = detect_crashloop()

    if issues:
        print("🚨 Detected issues:")
        for issue in issues:
            issues_detected.inc()
            issue_type_counter.labels(reason=issue["reason"]).inc()
            print(f"Pod: {issue['pod']} | NS: {issue['namespace']} | Reason: {issue['reason']}")
    else:
        print("✅ No issues detected.")
    time.sleep(30)

    log_scenario(path, issues)
