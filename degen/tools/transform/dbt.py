import yaml
from degen.tools.base import Tool
from degen.core.phases import Phase


class DBTTool(Tool):

    name = "dbt"
    phase = Phase.TRANSFORM

    def __init__(self):
        self.store_tool = None

    def configure_store(self, store_tool):
        self.store_tool = store_tool

    def get_python_dependencies(self):
        deps = ["dbt-core==1.8.7"]
        if self.store_tool:
            adapter = self.store_tool.get_dbt_adapter()
            if adapter:
                deps.append(adapter)
        else:
            deps.append("dbt-duckdb==1.8.1")
        return deps

    def get_env_variables(self):
        return {
            "DBT_THREADS": "4",
            "DBT_TARGET": "dev",
        }

    def build_profiles_yaml(self, project_name: str) -> str:
        if not self.store_tool:
            return ""
        profile = self.store_tool.get_dbt_profile(project_name)
        if not profile:
            return ""
        data = {
            profile["profile_name"]: {
                "target": "dev",
                "outputs": {
                    "dev": profile["config"]
                },
            }
        }
        return yaml.dump(data, sort_keys=False)

    def get_makefile_targets(self):
        return {
            "install": [
                "$(VENV)/bin/dbt init $(PROJECT_NAME) --skip-profile-setup || true",
            ],
            "run": [
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt run --profiles-dir ..",
            ],
            "seed": [
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt seed --profiles-dir ..",
            ],
            "test": [
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt test --profiles-dir ..",
            ],
            "docs": [
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt docs generate --profiles-dir ..",
                "cd $(PROJECT_NAME) && ../$(VENV)/bin/dbt docs serve --profiles-dir .. --port 8081",
            ],
        }

    def get_ui_urls(self):
        return {"dbt docs": "http://localhost:8081  (via: degen docs)"}
