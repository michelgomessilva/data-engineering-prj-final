from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.kubernetes.volume import Volume
from airflow.kubernetes.volume_mount import VolumeMount
from airflow.utils.task_group import TaskGroup

# Configurações globais
PROJECT_ID = "data-eng-dev-437916"
REGION = "europe-west1"
IMAGE_NAME = "grupo-2-pipeline-app"
DOCKER_TAG = "latest"
ARTIFACT_IMAGE = f"ghcr.io/michelsilva/{IMAGE_NAME}:{DOCKER_TAG}"
DOCKER_CONFIG_PATH = "/root/.docker"

# Volume para montar config.json
volume_mount = VolumeMount(
    name="docker-config-volume",
    mount_path=DOCKER_CONFIG_PATH,
    sub_path=None,
    read_only=True,
)

volume = Volume(
    name="docker-config-volume",
    configs={
        "gcs": {
            "bucket": "europe-west1-airflow-196fdba9-bucket",
            "object": "data/grupo-2/docker_auth_config.json",
            "path": f"{DOCKER_CONFIG_PATH}/config.json",  # onde o arquivo será montado
        }
    },
)

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
    schedule_interval="12 */4 * * *",  # Executa a cada 4 horas
    catchup=False,
    max_active_runs=1,
    concurrency=5,
    description="Grupo 2: Pipeline principal de ingestão Carris Metropolitana",
    tags=["pipeline", "grupo-2"],
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
            volume_mounts=[volume_mount],
            volumes=[volume],
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
            volume_mounts=[volume_mount],
            volumes=[volume],
        )

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
        volume_mounts=[volume_mount],
        volumes=[volume],
    )

    # Orquestração
    ingest_all >> ingestion_group
