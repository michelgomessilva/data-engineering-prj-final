from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.stops_cleanser import cleanse_stops_df


def run_cleanse_stops():
    runner = BaseCleanseRunner(
        entity_name="stops",
        file_name="stops",
        cleanse_func=cleanse_stops_df,
        bq_table="staging_stops",
    )
    runner.run()
