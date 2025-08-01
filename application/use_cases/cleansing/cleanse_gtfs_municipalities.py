from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_municipalities_cleanser import cleanse_gtfs_municipalities_df


def run_cleanse_gtfs_municipalities():
    runner = BaseCleanseRunner(
        entity_name="gtfs/municipalities",
        file_name="gtfs/municipalities",
        cleanse_func=cleanse_gtfs_municipalities_df,
        bq_table="staging_gtfs_municipalities",
    )
    runner.run()
