from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_lines_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset lines a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de lines.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        trim(col("line_id")).alias("line_id"),
        upper(trim(col("short_name"))).alias("line_code"),
        upper(trim(col("long_name"))).alias("line_name"),
        trim(col("color")).alias("color"),
        trim(col("text_color")).alias("text_color"),
        col("localities"),
        col("municipalities"),
        col("routes"),
        col("patterns"),
        col("facilities"),
        col("date"),
    ).dropDuplicates(["line_id"])

    logger.success("✅ Cleansing do lines concluído.")
    return cleansed_df
