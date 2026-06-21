from degen.tools.extract.python import PythonExtractTool
from degen.tools.transform.dbt import DBTTool
from degen.tools.transform.pyspark import PySparkTool
from degen.tools.store.duckdb import DuckDBTool
from degen.tools.store.postgres import PostgresTool
from degen.tools.store.clickhouse import ClickHouseTool
from degen.tools.orchestrate.airflow import AirflowTool
from degen.tools.orchestrate.prefect import PrefectTool
from degen.tools.serve.metabase import MetabaseTool
from degen.tools.serve.grafana import GrafanaTool
from degen.tools.stream.kafka import KafkaTool

TOOL_REGISTRY = {
    "Python":     PythonExtractTool,
    "dbt":        DBTTool,
    "PySpark":    PySparkTool,
    "DuckDB":     DuckDBTool,
    "Postgres":   PostgresTool,
    "ClickHouse": ClickHouseTool,
    "Airflow":    AirflowTool,
    "Prefect":    PrefectTool,
    "Metabase":   MetabaseTool,
    "Grafana":    GrafanaTool,
    "Kafka":      KafkaTool,
}


def get_tool(name: str):
    if name not in TOOL_REGISTRY:
        raise ValueError(f"Tool '{name}' not registered. Available: {list(TOOL_REGISTRY)}")
    return TOOL_REGISTRY[name]()
