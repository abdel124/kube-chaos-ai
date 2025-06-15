import subprocess

def apply_manifest(manifest_path: str):
    """
    Applies the given Kubernetes YAML manifest using kubectl.
    
    Args:
        manifest_path (str): Path to the YAML file to apply.
    """
    print(f"[Injector] Applying manifest: {manifest_path}")
    try:
        result = subprocess.run(
            ["kubectl", "apply", "-f", manifest_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[Injector] Success:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"[Injector] Error applying manifest:\n{e.stderr}")
