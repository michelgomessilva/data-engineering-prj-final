from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_municipalities_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_municipalities a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_municipalities.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        upper(trim(col("district_id"))).alias("district_id"),
        upper(trim(col("district_name"))).alias("district_name"),
        upper(trim(col("municipality_id"))).alias("municipality_id"),
        upper(trim(col("municipality_name"))).alias("municipality_name"),
        upper(trim(col("municipality_prefix"))).alias("municipality_prefix"),
        upper(trim(col("region_id"))).alias("region_id"),
        upper(trim(col("region_name"))).alias("region_name"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(["district_id", "municipality_id", "region_id"])

    logger.success("✅ Cleansing do gtfs_municipalities concluído.")
    return cleansed_df
