import posixpath
from pathlib import Path

from pyspark.sql.functions import current_date

from configs.settings import Settings
from domain.normalizers.gtfs_normalizer import GTFSNormalizer
from domain.schemas.gtfs_schemas import GTFS_SCHEMAS
from domain.services.base_ingestion_services import IBaseIngestService
from infrastructure.api.carris_client import CarrisAPIClient
from infrastructure.logging.logger import logger
from infrastructure.spark.create_session_spark import get_spark_session
from infrastructure.storage.parquet_storage import ParquetStorage
from infrastructure.storage.zip_storage import ZipExtractor


class IngestGTFSService(IBaseIngestService):
    def __init__(self):
        logger.info("Inicializando IngestGTFSService...")

        self.api = CarrisAPIClient()
        self.url = f"{Settings.CARRIS_API_BASE}{Settings.GTFS_ENDPOINT}"
        logger.info(f"URL da API GTFS: {self.url}")

        self.download_dir = Settings.DOWNLOAD_DIR
        self.zip_extractor = ZipExtractor()
        self.spark = get_spark_session()
        self.storage = ParquetStorage()

    def ingest(self):
        logger.info("Iniciando processo de ingestão GTFS...")

        # Mapeia quantas partições/coalesces usar para cada tipo de arquivo
        GTFS_COALESCE_MAP = {
            "agency": 1,  # pequena (1-2 linhas)
            "calendar": 1,  # pequena
            "calendar_dates": 1,  # pequena
            "routes": 1,  # até algumas dezenas
            "shapes": 4,  # moderada
            "stops": 1,  # ~500-1000 entradas
            "stop_times": 8,  # grande (~10k+ linhas)
            "trips": 4,  # média (~5k-10k)
            "fare_attributes": 1,  # pequena
            "fare_rules": 1,  # pequena
            "frequencies": 1,  # pequena
            "transfers": 1,  # pequena
            "pathways": 1,  # pequena
            "levels": 1,  # pequena
            "translations": 1,  # pequena
            "feed_info": 1,  # sempre 1 linha
        }

        # 1. Baixar o arquivo ZIP da API
        zip_path = self.api.download_zip(self.url, self.download_dir)

        # 2. Extrair todos os arquivos .txt
        extracted_files = self.zip_extractor.extract_all(zip_path, self.download_dir)

        # 3. Processar cada arquivo .txt individualmente
        for file_path in extracted_files:
            filename = Path(file_path).stem
            logger.info(f"Processando arquivo: {filename}.txt")

            # 3.1 Obter schema
            schema = GTFS_SCHEMAS.get(filename)
            if not schema:
                logger.warning(
                    f"Schema não encontrado para {filename}.txt. Pulando arquivo."
                )
                continue

            # 3.2 Ler como DataFrame Spark diretamente via GTFSNormalizer
            try:
                df = GTFSNormalizer.normalize(self.spark, file_path, schema=schema)
            except Exception as e:
                logger.exception(f"Erro ao normalizar {filename}.txt: {e}")
                continue

            if df.limit(1).count() == 0:
                logger.warning(f"Nenhum dado encontrado no arquivo {filename}.txt")
                continue

            # Aplica metadata + particionamento dinâmico
            df = df.withColumn("date", current_date())

            # Aplica número de coalesces dinâmico
            coalesce = GTFS_COALESCE_MAP.get(filename, 4)
            df = df.repartition(coalesce).persist()
            logger.info(f"{filename}.txt → {coalesce} partições antes do save")

            # 3.4 Caminho final no GCS
            gcs_path = posixpath.join(
                Settings.get_raw_path(Settings.GTFS_ENDPOINT), filename
            )
            logger.info(f"Salvando DataFrame no GCS: {gcs_path}")
            # 3.5 Salvar como Parquet particionado por data
            self.storage.save(
                df, gcs_path, mode="overwrite", partition_by=["date"], coalesce=coalesce
            )

            logger.success(f"Ingestão de {filename}.txt concluída com sucesso.")
