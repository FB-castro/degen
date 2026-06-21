from degen.tools.base import Tool
from degen.core.phases import Phase


_BATCH_JOB = '''\
import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw")


def transform():
    spark = (
        SparkSession.builder
        .master(SPARK_MASTER)
        .appName("degen-transform")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    logger.info(f"Reading from {RAW_DATA_PATH}")
    df = spark.read.csv(f"{RAW_DATA_PATH}/sample.csv", header=True, inferSchema=True)

    df_out = df.withColumn("value_doubled", F.col("value") * 2)
    df_out.show()

    df_out.write.mode("overwrite").parquet("data/processed/output.parquet")
    logger.info("Transform complete — output written to data/processed/output.parquet")
    spark.stop()


if __name__ == "__main__":
    transform()
'''

_STREAMING_JOB = '''\
import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "degen_events")

EVENT_SCHEMA = StructType([
    StructField("id", LongType()),
    StructField("value", StringType()),
    StructField("timestamp", DoubleType()),
])


def stream():
    spark = (
        SparkSession.builder
        .master(SPARK_MASTER)
        .appName("degen-streaming")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
        )
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    logger.info(f"Connecting to Kafka at {KAFKA_BROKER}, topic={KAFKA_TOPIC}")

    raw = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BROKER)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "earliest")
        .load()
    )

    parsed = raw.select(
        F.from_json(F.col("value").cast("string"), EVENT_SCHEMA).alias("data")
    ).select("data.*")

    query = (
        parsed.writeStream
        .format("console")
        .outputMode("append")
        .trigger(processingTime="5 seconds")
        .start()
    )

    logger.info("Streaming job started — waiting for events...")
    query.awaitTermination()


if __name__ == "__main__":
    stream()
'''


class PySparkTool(Tool):

    name = "PySpark"
    phase = Phase.TRANSFORM

    def __init__(self):
        self.stream_tool = None

    def configure_stream(self, stream_tool):
        self.stream_tool = stream_tool

    def get_python_dependencies(self):
        deps = [
            "pyspark==3.5.1",
            "python-dotenv>=1.0.0",
        ]
        if self.stream_tool:
            deps.append("kafka-python>=2.0.0")
        return deps

    def get_env_variables(self):
        return {
            "SPARK_MASTER": "local[*]",
        }

    def get_project_structure(self):
        if self.stream_tool:
            return {
                "src": {"streaming_job.py": _STREAMING_JOB},
                "data/processed": {},
            }
        return {
            "src": {"transform.py": _BATCH_JOB},
            "data/processed": {},
        }

    def get_ui_urls(self):
        if self.stream_tool:
            return {"Spark UI": "http://localhost:4040  (available while degen stream is running)"}
        return {"Spark UI": "http://localhost:4040  (available while degen run is running)"}

    def get_makefile_targets(self):
        if self.stream_tool:
            return {
                "stream": ["$(MAKE) create-topic", "$(VENV)/bin/python src/streaming_job.py"],
            }
        return {
            "run": ["$(VENV)/bin/python src/transform.py"],
        }
