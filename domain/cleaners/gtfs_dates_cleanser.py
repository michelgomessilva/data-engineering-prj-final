from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_dates_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_dates a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_dates.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        upper(trim(col("date"))).alias("date"),
        upper(trim(col("day_type"))).alias("day_type"),
        upper(trim(col("holiday"))).alias("holiday"),
        upper(trim(col("notes"))).alias("notes"),
        upper(trim(col("period"))).alias("period"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates()

    logger.success("✅ Cleansing do gtfs_dates concluído.")
    return cleansed_df
