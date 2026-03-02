from degen.tools.extract.python import PythonExtractTool
from degen.tools.store.duckdb import DuckDBTool
from degen.tools.transform.dbt import DBTTool
from degen.tools.store.postgres import PostgresTool

TOOL_REGISTRY = {
    "Python": PythonExtractTool,
    "DuckDB": DuckDBTool,
    "dbt": DBTTool,
    "Postgres": PostgresTool
}


def get_tool(name: str):
    if name not in TOOL_REGISTRY:
        raise ValueError(f"Tool '{name}' not registered")
    return TOOL_REGISTRY[name]()