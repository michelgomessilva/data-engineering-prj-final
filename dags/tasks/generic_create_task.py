from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import V1ResourceRequirements


def create_task(task_id, use_case, image, env_vars):
    return KubernetesPodOperator(
        task_id=task_id,
        name=task_id.replace("_", "-"),
        namespace="default",
        image=image,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", use_case],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars=env_vars,
        container_resources=V1ResourceRequirements(
            requests={"memory": "8Gi", "cpu": "4"},
            limits={"memory": "16Gi", "cpu": "8"},
        ),
    )
