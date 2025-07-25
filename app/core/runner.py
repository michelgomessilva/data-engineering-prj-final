import time
from datetime import datetime

from infrastructure.logging.logger import logger


def run_use_case(use_case: str, use_cases: dict):
    logger.info("=" * 60)
    logger.info("🚀 Projeto de Engenharia de Dados iniciado")
    logger.info(f"📅 Data/Hora: {datetime.now().isoformat()}")
    start = time.time()

    logger.info(f"🔧 Executando use case: {use_case}")
    use_cases[use_case]()

    duration = time.time() - start
    minutes = int(duration // 60)
    seconds = duration % 60
    logger.info(f"✅ Execução finalizada em {minutes}m {seconds:.2f}s")
    logger.info("=" * 60)
