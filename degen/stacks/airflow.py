from pathlib import Path
from degen.stacks.base import Stack
from degen.registry.stack_registry import StackRegistry


class AirflowStack(Stack):
    name = "Airflow + Postgres"

    def apply_stack(self, root: Path):

        # requirements
        (root / "requirements.txt").write_text(
            """apache-airflow==2.9.1
psycopg2-binary==2.9.9
"""
        )

        # .env
        (root / ".env").write_text(
            """POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV=dev
"""
        )

        # docker-compose
        (root / "docker-compose.yml").write_text(
            """

services:
  postgres:
    image: postgres:16
    env_file:
      - .env
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data

  airflow:
    image: apache/airflow:2.9.1
    depends_on:
      - postgres
    env_file:
      - .env
    volumes:
      - ./dags:/opt/airflow/dags
    ports:
      - "8080:8080"
    command: >
      bash -c "
      airflow db init &&
      airflow users create --username admin --password admin \
      --firstname admin --lastname admin --role Admin --email admin@example.com &&
      airflow webserver & airflow scheduler
      "

volumes:
  postgres-db-volume:
"""
        )

        # DAG mínimo
        (root / "dags/hello_dag.py").write_text(
            """from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def hello():
    print("Airflow pipeline running")


with DAG(
    dag_id="hello_elt",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="hello_task",
        python_callable=hello,
    )
"""
        )


StackRegistry.register(AirflowStack)