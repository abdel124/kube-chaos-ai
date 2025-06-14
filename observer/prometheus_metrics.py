from prometheus_client import start_http_server, Counter

# Metrics
scenarios_generated = Counter(
    "scenarios_generated_total", "Total generated Kubernetes scenarios"
)

issues_detected = Counter(
    "issues_detected_total", "Total issues detected in deployed scenarios"
)

issue_type_counter = Counter(
    "issue_type_total", "Count of issue types", ["reason"]
)

def start_metrics_server(port=8001):
    start_http_server(port)
    print(f"[METRICS] Prometheus metrics server running on port {port}")
