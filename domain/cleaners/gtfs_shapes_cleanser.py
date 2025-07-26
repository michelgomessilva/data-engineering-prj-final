from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, trim, upper

from infrastructure.logging.logger import logger


def cleanse_gtfs_shapes_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_shapes a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes).

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_shapes.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
    cleansed_df = df.select(
        trim(col("shape_id")).alias("shape_id"),
        upper(trim(col("shape_pt_lat"))).alias("latitude"),
        upper(trim(col("shape_pt_lon"))).alias("longitude"),
        upper(trim(col("shape_dist_traveled"))).cast("float").alias("distance"),
        trim(col("shape_pt_sequence")).alias("sequence"),
        col("ingestion_date"),
        col("partition_date"),
    ).dropDuplicates(
        [
            "shape_id",
            "latitude",
            "longitude",
            "distance",
            "sequence",
        ]
    )

    logger.success("✅ Cleansing do gtfs_shapes concluído.")
    return cleansed_df
