from pyspark.sql import SparkSession

from configs.settings import Settings
from infrastructure.logging.logger import logger


def get_spark_session(app_name: str = Settings.APP_NAME) -> SparkSession:
    """
    Cria e retorna uma SparkSession com configurações adequadas para integração com GCS.

    Requer:
    - Conector GCS instalado: com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5
    - Autenticação configurada via ADC (Application Default Credentials)
    """

    logger.info(f"SparkSession criada com nome: {app_name}")

    session = (
        SparkSession.builder.appName(app_name)
        .config("spark.hadoop.fs.gs.auth.service.account.enable", "true")
        # Configurações de integração com GCS
        .config(
            "spark.hadoop.google.cloud.auth.service.account.json.keyfile",
            Settings.GOOGLE_APPLICATION_CREDENTIALS,
        )
        # Performance e memória
        .config("spark.driver.memory", "4g")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.hadoop.hadoop.security.authentication", "simple")
        .config(
            "spark.driver.extraJavaOptions",
            "--add-opens java.base/javax.security.auth=ALL-UNNAMED",
        )
        .config("spark.sql.shuffle.partitions", "100")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "64MB")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.parquet.compression.codec", "snappy")
        .config("parquet.block.size", 134217728)
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
        .config("spark.speculation", "false")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.kryoserializer.buffer.max", "512m")
        # GCS Integration
        .config(
            "spark.jars.packages",
            "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5",
        )
        .config(
            "spark.hadoop.fs.gs.impl",
            "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem",
        )
        .config(
            "spark.hadoop.fs.AbstractFileSystem.gs.impl",
            "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS",
        )
        .getOrCreate()
    )
    logger.info(f"Usando GCS com chave: {Settings.GOOGLE_APPLICATION_CREDENTIALS}")
    logger.info("SparkSession criada com sucesso")
    return session
