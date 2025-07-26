from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_stops_cleanser import cleanse_gtfs_stops_df


def run_cleanse_gtfs_stops():
    runner = BaseCleanseRunner(
        entity_name="gtfs/stops",
        file_name="gtfs/stops",
        cleanse_func=cleanse_gtfs_stops_df,
        bq_table="staging_gtfs_stops",
    )
    runner.run()
