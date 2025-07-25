"""
IngestVehiclesService

Classe responsável por orquestrar o processo de ingestão de dados brutos (raw)
de veículos da API da Carris Metropolitana,
normalizar os dados, convertê-los em DataFrame do Spark, e armazená-los em
formato Parquet no Google Cloud Storage (GCS),
organizados em partições diárias.

Responsabilidades:
- Buscar os dados da API externa definida no settings (endpoint de municípios).
- Normalizar os dados JSON em um formato tabular.
- Converter para Spark DataFrame.
- Adicionar metadados como a data de ingestão.
- Salvar os dados particionados por data no bucket do GCS, na camada raw.

Atributos:
- self.api: instância da MunicipalitiesCarrisAPI (para chamadas HTTP).
- self.spark: sessão Spark obtida pela função `get_spark_session`.
- self.repo: responsável por converter os dados normalizados em DataFrame.
- self.storage: responsável por salvar o DataFrame no storage (Parquet + GCS).

Método principal:
- ingest(): executa todo o pipeline de ingestão raw.
"""

from pyspark.sql.functions import current_date

from configs.settings import Settings
from domain.normalizers.municipalities_normalizer import MunicipalitiesNormalizer
from domain.schemas.municipalities_schema import municipalities_schema
from domain.services.base_ingestion_services import IBaseIngestService
from infrastructure.api.carris_client import CarrisAPIClient
from infrastructure.logging.logger import logger
from infrastructure.repositories.generic_spark_repository import GenericSparkRepository
from infrastructure.spark.create_session_spark import get_spark_session
from infrastructure.storage.parquet_storage import ParquetStorage


class IngestMunicipalitiesService(IBaseIngestService):
    def __init__(self):
        logger.info("Inicializando IngestMunicipalitiesService...")

        self.api = CarrisAPIClient()
        logger.debug("Cliente da API Carris inicializado.")

        self.spark = get_spark_session()
        logger.debug("Sessão Spark obtida com sucesso.")

        self.repo = GenericSparkRepository(self.spark, schema=municipalities_schema)
        logger.debug("Repositório genérico com schema de municípios criado.")

        self.storage = ParquetStorage()
        logger.debug("Serviço de armazenamento Parquet instanciado.")

    def ingest(self):
        logger.info("Iniciando pipeline de ingestão de municípios...")

        logger.info(f"Buscando dados do endpoint: {Settings.MUNICIPALITIES_ENDPOINT}")
        raw_data = self.api.fetch(Settings.MUNICIPALITIES_ENDPOINT)
        logger.success(f"{len(raw_data)} registros brutos recebidos da API.")

        logger.info("Normalizando dados brutos...")
        normalized = MunicipalitiesNormalizer.normalize(raw_data)
        logger.success(f"Normalização concluída. Total de registros: {len(normalized)}")

        logger.info("🧪 Convertendo para DataFrame do Spark...")
        df = self.repo.to_dataframe(normalized)
        logger.debug("Esquema do DataFrame:")
        df.printSchema()

        # Adiciona a coluna 'date' para particionamento por data
        df = df.withColumn("date", current_date())
        logger.debug("Coluna 'date' adicionada ao DataFrame.")

        # Define o caminho de destino no bucket
        logger.info("Salvando dados no GCS particionados por data...")
        gcs_path = Settings.get_raw_path(Settings.MUNICIPALITIES_ENDPOINT)

        # Salva o DataFrame no GCS particionado por data
        logger.info(f"Salvando DataFrame no GCS: {gcs_path}")
        self.storage.save(df, gcs_path, mode="overwrite", partition_by=["date"])
        logger.success("Dados de municipalities salvos com sucesso no GCS!")


def run_ingest_municipalities():
    """
    Função utilizada como ponto de entrada para execução do pipeline de ingestão
    de municípios. Ela instancia o serviço `IngestMunicipalitiesService` e executa o método
    `ingest()`.

    Essa função é usada diretamente como `python_callable` na DAG do Airflow.
    """
    logger.info("Iniciando use case: ingest_municipalities")
    service = IngestMunicipalitiesService()
    service.ingest()
    logger.success("Use case 'ingest_municipalities' finalizado com sucesso.")
