from abc import ABC
from degen.core.phases import Phase


_MAKE_VARS = [
    ("$(VENV)/bin/", ".venv/bin/"),  # must come before bare $(VENV)
    ("$(VENV)", ".venv"),
    ("$(PIP)", ".venv/bin/pip"),
    ("$(KAFKA_TOPIC)", "$KAFKA_TOPIC"),
    ("$(KAFKA_BROKER)", "$KAFKA_BROKER"),
]


class Tool(ABC):

    name: str
    phase: Phase

    def get_python_dependencies(self):
        return []

    def get_project_structure(self):
        return {}

    def get_dbt_adapter(self):
        return None

    def get_dbt_profile(self, project_name: str):
        return None

    def get_docker_services(self):
        return {}

    def get_docker_volumes(self):
        return {}

    def get_docker_networks(self):
        return {}

    def get_makefile_targets(self):
        return {}

    def get_env_variables(self):
        return {}

    def get_ui_urls(self) -> dict[str, str]:
        return {}

    def get_cli_commands(self, project_name: str = "") -> dict:
        """Resolve get_makefile_targets() into plain shell commands for degen.yaml."""
        result = {}
        for target, cmds in self.get_makefile_targets().items():
            deps, steps = [], []
            for cmd in cmds:
                if cmd.startswith("$(MAKE) "):
                    deps.append(cmd[len("$(MAKE) "):])
                else:
                    resolved = cmd
                    for make_var, shell_val in _MAKE_VARS:
                        resolved = resolved.replace(make_var, shell_val)
                    if project_name:
                        resolved = resolved.replace("$(PROJECT_NAME)", project_name)
                    steps.append(resolved)
            entry: dict = {}
            if deps:
                entry["deps"] = deps
            if steps:
                entry["steps"] = steps
            result[target] = entry
        return result
