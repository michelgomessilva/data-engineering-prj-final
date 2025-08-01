from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_dates_cleanser import cleanse_gtfs_dates_df


def run_cleanse_gtfs_dates():
    runner = BaseCleanseRunner(
        entity_name="gtfs/dates",
        file_name="gtfs/dates",
        cleanse_func=cleanse_gtfs_dates_df,
        bq_table="staging_gtfs_dates",
    )
    runner.run()
