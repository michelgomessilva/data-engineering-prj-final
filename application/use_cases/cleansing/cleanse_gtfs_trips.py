from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_trips_cleanser import cleanse_gtfs_trips_df


def run_cleanse_gtfs_trips():
    runner = BaseCleanseRunner(
        entity_name="gtfs/trips",
        file_name="gtfs/trips",
        cleanse_func=cleanse_gtfs_trips_df,
        bq_table="staging_gtfs_trips",
    )
    runner.run()
