import time
from typing import Dict, List, Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from infrastructure.logging.logger import logger


class GenericSparkRepository:
    """
    Repositório genérico para converter dados em DataFrames com um schema definido dinamicamente.

    Essa classe pode ser reutilizada para diferentes domínios (ex: veículos, paragens, linhas),
    bastando fornecer o schema correspondente na inicialização.

    Attributes:
        spark (SparkSession): Sessão Spark usada para criação de DataFrames.
        schema (StructType): Esquema Spark que define a estrutura do DataFrame.
    """

    def __init__(self, spark: SparkSession, schema: Optional[StructType] = None):
        """
        Inicializa o repositório genérico com uma sessão Spark e um schema específico.

        Args:
            spark (SparkSession): Sessão Spark já configurada.
            schema (StructType): Esquema do DataFrame que será utilizado.
        """
        self.spark = spark
        self.schema = schema
        if self.schema:
            logger.debug(
                f"GenericSparkRepository inicializado com schema: {self.schema.simpleString()}"
            )
        else:
            logger.warning(
                "GenericSparkRepository inicializado sem schema fixo. Será necessário "
                "passar schema dinamicamente no método to_dataframe."
            )

    def to_dataframe(
        self, data: List[Dict], schema: Optional[StructType] = None
    ) -> DataFrame:
        """
        Converte uma lista de dicionários em um DataFrame Spark com o schema especificado.

        Args:
            data (list): Lista de registros (dicionários) com os dados a serem convertidos.

        Returns:
            DataFrame: DataFrame Spark estruturado conforme o schema fornecido.

        Raises:
            ValueError: Se os dados estiverem vazios ou se a conversão falhar.
        """
        logger.info(
            f"Iniciando conversão de {len(data)} registros para DataFrame Spark."
        )
        if not data:
            logger.warning(
                "Lista de dados vazia recebida. Nenhum DataFrame será criado."
            )
            raise ValueError("A lista de dados fornecida está vazia.")

        effective_schema = schema or self.schema
        if not effective_schema:
            raise ValueError("Nenhum schema fornecido.")

        try:
            start = time.time()
            # num_partitions = max(100, len(data) // 1000)
            # logger.info(f"Usando {num_partitions} slices para paralelização.")
            # rdd = self.spark.sparkContext.parallelize(data, numSlices=num_partitions)
            rdd = self.spark.sparkContext.parallelize(data)
            df = self.spark.createDataFrame(rdd, self.schema)
            duration = time.time() - start
            logger.info(f"DataFrame criado com sucesso em {duration:.2f} segundos.")
            return df
        except Exception as e:
            schema_str = self.schema.simpleString() if self.schema else "None"
            logger.error(
                f"Erro ao converter dados para DataFrame com schema: {schema_str}"
            )
            logger.exception(e)
            raise ValueError(f"Falha na conversão para DataFrame: {str(e)}")
