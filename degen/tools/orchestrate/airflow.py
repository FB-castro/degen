from degen.tools.base import Tool
from degen.core.phases import Phase


_DAG_TEMPLATE = '''\
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "degen",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="pipeline_dag",
    default_args=default_args,
    description="DEGEN-generated pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["degen"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python /opt/airflow/src/extract.py",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="dbt run --profiles-dir /opt/airflow --project-dir /opt/airflow/{{ var.value.project_name }}",
    )

    extract >> transform
'''

_AIRFLOW_COMMON_ENV = {
    "AIRFLOW__CORE__EXECUTOR": "LocalExecutor",
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN": (
        "postgresql+psycopg2://airflow:airflow@airflow-postgres/airflow"
    ),
    "AIRFLOW__CORE__LOAD_EXAMPLES": "false",
    "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "true",
}


class AirflowTool(Tool):

    name = "Airflow"
    phase = Phase.ORCHESTRATE

    def get_env_variables(self):
        return {
            "AIRFLOW_UID": "50000",
        }

    def get_project_structure(self):
        return {
            "dags": {"pipeline_dag.py": _DAG_TEMPLATE},
        }

    def get_docker_services(self):
        return {
            "airflow-postgres": {
                "image": "postgres:16",
                "environment": {
                    "POSTGRES_USER": "airflow",
                    "POSTGRES_PASSWORD": "airflow",
                    "POSTGRES_DB": "airflow",
                },
                "volumes": ["airflow_postgres_data:/var/lib/postgresql/data"],
                "networks": ["degen_net"],
                "healthcheck": {
                    "test": ["CMD", "pg_isready", "-U", "airflow"],
                    "interval": "10s",
                    "retries": 5,
                    "start_period": "5s",
                },
            },
            "airflow-init": {
                "image": "apache/airflow:2.9.3",
                "depends_on": {
                    "airflow-postgres": {"condition": "service_healthy"}
                },
                "environment": {
                    **_AIRFLOW_COMMON_ENV,
                    "_AIRFLOW_DB_MIGRATE": "true",
                    "_AIRFLOW_WWW_USER_CREATE": "true",
                    "_AIRFLOW_WWW_USER_USERNAME": "admin",
                    "_AIRFLOW_WWW_USER_PASSWORD": "admin",
                },
                "entrypoint": "/bin/bash",
                "command": [
                    "-c",
                    "airflow db migrate && "
                    "airflow users create --username admin --firstname Admin "
                    "--lastname User --role Admin --email admin@example.com "
                    "--password admin || true",
                ],
                "volumes": ["./dags:/opt/airflow/dags", "./src:/opt/airflow/src"],
                "networks": ["degen_net"],
            },
            "airflow-webserver": {
                "image": "apache/airflow:2.9.3",
                "command": "webserver",
                "ports": ["8080:8080"],
                "depends_on": {
                    "airflow-postgres": {"condition": "service_healthy"}
                },
                "environment": _AIRFLOW_COMMON_ENV,
                "volumes": ["./dags:/opt/airflow/dags", "./src:/opt/airflow/src"],
                "networks": ["degen_net"],
                "healthcheck": {
                    "test": ["CMD", "curl", "--fail", "http://localhost:8080/health"],
                    "interval": "30s",
                    "timeout": "10s",
                    "retries": 5,
                    "start_period": "30s",
                },
            },
            "airflow-scheduler": {
                "image": "apache/airflow:2.9.3",
                "command": "scheduler",
                "depends_on": {
                    "airflow-postgres": {"condition": "service_healthy"}
                },
                "environment": _AIRFLOW_COMMON_ENV,
                "volumes": ["./dags:/opt/airflow/dags", "./src:/opt/airflow/src"],
                "networks": ["degen_net"],
            },
        }

    def get_docker_volumes(self):
        return {"airflow_postgres_data": {}}

    def get_docker_networks(self):
        return {"degen_net": {"driver": "bridge"}}

    def get_ui_urls(self):
        return {"Airflow": "http://localhost:8080  [admin / admin]"}

    def get_makefile_targets(self):
        return {
            "orchestrate": [
                "@echo 'Airflow UI: http://localhost:8080  (admin/admin)'",
                "@echo 'Run: make docker-up to start Airflow'",
            ],
        }
