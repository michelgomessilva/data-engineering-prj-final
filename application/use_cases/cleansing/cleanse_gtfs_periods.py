from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_periods_cleanser import cleanse_gtfs_periods_df


def run_cleanse_gtfs_periods():
    runner = BaseCleanseRunner(
        entity_name="gtfs/periods",
        file_name="gtfs/periods",
        cleanse_func=cleanse_gtfs_periods_df,
        bq_table="staging_gtfs_periods",
    )
    runner.run()
