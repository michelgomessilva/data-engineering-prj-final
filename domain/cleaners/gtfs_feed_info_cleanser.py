from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_feed_info_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_feed_info a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_feed_info.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        upper(trim(col("default_lang"))).alias("default_lang"),
        trim(col("feed_contact_url")).alias("feed_contact_url"),
        upper(trim(col("feed_end_date"))).alias("feed_end_date"),
        upper(trim(col("feed_lang"))).alias("feed_lang"),
        trim(col("feed_publisher_name")).alias("feed_publisher_name"),
        upper(trim(col("feed_publisher_url"))).alias("feed_publisher_url"),
        upper(trim(col("feed_start_date"))).alias("feed_start_date"),
        upper(trim(col("feed_version"))).alias("feed_version"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates()

    logger.success("✅ Cleansing do gtfs_feed_info concluído.")
    return cleansed_df
