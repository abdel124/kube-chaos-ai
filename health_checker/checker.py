from utils.kube_client import get_core_v1_client

def detect_crashloop():
    v1 = get_core_v1_client()
    pods = v1.list_pod_for_all_namespaces(watch=False)

    issues = []
    for pod in pods.items:
        statuses = pod.status.container_statuses
        if statuses:
            for container in statuses:
                state = container.state
                if state and state.waiting and state.waiting.reason in [
                    "CrashLoopBackOff", "ErrImagePull", "ImagePullBackOff"
                ]:
                    issues.append({
                        "pod": pod.metadata.name,
                        "namespace": pod.metadata.namespace,
                        "reason": state.waiting.reason,
                    })

    return issues
