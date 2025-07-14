# infrastructure/storage/parquet_storage.py

"""
Módulo responsável pelo armazenamento de DataFrames do PySpark no formato Parquet,
com suporte a coalescência de arquivos, particionamento por colunas e leitura da
base path via variáveis centralizadas em configurações.

Esta classe é utilizada para persistência de dados nas diferentes camadas do
data lake, como raw, bronze, silver, etc.
"""

import time
from typing import List, Optional

from pyspark.sql import DataFrame

from configs.settings import Settings
from infrastructure.logging.logger import logger


class ParquetStorage:
    """
    Classe responsável por salvar DataFrames do PySpark no formato Parquet em um
    caminho configurado, como Google Cloud Storage (GCS) ou sistema local.

    Attributes:
        base_path (str): Caminho base onde os dados serão armazenados.
                         É definido por `Settings.GCS_BASE_PATH`.

    Raises:
        ValueError: Se a configuração de caminho base estiver ausente.
    """

    def __init__(self):
        self.base_path = Settings.GCS_BASE_PATH
        if not self.base_path:
            logger.error("GCS_BASE_PATH não está configurado nos Settings.")
            raise ValueError("GCS_BASE_PATH não está configurado nos Settings.")
        logger.info(f"ParquetStorage inicializado com base_path: {self.base_path}")

    def save(
        self,
        df: DataFrame,
        relative_path: str,
        mode: str = "overwrite",
        partition_by: Optional[List[str]] = None,
        coalesce: Optional[int] = 1,
    ):
        """
        Salva um DataFrame como arquivo Parquet.

        Args:
            df (DataFrame): O DataFrame do PySpark a ser salvo.
            relative_path (str): Caminho relativo à base_path onde os arquivos serão gravados.
                                 Exemplo: "raw/vehicles/".
            mode (str): Modo de escrita ("overwrite", "append", etc.). Default: "overwrite".
            partition_by (List[str], opcional): Colunas pelas quais os dados serão particionados.
            coalesce (int, opcional): Número de arquivos a serem gerados após coalesce. Default: 1.

        Raises:
            Exception: Qualquer erro que ocorra durante o processo de gravação.
        """
        # full_path = os.path.join(self.base_path, relative_path)
        full_path = relative_path
        logger.info(f"Iniciando salvamento do DataFrame no caminho: {full_path}")
        logger.debug(
            f"Modo: {mode} | PartitionBy: {partition_by} | Coalesce: {coalesce}"
        )

        try:
            start = time.time()
            num_partitions = coalesce if coalesce is not None else 1
            writer = df.coalesce(num_partitions).write.mode(mode)
            if partition_by:
                writer = writer.partitionBy(*partition_by)
            writer.parquet(full_path)
            duration = time.time() - start
            logger.info(f"DataFrame salvo com sucesso em {duration:.2f} segundos.")
        except Exception as e:
            logger.error(f"Erro ao salvar DataFrame em {full_path}")
            logger.exception(e)
            raise
