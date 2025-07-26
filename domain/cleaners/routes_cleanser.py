from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_routes_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset routes a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de routes.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        trim(col("route_id")).alias("route_id"),
        trim(col("line_id")).alias("line_id"),
        trim(col("short_name")).alias("route_code"),
        upper(trim(col("long_name"))).alias("route_name"),
        upper(trim(col("color"))).alias("color"),
        upper(trim(col("text_color"))).alias("text_color"),
        upper(trim(col("localities"))).alias("localities"),
        col("municipalities"),
        col("patterns"),
        col("facilities"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(["route_id"])

    logger.success("✅ Cleansing do routes concluído.")
    return cleansed_df
