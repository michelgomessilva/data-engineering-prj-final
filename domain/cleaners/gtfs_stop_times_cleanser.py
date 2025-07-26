from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_stop_times_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_stop_times a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_stop_times.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        trim(col("stop_id")).alias("stop_id"),
        upper(trim(col("stop_name"))).alias("stop_name"),
        upper(trim(col("stop_name_new"))).alias("stop_name_new"),
        upper(trim(col("stop_short_name"))).alias("stop_short_name"),
        trim(col("stop_lat")).alias("latitude"),
        trim(col("stop_lon")).alias("longitude"),
        upper(trim(col("operational_status"))).alias("operational_status"),
        trim(col("region_id")).alias("region_id"),
        upper(trim(col("region_name"))).alias("region_name"),
        trim(col("district_id")).alias("district_id"),
        upper(trim(col("district_name"))).alias("district_name"),
        trim(col("municipality_id")).alias("municipality_id"),
        upper(trim(col("municipality_name"))).alias("municipality_name"),
        upper(trim(col("locality"))).alias("localities"),
        trim(col("stop_code")).alias("stop_code"),
        upper(trim(col("tts_stop_name"))).alias("tts_stop_name"),
        upper(trim(col("location_type"))).alias("location_type"),
        upper(trim(col("near_hospital"))).alias("near_hospital"),
        upper(trim(col("near_school"))).alias("near_school"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(["stop_id"])

    logger.success("✅ Cleansing do gtfs_stop_times concluído.")
    return cleansed_df
