from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_routes_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset routes a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_routes.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        upper(trim(col("route_id"))).alias("route_id"),
        upper(trim(col("agency_id"))).alias("agency_id"),
        upper(trim(col("line_id"))).alias("line_id"),
        upper(trim(col("circular"))).alias("circular"),
        upper(trim(col("line_long_name"))).alias("line_long_name"),
        upper(trim(col("line_short_name"))).alias("line_short_name"),
        upper(trim(col("path_type"))).alias("path_type"),
        upper(trim(col("route_color"))).alias("route_color"),
        upper(trim(col("route_long_name"))).alias("route_long_name"),
        upper(trim(col("route_short_name"))).alias("route_short_name"),
        upper(trim(col("route_text_color"))).alias("route_text_color"),
        upper(trim(col("route_type"))).alias("route_type"),
        upper(trim(col("school"))).alias("school"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(["route_id", "agency_id", "line_id"])

    logger.success("✅ Cleansing do gtfs_routes concluído.")
    return cleansed_df
