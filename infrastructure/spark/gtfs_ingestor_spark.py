import os

from pyspark.sql import SparkSession


def ingest_gtfs_files(folder_path: str, output_base_path: str, spark: SparkSession):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            table = filename.replace(".txt", "")
            file_path = os.path.join(folder_path, filename)
            df = spark.read.csv(file_path, header=True, inferSchema=True)
            output_path = os.path.join(output_base_path, table)
            df.write.mode("overwrite").parquet(output_path)
