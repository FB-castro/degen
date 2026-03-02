from degen.tools.base import Tool
from degen.core.phases import Phase


class DuckDBTool(Tool):

    name = "DuckDB"
    phase = Phase.STORE

    def get_python_dependencies(self):
        return ["duckdb==0.10.2"]

    def get_env_variables(self):
        return {
            "DUCKDB_PATH": "data/warehouse.duckdb"
        }
    
    def get_dbt_profile(self, project_name: str):
        return {
            "profile_name": project_name,
            "config": {
                "type": "duckdb",
                "path": "../${DUCKDB_PATH}",
                "threads": "${DBT_THREADS}"
            }
        }
    
    def get_project_structure(self):
        return {
            "data/raw": {},
            "data": {}
        }