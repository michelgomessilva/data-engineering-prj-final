from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_stop_times_cleanser import cleanse_gtfs_stop_times_df


def run_cleanse_gtfs_stop_times():
    runner = BaseCleanseRunner(
        entity_name="gtfs/stop_times",
        file_name="gtfs/stop_times",
        cleanse_func=cleanse_gtfs_stop_times_df,
        bq_table="staging_gtfs_stop_times",
    )
    runner.run()
