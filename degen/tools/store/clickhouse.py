from degen.tools.base import Tool
from degen.core.phases import Phase


class ClickHouseTool(Tool):

    name = "ClickHouse"
    phase = Phase.STORE

    def get_python_dependencies(self):
        return ["clickhouse-driver>=0.2.7"]

    def get_env_variables(self):
        return {
            "CLICKHOUSE_HOST": "localhost",
            "CLICKHOUSE_PORT": "8123",
            "CLICKHOUSE_USER": "default",
            "CLICKHOUSE_PASSWORD": "",
            "CLICKHOUSE_DB": "default",
        }

    def get_dbt_adapter(self):
        return "dbt-clickhouse==1.8.0"

    def get_dbt_profile(self, project_name: str):
        return {
            "profile_name": project_name,
            "config": {
                "type": "clickhouse",
                "schema": "${CLICKHOUSE_DB}",
                "host": "${CLICKHOUSE_HOST}",
                "port": 8123,
                "user": "${CLICKHOUSE_USER}",
                "password": "${CLICKHOUSE_PASSWORD}",
                "secure": False,
                "threads": 4,
            },
        }

    def get_docker_services(self):
        return {
            "clickhouse": {
                "image": "clickhouse/clickhouse-server:24.6",
                "container_name": "degen_clickhouse",
                "ports": ["8123:8123", "9000:9000"],
                "volumes": ["clickhouse_data:/var/lib/clickhouse"],
                "networks": ["degen_net"],
                "ulimits": {
                    "nofile": {
                        "soft": 262144,
                        "hard": 262144,
                    }
                },
                "healthcheck": {
                    "test": ["CMD", "wget", "--spider", "-q", "http://localhost:8123/ping"],
                    "interval": "10s",
                    "retries": 5,
                    "start_period": "10s",
                },
            }
        }

    def get_ui_urls(self):
        return {
            "ClickHouse Play": "http://localhost:8123/play",
        }

    def get_docker_volumes(self):
        return {"clickhouse_data": {}}

    def get_docker_networks(self):
        return {"degen_net": {"driver": "bridge"}}
