from pathlib import Path
from urllib.parse import urlparse

from google.cloud import storage

from configs.settings import Settings
from infrastructure.logging.logger import logger


def parse_gcs_path(full_gcs_path: str) -> tuple[str, str]:
    """
    Converte um path tipo gs://bucket/path/to/blob em (bucket, path/to/blob).
    """
    parsed = urlparse(full_gcs_path)
    bucket = parsed.netloc
    path = parsed.path.lstrip("/")
    return bucket, path


class GCSUploader:
    """
    Responsável por fazer upload de arquivos locais (ex: Parquet) para um bucket no GCS.

    Atributos:
        bucket_name (str): Nome do bucket no GCS (vem de Settings).
        client (storage.Client): Cliente da Google Cloud Storage autenticado.
    """

    def __init__(self):
        self.bucket_name = Settings.GCS_BUCKET
        self.base_path = Settings.GCS_BASE_PATH.strip("/").replace("gs://", "")
        self.client = storage.Client(project=Settings.GCP_PROJECT_ID)
        self.bucket = self.client.bucket(self.bucket_name)
        logger.info(f"Cliente GCS inicializado para o bucket: {self.bucket_name}")
        logger.info(f"Prefixo base configurado: {self.base_path}")

    def upload_file(self, local_path: str, full_gcs_path: str) -> None:
        """
        Faz o upload de um único arquivo para o GCS.

        Args:
            local_path (str): Caminho completo do arquivo local.
            gcs_path (str): Caminho dentro do bucket GCS onde o arquivo será salvo.

        Raises:
            FileNotFoundError: Se o arquivo local não existir.
            Exception: Para erros genéricos de upload.
        """
        local_file = Path(local_path)
        if not local_file.exists():
            logger.error(f"Arquivo não encontrado: {local_path}")
            raise FileNotFoundError(f"Arquivo não encontrado: {local_path}")

        bucket_name, blob_path = parse_gcs_path(full_gcs_path)

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        logger.info(
            f"Upload para gs://{bucket_name}/{blob_path} a partir de {local_path}"
        )

        try:
            blob.upload_from_filename(str(local_file))
            logger.info(
                f"Upload realizado com sucesso: {local_path} → gs://{bucket_name}/{blob_path}"
            )
        except Exception as e:
            logger.error(f"Erro ao fazer upload para o GCS: {e}")
            raise

    def upload_directory(
        self, local_folder: str, gcs_dir: str, file_extension: str = ".parquet"
    ) -> None:
        """
        Faz o upload de todos os arquivos com a extensão desejada de um diretório local para o GCS.

        Args:
            local_folder (str): Caminho da pasta local.
            gcs_dir (str): Caminho base dentro do bucket.
            file_extension (str): Extensão dos arquivos a serem enviados (default: '.parquet').
        """
        local_dir_path = Path(local_folder)

        if not local_dir_path.exists() or not local_dir_path.is_dir():
            logger.error(f"Pasta local inválida: {local_folder}")
            raise NotADirectoryError(f"Pasta local inválida: {local_folder}")

        files = [
            f
            for f in local_dir_path.rglob("*")
            if f.suffix.lower() == file_extension.lower()
        ]
        if not files:
            logger.warning(
                f"Nenhum arquivo '{file_extension}' encontrado em: {local_folder}"
            )
            return

        logger.info(f"Iniciando upload de {len(files)} arquivos para o GCS...")
        logger.debug(f"Prefixo remoto base: {gcs_dir}")

        for file in files:
            relative_path = file.relative_to(local_dir_path).as_posix()
            full_gcs_path = f"{gcs_dir.strip('/')}/{relative_path}".replace("\\", "/")
            logger.debug(f"Arquivo relativo: {relative_path}")
            logger.debug(f"Path final no GCS: {full_gcs_path}")
            self.upload_file(str(file), full_gcs_path)

        logger.success(
            f"Upload de diretório finalizado: {local_folder} → {full_gcs_path.strip('/')}/"
        )
