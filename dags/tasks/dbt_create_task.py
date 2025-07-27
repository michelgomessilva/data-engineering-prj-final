"""
Módulo responsável por criar uma task do Airflow para execução do comando `dbt run`
dentro de um container Kubernetes no Composer.
"""

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import V1ResourceRequirements


def create_dbt_run_task(image, env_vars):
    """
    Cria uma task do Airflow baseada no KubernetesPodOperator para executar
    o comando `dbt run` dentro de um container com imagem pré-configurada.

    Args:
        image (str): Imagem Docker contendo o dbt instalado.
        env_vars (dict): Variáveis de ambiente, incluindo as credenciais GCP.

    Returns:
        KubernetesPodOperator: Task configurada para execução do dbt.
    """
    return KubernetesPodOperator(
        task_id="dbt_run",
        name="dbt-run",
        namespace="default",
        image=image,
        image_pull_policy="Always",
        cmds=["dbt"],
        arguments=["run", "--project-dir", "/app/dbt", "--profiles-dir", "/app/dbt"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars=env_vars,
        container_resources=V1ResourceRequirements(
            requests={"memory": "2Gi", "cpu": "1"},
            limits={"memory": "4Gi", "cpu": "2"},
        ),
    )
