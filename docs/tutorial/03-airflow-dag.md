# 3. Create the Airflow DAG

In this step you'll write the DAG that orchestrates the full pipeline.

A DAG (Directed Acyclic Graph) defines the tasks and the order they run. Airflow reads every `.py` file in the `dags/` folder and registers them automatically.

---

## The generated template

DEGEN already created a starter DAG at `dags/pipeline_dag.py`. Open it:

```python title="dags/pipeline_dag.py" linenums="1"
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    dag_id="sales_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    def extract():
        print("TODO: add extract logic")

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )
```

It's minimal on purpose. You'll expand it now.

---

## Replace with the full DAG

Open `dags/pipeline_dag.py` and replace its contents with the following:

```python title="dags/pipeline_dag.py" linenums="1"
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Absolute path to the project root (where degen.yaml lives)
PROJECT_ROOT = Path(__file__).parent.parent

default_args = {
    "owner": "degen",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def run_extract(**context):
    """Generate synthetic daily sales data and write to data/raw/."""
    import csv
    import random
    from datetime import date

    output = PROJECT_ROOT / "data" / "raw" / "sales.csv"
    output.parent.mkdir(parents=True, exist_ok=True)

    products = ["Widget A", "Widget B", "Widget C", "Gadget X", "Gadget Y"]
    regions  = ["north", "south", "east", "west"]
    today    = context["ds"]                          # Airflow injects the execution date

    rows = [
        {
            "date":     today,
            "product":  random.choice(products),
            "region":   random.choice(regions),
            "quantity": random.randint(1, 50),
            "price":    round(random.uniform(9.99, 199.99), 2),
        }
        for _ in range(200)
    ]

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} records for {today} → {output}")


def run_pyspark(**context):
    """Run the PySpark transformation job."""
    script = PROJECT_ROOT / "src" / "pyspark_transform.py"
    venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"

    result = subprocess.run(
        [str(venv_python), str(script)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"PySpark job failed (exit {result.returncode})")


with DAG(
    dag_id="sales_pipeline",
    description="Daily sales ETL: extract → PySpark → dbt",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["degen", "sales"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=run_extract,
    )

    pyspark_transform = PythonOperator(
        task_id="pyspark_transform",
        python_callable=run_pyspark,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"cd {PROJECT_ROOT}/sales_pipeline && "
            f"{PROJECT_ROOT}/.venv/bin/dbt run --profiles-dir {PROJECT_ROOT}"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"cd {PROJECT_ROOT}/sales_pipeline && "
            f"{PROJECT_ROOT}/.venv/bin/dbt test --profiles-dir {PROJECT_ROOT}"
        ),
    )

    # Pipeline order: extract → pyspark → dbt run → dbt test
    extract >> pyspark_transform >> dbt_run >> dbt_test
```

Save the file. No restart needed — Airflow rescans `dags/` every 30 seconds.

---

## Verify in Airflow UI

Open **http://localhost:8080** and refresh the page.

You should see `sales_pipeline` in the list with 4 tasks:

```
extract  →  pyspark_transform  →  dbt_run  →  dbt_test
```

Click on the DAG name → **Graph** tab to see the task dependency visualization.

!!! tip
    If the DAG doesn't appear after 60 seconds, check for syntax errors:
    ```bash
    .venv/bin/python dags/pipeline_dag.py
    ```
    No output means no errors.

---

## What `>> ` means

The `>>` operator in Airflow sets the execution order:

```python
extract >> pyspark_transform >> dbt_run >> dbt_test
```

This means:
- `pyspark_transform` only starts after `extract` succeeds
- `dbt_run` only starts after `pyspark_transform` succeeds
- `dbt_test` only starts after `dbt_run` succeeds

If any task fails, the pipeline stops there and retries up to `retries=1` times.

[Next: Write the PySpark Job →](04-pyspark.md){ .md-button .md-button--primary }
