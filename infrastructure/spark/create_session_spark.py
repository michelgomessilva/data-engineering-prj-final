"""
Módulo responsável por configurar e retornar a SparkSession da aplicação.

Este módulo centraliza as configurações necessárias para integração com o Google Cloud Storage (GCS),
incluindo a utilização do conector GCS apropriado, além de parametrizar o nome da aplicação Spark.

A configuração desativa o uso explícito de autenticação por service account
(`spark.hadoop.google.cloud.auth.service.account.enable = false`),
assumindo que as credenciais estão disponíveis no ambiente padrão (ADC - Application Default Credentials).

A configuração padrão do pacote GCS conector utilizada aqui é:
- com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5

Uso:
    from infrastructure.spark.create_session_spark import get_spark_session
    spark = get_spark_session()
"""

from pyspark.sql import SparkSession

from configs.settings import Settings
from infrastructure.logging.logger import logger


def get_spark_session(app_name: str = Settings.APP_NAME) -> SparkSession:
    """
    Cria e retorna uma SparkSession com configurações adequadas para integração com GCS.

    Args:
        app_name (str): Nome da aplicação Spark (usado no UI e logs do Spark).

    Returns:
        SparkSession: Sessão Spark configurada.

    """
    logger.info(f"SparkSession criada com nome: {app_name}")

    session = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.hadoop.hadoop.security.authentication", "simple")
        .config(
            "spark.driver.extraJavaOptions",
            "--add-opens java.base/javax.security.auth=ALL-UNNAMED",
        )
        .getOrCreate()
    )

    logger.info("SparkSession criada com sucesso")
    return session
