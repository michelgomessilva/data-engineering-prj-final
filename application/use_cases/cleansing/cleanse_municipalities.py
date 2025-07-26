from domain.cleaners.base_cleaner_runner import BaseCleanseRunner
from domain.cleaners.municipalities_cleanser import cleanse_municipalities_df


def run_cleanse_municipalities():
    runner = BaseCleanseRunner(
        entity_name="municipalities",
        file_name="municipalities",
        cleanse_func=cleanse_municipalities_df,
        bq_table="staging_municipalities",
    )
    runner.run()
