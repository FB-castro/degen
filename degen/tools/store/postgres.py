from degen.tools.base import Tool
from degen.core.phases import Phase


class PostgresTool(Tool):

    name = "Postgres"
    phase = Phase.STORE

    def get_env_variables(self):
        return {
            "POSTGRES_USER": "degen",
            "POSTGRES_PASSWORD": "degen",
            "POSTGRES_DB": "degen"
        }
    
    def get_docker_services(self):
        return {
            "postgres": {
                "image": "postgres:16",
                "container_name": "degen_postgres",
                "environment": {
                    "POSTGRES_USER": "${POSTGRES_USER}",
                    "POSTGRES_PASSWORD": "${POSTGRES_PASSWORD}",
                    "POSTGRES_DB": "${POSTGRES_DB}"
                },
                "ports": ["5432:5432"],
                "volumes": ["postgres_data:/var/lib/postgresql/data"],
                "networks": ["degen_net"]
            }
        }
    
    def get_dbt_profile(self, project_name: str):
        return {
            "profile_name": project_name,
            "config": {
                "type": "postgres",
                "host": "${POSTGRES_HOST}",
                "user": "${POSTGRES_USER}",
                "password": "${POSTGRES_PASSWORD}",
                "port": "${POSTGRES_PORT}",
                "dbname": "${POSTGRES_DB}",
                "schema": "public",
                "threads": "${DBT_THREADS}"
            }
        }

    def get_docker_volumes(self):
        return {
            "postgres_data": {}
        }

    def get_docker_networks(self):
        return {
            "degen_net": {
                "driver": "bridge"
            }
        }