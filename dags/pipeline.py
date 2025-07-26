from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import V1ResourceRequirements

IMAGE_URI = "__IMAGE_PLACEHOLDER__"

# Parâmetros padrão para todas as tasks
default_args = {
    "owner": "michelsilva",
    "depends_on_past": False,
    "email": ["michel.gomes.silva@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 7, 15),
}

# Definição da DAG
with DAG(
    dag_id="grupo_2_pipeline",
    default_args=default_args,
    schedule_interval="12 */4 * * *",  # Executa a cada 4 horas às 12min
    catchup=False,
    max_active_runs=1,
    concurrency=10,
    description="Grupo 2: Pipeline principal de ingestão Carris Metropolitana",
    tags=["pipeline", "grupo-2"],
) as dag:

    ingest_vehicles = KubernetesPodOperator(
        task_id="ingest_vehicles",
        name="ingest_vehicles",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "ingest_vehicles"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
    )

    ingest_municipalities = KubernetesPodOperator(
        task_id="ingest_municipalities",
        name="ingest_municipalities",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "ingest_municipalities"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
    )

    ingest_lines = KubernetesPodOperator(
        task_id="ingest_lines",
        name="ingest_lines",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "ingest_lines"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
    )

    ingest_routes = KubernetesPodOperator(
        task_id="ingest_routes",
        name="ingest_routes",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "ingest_routes"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
    )

    ingest_stops = KubernetesPodOperator(
        task_id="ingest_stops",
        name="ingest_stops",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "ingest_stops"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
    )

    ingest_gtfs = KubernetesPodOperator(
        task_id="ingest_gtfs",
        name="ingest-gtfs",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "ingest_gtfs"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
        container_resources=V1ResourceRequirements(
            requests={"memory": "8Gi", "cpu": "4"},
            limits={"memory": "16Gi", "cpu": "8"},
        ),
    )

    cleanse_lines = KubernetesPodOperator(
        task_id="cleanse_lines",
        name="cleanse-lines",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["python", "-m", "app.main"],
        arguments=["--use-case", "cleanse_lines"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
    )

    dbt_run = KubernetesPodOperator(
        task_id="dbt_run",
        name="dbt-run",
        namespace="default",
        image=IMAGE_URI,
        image_pull_policy="Always",
        cmds=["dbt"],
        arguments=["run", "--project-dir", "/app/dbt", "--profiles-dir", "/app/dbt"],
        get_logs=True,
        is_delete_operator_pod=True,
        log_events_on_failure=False,
        env_vars={
            "APP_ENV": "production",
            "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
        },
        container_resources=V1ResourceRequirements(
            requests={"memory": "2Gi", "cpu": "1"},
            limits={"memory": "4Gi", "cpu": "2"},
        ),
    )

    (
        [
            ingest_vehicles,
            ingest_municipalities,
            ingest_lines,
            ingest_routes,
            ingest_stops,
        ]
        >> ingest_gtfs
        >> cleanse_lines
        >> dbt_run
    )
