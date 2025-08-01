from typing import Callable

from application.use_cases.cleansing.cleanse_gtfs_calendar_dates import (
    run_cleanse_gtfs_calendar_dates,
)
from application.use_cases.cleansing.cleanse_gtfs_dates import run_cleanse_gtfs_dates
from application.use_cases.cleansing.cleanse_gtfs_feed_info import (
    run_cleanse_gtfs_feed_info,
)
from application.use_cases.cleansing.cleanse_gtfs_municipalities import (
    run_cleanse_gtfs_municipalities,
)
from application.use_cases.cleansing.cleanse_gtfs_periods import (
    run_cleanse_gtfs_periods,
)
from application.use_cases.cleansing.cleanse_gtfs_routes import run_cleanse_gtfs_routes
from application.use_cases.cleansing.cleanse_gtfs_shapes import run_cleanse_gtfs_shapes
from application.use_cases.cleansing.cleanse_gtfs_stop_times import (
    run_cleanse_gtfs_stop_times,
)
from application.use_cases.cleansing.cleanse_gtfs_stops import run_cleanse_gtfs_stops
from application.use_cases.cleansing.cleanse_gtfs_trips import run_cleanse_gtfs_trips
from application.use_cases.cleansing.cleanse_lines import run_cleanse_lines
from application.use_cases.cleansing.cleanse_municipalities import (
    run_cleanse_municipalities,
)
from application.use_cases.cleansing.cleanse_routes import run_cleanse_routes
from application.use_cases.cleansing.cleanse_stops import run_cleanse_stops
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
    USE_CASES["cleanse_municipalities"]()
    USE_CASES["cleanse_stops"]()
    USE_CASES["cleanse_routes"]()
    USE_CASES["cleanse_gtfs_stops"]()
    USE_CASES["cleanse_gtfs_stop_times"]()
    USE_CASES["cleanse_gtfs_shapes"]()
    USE_CASES["cleanse_gtfs_trips"]()
    USE_CASES["cleanse_gtfs_periods"]()
    USE_CASES["cleanse_gtfs_routes"]()
    USE_CASES["cleanse_gtfs_municipalities"]()
    USE_CASES["cleanse_gtfs_feed_info"]()
    USE_CASES["cleanse_gtfs_calendar_dates"]()
    USE_CASES["cleanse_gtfs_dates"]()


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
    "cleanse_municipalities": run_cleanse_municipalities,
    "cleanse_stops": run_cleanse_stops,
    "cleanse_routes": run_cleanse_routes,
    "cleanse_gtfs_stops": run_cleanse_gtfs_stops,
    "cleanse_gtfs_stop_times": run_cleanse_gtfs_stop_times,
    "cleanse_gtfs_shapes": run_cleanse_gtfs_shapes,
    "cleanse_gtfs_trips": run_cleanse_gtfs_trips,
    "cleanse_gtfs_periods": run_cleanse_gtfs_periods,
    "cleanse_gtfs_routes": run_cleanse_gtfs_routes,
    "cleanse_gtfs_municipalities": run_cleanse_gtfs_municipalities,
    "cleanse_gtfs_feed_info": run_cleanse_gtfs_feed_info,
    "cleanse_gtfs_calendar_dates": run_cleanse_gtfs_calendar_dates,
    "cleanse_gtfs_dates": run_cleanse_gtfs_dates,
    "endpoints": run_endpoints,
    "all": run_all,
}
