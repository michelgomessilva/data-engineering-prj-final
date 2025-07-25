import os
from datetime import datetime
from typing import Any, Dict, Optional

import requests  # type: ignore

from configs.settings import Settings
from infrastructure.logging.logger import logger


class CarrisAPIClient:
    """
    CarrisAPIClient

    Cliente HTTP responsável por realizar requisições à API da Carris Metropolitana.

    Este cliente encapsula a lógica de construção da URL base, manipulação de parâmetros e headers,
    e o tratamento de resposta HTTP com verificação de status e conversão segura para JSON.

    Atributos:
        base_url (str): URL base da API Carris, obtida a partir das configurações (Settings).

    Métodos:
        fetch(endpoint, params, headers, timeout): Realiza uma requisição GET para o endpoint da API
        e retorna os dados em formato JSON.
    """

    def __init__(self):
        """
        Inicializa o cliente da API da Carris Metropolitana com a URL base definida em Settings.
        """
        self.base_url = Settings.CARRIS_API_BASE.rstrip("/")
        logger.info(f"CarrisAPIClient inicializado com base_url: {self.base_url}")

    def fetch(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> list:
        """
        Realiza uma requisição GET para o endpoint da API.

        Args:
            endpoint (str): Caminho do endpoint (ex: 'vehicles', 'lines', etc.)
            params (dict): Parâmetros de query string
            headers (dict): Headers HTTP (ex: auth token)
            timeout (int): Timeout da requisição em segundos

        Returns:
            list: Lista de dados JSON retornados pela API

        Raises:
            HTTPError: Se o status da resposta indicar erro.
            ValueError: Se a resposta não for um JSON válido.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"Iniciando requisição GET para URL: {url}")

        try:
            response = requests.get(
                url, params=params, headers=headers, timeout=timeout
            )
            response.raise_for_status()
            logger.info(
                f"Requisição para {url} retornou com status: {response.status_code}"
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro durante requisição GET para {url}: {str(e)}")
            raise

        try:
            json_data = response.json()
            logger.info(
                f"Resposta JSON parseada com sucesso. "
                f"Total de registros: {len(json_data) if isinstance(json_data, list) else 'N/A'}"
            )
            return json_data
        except ValueError:
            logger.error(
                f"Falha ao converter resposta da API em JSON para o endpoint {endpoint}. Conteúdo: {response.text}"
            )
            raise ValueError(
                f"Resposta inválida da API para endpoint {endpoint}: {response.text}"
            )
        except Exception as e:
            logger.error(f"Erro inesperado ao processar resposta JSON: {str(e)}")
            raise ValueError(
                f"Erro ao processar resposta JSON para endpoint {endpoint}: {str(e)}"
            )

    def download_zip(self, url: str, download_dir: str) -> str:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erro ao baixar arquivo: {response.status_code}")

        # Gera timestamp no formato yyyy-mm-dd-hh-mm-ss
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"gtfs-{timestamp}.zip"

        # Caminho final com timestamp
        zip_path = os.path.join(download_dir, filename)
        os.makedirs(download_dir, exist_ok=True)  # Garante que o diretório existe

        with open(zip_path, "wb") as f:
            f.write(response.content)

        return zip_path
