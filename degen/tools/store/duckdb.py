from degen.tools.base import Tool
from degen.core.phases import Phase


class DuckDBTool(Tool):

    name = "DuckDB"
    phase = Phase.STORE

    def get_python_dependencies(self):
        return ["duckdb>=0.10.0"]

    def get_env_variables(self):
        return {
            "DUCKDB_PATH": "data/warehouse.duckdb",
        }

    def get_dbt_adapter(self):
        return "dbt-duckdb==1.8.1"

    def get_dbt_profile(self, project_name: str):
        return {
            "profile_name": project_name,
            "config": {
                "type": "duckdb",
                "path": "../data/warehouse.duckdb",
                "threads": 4,
            },
        }

    def get_project_structure(self):
        return {
            "data/raw": {},
            "data": {},
            "notebooks": {},
        }

    def get_makefile_targets(self):
        return {
            "notebook": [
                "$(PIP) install --quiet jupyterlab duckdb ipykernel",
                "$(VENV)/bin/jupyter lab --notebook-dir=. --port=8888",
            ]
        }

    def get_ui_urls(self):
        return {"Jupyter Lab (DuckDB)": "http://localhost:8888  (via: degen notebook)"}
