from degen.tools.base import Tool
from degen.core.phases import Phase


class MetabaseTool(Tool):

    name = "Metabase"
    phase = Phase.SERVE

    def get_env_variables(self):
        return {
            "MB_DB_TYPE": "h2",
            "MB_DB_FILE": "/metabase-data/metabase.db",
        }

    def get_docker_services(self):
        return {
            "metabase": {
                "image": "metabase/metabase:v0.50.14",
                "container_name": "degen_metabase",
                "ports": ["3000:3000"],
                "environment": {
                    "MB_DB_TYPE": "${MB_DB_TYPE}",
                    "MB_DB_FILE": "${MB_DB_FILE}",
                },
                "volumes": ["metabase_data:/metabase-data"],
                "networks": ["degen_net"],
                "healthcheck": {
                    "test": ["CMD", "curl", "--fail", "http://localhost:3000/api/health"],
                    "interval": "30s",
                    "timeout": "10s",
                    "retries": 5,
                    "start_period": "60s",
                },
            }
        }

    def get_docker_volumes(self):
        return {"metabase_data": {}}

    def get_docker_networks(self):
        return {"degen_net": {"driver": "bridge"}}

    def get_ui_urls(self):
        return {"Metabase": "http://localhost:3000"}

    def get_makefile_targets(self):
        return {
            "serve": ["@echo 'Metabase: http://localhost:3000  (run: make docker-up first)'"],
        }
