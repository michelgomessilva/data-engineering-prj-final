"""
Módulo responsável por criar operadores KubernetesPodOperator
padronizados para execução de use-cases Python no Airflow.
"""

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import V1ResourceRequirements


def create_task(task_id, use_case, image, env_vars):
    """
    Cria uma task do Airflow baseada no KubernetesPodOperator para executar
    um use-case Python com argumentos e recursos pré-definidos.

    Args:
        task_id (str): Identificador único da task no Airflow.
        use_case (str): Nome do use-case a ser passado como argumento para a aplicação.
        image (str): Imagem Docker que será usada no container.
        env_vars (dict): Variáveis de ambiente a serem passadas para o container.

    Returns:
        KubernetesPodOperator: Instância configurada da task para uso na DAG.
    """
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
