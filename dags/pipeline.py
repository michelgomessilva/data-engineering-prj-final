"""
Grupo 2: Pipeline principal de ingestão e transformação de dados da Carris Metropolitana.

Esta DAG realiza a orquestração das seguintes etapas:
1. Ingestão de múltiplas fontes (vehicles, municipalities, lines, routes, stops).
2. Ingestão consolidada do pacote GTFS.
3. Limpeza (cleanse) dos dados ingeridos.
4. Execução do dbt para modelagem e transformação.

Executada automaticamente a cada 4 horas, aos 12 minutos.
"""

from datetime import datetime, timedelta

from airflow import DAG
from grupo_2.tasks.dbt_create_task import create_dbt_run_task
from grupo_2.tasks.generic_create_task import create_task

# Imagem Docker publicada com todos os pacotes necessários (Spark, DBT etc.)
IMAGE_URI = "__IMAGE_PLACEHOLDER__"

# Variáveis de ambiente padrão para todas as tasks
ENV_VARS = {
    "APP_ENV": "production",
    "GOOGLE_APPLICATION_CREDENTIALS": "/app/gcp-key.json",
}

# Argumentos padrão usados por todas as tasks
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

# Instância da DAG
with DAG(
    dag_id="grupo_2_pipeline",
    default_args=default_args,
    schedule_interval="12 */4 * * *",  # Executa a cada 4 horas, aos 12 minutos
    catchup=False,
    max_active_runs=1,
    concurrency=3,
    description="Grupo 2: Pipeline principal de ingestão e transformação da Carris Metropolitana.",
    tags=["pipeline", "grupo-2"],
) as dag:

    # 1. Tarefas de ingestão de dados brutos por tipo
    ingest_vehicles = create_task(
        "ingest_vehicles", "ingest_vehicles", IMAGE_URI, ENV_VARS
    )
    ingest_municipalities = create_task(
        "ingest_municipalities", "ingest_municipalities", IMAGE_URI, ENV_VARS
    )
    ingest_lines = create_task("ingest_lines", "ingest_lines", IMAGE_URI, ENV_VARS)
    ingest_routes = create_task("ingest_routes", "ingest_routes", IMAGE_URI, ENV_VARS)
    ingest_stops = create_task("ingest_stops", "ingest_stops", IMAGE_URI, ENV_VARS)

    # 2. Ingestão consolidada via GTFS
    ingest_gtfs = create_task("ingest_gtfs", "ingest_gtfs", IMAGE_URI, ENV_VARS)

    # 3. Limpeza e normalização dos dados
    cleanse_lines = create_task("cleanse_lines", "cleanse_lines", IMAGE_URI, ENV_VARS)
    cleanse_municipalities = create_task(
        "cleanse_municipalities", "cleanse_municipalities", IMAGE_URI, ENV_VARS
    )
    cleanse_stops = create_task("cleanse_stops", "cleanse_stops", IMAGE_URI, ENV_VARS)
    cleanse_routes = create_task(
        "cleanse_routes", "cleanse_routes", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_stops = create_task(
        "cleanse_gtfs_stops", "cleanse_gtfs_stops", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_stop_times = create_task(
        "cleanse_gtfs_stop_times", "cleanse_gtfs_stop_times", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_shapes = create_task(
        "cleanse_gtfs_shapes", "cleanse_gtfs_shapes", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_trips = create_task(
        "cleanse_gtfs_trips", "cleanse_gtfs_trips", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_periods = create_task(
        "cleanse_gtfs_periods", "cleanse_gtfs_periods", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_routes = create_task(
        "cleanse_gtfs_routes", "cleanse_gtfs_routes", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_municipalities = create_task(
        "cleanse_gtfs_municipalities",
        "cleanse_gtfs_municipalities",
        IMAGE_URI,
        ENV_VARS,
    )
    cleanse_gtfs_feed_info = create_task(
        "cleanse_gtfs_feed_info", "cleanse_gtfs_feed_info", IMAGE_URI, ENV_VARS
    )
    cleanse_gtfs_calendar_dates = create_task(
        "cleanse_gtfs_calendar_dates",
        "cleanse_gtfs_calendar_dates",
        IMAGE_URI,
        ENV_VARS,
    )
    cleanse_gtfs_dates = create_task(
        "cleanse_gtfs_dates", "cleanse_gtfs_dates", IMAGE_URI, ENV_VARS
    )

    # 4. Execução do dbt para transformação final dos dados
    dbt_run = create_dbt_run_task(IMAGE_URI, ENV_VARS)

    # Encadeamento das tarefas
    (
        [
            ingest_vehicles,
            ingest_municipalities,
            ingest_lines,
            ingest_routes,
            ingest_stops,
        ]
        >> ingest_gtfs
        >> [
            cleanse_lines,
            cleanse_municipalities,
            cleanse_stops,
            cleanse_routes,
        ]
        >> [
            cleanse_gtfs_periods,
            cleanse_gtfs_routes,
            cleanse_gtfs_municipalities,
            cleanse_gtfs_feed_info,
            cleanse_gtfs_calendar_dates,
            cleanse_gtfs_dates,
        ]
        >> cleanse_gtfs_stops
        >> cleanse_gtfs_trips
        >> cleanse_gtfs_stop_times
        >> cleanse_gtfs_shapes
        >> dbt_run
    )
