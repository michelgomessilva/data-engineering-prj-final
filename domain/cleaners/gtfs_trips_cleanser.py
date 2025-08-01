from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_trips_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_trips a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_trips.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        upper(trim(col("trip_id"))).alias("trip_id"),
        upper(trim(col("route_id"))).alias("route_id"),
        upper(trim(col("pattern_id"))).alias("pattern_id"),
        upper(trim(col("shape_id"))).alias("shape_id"),
        upper(trim(col("service_id"))).alias("service_id"),
        upper(trim(col("direction_id"))).alias("direction_id"),
        upper(trim(col("trip_headsign"))).alias("trip_headsign"),
        upper(trim(col("calendar_desc"))).alias("calendar_desc"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(["trip_id", "route_id", "pattern_id", "shape_id", "service_id"])

    logger.success("✅ Cleansing do gtfs_trips concluído.")
    return cleansed_df
