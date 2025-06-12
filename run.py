import subprocess
from health_checker.checker import detect_crashloop
from ai_generator.generator import generate_yaml

def apply_manifest(yaml_path):
    print(f"Applying manifest: {yaml_path}")
    subprocess.run(["kubectl", "apply", "-f", yaml_path], check=True)

if __name__ == "__main__":
    path = generate_yaml()
    if not path:
        print("❌ Skipping deployment due to invalid YAML.")
        exit(1)
    apply_manifest(path)

    print("\nChecking for issues...")
    issues = detect_crashloop()
    if issues:
        print("Detected issues:")
        for issue in issues:
            print(f"🚨 Pod: {issue['pod']} in ns: {issue['namespace']} | Reason: {issue['reason']}")
    else:
        print("✅ No issues detected.")
