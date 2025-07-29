from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, expr, row_number, substring, trim, upper
from pyspark.sql.window import Window

from infrastructure.logging.logger import logger


def cleanse_gtfs_stop_times_df(spark: SparkSession, input_path: str) -> DataFrame:
    """
    Realiza o cleansing do dataset gtfs_stop_times a partir dos dados raw em Parquet.

    Aplica limpeza nas colunas principais, removendo espaços e aplicando
    formatação consistente (ex: UPPERCASE para nomes). Também gera colunas
    line_id, route_id e service_id a partir de trip_id.

    Args:
        spark (SparkSession): Sessão Spark ativa.
        input_path (str): Caminho no GCS para o arquivo Parquet de gtfs_stop_times.

    Returns:
        DataFrame: DataFrame transformado pronto para ser salvo no BigQuery.
    """
    logger.info(f"🔍 Lendo arquivo raw Parquet de: {input_path}")
    df = spark.read.parquet(input_path)

    logger.info("🧹 Limpando e padronizando colunas...")
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
        col("ingestion_date"),
        col("partition_date"),
    )

    logger.info(
        "Após selecionar e limpar colunas, temos {} registros.".format(
            cleaned_df.count()
        )
    )

    # Adiciona line_id (4 primeiros caracteres)
    cleaned_df = cleaned_df.withColumn("line_id", substring("trip_id", 1, 4)).alias(
        "line_id"
    )

    # Adiciona route_id (line_id + "_" + primeiro dígito após o primeiro "_")
    cleaned_df = cleaned_df.withColumn(
        "route_id", expr("concat(substring(trip_id, 1, 5), split(trip_id, '_')[1])")
    ).alias("route_id")

    # Adiciona service_id (regra condicional com pipe ou underscores)
    cleaned_df = cleaned_df.withColumn(
        "service_id",
        expr(
            """
            CASE
                WHEN trip_id LIKE '%|%' THEN
                    concat_ws('_',
                        slice(
                            split(translate(trip_id, '|', '_'), '_'),
                            -2,
                            2
                        )
                    )
                ELSE
                    concat_ws('_',
                        slice(
                            split(trip_id, '_'),
                            -3,
                            3
                        )
                    )
            END
        """
        ),
    ).alias("service_id")

    # Deduplicação por janela
    window_spec = Window.partitionBy("stop_id", "trip_id", "stop_sequence").orderBy(
        col("ingestion_date").desc()
    )

    ranked_df = cleaned_df.withColumn("row_num", row_number().over(window_spec))

    cleansed_df = ranked_df.filter(col("row_num") == 1).drop("row_num")

    logger.success(
        "✅ Cleansing do gtfs_stop_times concluído com line_id, route_id e service_id."
    )
    return cleansed_df
