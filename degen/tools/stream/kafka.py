from degen.tools.base import Tool
from degen.core.phases import Phase


_PRODUCER_TEMPLATE = '''\
import os
import json
import time
import logging
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "degen_events")


def produce(n: int = 100) -> None:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    logger.info(f"Producing {n} events to topic '{KAFKA_TOPIC}' on {KAFKA_BROKER}")
    for i in range(n):
        event = {"id": i, "value": f"event_{i}", "timestamp": time.time()}
        producer.send(KAFKA_TOPIC, event)
        logger.info(f"Sent: {event}")

    producer.flush()
    producer.close()
    logger.info("Done producing.")


if __name__ == "__main__":
    produce()
'''


class KafkaTool(Tool):

    name = "Kafka"
    phase = Phase.STREAM

    def get_python_dependencies(self):
        return [
            "kafka-python>=2.0.0",
            "python-dotenv>=1.0.0",
        ]

    def get_env_variables(self):
        return {
            "KAFKA_BROKER": "localhost:9092",
            "KAFKA_TOPIC": "degen_events",
        }

    def get_project_structure(self):
        return {
            "src": {"producer.py": _PRODUCER_TEMPLATE},
        }

    def get_docker_services(self):
        return {
            "kafka-ui": {
                "image": "provectuslabs/kafka-ui:latest",
                "container_name": "degen_kafka_ui",
                "ports": ["8082:8080"],
                "environment": {
                    "KAFKA_CLUSTERS_0_NAME": "local",
                    "KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS": "kafka:29092",
                },
                "networks": ["degen_net"],
                "depends_on": ["kafka"],
            },
            "kafka": {
                "image": "apache/kafka:3.7.0",
                "container_name": "degen_kafka",
                "ports": ["9092:9092"],
                "environment": {
                    "KAFKA_NODE_ID": "1",
                    "KAFKA_PROCESS_ROLES": "broker,controller",
                    "KAFKA_LISTENERS": "PLAINTEXT://0.0.0.0:9092,INTERNAL://0.0.0.0:29092,CONTROLLER://0.0.0.0:9093",
                    "KAFKA_ADVERTISED_LISTENERS": "PLAINTEXT://localhost:9092,INTERNAL://kafka:29092",
                    "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": "PLAINTEXT:PLAINTEXT,INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT",
                    "KAFKA_CONTROLLER_QUORUM_VOTERS": "1@kafka:9093",
                    "KAFKA_CONTROLLER_LISTENER_NAMES": "CONTROLLER",
                    "KAFKA_INTER_BROKER_LISTENER_NAME": "INTERNAL",
                    "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": "1",
                    "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR": "1",
                    "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR": "1",
                    "CLUSTER_ID": "MkU3OEVBNTcwNTJENDM2Qg",
                },
                "volumes": ["kafka_data:/var/lib/kafka/data"],
                "networks": ["degen_net"],
                "healthcheck": {
                    "test": [
                        "CMD",
                        "/opt/kafka/bin/kafka-topics.sh",
                        "--bootstrap-server",
                        "localhost:9092",
                        "--list",
                    ],
                    "interval": "15s",
                    "retries": 5,
                    "start_period": "30s",
                },
            }
        }

    def get_docker_volumes(self):
        return {"kafka_data": {}}

    def get_docker_networks(self):
        return {"degen_net": {"driver": "bridge"}}

    def get_ui_urls(self):
        return {"Kafka UI": "http://localhost:8082"}

    def get_makefile_targets(self):
        return {
            "create-topic": [
                "docker exec degen_kafka /opt/kafka/bin/kafka-topics.sh "
                "--create --bootstrap-server localhost:9092 "
                "--topic $(KAFKA_TOPIC) "
                "--partitions 1 --replication-factor 1 "
                "--if-not-exists"
            ],
            "produce": ["$(MAKE) create-topic", "$(VENV)/bin/python src/producer.py"],
        }
