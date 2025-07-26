from pyspark.sql.types import ArrayType, DateType, StringType, StructField, StructType

stops_schema = StructType(
    [
        StructField("district_id", StringType(), True),
        StructField("district_name", StringType(), True),
        StructField("facilities", ArrayType(StringType(), True), True),
        StructField("stop_id", StringType(), True),
        StructField("latitude", StringType(), True),
        StructField("lines", ArrayType(StringType(), True), True),
        StructField("locality", StringType(), True),
        StructField("longitude", StringType(), True),
        StructField("municipality_id", StringType(), True),
        StructField("municipality_name", StringType(), True),
        StructField("stop_name", StringType(), True),
        StructField("operational_status", StringType(), True),
        StructField("parish_id", StringType(), True),
        StructField("parish_name", StringType(), True),
        StructField("patterns", ArrayType(StringType(), True), True),
        StructField("region_id", StringType(), True),
        StructField("region_name", StringType(), True),
        StructField("routes", ArrayType(StringType(), True), True),
        StructField("short_name", StringType(), True),
        StructField("tts_name", StringType(), True),
        StructField("wheelchair_boarding", StringType(), True),
        StructField("ingestion_date", DateType(), True),
        StructField("partition_date", DateType(), True),
    ]
)
