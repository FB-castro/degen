from pathlib import Path
from degen.stacks.base import Stack
from degen.registry.stack_registry import StackRegistry


class SparkStack(Stack):
    name = "Spark + MinIO"

    def apply_stack(self, root: Path):

        # requirements
        (root / "requirements.txt").write_text(
            """pyspark==3.5.1
python-dotenv==1.0.1
"""
        )

        # .env
        (root / ".env").write_text(
            """MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
ENV=dev
"""
        )

        # Dockerfile
        (root / "Dockerfile").write_text(
            """FROM bitnami/spark:3.5.1
WORKDIR /app
COPY . .
"""
        )

        # docker-compose
        (root / "docker-compose.yml").write_text(
            """

services:

  minio:
    image: minio/minio:RELEASE.2024-02-17T01-15-03Z
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minio
      - MINIO_ROOT_PASSWORD=minio123
    ports:
      - "9000:9000"
      - "9001:9001"

  spark:
    image: bitnami/spark:3.5.1
    volumes:
      - .:/app
    working_dir: /app
    command: spark-submit src/pipeline.py
"""
        )

        # Pipeline mínimo
        (root / "src/pipeline.py").write_text(
            """from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MedallionPipeline").getOrCreate()

data = [(1, "Alice", 100), (2, "Bob", 200)]
columns = ["id", "name", "value"]

df = spark.createDataFrame(data, columns)

df.write.mode("overwrite").parquet("lake/bronze/data")

df_silver = df.withColumn("value_double", df.value * 2)
df_silver.write.mode("overwrite").parquet("lake/silver/data")

df_gold = df_silver.groupBy().sum("value_double")
df_gold.write.mode("overwrite").parquet("lake/gold/data")

print("Medallion pipeline executed successfully")

spark.stop()
"""
        )


StackRegistry.register(SparkStack)