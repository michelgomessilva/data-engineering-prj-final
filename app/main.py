import argparse

from app.core.registry import USE_CASES
from app.core.runner import run_use_case
from configs.settings import Settings
from infrastructure.logging.logger import setup_logger


def main():
    setup_logger(Settings.get_local_log_path(), Settings.APP_ENV)

    parser = argparse.ArgumentParser(description="Executor de use cases da pipeline.")
    parser.add_argument(
        "--use-case",
        type=str,
        choices=USE_CASES.keys(),
        required=True,
        help="Nome do use case a ser executado. Ex: ingest_vehicles ou all",
    )
    args = parser.parse_args()
    run_use_case(args.use_case, USE_CASES)


if __name__ == "__main__":
    main()
