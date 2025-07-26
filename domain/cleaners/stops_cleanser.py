from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_stops_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset stops a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de stops.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        trim(col("stop_id")).alias("stop_id"),
        upper(trim(col("stop_name"))).alias("stop_name"),
        upper(trim(col("short_name"))).alias("short_name"),
        trim(col("district_id")).alias("district_id"),
        trim(col("municipality_id")).alias("municipality_id"),
        upper(trim(col("region_id"))).alias("region_id"),
        upper(trim(col("district_name"))).alias("district_name"),
        upper(trim(col("municipality_name"))).alias("municipality_name"),
        upper(trim(col("region_name"))).alias("region_name"),
        trim(col("latitude")).alias("latitude"),
        trim(col("longitude")).alias("longitude"),
        col("facilities"),
        col("lines"),
        upper(trim(col("locality"))).alias("localities"),
        upper(trim(col("operational_status"))).alias("operational_status"),
        col("patterns"),
        col("routes"),
        upper(trim(col("tts_name"))).alias("tts_name"),
        col("wheelchair_boarding"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(["stop_id"])

    logger.success("✅ Cleansing do stops concluído.")
    return cleansed_df
