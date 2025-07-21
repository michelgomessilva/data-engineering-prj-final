import os
from pathlib import Path

from pyspark.sql.functions import current_date

from configs.settings import Settings
from domain.normalizers.gtfs_normalizer import GTFSNormalizer
from domain.schemas.gtfs_schemas import GTFS_SCHEMAS
from domain.services.base_ingestion_services import IBaseIngestService
from infrastructure.api.carris_client import CarrisAPIClient
from infrastructure.logging.logger import logger
from infrastructure.repositories.generic_spark_repository import GenericSparkRepository
from infrastructure.spark.create_session_spark import get_spark_session
from infrastructure.storage.gcs_uploader import GCSUploader
from infrastructure.storage.parquet_storage import ParquetStorage
from infrastructure.storage.zip_storage import ZipExtractor


class IngestGTFSService(IBaseIngestService):
    def __init__(self):
        logger.info("Inicializando IngestGTFSService...")

        self.api = CarrisAPIClient()
        self.url = Settings.CARRIS_API_BASE + Settings.GTFS_ENDPOINT
        logger.info(f"URL da API GTFS: {self.url}")
        self.download_dir = Settings.DOWNLOAD_DIR  # destino do zip e extração
        self.zip_extractor = ZipExtractor()
        self.spark = get_spark_session()
        self.repo = GenericSparkRepository(
            self.spark
        )  # schema definido no to_dataframe()
        self.storage = ParquetStorage()

    def ingest(self):
        # 1. Baixar o .zip do endpoint
        zip_path = self.api.download_zip(self.url, self.download_dir)

        # 2. Extrair os arquivos
        extracted_files = self.zip_extractor.extract_all(zip_path, self.download_dir)

        # 3. Para cada arquivo extraído
        for file_path in extracted_files:
            filename = Path(file_path).stem  # ex: routes, trips
            # if filename != "agency":
            #    continue  # Ignora arquivos que não são relevantes para GTFS

            logger.info(f"Iniciando processamento do arquivo: {filename}.txt")

            # Se o arquivo for maior que 32MB, divide em partes
            if self.zip_extractor.is_file_larger_than_32mb(file_path):
                logger.warning(
                    f"O arquivo {filename}.txt tem mais de 32MB. Dividindo em partes..."
                )
                parts = self.zip_extractor.split_file_by_size(
                    file_path,
                    output_dir=f"{self.download_dir}/{filename}/temp_parts/",
                    max_size_mb=32,
                )
            else:
                parts = [file_path]

            for part in parts:
                logger.info(f"Processando parte: {os.path.basename(part)}")

                # Normalizar (CSV → Dict)
                records = GTFSNormalizer.normalize(part)

                if not records:
                    logger.warning(f"Nenhum dado encontrado no arquivo {part}")
                    continue

                # Converter para Spark DataFrame com schema adequado
                schema = GTFS_SCHEMAS[filename]
                df = self.repo.to_dataframe(records, schema=schema)
                df = df.withColumn("date", current_date())

                # Define o caminho de destino no bucket
                local_folder = Settings.get_local_raw_path(Settings.GTFS_ENDPOINT)
                local_folder = os.path.join(local_folder, filename)
                logger.info(f"Caminho de destino: {local_folder}")
                # Salva localmente
                self.storage.save(df, local_folder, "append", partition_by=["date"])
                logger.success(f"Parte {os.path.basename(part)} salva com sucesso!")

            # Upload para GCS
            logger.info(f"Fazendo upload do arquivo {filename}.parquet para o GCS...")
            uploader = GCSUploader()
            uploader.upload_directory(
                local_folder=local_folder,
                gcs_dir=Settings.get_raw_path(Settings.GTFS_ENDPOINT + "/" + filename),
                file_extension=".parquet",
            )

            logger.success(f"Ingestão do {filename} concluída com sucesso.")
