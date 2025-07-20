from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.task_group import TaskGroup

# Imagem pública (ou privada, mas no Artifact Registry)
IMAGE_URI = "europe-west1-docker.pkg.dev/data-eng-dev-437916/pipelines/grupo-2-pipeline-app:latest"

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

with DAG(
    dag_id="pipeline_dag",
    default_args=default_args,
    schedule_interval="12 */4 * * *",
    catchup=False,
    max_active_runs=1,
    concurrency=5,
    description="Grupo 2: Pipeline principal de ingestão Carris Metropolitana",
    tags=["pipeline", "grupo-2"],
) as dag:

    with TaskGroup(
        "ingestion_tasks", tooltip="Ingestões individuais por dataset"
    ) as ingestion_group:

        ingest_vehicles = KubernetesPodOperator(
            task_id="ingest_vehicles",
            name="ingest-vehicles",
            namespace="default",
            image=IMAGE_URI,
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
            image=IMAGE_URI,
            cmds=["python", "-m", "app.main"],
            arguments=["--use-case", "ingest_municipalities"],
            get_logs=True,
            is_delete_operator_pod=True,
            env_vars={"APP_ENV": "production"},
        )

    ingest_all = KubernetesPodOperator(
        task_id="ingest_all",
        name="ingest-all",
        namespace="default",
        image=IMAGE_URI,
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "all"],
        get_logs=True,
        is_delete_operator_pod=True,
        env_vars={"APP_ENV": "production"},
    )

    ingest_all >> ingestion_group
