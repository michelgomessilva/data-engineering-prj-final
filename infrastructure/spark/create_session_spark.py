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
        # apenas o shaded
        .config("spark.jars", "/opt/spark/jars/gcs-connector-hadoop3-2.2.20-shaded.jar")
        # Implementações GCS
        .config(
            "spark.hadoop.fs.gs.impl",
            "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem",
        )
        .config(
            "spark.hadoop.fs.AbstractFileSystem.gs.impl",
            "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS",
        )
        # Autenticação (use uma só variante; estas funcionam com o connector 2.x)
        .config("spark.hadoop.fs.gs.auth.service.account.enable", "true")
        .config(
            "spark.hadoop.fs.gs.auth.service.account.json.keyfile",
            Settings.GOOGLE_APPLICATION_CREDENTIALS,
        )
        # Performance (igual ao seu)
        .config("spark.driver.memory", "4g")
        .config("spark.sql.session.timeZone", "UTC")
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
        .getOrCreate()
    )

    logger.info(f"Usando GCS com chave: {Settings.GOOGLE_APPLICATION_CREDENTIALS}")

    hc = session._jsc.hadoopConfiguration()

    logger.info("fs.gs.impl = %s", hc.get("fs.gs.impl"))
    logger.info("spark.jars = %s", session.sparkContext.getConf().get("spark.jars"))

    # Testa se a classe existe
    try:
        cls = session._jvm.java.lang.Class.forName(
            "com.google.api.client.http.HttpRequestInitializer"
        )
        logger.info(
            "HttpRequestInitializer FOUND at: %s",
            cls.getProtectionDomain().getCodeSource().getLocation(),
        )
    except Exception as e:
        logger.exception("HttpRequestInitializer MISSING: %s", e)

    logger.info("SparkSession criada com sucesso")
    return session
