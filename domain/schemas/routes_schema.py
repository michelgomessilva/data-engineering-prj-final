from pyspark.sql.types import ArrayType, StringType, StructField, StructType

routes_schema = StructType(
    [
        StructField("color", StringType(), True),
        StructField("facilities", ArrayType(StringType(), True), True),
        StructField("route_id", StringType(), True),
        StructField("line_id", StringType(), True),
        StructField("localities", ArrayType(StringType(), True), True),
        StructField("long_name", StringType(), True),
        StructField("municipalities", ArrayType(StringType(), True), True),
        StructField("patterns", ArrayType(StringType(), True), True),
        StructField("short_name", StringType(), True),
        StructField("text_color", StringType(), True),
    ]
)
