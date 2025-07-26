from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.gtfs_shapes_cleanser import cleanse_gtfs_shapes_df


def run_cleanse_gtfs_shapes():
    runner = BaseCleanseRunner(
        entity_name="gtfs/shapes",
        file_name="gtfs/shapes",
        cleanse_func=cleanse_gtfs_shapes_df,
        bq_table="staging_gtfs_shapes",
    )
    runner.run()
