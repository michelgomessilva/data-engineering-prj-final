from pyspark.sql.types import ArrayType, DateType, StringType, StructField, StructType

lines_schema = StructType(
    [
        StructField("color", StringType(), True),
        StructField("facilities", ArrayType(StringType(), True), True),
        StructField("line_id", StringType(), True),
        StructField("localities", ArrayType(StringType(), True), True),
        StructField("long_name", StringType(), True),
        StructField("municipalities", ArrayType(StringType(), True), True),
        StructField("patterns", ArrayType(StringType(), True), True),
        StructField("routes", ArrayType(StringType(), True), True),
        StructField("short_name", StringType(), True),
        StructField("text_color", StringType(), True),
        StructField("ingestion_date", DateType(), True),
        StructField("partition_date", DateType(), True),
    ]
)
