"""
pipeline.py

DAG principal do Airflow para orquestrar o pipeline de ingestão de dados
da Carris Metropolitana, utilizando contêineres Docker executados via KubernetesPodOperator.

Funcionalidades:
- Cada tarefa representa um use case da aplicação e roda em um pod isolado.
- As imagens Docker são geradas pelo CI/CD e publicadas no Artifact Registry.
- Os pods são descartados após a execução (`is_delete_operator_pod=True`).
- Organização visual no Composer via TaskGroup.
- Possibilidade de execução de todos os use cases com uma única task (`--use-case all`).

Pré-requisitos:
- A imagem Docker da aplicação deve estar disponível em:
  europe-west1-docker.pkg.dev/data-eng-dev-437916/pipelines/grupo-2-pipeline-app:latest
- O DAG deve estar salvo no bucket do Composer em: gs://<COMPOSER_BUCKET>/dags/grupo_2/
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.task_group import TaskGroup

# Configurações globais
PROJECT_ID = "data-eng-dev-437916"
REGION = "europe-west1"
REPO = "pipelines"
IMAGE_NAME = "grupo-2-pipeline-app"
DOCKER_TAG = "latest"
ARTIFACT_IMAGE = f"ghcr.io/michelsilva/{IMAGE_NAME}:{DOCKER_TAG}"

# Argumentos padrão para todas as tasks
default_args = {
    "owner": "michelsilva",
    "depends_on_past": False,
    "email": ["michel.gomes.silva@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "start_date": datetime(2025, 7, 15),
}

# Criação da DAG principal
with DAG(
    dag_id="pipeline_dag",
    default_args=default_args,
    schedule_interval="12 */4 * * *",  # Executa a cada 4 horas, minuto 12
    catchup=False,
    max_active_runs=1,
    concurrency=5,
    description="Pipeline principal de ingestão Carris Metropolitana via Docker/K8s",
    tags=["pipeline", "grupo-2", "kubernetes", "docker"],
) as dag:

    # TaskGroup: Use Cases Individuais
    with TaskGroup(
        "ingestion_tasks", tooltip="Ingestões individuais por dataset"
    ) as ingestion_group:

        ingest_vehicles = KubernetesPodOperator(
            task_id="ingest_vehicles",
            name="ingest-vehicles",
            namespace="default",
            image=ARTIFACT_IMAGE,
            cmds=["python", "-m", "app.main"],
            arguments=["--use-case", "ingest_vehicles"],
            get_logs=True,
            is_delete_operator_pod=True,
            env_vars={"APP_ENV": "production"},
        )

        ingest_municipalities = KubernetesPodOperator(
            task_id="ingest_municipalities",
            name="ingest-municipalities",
            namespace="default",
            image=ARTIFACT_IMAGE,
            cmds=["python", "-m", "app.main"],
            arguments=["--use-case", "ingest_municipalities"],
            get_logs=True,
            is_delete_operator_pod=True,
            env_vars={"APP_ENV": "production"},
        )

        # (futuro)
        # ingest_stops = KubernetesPodOperator(...)

    # Task: Executa todos os use-cases de uma só vez
    ingest_all = KubernetesPodOperator(
        task_id="ingest_all",
        name="ingest-all",
        namespace="default",
        image=ARTIFACT_IMAGE,
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "all"],
        get_logs=True,
        is_delete_operator_pod=True,
        env_vars={"APP_ENV": "production"},
    )

    # Orquestração
    ingest_all >> ingestion_group
