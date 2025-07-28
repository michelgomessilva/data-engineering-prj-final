from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_feed_info_cleanser import cleanse_gtfs_feed_info_df


def run_cleanse_gtfs_feed_info():
    runner = BaseCleanseRunner(
        entity_name="gtfs/feed_info",
        file_name="gtfs/feed_info",
        cleanse_func=cleanse_gtfs_feed_info_df,
        bq_table="staging_gtfs_feed_info",
    )
    runner.run()
