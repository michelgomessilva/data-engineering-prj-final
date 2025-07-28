from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, row_number, split, substring, trim, upper
from pyspark.sql.window import Window

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
    # 1. Seleção e limpeza das colunas
    cleaned_df = df.select(
        trim(col("stop_id")).alias("stop_id"),
        upper(trim(col("trip_id"))).alias("trip_id"),
        col("arrival_time"),
        col("departure_time"),
        col("drop_off_type"),
        col("pickup_type"),
        col("shape_dist_traveled"),
        col("stop_sequence"),
        col("timepoint"),
        substring(upper(trim(col("trip_id"))), 1, 4).alias("line_id"),
        split(upper(trim(col("trip_id"))), "_|\\|").alias("trip_id_parts"),
        col("ingestion_date"),
        col("partition_date"),
    )

    logger.info(
        "Após selecionar e limpar colunas, temos {} registros.".format(
            cleaned_df.count()
        )
    )

    # 2. Definição da janela para deduplicar
    window_spec = Window.partitionBy("stop_id", "trip_id", "stop_sequence").orderBy(
        col("ingestion_date").desc()
    )

    logger.info(
        "Após definir a janela, temos {} partições.".format(window_spec.partitionBy)
    )

    # 3. Gera ranking por partição
    ranked_df = cleaned_df.withColumn("row_num", row_number().over(window_spec))

    logger.info("Após aplicar o ranking, temos {} registros.".format(ranked_df.count()))

    # 4. Mantém apenas a primeira ocorrência (mais recente)
    cleansed_df = ranked_df.filter(col("row_num") == 1).drop("row_num")

    logger.info(
        "Após filtrar por ocorrências únicas, temos {} registros.".format(
            cleansed_df.count()
        )
    )

    logger.success("✅ Cleansing do gtfs_stops concluído.")
    return cleansed_df
