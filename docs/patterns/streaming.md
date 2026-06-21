# Streaming

Real-time event processing with Kafka and PySpark Structured Streaming.

**Best for:** event-driven architectures, IoT pipelines, real-time analytics, log processing.

---

## Tools

| Phase | Options |
|---|---|
| Stream | Kafka |
| Process | PySpark |
| Store | ClickHouse |

---

## Create the project

```bash
degen init
```

Select **Streaming**. This guide uses **Kafka + PySpark**.

```bash
cd my_streaming_project
```

---

## Install

```bash
degen install
```

Installs: pyspark, kafka-python, and configures Spark to use the Kafka connector.

---

## Start services

```bash
degen docker-up
```

Starts four containers:

| Container | Service | Port |
|---|---|---|
| `degen_kafka` | Apache Kafka 3.7 (KRaft) | 9092 |
| `degen_kafka_ui` | Kafka UI | 8082 |
| `degen_zookeeper` | — | (not used, KRaft mode) |

Wait for Kafka to become healthy:

```bash
degen status
```

```
Docker services:
NAME              STATUS
degen_kafka       Up (healthy)
degen_kafka_ui    Up
```

---

## Create the topic

```bash
degen create-topic
```

Creates the Kafka topic defined in `.env` (default: `degen-events`).

---

## Produce events

```bash
degen produce
```

Sends 100 synthetic events to Kafka:

```
degen produce
────────────
Sending 100 events to topic 'degen-events' on localhost:9092
✓ Sent 100 events
```

Each event is a JSON payload:

```json
{ "id": "a3b1c2d4", "value": 42, "ts": "2024-01-15T12:34:56Z" }
```

---

## Start the consumer

```bash
degen stream
```

Starts a PySpark Structured Streaming job that reads from Kafka and prints micro-batches to the console:

```
degen stream
────────────
Batch 1: 20 rows
+------+------+--------------------+
|    id| value|                  ts|
+------+------+--------------------+
|a3b1c2|    42|2024-01-15T12:34:...|
|b4d2e1|    87|2024-01-15T12:34:...|
...

Batch 2: 20 rows
...
```

The consumer runs continuously. Press `Ctrl+C` to stop.

---

## Kafka UI — browse topics and messages

Open **http://localhost:8082**

Navigate to:

- **Topics → degen-events** — see message count, offsets, partitions
- **Topics → degen-events → Messages** — browse individual events in real time
- **Consumers** — active consumer groups and lag

!!! tip
    Produce more events in a second terminal while the Kafka UI is open to watch messages appear live.

---

## PySpark UI — monitor streaming jobs

When `degen stream` is running, open **http://localhost:4040**

- **Streaming** tab → micro-batch timeline, processing rates, input rates
- **Jobs** → execution plan for each batch
- **SQL** → query plans

---

## Produce events continuously

To test sustained load, produce events in a loop from a separate terminal:

```bash
for i in {1..10}; do degen produce; sleep 2; done
```

Watch Kafka UI lag and PySpark batch sizes increase in real time.

---

## Customizing the producer

Edit `src/producer.py`:

```python
import json
import uuid
from datetime import datetime, timezone
from kafka import KafkaProducer

def produce(topic: str, broker: str, count: int = 100):
    producer = KafkaProducer(
        bootstrap_servers=broker,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    for _ in range(count):
        event = {
            "id": str(uuid.uuid4()),
            "value": random.randint(1, 1000),
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        producer.send(topic, event)
    producer.flush()
```

Replace the synthetic events with your real data source: HTTP API, database CDC, IoT sensors, etc.

---

## Customizing the consumer

Edit `src/consumer.py`:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

schema = StructType() \
    .add("id", StringType()) \
    .add("value", IntegerType()) \
    .add("ts", StringType())

def stream(topic: str, broker: str):
    spark = SparkSession.builder \
        .appName("degen-streaming") \
        .getOrCreate()

    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", broker) \
        .option("subscribe", topic) \
        .load()

    parsed = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    # Add your transformations here:
    # aggregated = parsed.groupBy("id").count()

    query = parsed.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
```

---

## Project structure

```
my_streaming_project/
├── degen.yaml
├── .env                    # KAFKA_TOPIC, KAFKA_BROKER
├── docker-compose.yml      # Kafka + Kafka UI
├── requirements.txt
└── src/
    ├── producer.py         # sends events to Kafka
    └── consumer.py         # PySpark streaming job
```

---

## Environment variables

Edit `.env` to configure Kafka:

```bash
KAFKA_BROKER=localhost:9092
KAFKA_TOPIC=degen-events
```

All `degen` commands pick up `.env` automatically.
