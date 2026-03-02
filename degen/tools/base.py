from abc import ABC
from degen.core.phases import Phase


class Tool(ABC):

    name: str
    phase: Phase

    # -------------------------
    # Python deps
    # -------------------------

    def get_python_dependencies(self):
        return []

    # -------------------------
    # Project structure
    # -------------------------

    def get_project_structure(self):
        return {}
    
    def get_dbt_profile(self, project_name: str):
        return None

    # -------------------------
    # Docker
    # -------------------------

    def get_docker_services(self):
        return {}

    def get_docker_volumes(self):
        return {}

    def get_docker_networks(self):
        return {}

    # -------------------------
    # Makefile contributions
    # -------------------------

    def get_makefile_targets(self):
        """
        Return dict like:
        {
            "install": ["command1", "command2"],
            "run": ["command"],
        }
        """
        return {}
    
    # -------------------------
    # Environment
    # -------------------------
    def get_env_variables(self):
        return {}