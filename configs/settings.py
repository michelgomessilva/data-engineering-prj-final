import os
from datetime import datetime
from urllib.parse import urlparse

from dotenv import load_dotenv

from infrastructure.logging.logger import logger

load_dotenv()


class Settings:
    """
    Classe responsável por carregar e expor as configurações do projeto.

    As configurações são carregadas a partir das variáveis de ambiente, utilizando o `.env`
    como fallback durante o desenvolvimento. Essa classe centraliza os parâmetros de execução,
    como paths para storage, endpoints de APIs e ambiente de execução.

    Attributes:
        GCS_BASE_PATH (str): Caminho base do bucket no Google Cloud Storage.
        RAW_FOLDER (str): Nome da subpasta usada para armazenar dados brutos (raw).
        STAGING_FOLDER (str): Nome da subpasta para dados transformados (staging/silver).
        GOLD_FOLDER (str): Nome da subpasta para dados finais (gold).
        CARRIS_API_BASE (str): URL base da API da Carris Metropolitana.
        VEHICLES_ENDPOINT (str): Nome do endpoint para buscar os veículos.
        APP_ENV (str): Ambiente de execução (ex: "dev", "prod").
    """

    # Diretório base do projeto (ajustável para local ou Composer)
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_BASE_PATH = os.getenv("APP_BASE_PATH", ".")

    # Logs
    LOGS_FOLDER = os.getenv("LOGS_FOLDER", "logs")

    # GCS
    GCS_BUCKET = os.getenv("GCS_BUCKET", "applied-project")
    GCS_BASE_PATH = os.getenv("GCS_BASE_PATH", "gs://applied-project/grupo-2")
    RAW_FOLDER = os.getenv("RAW_FOLDER", "raw")
    STAGING_FOLDER = os.getenv("STAGING_FOLDER", "staging")
    GOLD_FOLDER = os.getenv("GOLD_FOLDER", "gold")

    # GCP
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "data-eng-dev-437916")

    # API
    CARRIS_API_BASE = os.getenv(
        "CARRIS_API_BASE", "https://api.carrismetropolitana.pt/"
    )
    VEHICLES_ENDPOINT = os.getenv("VEHICLES_ENDPOINT", "vehicles")

    # ENV
    APP_ENV = os.getenv("APP_ENV", "dev")
    APP_NAME = os.getenv("APP_NAME", "Group2FinalProject")

    @classmethod
    def get_local_raw_path(cls, subpath: str = "") -> str:
        """
        Gera o caminho local completo para a pasta de dados 'raw'.

        Esse método é útil durante o desenvolvimento local, permitindo
        salvar os arquivos Parquet em diretórios locais antes de fazer upload ao GCS.

        Args:
            subpath (str): Subcaminho relativo dentro da pasta raw local (opcional).

        Returns:
            str: Caminho absoluto local para o arquivo ou diretório.
        """
        # Gera a data atual no formato YYYY-MM-DD
        today_str = datetime.now().strftime("%Y-%m-%d")
        local_base = os.path.join(cls.APP_BASE_PATH, "data", cls.RAW_FOLDER, today_str)
        return os.path.join(local_base, subpath).replace("\\", "/").rstrip("/")

    @classmethod
    def get_local_log_path(cls, filename: str = "") -> str:
        """
        Gera o caminho absoluto para salvar arquivos de log no ambiente local ou no Composer.

        O caminho base é definido a partir da variável `APP_BASE_PATH`, que pode representar
        o diretório atual (em desenvolvimento local) ou o path montado no Composer
        (ex: /home/airflow/gcs/data/grupo-2).

        Args:
            filename (str): Nome do arquivo de log (opcional). Pode incluir subdiretórios.

        Returns:
            str: Caminho completo para o arquivo de log, com separadores de diretório padronizados.

        Exemplo:
            - Ambiente local:
                APP_BASE_PATH = "."
                LOGS_FOLDER = "logs"
                get_local_log_path("ingest.log") → "./logs/ingest.log"

            - Ambiente de produção (Composer):
                APP_BASE_PATH = "/home/airflow/gcs/data/grupo-2"
                LOGS_FOLDER = "logs"
                get_local_log_path("pipeline/ingest.log") →
                    "/home/airflow/gcs/data/grupo-2/logs/pipeline/ingest.log"
        """
        log_base = os.path.join(cls.APP_BASE_PATH, cls.LOGS_FOLDER)
        return os.path.join(log_base, filename).replace("\\", "/").rstrip("/")

    @classmethod
    def get_raw_path(cls, subpath: str = "") -> str:
        """
        Gera o caminho completo para a pasta de dados 'raw'.

        Args:
            subpath (str): Subcaminho relativo dentro do bucket raw (opcional).

        Returns:
            str: Caminho completo do arquivo ou diretório no bucket raw.
        """
        parsed = urlparse(cls.GCS_BASE_PATH)
        logger.info(f"Parsed GCS base path: {parsed}")
        base = parsed.path.strip("/")
        logger.info(f"Base path for GCS: {base}")
        complete_path = f"{base}/{cls.RAW_FOLDER}/{subpath}".rstrip("/")
        logger.info(f"Complete raw path: {complete_path}")
        return complete_path

    @classmethod
    def get_staging_path(cls, subpath: str = "") -> str:
        """
        Gera o caminho completo para a pasta de dados 'staging'.

        Args:
            subpath (str): Subcaminho relativo dentro do bucket staging (opcional).

        Returns:
            str: Caminho completo do arquivo ou diretório no bucket staging.
        """
        return f"{cls.GCS_BASE_PATH}/{cls.STAGING_FOLDER}/{subpath}".rstrip("/")

    @classmethod
    def get_gold_path(cls, subpath: str = "") -> str:
        """
        Gera o caminho completo para a pasta de dados 'gold'.

        Args:
            subpath (str): Subcaminho relativo dentro do bucket gold (opcional).

        Returns:
            str: Caminho completo do arquivo ou diretório no bucket gold.
        """
        return f"{cls.GCS_BASE_PATH}/{cls.GOLD_FOLDER}/{subpath}".rstrip("/")
