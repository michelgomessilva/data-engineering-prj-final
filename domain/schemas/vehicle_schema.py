from pyspark.sql.types import (
    DateType,
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

vehicle_schema = StructType(
    [
        StructField("vehicle_id", StringType(), True),
        StructField("line_id", IntegerType(), True),
        StructField("trip_id", StringType(), True),
        StructField("pattern_id", StringType(), True),
        StructField("route_id", StringType(), True),
        StructField("shift_id", StringType(), True),
        StructField("stop_id", IntegerType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("schedule_relationship", StringType(), True),
        StructField("current_status", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", IntegerType(), True),
        StructField("timestamp", LongType(), True),
        StructField("ingestion_date", DateType(), True),
        StructField("partition_date", DateType(), True),
    ]
)
