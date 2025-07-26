from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.routes_cleanser import cleanse_routes_df


def run_cleanse_routes():
    runner = BaseCleanseRunner(
        entity_name="routes",
        file_name="routes",
        cleanse_func=cleanse_routes_df,
        bq_table="staging_routes",
    )
    runner.run()
