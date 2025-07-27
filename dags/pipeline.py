from datetime import datetime, timedelta

from airflow import DAG
from tasks.dbt_create_task import create_dbt_run_task
from tasks.generic_create_task import create_task

IMAGE_URI = "__IMAGE_PLACEHOLDER__"
ENV_VARS = {
    "APP_ENV": "production",
    "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
}

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
    description="Grupo 2: Pipeline principal.",
    tags=["pipeline", "grupo-2"],
) as dag:

    # Tarefas de ingestão
    ingest_vehicles = create_task(
        "ingest_vehicles", "ingest_vehicles", IMAGE_URI, ENV_VARS
    )
    ingest_municipalities = create_task(
        "ingest_municipalities", "ingest_municipalities", IMAGE_URI, ENV_VARS
    )
    ingest_lines = create_task("ingest_lines", "ingest_lines", IMAGE_URI, ENV_VARS)
    ingest_routes = create_task("ingest_routes", "ingest_routes", IMAGE_URI, ENV_VARS)
    ingest_stops = create_task("ingest_stops", "ingest_stops", IMAGE_URI, ENV_VARS)
    ingest_gtfs = create_task("ingest_gtfs", "ingest_gtfs", IMAGE_URI, ENV_VARS)

    # Tarefa de limpeza
    cleanse_lines = create_task("cleanse_lines", "cleanse_lines", IMAGE_URI, ENV_VARS)
    dbt_run = create_dbt_run_task(IMAGE_URI, ENV_VARS)

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
