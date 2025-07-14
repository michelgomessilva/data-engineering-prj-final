from pyspark.sql.types import (
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
        StructField("line_id", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("timestamp", LongType(), True),
        StructField("CURRENT_STATUS", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", IntegerType(), True),
        StructField("trip_id", StringType(), True),
    ]
)
