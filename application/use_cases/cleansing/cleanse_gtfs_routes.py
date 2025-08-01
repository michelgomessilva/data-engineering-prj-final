from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_routes_cleanser import cleanse_gtfs_routes_df


def run_cleanse_gtfs_routes():
    runner = BaseCleanseRunner(
        entity_name="gtfs/routes",
        file_name="gtfs/routes",
        cleanse_func=cleanse_gtfs_routes_df,
        bq_table="staging_gtfs_routes",
    )
    runner.run()
