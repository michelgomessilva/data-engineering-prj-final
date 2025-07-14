"""
Main module

Este módulo serve como ponto de entrada principal da aplicação de engenharia de dados.
Ele permite a execução via linha de comando de diferentes use cases de forma modular.

Funcionalidades:
- Ingestão de dados de veículos via API externa (Carris Metropolitana).
- Estrutura pronta para adicionar múltiplos use cases.
- Logging com loguru.
- Suporte a execução individual ou total dos pipelines.

Uso:
    python main.py --use-case ingest_vehicles
    python main.py --use-case all
"""

import argparse
import os
import sys
from datetime import datetime

from loguru import logger

# Importações dos use cases
from application.use_cases.ingest_vehicles import IngestVehiclesService

# Adiciona o diretório raiz ao sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def run_ingest_vehicles():
    logger.info("Iniciando use case: ingest_vehicles")
    service = IngestVehiclesService()
    service.ingest()
    logger.success("Use case 'ingest_vehicles' finalizado com sucesso.")


# Mapeamento de use cases
USE_CASES = {
    "ingest_vehicles": run_ingest_vehicles,
    # "ingest_inspections": run_ingest_inspections,
    # "generate_report": run_generate_report,
    "all": lambda: [
        func()
        for func in [
            run_ingest_vehicles,
            # run_ingest_inspections,
            # run_generate_report,
        ]
    ],
}


def main():
    logger.info("=" * 60)
    logger.info("🚀 Projeto de Engenharia de Dados iniciado")
    logger.info(f"📅 Data/Hora: {datetime.now().isoformat()}")

    parser = argparse.ArgumentParser(description="Executor de use cases da pipeline.")
    parser.add_argument(
        "--use-case",
        type=str,
        choices=USE_CASES.keys(),
        required=True,
        help="Nome do use case a ser executado. Ex: ingest_vehicles ou all",
    )
    args = parser.parse_args()

    logger.info(f"🔧 Executando use case: {args.use_case}")
    USE_CASES[args.use_case]()
    logger.info("✅ Execução finalizada.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
