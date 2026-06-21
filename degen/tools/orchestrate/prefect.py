from degen.tools.base import Tool
from degen.core.phases import Phase


_FLOW_TEMPLATE = '''\
import time
import logging
from prefect import flow, task

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@task(name="extract", retries=2, retry_delay_seconds=10, log_prints=True)
def extract() -> list[dict]:
    print("Extracting data...")
    records = [{"id": i, "value": i * 10} for i in range(1, 6)]
    print(f"Extracted {len(records)} records")
    return records


@task(name="transform", retries=1, log_prints=True)
def transform(records: list[dict]) -> list[dict]:
    print("Transforming data...")
    result = [{"id": r["id"], "value": r["value"], "doubled": r["value"] * 2} for r in records]
    print(f"Transformed {len(result)} records")
    return result


@task(name="load", log_prints=True)
def load(records: list[dict]) -> None:
    print("Loading data...")
    for r in records:
        print(f"  → {r}")
    print("Load complete.")


@flow(name="degen-pipeline", log_prints=True)
def pipeline():
    raw = extract()
    transformed = transform(raw)
    load(transformed)


if __name__ == "__main__":
    pipeline()
'''


class PrefectTool(Tool):

    name = "Prefect"
    phase = Phase.ORCHESTRATE

    def get_python_dependencies(self):
        return ["prefect>=3.0.0"]

    def get_env_variables(self):
        return {
            "PREFECT_API_URL": "http://localhost:4200/api",
        }

    def get_project_structure(self):
        return {
            "flows": {"pipeline_flow.py": _FLOW_TEMPLATE},
        }

    def get_ui_urls(self):
        return {"Prefect": "http://localhost:4200  (via: degen prefect-server)"}

    def get_makefile_targets(self):
        return {
            "prefect-server": [
                "$(VENV)/bin/prefect server start &",
                "@echo 'Prefect UI: http://localhost:4200'",
            ],
            "run": ["$(VENV)/bin/python flows/pipeline_flow.py"],
        }
