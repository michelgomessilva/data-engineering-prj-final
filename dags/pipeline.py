"""
pipeline.py

DAG principal do Airflow para orquestrar o pipeline de ingestão de dados
da Carris Metropolitana.

Esta DAG executa uma tarefa de ingestão (`ingest_task`) que:
- Consome dados da API da Carris.
- Normaliza e transforma os dados com Spark.
- Salva os dados em formato Parquet.
- Faz o upload dos dados particionados para o GCS na camada `raw`.

A DAG pode ser agendada de forma periódica ou executada sob demanda.

Pré-requisitos:
- O código do projeto deve estar disponível no bucket do Composer (pasta `dags/` ou `data/`).
- A pasta `/home/airflow/gcs/data` deve conter todo o projeto Python.
"""

import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Adiciona o caminho da raiz do projeto ao sys.path para permitir imports
project_path = "/home/airflow/gcs/data/grupo-2"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Importa a função de ingestão
from application.use_cases.ingest_vehicles import run_ingest_vehicles

# Argumentos padrão para a DAG
default_args = {
    "owner": "michel",
    "start_date": datetime(2025, 7, 15),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Definição da DAG
with DAG(
    dag_id="pipeline_dag",
    default_args=default_args,
    schedule_interval=None,  # Altere para "@daily" se desejar execução periódica
    catchup=False,
    description="Pipeline principal: Ingestão de dados Carris - Grupo 2",
    tags=["pipeline", "vehicles", "grupo-2"],
) as dag:

    # Task de ingestão de dados
    ingest_task = PythonOperator(
        task_id="ingest_vehicles", python_callable=run_ingest_vehicles
    )

    # Futuras tasks (ex: transform_task, load_task) podem ser adicionadas aqui

    ingest_task
