from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_periods_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_periods a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_periods.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        upper(trim(col("period_id"))).alias("period_id"),
        upper(trim(col("period_name"))).alias("period_name"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates()

    logger.success("✅ Cleansing do gtfs_periods concluído.")
    return cleansed_df
