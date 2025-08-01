import time

from infrastructure.logging.logger import logger


def write_to_bigquery(
    df,
    dataset: str,
    table: str,
    mode: str = "overwrite",  # overwrite ou append
    partition_field: (
        str | None
    ) = None,  # nome da coluna de partição (ex: "partition_date")
) -> None:
    """
    Escreve um DataFrame Spark no BigQuery com suporte a:
    - Escrita 'overwrite' ou 'append'
    - Particionamento por coluna de data
    - Reparticionamento dinâmico
    - Medição de tempo de execução

    Args:
        df (DataFrame): DataFrame Spark a ser salvo.
        dataset (str): Nome do dataset no BigQuery.
        table (str): Nome da tabela de destino.
        mode (str): Modo de escrita: "overwrite" ou "append". Default: "overwrite".
        partition_field (str | None): Nome da coluna usada como campo de partição (se houver).
    """
    full_table = f"{dataset}.{table}"
    logger.info(f"Iniciando escrita no BigQuery: {full_table}")

    try:
        # Mede o tempo de início
        start_time = time.perf_counter()

        # Calcula número de partições dinamicamente (1 partição por ~1 milhão de registros, mínimo 4)
        record_count = df.count()
        num_partitions = max(4, record_count // 1000000)
        logger.info(
            f"Total de registros: {record_count} — particionando em {num_partitions} partições..."
        )
        df = df.repartition(num_partitions)

        writer = (
            df.write.format("bigquery")
            .option("table", full_table)
            .option("writeMethod", "indirect")
            .option("parentProject", "data-eng-dev-437916")
            .option("temporaryGcsBucket", "europe-west1-airflow-196fdba9-bucket")
            .option("temporaryGcsPath", "data/grupo-2")
            .mode(mode)
        )
        # .option("temporaryGcsBucket", "data-eng-dev-437916-staging")

        if mode == "overwrite":
            writer = writer.option("writeDisposition", "WRITE_TRUNCATE")
        elif mode == "append":
            writer = writer.option("writeDisposition", "WRITE_APPEND")

        if partition_field:
            writer = writer.option("partitionField", partition_field)

        writer.save()

        elapsed = time.perf_counter() - start_time
        logger.success(
            f"Escrita no BigQuery concluída com sucesso em {elapsed:.2f} segundos: {full_table}"
        )

    except Exception as e:
        logger.error(f"Falha ao gravar no BigQuery: {e}")
        raise
