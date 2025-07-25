from typing import Callable

from pyspark.sql import DataFrame

from configs.settings import Settings
from infrastructure.logging.logger import logger
from infrastructure.repositories.bigquery_writer import write_to_bigquery
from infrastructure.spark.spark_singleton import get_spark_session


class BaseCleanseRunner:
    """
    Classe base genérica para execução do pipeline de cleansing:
    - Leitura de dados raw em Parquet.
    - Aplicação de função de limpeza.
    - Escrita dos dados limpos no BigQuery.
    """

    def __init__(
        self,
        entity_name: str,
        file_name: str,
        cleanse_func: Callable[[object, str], DataFrame],
        bq_table: str,
    ):
        """
        :param entity_name: Nome da entidade (ex: "lines", "stops")
        :param file_name: Nome do arquivo Parquet (ex: "lines.parquet")
        :param cleanse_func: Função que recebe (spark, parquet_path) → DataFrame limpo
        :param bq_table: Nome da tabela de destino no BigQuery
        """
        self.entity_name = entity_name
        self.file_name = file_name
        self.cleanse_func = cleanse_func
        self.bq_table = bq_table

    def run(self):
        """
        Executa o pipeline completo de leitura → limpeza → gravação.
        """
        logger.info(
            f"Iniciando processo de cleansing da entidade '{self.entity_name}'..."
        )

        try:
            spark = get_spark_session()
            parquet_path = Settings.get_raw_path(self.file_name)
            logger.info(f"Lendo dados raw de: {parquet_path}")

            df_clean = self.cleanse_func(spark, parquet_path)
            logger.info(f"Dados de '{self.entity_name}' limpos com sucesso.")

            dataset = Settings.get_bq_dataset()
            logger.info(f"Gravando dados limpos no BigQuery: {dataset}.{self.bq_table}")
            write_to_bigquery(df_clean, dataset, self.bq_table)

            logger.success(
                f"Cleansing e carga da entidade '{self.entity_name}' concluídos com sucesso!"
            )

        except Exception as e:
            logger.exception(f"Erro ao processar a entidade '{self.entity_name}'")
            raise e
