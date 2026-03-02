from degen.tools.base import Tool
from degen.core.phases import Phase


class DBTTool(Tool):

    def __init__(self):
        self.store_tool = None

    def configure_store(self, store_tool):
        self.store_tool = store_tool

    name = "dbt"
    phase = Phase.TRANSFORM

    def get_python_dependencies(self):
        return [
            "dbt-core==1.7.14",
            "dbt-duckdb==1.7.2"
        ]

    def get_env_variables(self):
        return {
            "DBT_THREADS": "1",
            "DBT_TARGET": "dev"
        }


    def get_makefile_targets(self):

        install_commands = [
            "$(VENV)/bin/dbt init $(PROJECT_NAME) --skip-profile-setup || true"
        ]

        if not self.store_tool:
            return {"install": install_commands}

        profile = self.store_tool.get_dbt_profile("$(PROJECT_NAME)")

        profile_name = profile["profile_name"]
        config = profile["config"]

        profile_lines = [
            f'echo "{profile_name}:" > $(PROJECT_NAME)/profiles.yml',
            'echo "  target: dev" >> $(PROJECT_NAME)/profiles.yml',
            'echo "  outputs:" >> $(PROJECT_NAME)/profiles.yml',
            'echo "    dev:" >> $(PROJECT_NAME)/profiles.yml'
        ]

        for key, value in config.items():
            profile_lines.append(
                f'echo "      {key}: {value}" >> $(PROJECT_NAME)/profiles.yml'
            )

        install_commands.extend(profile_lines)

        return {
            "install": install_commands,
            "run": [
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt run"
            ],
            "seed": [
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt seed"
            ],
            "test": [
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt test"
            ]
        }