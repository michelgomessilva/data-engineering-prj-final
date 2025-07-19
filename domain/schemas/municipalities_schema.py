from pyspark.sql.types import StringType, StructField, StructType

municipalities_schema = StructType(
    [
        StructField("district_id", StringType(), True),
        StructField("district_name", StringType(), True),
        StructField("municipality_id", StringType(), True),
        StructField("municipality_name", StringType(), True),
        StructField("prefix", StringType(), True),
        StructField("region_id", StringType(), True),
        StructField("region_name", StringType(), True),
    ]
)
