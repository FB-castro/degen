from degen.tools.base import Tool
from degen.core.phases import Phase


class GrafanaTool(Tool):

    name = "Grafana"
    phase = Phase.SERVE

    def get_env_variables(self):
        return {
            "GF_SECURITY_ADMIN_USER": "admin",
            "GF_SECURITY_ADMIN_PASSWORD": "admin",
        }

    def get_docker_services(self):
        return {
            "grafana": {
                "image": "grafana/grafana:11.1.3",
                "container_name": "degen_grafana",
                "ports": ["3001:3000"],
                "environment": {
                    "GF_SECURITY_ADMIN_USER": "${GF_SECURITY_ADMIN_USER}",
                    "GF_SECURITY_ADMIN_PASSWORD": "${GF_SECURITY_ADMIN_PASSWORD}",
                },
                "volumes": ["grafana_data:/var/lib/grafana"],
                "networks": ["degen_net"],
                "healthcheck": {
                    "test": ["CMD", "wget", "--spider", "-q", "http://localhost:3000/api/health"],
                    "interval": "15s",
                    "retries": 5,
                    "start_period": "30s",
                },
            }
        }

    def get_docker_volumes(self):
        return {"grafana_data": {}}

    def get_docker_networks(self):
        return {"degen_net": {"driver": "bridge"}}

    def get_ui_urls(self):
        return {"Grafana": "http://localhost:3001  [admin / admin]"}

    def get_makefile_targets(self):
        return {
            "serve": ["@echo 'Grafana: http://localhost:3001  (admin/admin — run: make docker-up first)'"],
        }
