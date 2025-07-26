from infrastructure.logging.logger import logger


def write_to_bigquery(df, dataset: str, table: str) -> None:
    """
    Escreve um DataFrame Spark no BigQuery usando o conector nativo.

    Args:
        df (DataFrame): DataFrame Spark a ser salvo.
        dataset (str): Nome do dataset no BigQuery.
        table (str): Nome da tabela de destino.

    Raises:
        Exception: Se a escrita falhar.
    """
    full_table = f"{dataset}.{table}"
    logger.info(f"Iniciando escrita no BigQuery: {full_table}")

    try:
        df.write.format("bigquery").option("table", full_table).option(
            "writeMethod", "direct"
        ).option("writeDisposition", "WRITE_TRUNCATE").option(
            "parentProject", "data-eng-dev-437916"
        ).mode(
            "overwrite"
        ).save()

        logger.success(f"Escrita concluída com sucesso: {full_table}")

    except Exception as e:
        logger.error(f"Falha ao gravar no BigQuery: {e}")
        raise
