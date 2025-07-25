from typing import Callable

from application.use_cases.cleansing.cleanse_lines import run_cleanse_lines
from application.use_cases.ingest_gtfs import IngestGTFSService
from application.use_cases.ingest_lines import IngestLinesService
from application.use_cases.ingest_municipalities import IngestMunicipalitiesService
from application.use_cases.ingest_routes import IngestRoutesService
from application.use_cases.ingest_stops import IngestStopsService
from application.use_cases.ingest_vehicles import IngestVehiclesService


def wrap_ingestion(service_cls, name: str):
    def _run():
        from infrastructure.logging.logger import logger

        logger.info(f"Iniciando use case: {name}")
        service = service_cls()
        service.ingest()
        logger.success(f"Use case '{name}' finalizado com sucesso.")

    return _run


def run_endpoints():
    USE_CASES["ingest_vehicles"]()
    USE_CASES["ingest_municipalities"]()
    USE_CASES["ingest_lines"]()
    USE_CASES["ingest_routes"]()
    USE_CASES["ingest_stops"]()


def run_all():
    run_endpoints()
    USE_CASES["ingest_gtfs"]()
    USE_CASES["cleanse_lines"]()


USE_CASES: dict[str, Callable[[], None]] = {
    "ingest_vehicles": wrap_ingestion(IngestVehiclesService, "ingest_vehicles"),
    "ingest_municipalities": wrap_ingestion(
        IngestMunicipalitiesService, "ingest_municipalities"
    ),
    "ingest_lines": wrap_ingestion(IngestLinesService, "ingest_lines"),
    "ingest_routes": wrap_ingestion(IngestRoutesService, "ingest_routes"),
    "ingest_stops": wrap_ingestion(IngestStopsService, "ingest_stops"),
    "ingest_gtfs": wrap_ingestion(IngestGTFSService, "ingest_gtfs"),
    "cleanse_lines": run_cleanse_lines,
    "endpoints": run_endpoints,
    "all": run_all,
}
