import json
from degen.tools.base import Tool
from degen.core.phases import Phase


_SERVERS_JSON = json.dumps({
    "Servers": {
        "1": {
            "Name": "DEGEN Postgres",
            "Group": "Servers",
            "Host": "postgres",
            "Port": 5432,
            "MaintenanceDB": "postgres",
            "Username": "degen",
            "SSLMode": "prefer",
        }
    }
}, indent=2)


class PostgresTool(Tool):

    name = "Postgres"
    phase = Phase.STORE

    def get_python_dependencies(self):
        return ["psycopg2-binary>=2.9.9"]

    def get_env_variables(self):
        return {
            "POSTGRES_HOST": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_USER": "degen",
            "POSTGRES_PASSWORD": "degen",
            "POSTGRES_DB": "degen",
            "PGADMIN_DEFAULT_EMAIL": "admin@degen.io",
            "PGADMIN_DEFAULT_PASSWORD": "degen",
        }

    def get_project_structure(self):
        return {"pgadmin": {"servers.json": _SERVERS_JSON}}

    def get_ui_urls(self):
        return {"pgAdmin (Postgres)": "http://localhost:5050  [admin@degen.io / degen]"}

    def get_dbt_adapter(self):
        return "dbt-postgres==1.8.2"

    def get_dbt_profile(self, project_name: str):
        return {
            "profile_name": project_name,
            "config": {
                "type": "postgres",
                "host": "{{ env_var('POSTGRES_HOST', 'localhost') }}",
                "port": 5432,
                "user": "{{ env_var('POSTGRES_USER', 'degen') }}",
                "password": "{{ env_var('POSTGRES_PASSWORD', 'degen') }}",
                "dbname": "{{ env_var('POSTGRES_DB', 'degen') }}",
                "schema": "public",
                "threads": 4,
            },
        }

    def get_docker_services(self):
        return {
            "pgadmin": {
                "image": "dpage/pgadmin4:8.10",
                "container_name": "degen_pgadmin",
                "ports": ["5050:80"],
                "environment": {
                    "PGADMIN_DEFAULT_EMAIL": "${PGADMIN_DEFAULT_EMAIL}",
                    "PGADMIN_DEFAULT_PASSWORD": "${PGADMIN_DEFAULT_PASSWORD}",
                    "PGADMIN_SERVER_JSON_FILE": "/pgadmin4/servers.json",
                },
                "volumes": [
                    "./pgadmin/servers.json:/pgadmin4/servers.json:ro",
                    "pgadmin_data:/var/lib/pgadmin",
                ],
                "networks": ["degen_net"],
                "depends_on": ["postgres"],
            },
            "postgres": {
                "image": "postgres:16",
                "container_name": "degen_postgres",
                "environment": {
                    "POSTGRES_USER": "${POSTGRES_USER}",
                    "POSTGRES_PASSWORD": "${POSTGRES_PASSWORD}",
                    "POSTGRES_DB": "${POSTGRES_DB}",
                },
                "ports": ["5432:5432"],
                "volumes": ["postgres_data:/var/lib/postgresql/data"],
                "networks": ["degen_net"],
                "healthcheck": {
                    "test": ["CMD", "pg_isready", "-U", "${POSTGRES_USER}"],
                    "interval": "10s",
                    "retries": 5,
                    "start_period": "5s",
                },
            }
        }

    def get_docker_volumes(self):
        return {"postgres_data": {}, "pgadmin_data": {}}

    def get_docker_networks(self):
        return {"degen_net": {"driver": "bridge"}}
