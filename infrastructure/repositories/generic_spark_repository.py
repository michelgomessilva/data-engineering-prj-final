import time

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

    def __init__(self, spark: SparkSession, schema: StructType):
        """
        Inicializa o repositório genérico com uma sessão Spark e um schema específico.

        Args:
            spark (SparkSession): Sessão Spark já configurada.
            schema (StructType): Esquema do DataFrame que será utilizado.
        """
        self.spark = spark
        self.schema = schema
        logger.info(
            f"GenericSparkRepository inicializado com schema: {self.schema.simpleString()}"
        )

    def to_dataframe(self, data: list) -> DataFrame:
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

        try:
            start = time.time()
            rdd = self.spark.sparkContext.parallelize(data)
            df = self.spark.createDataFrame(rdd, self.schema)
            duration = time.time() - start
            logger.info(f"DataFrame criado com sucesso em {duration:.2f} segundos.")
            return df
        except Exception as e:
            logger.error(
                f"Erro ao converter dados para DataFrame com schema: {self.schema.simpleString()}"
            )
            logger.exception(e)
            raise ValueError(f"Falha na conversão para DataFrame: {str(e)}")
