"""
IngestLinesService

Classe responsável por orquestrar o processo de ingestão de dados brutos (raw)
de veículos da API da Carris Metropolitana,
normalizar os dados, convertê-los em DataFrame do Spark, e armazená-los em
formato Parquet no Google Cloud Storage (GCS),
organizados em partições diárias.

Responsabilidades:
- Buscar os dados da API externa definida no settings (endpoint de lines).
- Normalizar os dados JSON em um formato tabular.
- Converter para Spark DataFrame.
- Adicionar metadados como a data de ingestão.
- Salvar os dados particionados por data no bucket do GCS, na camada raw.

Atributos:
- self.api: instância da LinesCarrisAPI (para chamadas HTTP).
- self.spark: sessão Spark obtida pela função `get_spark_session`.
- self.repo: responsável por converter os dados normalizados em DataFrame.
- self.storage: responsável por salvar o DataFrame no storage (Parquet + GCS).

Método principal:
- ingest(): executa todo o pipeline de ingestão raw.
"""

from pyspark.sql.functions import current_date

from configs.settings import Settings
from domain.normalizers.lines_normalizer import LinesNormalizer
from domain.schemas.lines_schema import lines_schema
from domain.services.base_ingestion_services import IBaseIngestService
from infrastructure.api.carris_client import CarrisAPIClient
from infrastructure.logging.logger import logger
from infrastructure.repositories.generic_spark_repository import GenericSparkRepository
from infrastructure.spark.spark_singleton import get_spark_session
from infrastructure.storage.parquet_storage import ParquetStorage


class IngestLinesService(IBaseIngestService):
    def __init__(self):
        logger.info("Inicializando IngestLinesService...")

        self.api = CarrisAPIClient()
        logger.debug("Cliente da API Carris inicializado.")

        self.spark = get_spark_session()
        logger.debug("Sessão Spark obtida com sucesso.")

        self.repo = GenericSparkRepository(self.spark, schema=lines_schema)
        logger.debug("Repositório genérico com schema de linhas criado.")

        self.storage = ParquetStorage()
        logger.debug("Serviço de armazenamento Parquet instanciado.")

    def ingest(self):
        logger.info("Iniciando pipeline de ingestão de linhas...")

        logger.info(f"Buscando dados do endpoint: {Settings.LINES_ENDPOINT}")
        raw_data = self.api.fetch(Settings.LINES_ENDPOINT)
        logger.success(f"{len(raw_data)} registros brutos recebidos da API.")

        logger.info("Normalizando dados brutos...")
        normalized = LinesNormalizer.normalize(raw_data)
        logger.success(f"Normalização concluída. Total de registros: {len(normalized)}")

        logger.info("🧪 Convertendo para DataFrame do Spark...")
        df = self.repo.to_dataframe(normalized)
        logger.debug("Esquema do DataFrame:")
        df.printSchema()

        # Adiciona a coluna 'date' para particionamento por data
        df = df.withColumn("date", current_date())
        logger.debug("Coluna 'date' adicionada ao DataFrame.")

        # Ajusta o número de partições com base no tamanho do DataFrame
        num_rows = df.count()
        coalesce = 1
        if num_rows < 10_000:
            coalesce = 1
        elif num_rows < 100_000:
            coalesce = 4
        else:
            df = df.repartition("date")

        # Define o caminho de destino no bucket
        logger.info("Salvando dados no GCS particionados por data...")
        gcs_path = Settings.get_raw_path(Settings.LINES_ENDPOINT)

        # Salva o DataFrame no GCS particionado por data
        logger.info(f"Salvando DataFrame no GCS: {gcs_path}")
        self.storage.save(df, gcs_path, mode="overwrite", coalesce=coalesce)
        logger.success("Dados de lines salvos com sucesso no GCS!")


def run_ingest_lines():
    """
    Função utilizada como ponto de entrada para execução do pipeline de ingestão
    de linhas. Ela instancia o serviço `IngestLinesService` e executa o método
    `ingest()`.

    Essa função é usada diretamente como `python_callable` na DAG do Airflow.
    """
    logger.info("Iniciando use case: ingest_lines")
    service = IngestLinesService()
    service.ingest()
    logger.success("Use case 'ingest_lines' finalizado com sucesso.")
