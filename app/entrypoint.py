"""
entrypoint.py

Este módulo serve como ponto de entrada principal da aplicação quando executada via Docker.
Responsabilidades:
- Carregar variáveis de ambiente a partir de um arquivo `.env` (caso exista);
- Corrigir dinamicamente o valor da variável de ambiente `JAVA_HOME`, necessária para execução do PySpark;
- Inicializar o sistema de logging configurado com `loguru`;
- Executar o `main.py` com base nos argumentos fornecidos (via argparse).

Uso:
    python -m app.entrypoint --use-case ingest_vehicles
"""

import os
import subprocess

from dotenv import load_dotenv

from app import main
from configs.settings import Settings
from infrastructure.logging.logger import setup_logger


def ensure_java_home():
    """
    Garante que a variável de ambiente JAVA_HOME esteja definida corretamente.
    Necessário para que o PySpark consiga iniciar o Java Gateway.
    """
    if "JAVA_HOME" not in os.environ or not os.environ["JAVA_HOME"]:
        try:
            # Detecta o caminho do binário do Java
            java_bin_path = (
                subprocess.check_output("readlink -f $(which java)", shell=True)
                .decode()
                .strip()
            )
            java_home = os.path.dirname(os.path.dirname(java_bin_path))
            os.environ["JAVA_HOME"] = java_home
            print(f"JAVA_HOME detectado automaticamente: {java_home}")
        except Exception as e:
            print("Falha ao detectar JAVA_HOME automaticamente.")
            print(f"Erro: {e}")
            raise


def bootstrap():
    """
    Executa o processo completo de inicialização da aplicação:
    - Carrega .env
    - Ajusta JAVA_HOME (PySpark)
    - Inicializa o logger
    - Executa a função principal
    """
    # 1. Carrega variáveis do .env (se existir)
    dotenv_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print("✅ .env carregado com sucesso")

    # 2. Garante que JAVA_HOME está definido corretamente para o PySpark
    ensure_java_home()

    # 3. Inicializa o logger com base no ambiente
    setup_logger(Settings.get_local_log_path(), Settings.APP_ENV)

    # 4. Executa a aplicação principal
    main.main()


if __name__ == "__main__":
    bootstrap()
