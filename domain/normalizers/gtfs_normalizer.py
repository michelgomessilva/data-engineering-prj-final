from typing import Optional

from pyspark.sql import DataFrame, SparkSession


class GTFSNormalizer:
    """
    Normaliza arquivos GTFS (.txt extraídos do ZIP) diretamente como Spark DataFrames.

    Exemplo: stops.txt, routes.txt, trips.txt etc.
    """

    @staticmethod
    def normalize(
        spark: SparkSession, file_path: str, schema: Optional[object] = None
    ) -> DataFrame:
        """
        Lê um arquivo GTFS (.txt) como Spark DataFrame, detectando o delimitador.

        Args:
            spark (SparkSession): Sessão ativa do Spark
            file_path (str): Caminho do arquivo .txt extraído
            schema (StructType, opcional): Schema para aplicar na leitura

        Returns:
            DataFrame: DataFrame Spark com os dados carregados
        """
        with open(file_path, "r", encoding="utf-8") as f:
            sample = f.read(1024)
            delimiter = "\t" if "\t" in sample else ","

        df = (
            spark.read.option("delimiter", delimiter)
            .option("header", True)
            .option("inferSchema", schema is None)
            .csv(file_path, schema=schema)
        )

        return df
