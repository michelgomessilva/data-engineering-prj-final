from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.lines_cleanser import cleanse_lines_df


def run_cleanse_lines():
    runner = BaseCleanseRunner(
        entity_name="lines",
        file_name="lines",
        cleanse_func=cleanse_lines_df,
        bq_table="staging_lines",
    )
    runner.run()
