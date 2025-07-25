# infrastructure/spark/spark_singleton.py

from pyspark.sql import SparkSession

from infrastructure.spark.create_session_spark import (
    get_spark_session as create_session,
)

_spark_instance: SparkSession = None


def get_spark_session() -> SparkSession:
    global _spark_instance

    if _spark_instance is None:
        _spark_instance = create_session()

    return _spark_instance
