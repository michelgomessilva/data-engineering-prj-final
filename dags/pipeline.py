from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

# Imagem pública no Docker Hub (sem autenticação necessária)
IMAGE_URI = "michelgomessilvax/grupo-2-pipeline-app:latest"

# Parâmetros padrão para todas as tasks
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

# Definição da DAG
with DAG(
    dag_id="grupo_2_pipeline",
    default_args=default_args,
    schedule_interval="12 */4 * * *",  # Executa a cada 4 horas às 12min
    catchup=False,
    max_active_runs=1,
    concurrency=5,
    description="Grupo 2: Pipeline principal de ingestão Carris Metropolitana",
    tags=["pipeline", "grupo-2"],
) as dag:

    # Task única que executa todos os use cases
    ingest_all = KubernetesPodOperator(
        task_id="ingest_all",
        name="ingest-all",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "all"],
        get_logs=True,
        is_delete_operator_pod=True,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
    )

    ingest_all
