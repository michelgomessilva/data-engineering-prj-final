"""
Logger Configuration Module

Este módulo configura o sistema de logging centralizado utilizando a biblioteca `loguru`,
para ser reutilizado em todo o projeto de Engenharia de Dados. Os logs são salvos em uma
pasta local chamada `logs/`, com rotação diária e compressão automática.

Recursos:
- Logs coloridos no terminal (nível INFO+)
- Logs detalhados no arquivo (nível DEBUG+)
- Retenção automática de logs por 10 dias
- Compressão em .zip de logs antigos
- Stacktrace e diagnose completo para erros

Uso:
    from infrastructure.logging.logger import logger

    logger.info("Mensagem informativa")
    logger.error("Mensagem de erro")
"""

from datetime import datetime
from pathlib import Path

from loguru import logger

from configs.settings import Settings

# ----------------------------------------
# Diretório base para armazenar arquivos de log
LOG_DIR = Path(Settings.get_local_log_path())
LOG_DIR.mkdir(exist_ok=True)

# Caminho completo do arquivo de log baseado na data atual
log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"

# ----------------------------------------
# Configuração do logger

# Remove qualquer handler padrão do loguru para evitar logs duplicados
logger.remove()

# Adiciona saída colorida no terminal (stdout)
logger.add(
    sink=lambda msg: print(msg, end=""),  # imprime no console
    level="INFO",  # nível mínimo INFO
    colorize=True,  # terminal com cor
)

# Adiciona saída para arquivo com configurações de produção
logger.add(
    str(log_file),
    level="DEBUG",  # nível mínimo DEBUG (mais detalhado)
    rotation="10 MB",  # rotaciona após 10 MB
    retention="10 days",  # mantém arquivos por até 10 dias
    compression="zip",  # compacta arquivos antigos
    backtrace=True,  # imprime stacktrace completo para exceções
    diagnose=True,  # inclui informações extras sobre variáveis em erro
    encoding="utf-8",  # evita problemas com acentuação
)

# ----------------------------------------
logger.info("Logger inicializado com sucesso.")
