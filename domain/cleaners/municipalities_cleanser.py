from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_municipalities_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset municipalities a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de municipalities.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        trim(col("municipality_id")),
        upper(trim(col("municipality_name"))),
        trim(col("district_id")),
        trim(col("region_id")),
        upper(trim(col("district_name"))),
        upper(trim(col("region_name"))),
        col("prefix"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(["municipality_id"])

    logger.success("✅ Cleansing do municipalities concluído.")
    return cleansed_df
