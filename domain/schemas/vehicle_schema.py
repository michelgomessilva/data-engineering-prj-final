from pyspark.sql.types import DoubleType, LongType, StringType, StructField, StructType

vehicle_schema = StructType(
    [
        StructField("vehicle_id", StringType(), True),
        StructField("line_id", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("timestamp", LongType(), True),
        StructField("current_status", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("trip_id", StringType(), True),
        StructField("bearing", LongType(), True),
        StructField("block_id", StringType(), True),
        StructField("pattern_id", StringType(), True),
        StructField("route_id", StringType(), True),
        StructField("schedule_relationship", StringType(), True),
        StructField("shift_id", StringType(), True),
        StructField("stop_id", StringType(), True),
    ]
)
